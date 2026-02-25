import requests
from embeddings import embed_text
from vector_store import search
from config import OLLAMA_HOST

def generate_answer(query: str):
    query_vector = embed_text(query)
    results = search(query_vector)

    #DEBUG NORMALIZATION
    if isinstance(results, tuple):
        # Sometimes query_points returns (points, time)
        results = results[0]

    # If results is QueryResponse-like
    if hasattr(results, "points"):
        results = results.points # type: ignore

    # If results contains tuple elements like (ScoredPoint, score)
    cleaned = []
    for hit in results:
        if isinstance(hit, tuple):
            hit = hit[0]
        cleaned.append(hit)

    results = cleaned
    # -----------------------------

    extracted_chunks = [
        hit.payload["text"]
        for hit in results
        if hasattr(hit, "payload") and hit.payload and "text" in hit.payload
    ]

    context = "\n\n".join(extracted_chunks)
   
    prompt = f"""
You are a study assistant.


Rules:
- If the query contains MULTIPLE questions, answer EVERY single one separately.
- Label each answer clearly as Q1, Q2, Q3,etc.
- For each 10-mark question, write 300-400 words with bullet points and end with a NOTE: section summarizing key takeaways.
- If the answer to a specific question is not found in the context, say "Not found in study material" for that question but still attempt a general answer.
- Do NOT skip any question. Do NOT stop early.

Context:
{context}

Question:
{query}

Answer:
"""

    try:
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
                "options": {
                "num_predict": 4096,  
                "temperature": 0.3 
                }
            },
            timeout=120
        )
        response.raise_for_status()
        return response.json().get("response", "No response generated.")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to generate answer from Ollama: {e}")

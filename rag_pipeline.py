import requests
from embeddings import embed_text
from vector_store import search
from config import OLLAMA_HOST

def generate_answer(query: str):
    query_vector = embed_text(query)
    results = search(query_vector)

    # ---- DEBUG NORMALIZATION ----
    if isinstance(results, tuple):
        # Sometimes query_points returns (points, time)
        results = results[0]

    # If results is QueryResponse-like
    if hasattr(results, "points"):
        results = results.points

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

Use the provided context to answer the question clearly and concisely.
If the answer is not found in the context, say you don't know.
If the user asks for a long 10 mark explanation, provide 300-400 words of content including bullet points and a NOTE: section.

Context:
{context}

Question:
{query}

Answer:
"""

    response = requests.post(
        f"{OLLAMA_HOST}/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )

    # Safely return the string response from Ollama
    return response.json().get("response", "No response generated.")
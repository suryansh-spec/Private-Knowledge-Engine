
import requests
from config import OLLAMA_HOST
"""
Embedding model is loaded once at startup.
"""
def embed_text(text: str):
    try:
        response = requests.post(
            f"{OLLAMA_HOST}/api/embeddings",
            json={
                "model": "nomic-embed-text",
                "prompt": text
            },
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        if "embedding" not in data:
            raise ValueError(f"Ollama returned no embedding. Response: {data}")
        return data["embedding"]
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to connect to Ollama at {OLLAMA_HOST}: {e}")

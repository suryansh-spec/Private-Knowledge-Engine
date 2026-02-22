import requests
from config import OLLAMA_HOST

"""
Embedding model is loaded once at startup.
"""


def embed_text(text: str):
    response = requests.post(
        f"{OLLAMA_HOST}/api/embeddings",
        json={
            "model": "nomic-embed-text",
            "prompt": text
        }
    )
    print("Ollama response :", response.json())
    return response.json()["embedding"]
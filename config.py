import os

"""
This file centralizes configuration.

All environment variables are read here once.
"""

QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = 6333

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# IMPORTANT: Put your actual API key in docker-compose.yml
API_KEY = os.getenv("API_KEY", "change_me")

COLLECTION_NAME = "study_docs"

EMBEDDING_MODEL = "nomic-embed-text"
EMBEDDING_DIM = 768

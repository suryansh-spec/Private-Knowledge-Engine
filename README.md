# Private-Knowledge-Engine
Private modular RAG system built with containerized services (FastAPI + Ollama + Qdrant) for secure, local-first semantic search and context grounded llm inferences over personal academic documents.

A lightweight, containerized Retrieval-Augmented Generation (RAG) system using:

Ollama → Embeddings + LLM inference

Qdrant → Vector database

FastAPI → REST API backend

Docker Compose → Orchestration

This project allows you to ingest documents and query them using natural language with context-aware responses.

Architecture:- 

User Query
    ↓
FastAPI (rag-api)
    ↓
Ollama Embeddings API
    ↓
Qdrant (Vector Search)
    ↓
Ollama LLM (Answer Generation)
    ↓
Response

Key design decision:

No SentenceTransformers inside the container(sentence transformers need cuda and torch dependencies that increases the docker image size dramatically)

Ollama handles both embeddings and generation

Reduced image size and dependency complexity(combined size should not be more than 15gb)

📦 Tech Stack
Component	Purpose
Ollama	Embeddings + LLM inference
Qdrant	Vector similarity search
FastAPI	API layer
Docker	Containerization
🚀 Quick Start
1️⃣ Requirements

Docker

Docker Compose

Ollama installed locally (or containerized)

At least one embedding model pulled in Ollama

2️⃣ Pull Embedding Model

Example:

ollama pull nomic-embed-text

Optional LLM:

ollama pull mistral
3️⃣ Start the Stack
docker compose up -d

Swagger docs:

http://localhost:8000/docs
🧠 Embedding Model

This project uses Ollama’s embeddings API:

POST /api/embeddings

Example:

import requests

def embed(text):
    response = requests.post(
        "http://ollama:11434/api/embeddings",
        json={
            "model": "nomic-embed-text",
            "prompt": text
        }
    )
    return response.json()["embedding"]
📏 Vector Dimensions (Important)

Each embedding model has a fixed dimension.

Example:

Model	Dimension
nomic-embed-text	768
mxbai-embed-large	1024

Your Qdrant collection must match:

client.create_collection(
    collection_name="study_docs",
    vectors_config=models.VectorParams(
        size=768,
        distance=models.Distance.COSINE
    )
)

If dimensions mismatch, Qdrant will throw errors.

📥 Ingesting Documents

Before querying, you must ingest data.

Example flow:

chunks = split_text(document)
embeddings = [embed(chunk) for chunk in chunks]

points = [
    models.PointStruct(
        id=i,
        vector=emb,
        payload={"text": chunk}
    )
    for i, (emb, chunk) in enumerate(zip(embeddings, chunks))
]

client.upsert(collection_name="study_docs", points=points)

Without ingestion, queries will fail with:

Collection `study_docs` doesn't exist
🔎 Querying

Example API call:
consider this method to check the working of the system directly from terminal instead of browser

curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query":"Explain gradient descent"}'

Pipeline:

Query embedding generated via Ollama

Qdrant retrieves top matches

Context is passed to Ollama LLM

Final answer returned

🐛 Common Issues
Port 11434 already in use

You likely have Ollama running locally.
Either:

Stop local Ollama

Remove Ollama container from docker-compose

or, edit ollama port in dockerfile to 11435:11434


404 Collection Not Found

You haven’t created or ingested the collection.

Vector Size Mismatch

Embedding dimension does not match Qdrant configuration.

🧱 Design Philosophy

Minimal containers

Single inference backend (Ollama)

Explicit vector lifecycle management

Clear separation between ingestion and querying

🛠 Future Improvements

Add /ingest API endpoint

File upload support (.pdf, .txt, images)

enabeling this system to embedd images 

Caching layer

Authentication for remote access

Reverse proxy + HTTPS

Multi-user support

Remote deployment on home server

📌 Project Goals

This project demonstrates:

Practical RAG implementation

Vector DB integration

LLM orchestration

Containerized ML systems

Debugging distributed services

Managing SDK evolution

🧠 Why Ollama for Embeddings?

Using Ollama for embeddings:

Reduces container size

Removes PyTorch + HF dependency

Consolidates inference

Simplifies architecture

Improves maintainability

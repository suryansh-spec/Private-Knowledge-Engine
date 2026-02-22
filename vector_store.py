from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from config import QDRANT_HOST, QDRANT_PORT, COLLECTION_NAME, EMBEDDING_DIM

"""
This module handles:
- Collection creation
- Storing embeddings
- Searching

isolating DB logic from RAG logic.
"""

client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)


def create_collection_if_not_exists():
    """
    Creates collection once.
    """
    try:
        client.get_collection(COLLECTION_NAME)
    except:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=EMBEDDING_DIM,
                distance=Distance.COSINE
            ),
        )


def add_document(doc_id: str, vector, payload: dict):
    """
    Stores one chunk.

    payload contains:
    - text
    - source file
    - optional metadata
    """
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            {
                "id": doc_id,
                "vector": vector,
                "payload": payload
            }
        ]
    )


def search(query_vector, limit=5):
    """
    Always return a clean list of ScoredPoint objects.
    This function normalizes whatever Qdrant returns so that
    the pipeline layer does not need to care about API structure.
    """

    response = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=limit
    )

    # Case 1: Newer client returns (QueryResponse, time)
    if isinstance(response, tuple):
        response = response[0]

    # Case 2: QueryResponse object with .points
    if hasattr(response, "points"):
        return response.points

    # Case 3: Already a list
    if isinstance(response, list):
        return response

    raise ValueError("Unexpected Qdrant response structure")
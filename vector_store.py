from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from config import QDRANT_HOST, QDRANT_PORT, COLLECTION_NAME, EMBEDDING_DIM

"""
This module handles:
- Collection creation
- Storing embeddings
- Searching
"""

client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)


from qdrant_client.http.exceptions import UnexpectedResponse

def create_collection_if_not_exists():
    try:
        client.get_collection(COLLECTION_NAME)
    except UnexpectedResponse as e:
        if e.status_code == 404:
            client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=EMBEDDING_DIM,
                    distance=Distance.COSINE
                ),
            )
        else:
            raise


from qdrant_client.models import VectorParams, Distance, PointStruct

def add_document(doc_id: str, vector, payload: dict):
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=doc_id,
                vector=vector,
                payload=payload
            )
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

    # Case 1: newer client returns (QueryResponse, time)
    if isinstance(response, tuple):
        response = response[0]

    # Case 2: QueryResponse object with .points
    if hasattr(response, "points"):
        return response.points

    # Case 3: already a list
    if isinstance(response, list):
        return response

    raise ValueError("Unexpected Qdrant response structure")

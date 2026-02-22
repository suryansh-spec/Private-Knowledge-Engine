import os
import uuid
from embeddings import embed_text
from vector_store import add_document, create_collection_if_not_exists
from utils_doc import load_pdf, chunk_text

"""
ingestion script.

purpose:
convert docs (PDFs) into vector embeddings stored in Qdrant.

workflow:
1. Load PDF text
2. Chunk text
3. Embed each chunk
4. Store chunk + metadata

run inside container:

docker exec -it rag-api python ingest.py
"""


# Make sure your Docker volume mounts this correctly.
DATA_DIR = "/app/data/documents"


def ingest_all():
    create_collection_if_not_exists()

    for filename in os.listdir(DATA_DIR):

        # Only process PDFs for now
        if filename.lower().endswith(".pdf"):

            full_path = os.path.join(DATA_DIR, filename)
            print(f"Ingesting: {filename}")

            text = load_pdf(full_path)

            if not text.strip():
                print(f"Skipping {filename} (no extractable text)")
                continue

            chunks = chunk_text(text)

            for chunk in chunks:

                # Skip very tiny chunks
                if len(chunk.strip()) < 50:
                    continue

                vector = embed_text(chunk)

                add_document(
                    doc_id=str(uuid.uuid4()),
                    vector=vector,
                    payload={
                        "text": chunk,
                        "source": filename
                    }
                )

    print("Ingestion complete.")


if __name__ == "__main__":
    ingest_all()
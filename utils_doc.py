import fitz 
import os

"""
Utility module for:
- PDF loading (fast via PyMuPDF)
- Text chunking
"""


def load_pdf(path: str) -> str:
    """
    Extracts text from PDF using PyMuPDF.
    """

    text_chunks = []

    try:
        doc = fitz.open(path)

        for page_number in range(len(doc)):
            page = doc[page_number]

            # Extract plain text
            page_text = page.get_text("text")

            if page_text:
                text_chunks.append(page_text)

        doc.close()

    except Exception as e:
        print(f"Error reading {path}: {e}")
        return ""

    return "\n".join(text_chunks)


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 150):
    if overlap >= chunk_size:
        raise ValueError("overlap must be less than chunk_size")
    
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks

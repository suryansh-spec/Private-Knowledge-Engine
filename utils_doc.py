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

    Important design decisions:
    - open the document safely.
    - iterate page-by-page to avoid loading massive PDFs at once.
    - concatenate text cleanly.
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
    """
    Splits text into overlapping chunks.
    """

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from rag_pipeline import generate_answer
from config import API_KEY

"""
Main FastAPI app.

This exposes:
POST /query

Security:
Requires header:
x-api-key: your_seceret_key_here

IMPORTANT:
Replace API_KEY in docker-compose.yml
"""

app = FastAPI()


class QueryRequest(BaseModel):
    query: str


@app.post("/query")
async def query_endpoint(
    request: QueryRequest,
    x_api_key: str = Header(None)
):
    """
    Protect endpoint with API key.

    Even though Cloudflare Access already protects, this works as an extra layer of authentication
    """

    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized")

    answer = generate_answer(request.query)

    return {"answer": answer}
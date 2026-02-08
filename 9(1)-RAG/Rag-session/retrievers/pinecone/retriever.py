"""Vector retriever using Pinecone (cosine similarity)."""

import os

from dotenv import load_dotenv
from pinecone import Pinecone

from ingest.embedding import embed_query

load_dotenv()


def search(query: str, top_k: int = 10) -> list[dict]:
    """Vector cosine similarity search.

    Args:
        query: Search query string.
        top_k: Number of results to return.

    Returns:
        list[dict], each dict has keys: "id", "text", "score", "method".
        "method" should be "Vector".

    Hints:
        - Use embed_query(query) to get the query embedding vector
        - Connect: Pinecone(api_key=...) → pc.Index(index_name)
        - Use index.query(vector=..., top_k=..., include_metadata=True)
        - Text is in match["metadata"]["text"]
    """
    # TODO: Implement vector search
    pinecone = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index = pinecone.Index(os.getenv("PINECONE_INDEX"))
    query_vector = embed_query(query)
    response = index.query(
        vector=query_vector,
        top_k=top_k,
        include_metadata=True
    )
    results = []
    for match in response['matches']:
        result = {
            "id": match["id"],
            "text": match["metadata"]["text"],
            "score": match["score"],
            "method": "Vector"
        }
        results.append(result)
    return results

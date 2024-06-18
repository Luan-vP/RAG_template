import os

import weaviate
from fastapi import APIRouter

router = APIRouter()


# We assume that the Weaviate collection is configured with an LLM.
WEAVIATE_HOST = os.getenv("WEAVIATE_HOST") or "localhost"
WEAVIATE_COLLECTION_NAME = os.getenv("WEAVIATE_COLLECTION_NAME") or "WeaviateTextChunks"


client = weaviate.connect_to_local(host=WEAVIATE_HOST)
collection = client.collections.get(WEAVIATE_COLLECTION_NAME)


@router.get("/generative_search/{query}")
def generative_search(query: str):
    response = collection.generate.near_text(query=query, limit=5, grouped_task=query)
    return response.generated

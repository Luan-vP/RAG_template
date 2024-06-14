import os

import weaviate
from fastapi import APIRouter

router = APIRouter()


# We assume that the Weaviate collection is configured with an LLM.
WEAVIATE_HOST = (
    "localhost" if os.getenv("WEAVIATE_HOST") is None else os.getenv("WEAVIATE_HOST")
)
WEAVIATE_COLLECTION_NAME = "WeaviateTextChunks"


client = weaviate.connect_to_local(host=WEAVIATE_HOST)
collection = client.collections.get(WEAVIATE_COLLECTION_NAME)


@router.get("/generative_search/{query}")
def generative_search(query: str):
    collection.generate.near_text(query=query, limit=5, grouped_task=query)

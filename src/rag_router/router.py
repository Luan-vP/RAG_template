import os

import weaviate
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


def get_collection():

    WEAVIATE_HOST = os.getenv("WEAVIATE_HOST") or "localhost"
    WEAVIATE_COLLECTION_NAME = (
        os.getenv("WEAVIATE_COLLECTION_NAME") or "WeaviateTextChunks"
    )
    client = weaviate.connect_to_local(host=WEAVIATE_HOST)
    collection = client.collections.get(WEAVIATE_COLLECTION_NAME)

    try:
        yield collection
    finally:
        client.close()


class Query(BaseModel):
    query: str


@router.post("/generative_search")
def generative_search(input: Query):
    with get_collection() as collection:
        response = collection.generate.near_text(
            query=input.query, limit=5, grouped_task=input.query
        )
        return response.generated

import os
from pathlib import Path

import weaviate

WEAVIATE_COLLECTION_NAME = os.getenv("WEAVIATE_COLLECTION_NAME") or "WeaviateTextChunks"

client = weaviate.connect_to_local(host="localhost")

client.collections.delete(WEAVIATE_COLLECTION_NAME)

print(f"{WEAVIATE_COLLECTION_NAME} collection deleted.")

client.close()

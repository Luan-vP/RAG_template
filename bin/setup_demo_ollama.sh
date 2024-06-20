#!/bin/bash

docker-compose -f docker-compose.ollama.yaml up -d

export WEAVIATE_COLLECTION_NAME=rag_demo
python3 ./scripts/clear_weaviate_collection.py
python3 ./scripts/embed_and_upload_data.py

echo "RAG Demo is ready!"
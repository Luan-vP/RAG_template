#!/bin/bash

docker-compose -f ./docker/docker-compose.demo.yaml up -d

echo "Waiting for Weaviate to be ready... Take a nice deep breath 🌬️"
sleep 10s

export WEAVIATE_COLLECTION_NAME=Rag_demo
python3 ./scripts/clear_weaviate_collection.py
python3 ./scripts/embed_and_upload_data.py

echo "RAG Demo is ready!"
#!/bin/bash

docker-compose -f ./docker/docker-compose.demo.yaml up -d --build --remove-orphans

echo "Waiting for Weaviate to be ready... Take a nice deep breath 🌬️"
sleep 10s

export IS_DEMO=true
export WEAVIATE_COLLECTION_NAME=Rag_demo
python3 ./scripts/clear_weaviate_collection.py
python3 ./scripts/embed_and_upload_data.py

echo "RAG Demo is ready!"

echo "-----------------------------------"

echo "Testing direct LLM call"
QUERY="What happens in Season 4, Episode 3 of Adventure Time?"
echo "Query: $QUERY"

curl -s -S -X POST http://localhost:11434/api/generate -d @- <<EOF | jq -r '.response'
{
  "model": "llama3",
  "prompt": "$QUERY",
  "stream": false
}
EOF

echo "-----------------------------------"

echo "Testing RAG enabled search"

curl -X POST http://localhost:8888/generative_search -H "Content-Type: application/json" -d @- <<EOF
{
  "query": "$QUERY"
}
EOF

echo ""
echo "-----------------------------------"

sleep 10s

docker-compose -f ./docker/docker-compose.demo.yaml down

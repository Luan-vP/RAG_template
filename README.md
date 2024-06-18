# RAG Template
A template for simple RAG applications storing plaintext information in markdown files.

Configured for local Ollama instance, using llama3:8b for embedding and generative search.

## Requirements:
- Local weaviate instance
- Local Ollama instance with llama3

## Usage:
This project has been designed to integrate as flexibly as possible with existing projects. It will digest markdown files from a local directory, and upload embedded chunks to a local weaviate to be queried.

RAG functions can be served from a standalone server, or the router mounted to an existing FastAPI server. 

`docker-compose up` 
or `docker-compose -f docker-compose.ollama.yaml` up to use dockerised Ollama

`python ./scripts/embed_and_upload_data.py` to digest text files in `/data`

query the digested data with `GET http://localhost:8888/generative_search/{query}`

## TODO:
- [x] API endpoints
- [x] Dockerfile
- [x] Weaviate setup functions
- [ ] Integration tests with Weaviate (docker-compose)
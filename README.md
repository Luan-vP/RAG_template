# RAG Template
A template for simple RAG applications reading information from markdown files.

Configured for local Ollama instance, using `llama3:8b` for embedding and generative search.

## Requirements:
- Local weaviate instance
- Local Ollama instance with llama3
  
There are docker-compose files provided for this.

## Usage:
This project has been designed to integrate as flexibly as possible with existing projects.

---
### FastAPI applications:
```
from rag_router.router import router
app.include_router(router)
```
This mounts the `GET /generative_search/{query}` endpoint.

---
### Standalone deployment
To launch a local `weaviate` instance and a `rag_router` server:

`docker-compose up` 

N.B. you will need to have a locally running Ollama instance.

---

Or, to launch a dockerized `ollama` as well: 

`docker-compose -f docker-compose.ollama.yaml`

N.B. GPU optimised inference is not available on Docker for Mac.

---

### Data Upload

To digest `.md` files in the `./data` directory and upload them to weaviate: 

`python ./scripts/embed_and_upload_data.py`

You can now query this data using the `/generative_search/{query}` endpoint.

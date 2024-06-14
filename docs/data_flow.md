```mermaid
flowchart TD
A["User data input"] --> B["Save to markdown files in docker volume"]
B --> C["Manually run script: Read and upload files"]
C --> D["Chunks and embeddings in weaviate"]
```
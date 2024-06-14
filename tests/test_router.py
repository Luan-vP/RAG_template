from fastapi import FastAPI
from fastapi.testclient import TestClient

from ..src.router import router as rag_router

app = FastAPI()
app.include_router(rag_router)

client = TestClient(app)


def test_generative_search():
    response = client.get("/generative_search/What is the capital of Germany?")
    assert response.status_code == 200
    assert response.json() == {
        "result": [
            {
                "answer": "Berlin",
                "context": "Berlin is the capital of Germany.",
                "score": 0.99,
            }
        ]
    }

from fastapi.testclient import TestClient
from retrieval_pipeline import app

client = TestClient(app)

# Lets make some mock/fake objects

class FakeResponse:
    content = "smart answer"
class FakeDocument:
    page_content = "fake chunk"

from unittest.mock import patch

# Creating patches to mock objects. Order of line should match order of parameters.
@patch("retrieval_pipeline.supabase_client")
@patch("retrieval_pipeline.LLM")
@patch("retrieval_pipeline.vector_store.similarity_search", return_value=[FakeDocument()])
def test_chat(mock_search, mock_llm, mock_supabase):
    mock_llm.invoke.return_value = FakeResponse()
    response = client.post("/chat", json={"query": "What is the meaning of life?"})
    assert response.status_code == 200
    assert response.json() == "smart answer"

@patch("retrieval_pipeline.supabase_client")
@patch("retrieval_pipeline.LLM")
@patch("retrieval_pipeline.vector_store.similarity_search", return_value=[FakeDocument()])
def test_chat_with_history(mock_search, mock_llm, mock_supabase):
    mock_llm.invoke.return_value = FakeResponse()
    response = client.post("/chat", json={"query": "What is the meaning of life?", "history": [{"role": "user", "content": "What is the meaning of life?"}]})
    assert response.status_code == 200

# EMPTY REQUEST
def test_chat_empty_query():
    response = client.post("/chat", json={})
    assert response.status_code == 422  # validation error

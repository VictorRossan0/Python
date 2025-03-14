from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_account():
    response = client.post("/accounts/", json={"name": "Jane Doe", "balance": 100.0})
    assert response.status_code == 200
    assert response.json()["name"] == "Jane Doe"

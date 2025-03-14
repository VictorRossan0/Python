from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_transaction():
    response = client.post("/transactions/", json={"account_id": 1, "amount": 100.0, "type": "credit"})
    assert response.status_code == 200
    assert response.json()["amount"] == 100.0

def test_get_transaction():
    response = client.get("/transactions/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

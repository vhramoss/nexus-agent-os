from fastapi.testclient import TestClient
from nexus_os.api.main import app

def test_dlq_endpoint_returns_items():


    client = TestClient(app)

    response = client.get("/dlq")

    assert response.status_code == 200
    assert "items" in response.json()
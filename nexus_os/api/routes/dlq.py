from fastapi import APIRouter
from nexus_os.services.execution_service import get_dlq_items

router = APIRouter()


@router.get("/dlq")
def get_dlq():
    return {
        "items": get_dlq_items()
    }

def test_dlq_endpoint_returns_items():
    from fastapi.testclient import TestClient
    from nexus_os.api.main import app

    client = TestClient(app)

    response = client.get("/dlq")

    assert response.status_code == 200
    assert "items" in response.json()
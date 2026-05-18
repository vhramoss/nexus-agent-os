from fastapi.testclient import TestClient

from nexus_os.api.main import app

client = TestClient(app)


def test_health_endpoint_returns_200():
    # Act
    response = client.get("/health")

    # Assert
    assert response.status_code == 200


def test_run_endpoint_accepts_valid_goal():
    # Arrange
    payload = {"goal": "test execution"}

    # Act
    response = client.post("/run", json=payload)

    # Assert
    assert response.status_code == 200

    data = response.json()

    assert "trace_id" in data


def test_run_endpoint_rejects_empty_goal():
    # Arrange
    payload = {"goal": ""}

    # Act
    response = client.post("/run", json=payload)

    # Assert
    assert response.status_code == 400 or response.status_code == 422


def test_replay_returns_404_for_unknown_trace():
    # Act
    response = client.get("/replay/does-not-exist")

    # Assert
    assert response.status_code == 404


def test_run_then_replay_returns_events():
    # Arrange
    payload = {"goal": "test execution"}

    # Act
    run_response = client.post("/run", json=payload)

    trace_id = run_response.json()["trace_id"]

    replay_response = client.get(f"/replay/{trace_id}")

    # Assert
    assert replay_response.status_code == 200

    data = replay_response.json()

    assert "timeline" in data
    assert "metrics" in data

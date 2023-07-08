from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_healthcheck():
  # Act
  response = client.get("/api/v1/healthcheck")

  # Assert
  assert response.status_code == 200

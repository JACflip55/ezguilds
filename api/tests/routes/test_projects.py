from unittest.mock import patch

from src.models import Project


def test_create_project(authenticated_client):
    with patch("src.routes.projects.create_project") as mock_create:
        mock_create.return_value = Project(id="abc-123", owner_uid="test-user")
        response = authenticated_client.post("/projects")

    assert response.status_code == 201
    data = response.json()
    assert data["id"] == "abc-123"
    assert data["status"] == "uploading"


def test_create_project_unauthenticated():
    from fastapi.testclient import TestClient
    from src.main import app

    client = TestClient(app)
    response = client.post("/projects")
    assert response.status_code == 401

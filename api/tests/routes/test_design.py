from unittest.mock import patch

from src.models import Project


def test_get_design(authenticated_client):
    project = Project(id="abc-123", owner_uid="test-user", status="reviewing")
    project.design.status = "complete"
    project.design.gcs_path = "designs/abc-123/plan.svg"
    project.design.png_path = "designs/abc-123/plan.png"
    project.design.metadata_path = "designs/abc-123/metadata.json"

    with (
        patch("src.routes.design.get_project", return_value=project),
        patch("src.routes.design.get_signed_url", return_value="https://storage.example.com/signed"),
    ):
        response = authenticated_client.get("/projects/abc-123/design")

    assert response.status_code == 200
    data = response.json()
    assert data["svg_url"] == "https://storage.example.com/signed"
    assert data["png_url"] == "https://storage.example.com/signed"


def test_get_design_not_ready(authenticated_client):
    project = Project(id="abc-123", owner_uid="test-user", status="generating")

    with patch("src.routes.design.get_project", return_value=project):
        response = authenticated_client.get("/projects/abc-123/design")

    assert response.status_code == 409

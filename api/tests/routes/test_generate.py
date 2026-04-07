from unittest.mock import patch, MagicMock

from src.models import Project


def test_start_generation(authenticated_client):
    project = Project(id="abc-123", owner_uid="test-user", status="questioning")

    with (
        patch("src.routes.generate.get_project", return_value=project),
        patch("src.routes.generate.update_project") as mock_update,
        patch("src.routes.generate.enqueue_generation") as mock_enqueue,
    ):
        response = authenticated_client.post("/projects/abc-123/generate")

    assert response.status_code == 200
    mock_enqueue.assert_called_once_with("abc-123")
    mock_update.assert_called()


def test_get_status(authenticated_client):
    project = Project(id="abc-123", owner_uid="test-user", status="generating")
    project.design.status = "generating"

    with patch("src.routes.generate.get_project", return_value=project):
        response = authenticated_client.get("/projects/abc-123/status")

    assert response.status_code == 200
    assert response.json()["design_status"] == "generating"


def test_generate_wrong_owner(authenticated_client):
    project = Project(id="abc-123", owner_uid="other-user")

    with patch("src.routes.generate.get_project", return_value=project):
        response = authenticated_client.post("/projects/abc-123/generate")

    assert response.status_code == 403

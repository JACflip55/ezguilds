from unittest.mock import patch
from io import BytesIO

from src.models import Project, FileRef


def test_upload_file(authenticated_client):
    project = Project(id="abc-123", owner_uid="test-user")

    with (
        patch("src.routes.upload.get_project", return_value=project),
        patch("src.routes.upload.upload_file", return_value="uploads/abc-123/site.pdf"),
        patch("src.routes.upload.update_project") as mock_update,
    ):
        response = authenticated_client.post(
            "/projects/abc-123/upload",
            files={"file": ("site.pdf", b"fake-pdf", "application/pdf")},
            data={"file_type": "site_map"},
        )

    assert response.status_code == 200
    assert response.json()["name"] == "site.pdf"
    assert response.json()["type"] == "site_map"


def test_upload_wrong_owner(authenticated_client):
    project = Project(id="abc-123", owner_uid="other-user")

    with patch("src.routes.upload.get_project", return_value=project):
        response = authenticated_client.post(
            "/projects/abc-123/upload",
            files={"file": ("site.pdf", b"fake-pdf", "application/pdf")},
            data={"file_type": "site_map"},
        )

    assert response.status_code == 403


def test_upload_project_not_found(authenticated_client):
    with patch("src.routes.upload.get_project", return_value=None):
        response = authenticated_client.post(
            "/projects/abc-123/upload",
            files={"file": ("site.pdf", b"fake-pdf", "application/pdf")},
            data={"file_type": "site_map"},
        )

    assert response.status_code == 404

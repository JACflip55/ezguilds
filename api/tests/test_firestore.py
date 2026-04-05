from unittest.mock import MagicMock, patch

import pytest

from src.firestore import create_project, get_project, update_project
from src.models import Project


@pytest.fixture
def mock_db():
    with patch("src.firestore._get_db") as mock_get:
        db = MagicMock()
        mock_get.return_value = db
        yield db


def test_create_project(mock_db):
    mock_doc_ref = MagicMock()
    mock_db.collection.return_value.document.return_value = mock_doc_ref

    project = create_project(owner_uid="user-1")

    assert project.owner_uid == "user-1"
    assert project.status == "uploading"
    mock_doc_ref.set.assert_called_once()


def test_get_project_found(mock_db):
    mock_doc = MagicMock()
    mock_doc.exists = True
    mock_doc.to_dict.return_value = Project(id="abc", owner_uid="user-1").model_dump()
    mock_db.collection.return_value.document.return_value.get.return_value = mock_doc

    project = get_project("abc")

    assert project is not None
    assert project.id == "abc"


def test_get_project_not_found(mock_db):
    mock_doc = MagicMock()
    mock_doc.exists = False
    mock_db.collection.return_value.document.return_value.get.return_value = mock_doc

    project = get_project("nonexistent")

    assert project is None


def test_update_project(mock_db):
    mock_doc_ref = MagicMock()
    mock_db.collection.return_value.document.return_value = mock_doc_ref

    update_project("abc", {"status": "questioning"})

    mock_doc_ref.update.assert_called_once_with({"status": "questioning"})

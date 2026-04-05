from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture
def mock_firestore():
    with patch("src.firestore.firestore.Client") as mock_cls:
        mock_client = MagicMock()
        mock_cls.return_value = mock_client
        yield mock_client


@pytest.fixture
def authenticated_client():
    """Test client with auth bypassed — injects uid 'test-user'."""
    from src.auth import _get_uid_from_token

    app.dependency_overrides[_get_uid_from_token] = lambda: "test-user"
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

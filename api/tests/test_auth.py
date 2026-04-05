from unittest.mock import patch, MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.auth import require_auth


@pytest.fixture
def app_with_auth():
    app = FastAPI()

    @app.get("/protected")
    def protected(uid: str = require_auth):
        return {"uid": uid}

    return app


@pytest.fixture
def client(app_with_auth):
    return TestClient(app_with_auth)


def test_missing_auth_header_returns_401(client):
    response = client.get("/protected")
    assert response.status_code == 401
    assert response.json()["detail"] == "Missing authorization header"


def test_invalid_token_returns_401(client):
    with patch("src.auth.firebase_auth") as mock_auth:
        mock_auth.verify_id_token.side_effect = Exception("Invalid token")
        response = client.get("/protected", headers={"Authorization": "Bearer bad-token"})
    assert response.status_code == 401


def test_valid_token_returns_uid(client):
    with patch("src.auth.firebase_auth") as mock_auth:
        mock_auth.verify_id_token.return_value = {"uid": "user-123"}
        response = client.get("/protected", headers={"Authorization": "Bearer good-token"})
    assert response.status_code == 200
    assert response.json()["uid"] == "user-123"

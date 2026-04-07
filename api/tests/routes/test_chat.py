from unittest.mock import patch

from src.models import Project, ChatMessage


def test_send_chat_message(authenticated_client):
    project = Project(id="abc-123", owner_uid="test-user", status="reviewing")

    with (
        patch("src.routes.chat.get_project", return_value=project),
        patch("src.routes.chat.generate_chat_response", return_value={
            "response": "I can add more shade trees.",
            "needs_regeneration": False,
        }),
        patch("src.routes.chat.update_project") as mock_update,
    ):
        response = authenticated_client.post(
            "/projects/abc-123/chat",
            data={"message": "Add more shade trees on the south side"},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["response"] == "I can add more shade trees."
    assert data["needs_regeneration"] is False


def test_chat_triggers_regeneration(authenticated_client):
    project = Project(id="abc-123", owner_uid="test-user", status="reviewing")

    with (
        patch("src.routes.chat.get_project", return_value=project),
        patch("src.routes.chat.generate_chat_response", return_value={
            "response": "Updating the plan with fruit trees.",
            "needs_regeneration": True,
        }),
        patch("src.routes.chat.update_project"),
        patch("src.routes.chat.enqueue_generation") as mock_enqueue,
    ):
        response = authenticated_client.post(
            "/projects/abc-123/chat",
            data={"message": "Replace the herb spiral with fruit trees"},
        )

    assert response.status_code == 200
    assert response.json()["needs_regeneration"] is True
    mock_enqueue.assert_called_once_with("abc-123")


def test_chat_wrong_owner(authenticated_client):
    project = Project(id="abc-123", owner_uid="other-user")

    with patch("src.routes.chat.get_project", return_value=project):
        response = authenticated_client.post(
            "/projects/abc-123/chat",
            data={"message": "hello"},
        )

    assert response.status_code == 403

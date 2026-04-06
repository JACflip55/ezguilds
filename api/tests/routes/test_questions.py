from unittest.mock import patch

from src.models import Project, Answer


def test_get_next_question(authenticated_client):
    project = Project(id="abc-123", owner_uid="test-user", status="questioning")

    with (
        patch("src.routes.questions.get_project", return_value=project),
        patch("src.routes.questions.generate_next_question", return_value={
            "question": "What is your soil type?",
            "why": "Determines compatibility",
        }),
    ):
        response = authenticated_client.get("/projects/abc-123/questions")

    assert response.status_code == 200
    assert response.json()["question"] == "What is your soil type?"


def test_submit_answer(authenticated_client):
    project = Project(id="abc-123", owner_uid="test-user", status="questioning")

    with (
        patch("src.routes.questions.get_project", return_value=project),
        patch("src.routes.questions.update_project") as mock_update,
    ):
        response = authenticated_client.post(
            "/projects/abc-123/answers",
            json={"answer": "Clay loam"},
        )

    assert response.status_code == 200
    mock_update.assert_called_once()


def test_get_question_wrong_owner(authenticated_client):
    project = Project(id="abc-123", owner_uid="other-user")

    with patch("src.routes.questions.get_project", return_value=project):
        response = authenticated_client.get("/projects/abc-123/questions")

    assert response.status_code == 403

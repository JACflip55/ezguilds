from unittest.mock import patch, MagicMock

from src.gemini import generate_next_question, generate_chat_response


@patch("src.gemini._get_model")
def test_generate_next_question(mock_get_model):
    mock_model = MagicMock()
    mock_model.generate_content.return_value = MagicMock(
        text='{"question": "What is your soil type?", "why": "Determines plant compatibility"}'
    )
    mock_get_model.return_value = mock_model

    result = generate_next_question(
        goals="Grow food for family",
        location="Portland, OR",
        files_summary=["site-map.pdf (site_map)"],
        previous_answers=[],
    )

    assert result["question"] == "What is your soil type?"
    assert "why" in result


@patch("src.gemini._get_model")
def test_generate_next_question_with_previous_answers(mock_get_model):
    mock_model = MagicMock()
    mock_model.generate_content.return_value = MagicMock(
        text='{"question": "What is the sun exposure?", "why": "Affects plant placement"}'
    )
    mock_get_model.return_value = mock_model

    result = generate_next_question(
        goals="Grow food",
        location="Portland, OR",
        files_summary=["site-map.pdf (site_map)"],
        previous_answers=[{"question": "Soil type?", "answer": "Clay loam"}],
    )

    assert result["question"] == "What is the sun exposure?"
    # Verify previous answers were included in the prompt
    call_args = mock_model.generate_content.call_args[0][0]
    assert "Clay loam" in call_args

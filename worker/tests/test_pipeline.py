from unittest.mock import patch, MagicMock

from src.pipeline import run_generation


@patch("src.pipeline.upload_design")
@patch("src.pipeline.update_project")
@patch("src.pipeline.generate_design")
@patch("src.pipeline.get_project")
def test_pipeline_success(mock_get, mock_gen, mock_update, mock_upload):
    mock_get.return_value = {
        "id": "abc-123",
        "goals": "herb garden",
        "location": "Portland, OR",
        "scale": None,
        "detail_level": None,
        "context": {
            "files": [{"name": "site.pdf", "gcs_path": "uploads/abc/site.pdf", "type": "site_map"}],
            "answers": [{"question": "Sun?", "answer": "Full sun"}],
        },
    }
    mock_gen.return_value = {
        "title": "Herb Garden",
        "scale": "bed",
        "detail_level": "specific",
        "zones": [],
        "annotations": [],
        "summary": "A simple herb garden",
    }
    mock_upload.side_effect = [
        "designs/abc-123/plan.svg",
        "designs/abc-123/plan.png",
        "designs/abc-123/metadata.json",
    ]

    run_generation("abc-123")

    mock_get.assert_called_once_with("abc-123")
    mock_gen.assert_called_once()
    assert mock_upload.call_count == 3
    # Verify final status update marks complete
    final_update = mock_update.call_args_list[-1]
    assert final_update[0][1]["design.status"] == "complete"


@patch("src.pipeline.update_project")
@patch("src.pipeline.get_project")
def test_pipeline_project_not_found(mock_get, mock_update):
    mock_get.return_value = None

    run_generation("nonexistent")

    mock_update.assert_not_called()

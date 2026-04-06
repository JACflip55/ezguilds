from unittest.mock import MagicMock, patch
from io import BytesIO

from src.storage import upload_file, get_signed_url


@patch("src.storage._get_bucket")
def test_upload_file(mock_get_bucket):
    mock_bucket = MagicMock()
    mock_blob = MagicMock()
    mock_bucket.blob.return_value = mock_blob
    mock_get_bucket.return_value = mock_bucket

    gcs_path = upload_file(
        project_id="abc-123",
        filename="site.pdf",
        content=b"fake-pdf-bytes",
        content_type="application/pdf",
    )

    assert gcs_path == "uploads/abc-123/site.pdf"
    mock_blob.upload_from_string.assert_called_once_with(
        b"fake-pdf-bytes", content_type="application/pdf"
    )


@patch("src.storage._get_bucket")
def test_get_signed_url(mock_get_bucket):
    mock_bucket = MagicMock()
    mock_blob = MagicMock()
    mock_blob.generate_signed_url.return_value = "https://storage.example.com/signed"
    mock_bucket.blob.return_value = mock_blob
    mock_get_bucket.return_value = mock_bucket

    url = get_signed_url("uploads/abc-123/site.pdf")

    assert url == "https://storage.example.com/signed"

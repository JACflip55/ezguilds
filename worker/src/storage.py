import os

from google.cloud import storage

_bucket = None


def _get_bucket() -> storage.Bucket:
    global _bucket
    if _bucket is None:
        client = storage.Client()
        bucket_name = os.environ.get("GCS_BUCKET", "ezguilds-poc-uploads")
        _bucket = client.bucket(bucket_name)
    return _bucket


def upload_design(project_id: str, filename: str, content: bytes, content_type: str) -> str:
    bucket = _get_bucket()
    gcs_path = f"designs/{project_id}/{filename}"
    blob = bucket.blob(gcs_path)
    blob.upload_from_string(content, content_type=content_type)
    return gcs_path

from typing import Any, Optional

from google.cloud import firestore

_db = None


def _get_db() -> firestore.Client:
    global _db
    if _db is None:
        _db = firestore.Client()
    return _db


def get_project(project_id: str) -> Optional[dict]:
    db = _get_db()
    doc = db.collection("projects").document(project_id).get()
    if not doc.exists:
        return None
    return doc.to_dict()


def update_project(project_id: str, updates: dict[str, Any]) -> None:
    db = _get_db()
    db.collection("projects").document(project_id).update(updates)

import uuid
from typing import Any, Optional

from google.cloud import firestore

_db = None


def _get_db() -> firestore.Client:
    global _db
    if _db is None:
        _db = firestore.Client()
    return _db


COLLECTION = "projects"


def create_project(owner_uid: str) -> "Project":
    from src.models import Project

    db = _get_db()
    project_id = str(uuid.uuid4())
    project = Project(id=project_id, owner_uid=owner_uid)
    db.collection(COLLECTION).document(project_id).set(project.model_dump())
    return project


def get_project(project_id: str) -> Optional["Project"]:
    from src.models import Project

    db = _get_db()
    doc = db.collection(COLLECTION).document(project_id).get()
    if not doc.exists:
        return None
    return Project(**doc.to_dict())


def update_project(project_id: str, updates: dict[str, Any]) -> None:
    db = _get_db()
    db.collection(COLLECTION).document(project_id).update(updates)


def get_user_projects(owner_uid: str) -> list["Project"]:
    from src.models import Project

    db = _get_db()
    docs = (
        db.collection(COLLECTION)
        .where("owner_uid", "==", owner_uid)
        .order_by("created_at", direction=firestore.Query.DESCENDING)
        .stream()
    )
    return [Project(**doc.to_dict()) for doc in docs]

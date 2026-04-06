from fastapi import APIRouter, Depends

from src.auth import _get_uid_from_token
from src.firestore import create_project, get_user_projects

router = APIRouter()


@router.post("/projects", status_code=201)
def create(uid: str = Depends(_get_uid_from_token)):
    project = create_project(owner_uid=uid)
    return project.model_dump()


@router.get("/projects")
def list_projects(uid: str = Depends(_get_uid_from_token)):
    projects = get_user_projects(uid)
    return [p.model_dump() for p in projects]

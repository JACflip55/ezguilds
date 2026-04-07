from fastapi import APIRouter, Depends, HTTPException

from src.auth import _get_uid_from_token
from src.firestore import get_project
from src.storage import get_signed_url

router = APIRouter()


@router.get("/projects/{project_id}/design")
def get_design(project_id: str, uid: str = Depends(_get_uid_from_token)):
    project = get_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.owner_uid != uid:
        raise HTTPException(status_code=403, detail="Not your project")
    if project.design.status != "complete":
        raise HTTPException(status_code=409, detail="Design not ready")

    return {
        "svg_url": get_signed_url(project.design.gcs_path),
        "png_url": get_signed_url(project.design.png_path),
        "metadata_url": get_signed_url(project.design.metadata_path),
    }

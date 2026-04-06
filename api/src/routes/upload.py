from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form

from src.auth import _get_uid_from_token
from src.firestore import get_project, update_project
from src.storage import upload_file
from src.models import FileRef

router = APIRouter()


@router.post("/projects/{project_id}/upload")
async def upload(
    project_id: str,
    file: UploadFile = File(...),
    file_type: Literal["site_map", "soil_test", "photo", "other"] = Form("other"),
    uid: str = Depends(_get_uid_from_token),
):
    project = get_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.owner_uid != uid:
        raise HTTPException(status_code=403, detail="Not your project")

    content = await file.read()
    gcs_path = upload_file(
        project_id=project_id,
        filename=file.filename,
        content=content,
        content_type=file.content_type or "application/octet-stream",
    )

    file_ref = FileRef(name=file.filename, gcs_path=gcs_path, type=file_type)
    project.context.files.append(file_ref)
    update_project(project_id, {"context": project.context.model_dump()})

    return file_ref.model_dump()

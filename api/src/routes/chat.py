from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile, File

from src.auth import _get_uid_from_token
from src.firestore import get_project, update_project
from src.gemini import generate_chat_response
from src.models import ChatMessage
from src.routes.generate import enqueue_generation
from src.storage import upload_file

router = APIRouter()


@router.post("/projects/{project_id}/chat")
async def chat(
    project_id: str,
    message: str = Form(...),
    file: Optional[UploadFile] = File(None),
    uid: str = Depends(_get_uid_from_token),
):
    project = get_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.owner_uid != uid:
        raise HTTPException(status_code=403, detail="Not your project")

    # Handle optional file upload
    if file:
        content = await file.read()
        upload_file(
            project_id=project_id,
            filename=file.filename,
            content=content,
            content_type=file.content_type or "application/octet-stream",
        )

    # Build context for Gemini
    project_context = {
        "location": project.location,
        "scale": project.scale,
        "detail_level": project.detail_level,
        "goals": project.goals,
    }
    chat_history = [m.model_dump() for m in project.chat_history]

    result = generate_chat_response(
        project_context=project_context,
        chat_history=chat_history,
        new_message=message,
    )

    # Append messages to history
    project.chat_history.append(ChatMessage(role="user", content=message))
    project.chat_history.append(ChatMessage(role="assistant", content=result["response"]))
    update_project(project_id, {
        "chat_history": [m.model_dump() for m in project.chat_history],
    })

    # Trigger regeneration if needed
    if result.get("needs_regeneration"):
        update_project(project_id, {"status": "generating"})
        enqueue_generation(project_id)

    return result

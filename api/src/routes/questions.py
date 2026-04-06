from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from src.auth import _get_uid_from_token
from src.firestore import get_project, update_project
from src.gemini import generate_next_question
from src.models import Answer

router = APIRouter()


@router.get("/projects/{project_id}/questions")
def get_next(project_id: str, uid: str = Depends(_get_uid_from_token)):
    project = get_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.owner_uid != uid:
        raise HTTPException(status_code=403, detail="Not your project")

    if project.status == "uploading":
        update_project(project_id, {"status": "questioning"})

    files_summary = [f"{f.name} ({f.type})" for f in project.context.files]
    previous_answers = [a.model_dump() for a in project.context.answers]

    result = generate_next_question(
        goals=project.goals,
        location=project.location,
        files_summary=files_summary,
        previous_answers=previous_answers,
    )

    return result


class AnswerRequest(BaseModel):
    answer: str


@router.post("/projects/{project_id}/answers")
def submit_answer(
    project_id: str,
    body: AnswerRequest,
    uid: str = Depends(_get_uid_from_token),
):
    project = get_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.owner_uid != uid:
        raise HTTPException(status_code=403, detail="Not your project")

    # The question text comes from the last question generated — stored client-side
    # and sent back with the answer for now (POC simplification)
    next_order = len(project.context.answers) + 1
    answer = Answer(
        question="",  # Will be set by frontend in a future iteration
        answer=body.answer,
        order=next_order,
    )
    project.context.answers.append(answer)
    update_project(project_id, {"context": project.context.model_dump()})

    return {"status": "ok", "answer_count": next_order}

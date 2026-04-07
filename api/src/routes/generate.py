import json
import os

from fastapi import APIRouter, Depends, HTTPException
from google.cloud import tasks_v2

from src.auth import _get_uid_from_token
from src.firestore import get_project, update_project

router = APIRouter()


def enqueue_generation(project_id: str) -> None:
    client = tasks_v2.CloudTasksClient()
    project = os.environ.get("GCP_PROJECT", "ezguilds-poc")
    location = os.environ.get("GCP_REGION", "us-central1")
    queue = "ezguilds-generate"
    worker_url = os.environ.get(
        "WORKER_URL", "http://localhost:8001"
    )

    parent = client.queue_path(project, location, queue)
    task = {
        "http_request": {
            "http_method": tasks_v2.HttpMethod.POST,
            "url": f"{worker_url}/tasks/generate",
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"project_id": project_id}).encode(),
        }
    }
    client.create_task(parent=parent, task=task)


@router.post("/projects/{project_id}/generate")
def start_generation(project_id: str, uid: str = Depends(_get_uid_from_token)):
    project = get_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.owner_uid != uid:
        raise HTTPException(status_code=403, detail="Not your project")

    update_project(project_id, {
        "status": "generating",
        "design": {"status": "generating", "gcs_path": None, "png_path": None, "metadata_path": None, "generated_at": None},
    })

    enqueue_generation(project_id)
    return {"status": "generating"}


@router.get("/projects/{project_id}/status")
def get_status(project_id: str, uid: str = Depends(_get_uid_from_token)):
    project = get_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.owner_uid != uid:
        raise HTTPException(status_code=403, detail="Not your project")

    return {
        "project_status": project.status,
        "design_status": project.design.status,
    }

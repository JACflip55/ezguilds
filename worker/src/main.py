from fastapi import FastAPI, Request

from src.pipeline import run_generation

app = FastAPI(title="EZGuilds Worker")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/tasks/generate")
async def handle_generate_task(request: Request):
    body = await request.json()
    project_id = body["project_id"]
    run_generation(project_id)
    return {"status": "ok"}

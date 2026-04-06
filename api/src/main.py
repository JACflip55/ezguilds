from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes import projects, upload

app = FastAPI(title="EZGuilds API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(projects.router)
app.include_router(upload.router)


@app.get("/health")
def health():
    return {"status": "ok"}

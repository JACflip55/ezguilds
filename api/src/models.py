from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


class FileRef(BaseModel):
    name: str
    gcs_path: str
    type: Literal["site_map", "soil_test", "photo", "other"]


class Answer(BaseModel):
    question: str
    answer: str
    order: int


class ProjectContext(BaseModel):
    files: list[FileRef] = Field(default_factory=list)
    answers: list[Answer] = Field(default_factory=list)


class DesignState(BaseModel):
    status: Literal["pending", "generating", "complete", "failed"] = "pending"
    gcs_path: Optional[str] = None
    png_path: Optional[str] = None
    metadata_path: Optional[str] = None
    generated_at: Optional[datetime] = None


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str
    design_version: Optional[int] = None


class Project(BaseModel):
    id: str
    owner_uid: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: Literal["uploading", "questioning", "generating", "reviewing"] = "uploading"
    scale: Optional[Literal["bed", "yard", "smallholding", "acreage"]] = None
    detail_level: Optional[Literal["general", "moderate", "specific"]] = None
    location: Optional[str] = None
    hardiness_zone: Optional[str] = None
    goals: Optional[str] = None
    context: ProjectContext = Field(default_factory=ProjectContext)
    design: DesignState = Field(default_factory=DesignState)
    chat_history: list[ChatMessage] = Field(default_factory=list)

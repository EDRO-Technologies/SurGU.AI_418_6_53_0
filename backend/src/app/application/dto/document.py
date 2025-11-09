# app/application/dto/document.py
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class DocumentDTO(BaseModel):
    id: UUID
    filename: str
    path: str
    size: int
    upload_date: datetime
    description: str | None = None


class DocumentAddDTO(BaseModel):
    id: UUID
    filename: str
    path: str
    size: int
    user_id: UUID
    description: str | None = None


class DocumentResponse(BaseModel):
    id: UUID
    filename: str
    size: int
    upload_date: datetime
    path: str
    description: str | None = None

from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.application.dto.document import DocumentDTO
from app.infrastructure.sqla_persistance.models.base import Base


class DocumentModel(Base):
    __tablename__ = "documents"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(String(255))
    path: Mapped[str] = mapped_column(String(500))
    size: Mapped[int]
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.user_id"))
    upload_date: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    def to_dto(self) -> DocumentDTO:
        return DocumentDTO(
            id=self.id,
            filename=self.filename,
            path=self.path,
            size=self.size,
            upload_date=self.upload_date,
            description=self.description,
        )

from datetime import datetime
from typing import Literal
from uuid import UUID

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.application.dto.user import UserDTO, UserWithPasswordDTO
from app.infrastructure.sqla_persistance.models.base import Base


class UserModel(Base):
    __tablename__ = "users"

    user_id: Mapped[UUID] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(40), unique=True)
    password: Mapped[bytes]
    role: Mapped[Literal["user", "admin"]] = mapped_column(default="user")
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    def to_dto(self) -> UserDTO:
        return UserDTO(
            user_id=self.user_id,
            username=self.username,
            role=self.role,
            created_at=self.created_at,
        )

    def to_dto_with_pass(self) -> UserWithPasswordDTO:
        return UserWithPasswordDTO(
            user_id=self.user_id,
            username=self.username,
            password=self.password,
            role=self.role,
            created_at=self.created_at,
        )

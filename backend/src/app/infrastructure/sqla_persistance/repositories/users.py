from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dto.user import (
    UserDTO,
    UserRegistrationDTO,
    UserWithPasswordDTO,
)
from app.infrastructure.sqla_persistance.models.user import UserModel


class SqlaUserRepository:
    _model = UserModel

    def __init__(self, session: AsyncSession):
        self._session = session

    async def add_one(self, user: UserRegistrationDTO) -> None:
        await self._session.execute(insert(UserModel).values(user.model_dump()))

    async def get_one_by_username(self, username: str) -> UserDTO | None:
        user = (
            await self._session.execute(
                select(UserModel).where(UserModel.username == username)
            )
        ).scalar_one_or_none()
        return user.to_dto() if user else None

    async def get_one_by_username_with_password(
        self, username: str
    ) -> UserWithPasswordDTO | None:
        user = (
            await self._session.execute(
                select(UserModel).where(UserModel.username == username)
            )
        ).scalar_one_or_none()
        return user.to_dto_with_pass() if user else None

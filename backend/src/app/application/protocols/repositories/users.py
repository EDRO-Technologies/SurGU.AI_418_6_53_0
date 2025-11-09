from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from app.application.dto.user import UserAddDTO, UserDTO, UserWithPasswordDTO


class UserRepository(Protocol):
    @abstractmethod
    async def add_one(self, user: UserAddDTO) -> None: ...

    @abstractmethod
    async def get_one_by_username(self, username: str) -> UserDTO | None: ...

    @abstractmethod
    async def get_one_by_username_with_password(
        self, username: str
    ) -> UserWithPasswordDTO | None: ...

    @abstractmethod
    async def get_one_by_user_id(self, user_id: UUID) -> UserDTO | None: ...

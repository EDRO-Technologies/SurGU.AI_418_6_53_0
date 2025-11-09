from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.infrastructure.sqla_persistance.repositories.documents import (
    SqlaDocumentRepository,
)
from app.infrastructure.sqla_persistance.repositories.users import (
    SqlaUserRepository,
)


class SqlaTransactionManager:
    documents: SqlaDocumentRepository
    users: SqlaUserRepository

    def __init__(self, async_session_maker: async_sessionmaker[AsyncSession]):
        self._async_factory = async_session_maker

    async def __aenter__(self) -> Self:
        self._async_session: AsyncSession = self._async_factory()

        self.documents = SqlaDocumentRepository(self._async_session)
        self.users = SqlaUserRepository(self._async_session)

        return self

    async def __aexit__(self, *args: tuple) -> None:
        await self.rollback()
        await self._async_session.close()

    async def commit(self) -> None:
        await self._async_session.commit()

    async def rollback(self) -> None:
        await self._async_session.rollback()

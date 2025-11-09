from abc import abstractmethod
from typing import Protocol, Self

from app.application.protocols.repositories.documents import DocumentRepository
from app.application.protocols.repositories.users import UserRepository


class TransactionManager(Protocol):
    documents: DocumentRepository
    users: UserRepository

    @abstractmethod
    def __aenter__(self) -> Self: ...

    @abstractmethod
    async def __aexit__(self, *args: tuple) -> None:  # pyright: ignore[reportUnknownParameterType, reportMissingTypeArgument]
        ...

    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...

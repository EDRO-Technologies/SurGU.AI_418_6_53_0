from typing import Protocol
from uuid import UUID

from app.application.dto.document import DocumentAddDTO, DocumentDTO


class DocumentRepository(Protocol):
    async def add_one(self, document: DocumentAddDTO) -> None: ...

    async def get_one_by_id(self, document_id: UUID) -> DocumentDTO | None: ...

    async def get_all_by_user_id(
        self, user_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[DocumentDTO]: ...

    async def delete_one(self, document_id: UUID) -> None: ...

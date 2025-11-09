from uuid import UUID

from app.application.dto.document import DocumentDTO
from app.application.protocols.transaction_manager import TransactionManager


class ListDocumentsUsecase:
    def __init__(self, transaction_manager: TransactionManager):
        self._transaction_manager = transaction_manager

    async def __call__(
        self, user_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[DocumentDTO]:
        async with self._transaction_manager:
            return await self._transaction_manager.documents.get_all_by_user_id(
                user_id, skip=skip, limit=limit
            )

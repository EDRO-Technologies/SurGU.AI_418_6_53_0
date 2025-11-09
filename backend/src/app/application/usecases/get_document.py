from uuid import UUID

from app.application.dto.document import DocumentDTO
from app.application.exceptions.base import DocumentNotFoundError
from app.application.protocols.transaction_manager import TransactionManager


class GetDocumentUsecase:
    def __init__(self, transaction_manager: TransactionManager):
        self._transaction_manager = transaction_manager

    async def __call__(self, document_id: UUID) -> DocumentDTO:
        async with self._transaction_manager:
            document = await self._transaction_manager.documents.get_one_by_id(
                document_id
            )

            if document is None:
                raise DocumentNotFoundError

            return document

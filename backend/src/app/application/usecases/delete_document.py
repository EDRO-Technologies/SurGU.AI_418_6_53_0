from pathlib import Path
from uuid import UUID

from app.application.exceptions.base import DocumentNotFoundError
from app.application.protocols.transaction_manager import TransactionManager
from app.application.services.vector_store import VectorStoreService


class DeleteDocumentUsecase:
    def __init__(
        self,
        transaction_manager: TransactionManager,
        vector_store: VectorStoreService,
    ):
        self._transaction_manager = transaction_manager
        self._vector_store = vector_store

    async def __call__(self, document_id: UUID) -> None:
        async with self._transaction_manager:
            document = await self._transaction_manager.documents.get_one_by_id(
                document_id
            )

            if document is None:
                raise DocumentNotFoundError

            await self._vector_store.delete_documents(str(document_id))

            file_path = Path(document.path)
            if file_path.exists():
                file_path.unlink()

            await self._transaction_manager.documents.delete_one(document_id)
            await self._transaction_manager.commit()

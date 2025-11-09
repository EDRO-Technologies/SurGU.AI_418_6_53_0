from uuid import UUID

from app.application.protocols.transaction_manager import TransactionManager
from app.application.services.document_processor import DocumentProcessorService
from app.application.services.vector_store import VectorStoreService


class IndexDocumentUsecase:
    def __init__(
        self,
        transaction_manager: TransactionManager,
        document_processor: DocumentProcessorService,
        vector_store: VectorStoreService,
    ):
        self._transaction_manager = transaction_manager
        self._document_processor = document_processor
        self._vector_store = vector_store

    async def __call__(self, document_id: UUID) -> None:
        async with self._transaction_manager:
            document = await self._transaction_manager.documents.get_one_by_id(
                document_id
            )

            if not document:
                return

            chunks = await self._document_processor.process_document(
                document.path
            )
            await self._vector_store.add_documents(chunks, str(document_id))

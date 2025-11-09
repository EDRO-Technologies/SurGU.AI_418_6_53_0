from uuid import UUID, uuid4

from app.application.dto.document import DocumentAddDTO, DocumentDTO
from app.application.protocols.transaction_manager import TransactionManager


class UploadDocumentUsecase:
    def __init__(self, transaction_manager: TransactionManager):
        self._transaction_manager = transaction_manager

    async def __call__(
        self,
        filename: str,
        path: str,
        size: int,
        user_id: UUID,
        description: str | None = None,
    ) -> DocumentDTO:
        async with self._transaction_manager:
            document = DocumentAddDTO(
                id=uuid4(),
                filename=filename,
                path=path,
                size=size,
                user_id=user_id,
                description=description,
            )
            await self._transaction_manager.documents.add_one(document)
            await self._transaction_manager.commit()

            return await self._transaction_manager.documents.get_one_by_id(
                document.id
            )

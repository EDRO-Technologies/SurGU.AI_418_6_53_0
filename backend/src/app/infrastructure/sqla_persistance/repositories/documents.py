from uuid import UUID

from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dto.document import DocumentAddDTO, DocumentDTO
from app.infrastructure.sqla_persistance.models.document import DocumentModel


class SqlaDocumentRepository:
    _model = DocumentModel

    def __init__(self, session: AsyncSession):
        self._session = session

    async def add_one(self, document: DocumentAddDTO) -> None:
        await self._session.execute(
            insert(DocumentModel).values(document.model_dump())
        )

    async def get_one_by_id(self, document_id: UUID) -> DocumentDTO | None:
        document = (
            await self._session.execute(
                select(DocumentModel).where(DocumentModel.id == document_id)
            )
        ).scalar_one_or_none()
        return document.to_dto() if document else None

    async def get_all_by_user_id(
        self, user_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[DocumentDTO]:
        documents = (
            (
                await self._session.execute(
                    select(DocumentModel)
                    .where(DocumentModel.user_id == user_id)
                    .order_by(DocumentModel.upload_date.desc())
                    .offset(skip)
                    .limit(limit)
                )
            )
            .scalars()
            .all()
        )
        return [document.to_dto() for document in documents]

    async def delete_one(self, document_id: UUID) -> None:
        await self._session.execute(
            delete(DocumentModel).where(DocumentModel.id == document_id)
        )

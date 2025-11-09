from pathlib import Path
from uuid import UUID

import aiofiles
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status
from fastapi.responses import FileResponse

from app.application.dto.document import DocumentResponse
from app.application.usecases.delete_document import DeleteDocumentUsecase
from app.application.usecases.get_document import GetDocumentUsecase
from app.application.usecases.index_document import IndexDocumentUsecase
from app.application.usecases.list_documents import ListDocumentsUsecase
from app.application.usecases.upload_document import UploadDocumentUsecase
from app.main.config import AppConfig

document_router = APIRouter(
    prefix="/document", tags=["document"], route_class=DishkaRoute
)


def validate_file(file: UploadFile, config: AppConfig) -> None:
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Имя файла не указано",
        )

    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in config.allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Недопустимый тип файла. Разрешены: {', '.join(config.allowed_extensions)}",
        )


async def save_file_async(
    file: UploadFile, config: AppConfig, user_id: UUID
) -> tuple[str, int]:
    file_path = Path(config.documents_dir) / str(user_id) / file.filename

    content = await file.read()

    if len(content) > config.max_document_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Файл слишком большой. Максимум: {config.max_document_size / 1024 / 1024} MB",
        )

    file_path.parent.mkdir(parents=True, exist_ok=True)

    async with aiofiles.open(file_path, "wb") as f:
        await f.write(content)

    return str(file_path), len(content)


@document_router.post("", response_model=DocumentResponse, status_code=201)
async def upload_document(
    user_id: FromDishka[UUID],
    config: FromDishka[AppConfig],
    upload_usecase: FromDishka[UploadDocumentUsecase],
    index_usecase: FromDishka[IndexDocumentUsecase],
    file: UploadFile = File(...),
    description: str | None = Form(None),
) -> DocumentResponse:
    validate_file(file, config)

    file_path, file_size = await save_file_async(file, config, user_id)

    document = await upload_usecase(
        filename=file.filename,
        path=file_path,
        size=file_size,
        user_id=user_id,
        description=description,
    )

    await index_usecase(document.id)

    return DocumentResponse(
        id=document.id,
        filename=document.filename,
        size=document.size,
        upload_date=document.upload_date,
        path=document.path,
        description=document.description,
    )


@document_router.get("/{document_id}/download")
async def download_document(
    document_id: UUID,
    user_id: FromDishka[UUID],
    get_usecase: FromDishka[GetDocumentUsecase],
) -> FileResponse:
    document = await get_usecase(document_id, user_id)

    file_path = Path(document.path)

    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Документ не найден"
        )

    return FileResponse(
        path=file_path,
        filename=document.filename,
        media_type="application/octet-stream",
    )


@document_router.delete("/{document_id}", status_code=204)
async def delete_document(
    document_id: UUID,
    user_id: FromDishka[UUID],
    delete_usecase: FromDishka[DeleteDocumentUsecase],
):
    await delete_usecase(document_id)


@document_router.get("", response_model=list[DocumentResponse])
async def list_documents(
    user_id: FromDishka[UUID],
    list_usecase: FromDishka[ListDocumentsUsecase],
    skip: int = 0,
    limit: int = 100,
) -> list[DocumentResponse]:
    documents = await list_usecase(user_id, skip, limit)

    return [
        DocumentResponse(
            id=doc.id,
            filename=doc.filename,
            size=doc.size,
            upload_date=doc.upload_date,
            path=doc.path,
            description=doc.description,
        )
        for doc in documents
    ]

from fastapi import APIRouter

from app.presentation.api.v1.auth import auth_router
from app.presentation.api.v1.document import document_router
from app.presentation.api.v1.general import general_router


def create_api_root_router(prefix: str) -> APIRouter:
    root_router = APIRouter(prefix=f"{prefix}/v1")
    for router in [auth_router, document_router, general_router]:
        root_router.include_router(router)

    return root_router

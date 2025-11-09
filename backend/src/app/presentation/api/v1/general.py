from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from app.main.config import AppConfig

general_router = APIRouter(tags=["general"], route_class=DishkaRoute)


class HealthcheckResponse(BaseModel):
    status: str = "OK"


@general_router.get(
    "/healthcheck",
    response_model=HealthcheckResponse,
    status_code=status.HTTP_200_OK,
)
async def healthcheck() -> HealthcheckResponse:
    return HealthcheckResponse()


@general_router.get("/")
async def redirect_to_docs(
    app_config: FromDishka[AppConfig],
) -> RedirectResponse:
    return RedirectResponse(f"{app_config.prefix}{app_config.docs_url}")

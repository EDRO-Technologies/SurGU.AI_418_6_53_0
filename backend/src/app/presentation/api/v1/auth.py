from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Response

from app.application.dto.user import UserCredentialsDTO, UserRegistrationDTO
from app.application.usecases.auth_login import AuthLoginUsecase
from app.application.usecases.create_user import CreateUserUsecase
from app.main.config import JWTConfig

auth_router = APIRouter(prefix="/auth", tags=["auth"], route_class=DishkaRoute)


@auth_router.post("/login", response_model=None, status_code=204)
async def login(
    jwt_config: FromDishka[JWTConfig],
    credentials: UserCredentialsDTO,
    usecase: FromDishka[AuthLoginUsecase],
    response: Response,
):
    access_token = await usecase(credentials)
    response.set_cookie(
        "access_token",
        access_token,
        max_age=jwt_config.expire_at_seconds,
        httponly=True,
        samesite="strict",
    )


@auth_router.post("/registration", response_model=None, status_code=201)
async def registration(
    usecase: FromDishka[CreateUserUsecase], user: UserRegistrationDTO
):
    await usecase(user)


@auth_router.post("/logout", response_model=None, status_code=204)
async def logout(response: Response):
    response.delete_cookie("access_token")

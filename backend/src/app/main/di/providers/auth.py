from uuid import UUID

import jwt
from dishka import Provider, Scope, provide
from fastapi import Request

from app.application.auth_utils import jwt_decode
from app.application.exceptions.base import (
    InvalidTokenError,
    NotAuthenticatedError,
)
from app.main.config import JWTConfig


class AuthProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_user_id(self, request: Request, jwt_config: JWTConfig) -> UUID:
        access_token = request.cookies.get("access_token")

        if not access_token or not access_token.startswith("Bearer "):
            raise NotAuthenticatedError

        try:
            payload = jwt_decode(access_token.split()[1], jwt_config)
            sub = payload.get("sub", "")
            if not sub:
                raise InvalidTokenError
            return UUID(sub)
        except jwt.InvalidTokenError:
            raise InvalidTokenError

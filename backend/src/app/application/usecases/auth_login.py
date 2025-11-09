from app.application.auth_utils import is_valid_password, jwt_encode
from app.application.dto.user import UserCredentialsDTO
from app.application.exceptions.base import InvalidCredentialsError
from app.application.protocols.transaction_manager import TransactionManager
from app.main.config import JWTConfig


class AuthLoginUsecase:
    def __init__(
        self, transaction_manager: TransactionManager, jwt_config: JWTConfig
    ):
        self._jwt_config = jwt_config
        self._transaction_manager = transaction_manager

    async def __call__(self, credentials: UserCredentialsDTO) -> str:
        async with self._transaction_manager:
            user = await self._transaction_manager.users.get_one_by_username_with_password(
                credentials.username
            )

            if user is None or not is_valid_password(
                credentials.password, user.password
            ):
                raise InvalidCredentialsError

            access_token = jwt_encode(
                {"sub": str(user.user_id)}, self._jwt_config
            )

            return f"Bearer {access_token}"

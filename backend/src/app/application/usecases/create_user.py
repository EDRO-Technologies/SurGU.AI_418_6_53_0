from app.application.auth_utils import hash_password
from app.application.dto.user import UserAddDTO, UserRegistrationDTO
from app.application.exceptions.base import UserAlreadyExistsError
from app.application.protocols.transaction_manager import TransactionManager


class CreateUserUsecase:
    def __init__(self, transaction_manager: TransactionManager):
        self._transaction_manager = transaction_manager

    async def __call__(self, register_user: UserRegistrationDTO) -> None:
        async with self._transaction_manager:
            if (
                await self._transaction_manager.users.get_one_by_username(
                    register_user.username
                )
                is not None
            ):
                raise UserAlreadyExistsError

            user = UserAddDTO(
                username=register_user.username,
                password=hash_password(register_user.password),
                role=register_user.role,
            )
            await self._transaction_manager.users.add_one(user)
            await self._transaction_manager.commit()

from aiogram import Bot, Dispatcher
from dishka import AsyncContainer, Provider, make_async_container

from app.main.config import Config


def create_di_container(
    providers: list[Provider], config: Config, bot: Bot, dp: Dispatcher
) -> AsyncContainer:
    return make_async_container(
        *providers, context={bot: Bot, Config: config, dp: Dispatcher}
    )

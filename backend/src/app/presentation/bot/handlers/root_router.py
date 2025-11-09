from aiogram import Router

from app.presentation.bot.handlers.all_messages import all_messages_router
from app.presentation.bot.handlers.start import start_router


def create_bot_root_router() -> Router:
    root_router = Router()
    for router in [start_router, all_messages_router]:
        root_router.include_router(router)

    return root_router

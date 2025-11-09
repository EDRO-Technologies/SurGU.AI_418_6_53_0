from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from app.main.config import RedisConfig
from app.presentation.bot.handlers.root_router import create_bot_root_router


def create_bot(bot_token: str) -> Bot:
    return Bot(
        token=bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )


def create_dp(config: RedisConfig) -> Dispatcher:
    dp = Dispatcher(
        storage=RedisStorage.from_url(
            f"redis://{config.host}:{config.port}/{config.num_db}"
        )
    )
    dp.include_router(create_bot_root_router())
    return dp

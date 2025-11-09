import asyncio
import logging
from contextlib import asynccontextmanager

from dishka.integrations.aiogram import setup_dishka as aiogram_setup_dishka
from dishka.integrations.fastapi import setup_dishka as fastapi_setup_dishka
from fastapi import FastAPI

from app.application.services.scheduler import SchedulerService
from app.application.usecases.schedule_indexing import ScheduleIndexingUsecase
from app.main.bot import create_bot, create_dp
from app.main.config import Config
from app.main.di.container import create_di_container
from app.main.di.providers.provider_registry import get_providers
from app.presentation.api.v1.root_router import create_api_root_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    bot = app.state.bot
    dp = app.state.dispatcher
    container = app.state.dishka_container

    polling_task = asyncio.create_task(dp.start_polling(bot))
    app.state.bot_polling_task = polling_task

    async with container() as request_container:
        scheduler = await request_container.get(SchedulerService)
        schedule_indexing = await request_container.get(ScheduleIndexingUsecase)
        config = await request_container.get(Config)

        scheduler.start()
        await schedule_indexing(interval_seconds=config.rag.indexing_interval)
        app.state.scheduler = scheduler

        logger.info("Application started")
        logger.info(
            f"Indexing scheduler started (interval: {config.rag.indexing_interval}s)"
        )

        yield

        scheduler.stop()
        logger.info("Scheduler stopped")

    polling_task.cancel()
    try:
        await polling_task
    except asyncio.CancelledError:
        logger.info("Bot polling task cancelled")

    await container.close()


def create_app() -> FastAPI:
    config = Config()
    bot = create_bot(config.bot.token)
    dp = create_dp(config.redis)
    container = create_di_container(get_providers(), config, bot, dp)

    app = FastAPI(
        title="hackathon",
        prefix=config.app.prefix,
        lifespan=lifespan,
        docs_url=f"{config.app.prefix}{config.app.docs_url}",
        openapi_url=f"{config.app.prefix}{config.app.openapi_url}",
    )
    app.include_router(create_api_root_router(config.app.prefix))

    app.state.bot = bot
    app.state.dispatcher = dp
    app.state.dishka_container = container

    fastapi_setup_dishka(container, app)
    aiogram_setup_dishka(container, dp, auto_inject=True)

    return app

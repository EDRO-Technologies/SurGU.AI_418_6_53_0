from collections.abc import Callable

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger


class SchedulerService:
    def __init__(self):
        self._scheduler = AsyncIOScheduler()

    def start(self) -> None:
        self._scheduler.start()

    def stop(self) -> None:
        self._scheduler.shutdown()

    def add_job(
        self,
        func: Callable,
        interval_seconds: int,
        job_id: str,
    ) -> None:
        self._scheduler.add_job(
            func,
            trigger=IntervalTrigger(seconds=interval_seconds),
            id=job_id,
            replace_existing=True,
        )

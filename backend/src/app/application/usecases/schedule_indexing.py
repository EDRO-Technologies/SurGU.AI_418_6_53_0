from app.application.services.document_indexer import DocumentIndexerService
from app.application.services.scheduler import SchedulerService


class ScheduleIndexingUsecase:
    def __init__(
        self,
        scheduler: SchedulerService,
        indexer: DocumentIndexerService,
    ):
        self._scheduler = scheduler
        self._indexer = indexer

    async def __call__(self, interval_seconds: int = 60) -> None:
        self._scheduler.add_job(
            func=self._indexer.index_all_documents,
            interval_seconds=interval_seconds,
            job_id="document_indexing",
        )

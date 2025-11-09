from dishka import Provider, Scope, provide

from app.application.services.document_indexer import DocumentIndexerService
from app.application.services.document_processor import DocumentProcessorService
from app.application.services.rag_service import RAGService
from app.application.services.scheduler import SchedulerService
from app.application.services.vector_store import VectorStoreService
from app.main.config import AppConfig, OpenRouterConfig, RAGConfig


class RAGProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_document_processor(
        self, rag_config: RAGConfig
    ) -> DocumentProcessorService:
        return DocumentProcessorService(rag_config)

    @provide(scope=Scope.APP)
    def provide_vector_store(
        self, openrouter_config: OpenRouterConfig, rag_config: RAGConfig
    ) -> VectorStoreService:
        return VectorStoreService(openrouter_config, rag_config)

    @provide(scope=Scope.APP)
    def provide_rag_service(
        self,
        vector_store: VectorStoreService,
        openrouter_config: OpenRouterConfig,
        rag_config: RAGConfig,
    ) -> RAGService:
        return RAGService(vector_store, openrouter_config, rag_config)

    @provide(scope=Scope.APP)
    def provide_scheduler(self) -> SchedulerService:
        return SchedulerService()

    @provide(scope=Scope.APP)
    def provide_document_indexer(
        self,
        document_processor: DocumentProcessorService,
        vector_store: VectorStoreService,
        config: AppConfig,
    ) -> DocumentIndexerService:
        return DocumentIndexerService(document_processor, vector_store, config)

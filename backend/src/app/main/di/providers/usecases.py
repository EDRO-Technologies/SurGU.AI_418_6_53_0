from dishka import Provider, Scope, provide

from app.application.protocols.transaction_manager import TransactionManager
from app.application.services.document_indexer import DocumentIndexerService
from app.application.services.document_processor import DocumentProcessorService
from app.application.services.rag_service import RAGService
from app.application.services.scheduler import SchedulerService
from app.application.services.speech_to_text import SpeechToTextService
from app.application.services.vector_store import VectorStoreService
from app.application.usecases.answer_question import AnswerQuestionUsecase
from app.application.usecases.auth_login import AuthLoginUsecase
from app.application.usecases.create_user import CreateUserUsecase
from app.application.usecases.delete_document import DeleteDocumentUsecase
from app.application.usecases.get_document import GetDocumentUsecase
from app.application.usecases.index_document import IndexDocumentUsecase
from app.application.usecases.list_documents import ListDocumentsUsecase
from app.application.usecases.schedule_indexing import ScheduleIndexingUsecase
from app.application.usecases.transcribe_voice import TranscribeVoiceUsecase
from app.application.usecases.upload_document import UploadDocumentUsecase
from app.main.config import JWTConfig


class UseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_create_user_usecase(
        self, transaction_manager: TransactionManager
    ) -> CreateUserUsecase:
        return CreateUserUsecase(transaction_manager)

    @provide(scope=Scope.REQUEST)
    def provide_auth_login_usecase(
        self, transaction_manager: TransactionManager, jwt_config: JWTConfig
    ) -> AuthLoginUsecase:
        return AuthLoginUsecase(transaction_manager, jwt_config)

    @provide(scope=Scope.REQUEST)
    def provide_upload_document_usecase(
        self, transaction_manager: TransactionManager
    ) -> UploadDocumentUsecase:
        return UploadDocumentUsecase(transaction_manager)

    @provide(scope=Scope.REQUEST)
    def provide_get_document_usecase(
        self, transaction_manager: TransactionManager
    ) -> GetDocumentUsecase:
        return GetDocumentUsecase(transaction_manager)

    @provide(scope=Scope.REQUEST)
    def provide_delete_document_usecase(
        self,
        transaction_manager: TransactionManager,
        vector_store: VectorStoreService,
    ) -> DeleteDocumentUsecase:
        return DeleteDocumentUsecase(transaction_manager, vector_store)

    @provide(scope=Scope.REQUEST)
    def provide_list_documents_usecase(
        self, transaction_manager: TransactionManager
    ) -> ListDocumentsUsecase:
        return ListDocumentsUsecase(transaction_manager)

    @provide(scope=Scope.REQUEST)
    def provide_index_document_usecase(
        self,
        transaction_manager: TransactionManager,
        document_processor: DocumentProcessorService,
        vector_store: VectorStoreService,
    ) -> IndexDocumentUsecase:
        return IndexDocumentUsecase(
            transaction_manager, document_processor, vector_store
        )

    @provide(scope=Scope.REQUEST)
    def provide_answer_question_usecase(
        self, rag_service: RAGService
    ) -> AnswerQuestionUsecase:
        return AnswerQuestionUsecase(rag_service)

    @provide(scope=Scope.APP)
    def provide_schedule_indexing_usecase(
        self,
        scheduler: SchedulerService,
        indexer: DocumentIndexerService,
    ) -> ScheduleIndexingUsecase:
        return ScheduleIndexingUsecase(scheduler, indexer)

    @provide(scope=Scope.REQUEST)
    def provide_transcribe_voice_usecase(
        self, speech_to_text: SpeechToTextService
    ) -> TranscribeVoiceUsecase:
        return TranscribeVoiceUsecase(speech_to_text)

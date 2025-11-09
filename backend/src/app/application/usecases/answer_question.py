from app.application.services.rag_service import RAGService


class AnswerQuestionUsecase:
    def __init__(self, rag_service: RAGService):
        self._rag_service = rag_service

    async def __call__(self, question: str) -> str:
        return await self._rag_service.generate_answer(question)

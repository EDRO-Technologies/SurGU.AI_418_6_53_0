import logging

from langchain_core.documents import Document
from openai import AsyncOpenAI

from app.application.services.vector_store import VectorStoreService
from app.main.config import OpenRouterConfig, RAGConfig

logger = logging.getLogger(__name__)


class RAGService:
    def __init__(
        self,
        vector_store: VectorStoreService,
        openrouter_config: OpenRouterConfig,
        rag_config: RAGConfig,
    ):
        self._vector_store = vector_store
        self._config = rag_config
        self._client = AsyncOpenAI(
            api_key=openrouter_config.api_key,
            base_url=openrouter_config.base_url,
        )
        self._model = openrouter_config.model
        logger.info(f"RAGService initialized with model: {self._model}")

    async def generate_answer(self, question: str) -> str:
        logger.info(f"Generating answer for question: '{question}'")

        relevant_docs = await self._vector_store.search(
            question, top_k=self._config.top_k
        )

        if not relevant_docs:
            logger.warning("No relevant documents found")
            return "К сожалению, я не нашел релевантной информации в нормативных документах для ответа на ваш вопрос."

        logger.info(f"Building context from {len(relevant_docs)} documents")
        context = self._build_context(relevant_docs)
        prompt = self._build_prompt(context, question)

        logger.info("Sending request to LLM")
        response = await self._client.chat.completions.create(
            model=self._model,
            messages=[
                {
                    "role": "system",
                    "content": "Ты помощник по нормативным документам. Отвечай на вопросы пользователей на основе предоставленного контекста. Если информации недостаточно, так и скажи.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
        )

        answer = response.choices[0].message.content
        logger.info(f"Generated answer length: {len(answer)} characters")
        return answer

    def _build_context(self, documents: list[Document]) -> str:
        context_parts = []
        for i, doc in enumerate(documents, 1):
            source = doc.metadata.get("source", "Неизвестный источник")
            page = doc.metadata.get("page", "N/A")
            context_parts.append(
                f"[Фрагмент {i}] (Источник: {source}, Страница: {page})\n{doc.page_content}\n"
            )
        return "\n---\n".join(context_parts)

    def _build_prompt(self, context: str, question: str) -> str:
        return f"""На основе следующих фрагментов нормативных документов, ответь на вопрос пользователя.

Контекст:
{context}

Вопрос: {question}

Ответ должен быть:
- Точным и основанным только на предоставленном контексте
- На русском языке
- Структурированным и понятным
- Формат ссылок: [Документ: <название>, страница <№>, пункт(опционально)].
- Используй html форматирование, чтобы работало с телеграмом.
- Давай ответ кратко, по существу, без воды.

Ответ:"""

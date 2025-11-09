import logging

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

from app.main.config import OpenRouterConfig, RAGConfig

logger = logging.getLogger(__name__)


class VectorStoreService:
    def __init__(
        self, openrouter_config: OpenRouterConfig, rag_config: RAGConfig
    ):
        logger.info("Initializing VectorStoreService")
        logger.info(f"Vector DB path: {rag_config.vector_db_path}")
        logger.info("Embedding model: text-embedding-3-small")

        self._embeddings = OpenAIEmbeddings(
            openai_api_key=openrouter_config.api_key,
            openai_api_base=openrouter_config.base_url,
            model="text-embedding-3-small",
        )
        self._vector_store = Chroma(
            persist_directory=str(rag_config.vector_db_path),
            embedding_function=self._embeddings,
        )

        logger.info("VectorStoreService initialized")

    async def add_documents(
        self, documents: list[Document], document_id: str
    ) -> None:
        logger.info(f"Adding {len(documents)} documents with ID: {document_id}")

        for doc in documents:
            doc.metadata["document_id"] = document_id

        self._vector_store.add_documents(documents)
        logger.info("✓ Documents added to vector store")

    async def delete_documents(self, document_id: str) -> None:
        logger.info(f"Deleting documents with ID: {document_id}")

        results = self._vector_store.get(where={"document_id": document_id})
        if results and results.get("ids"):
            self._vector_store.delete(ids=results["ids"])
            logger.info(f"✓ Deleted {len(results['ids'])} chunks")
        else:
            logger.warning(f"No documents found with ID: {document_id}")

    async def search(self, query: str, top_k: int = 5) -> list[Document]:
        logger.info(f"Searching for: '{query}' (top_k={top_k})")

        results = self._vector_store.similarity_search(query, k=top_k)

        logger.info(f"Found {len(results)} results")
        for i, doc in enumerate(results, 1):
            logger.debug(f"Result {i}: {doc.page_content[:100]}...")

        return results

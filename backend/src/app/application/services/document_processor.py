import logging
import warnings

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.main.config import RAGConfig

logger = logging.getLogger(__name__)


class DocumentProcessorService:
    def __init__(self, config: RAGConfig):
        self._config = config
        self._text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
        )

    async def load_pdf(self, file_path: str) -> list[Document]:
        try:
            with warnings.catch_warnings():
                warnings.filterwarnings(
                    "ignore", message="incorrect startxref pointer"
                )
                warnings.filterwarnings(
                    "ignore", message="parsing for Object Streams"
                )
                loader = PyPDFLoader(file_path)
                documents = loader.load()

            if not documents:
                logger.warning(f"PDF file is empty or corrupted: {file_path}")
                return []

            return documents
        except Exception as e:
            logger.exception(f"Failed to load PDF {file_path}: {e}")
            return []

    async def split_documents(
        self, documents: list[Document]
    ) -> list[Document]:
        if not documents:
            return []
        return self._text_splitter.split_documents(documents)

    async def process_document(self, file_path: str) -> list[Document]:
        documents = await self.load_pdf(file_path)
        return await self.split_documents(documents)

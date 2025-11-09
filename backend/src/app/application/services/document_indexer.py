import logging
from pathlib import Path

from app.application.services.document_processor import DocumentProcessorService
from app.application.services.vector_store import VectorStoreService
from app.main.config import AppConfig

logger = logging.getLogger(__name__)


class DocumentIndexerService:
    def __init__(
        self,
        document_processor: DocumentProcessorService,
        vector_store: VectorStoreService,
        config: AppConfig,
    ):
        self._processor = document_processor
        self._vector_store = vector_store
        self._config = config
        self._indexed_files: set[str] = set()

    async def index_all_documents(self) -> None:
        documents_dir = Path(self._config.documents_dir)

        logger.info(f"Checking documents directory: {documents_dir}")

        if not documents_dir.exists():
            logger.warning(
                f"Documents directory does not exist: {documents_dir}"
            )
            return

        current_files = set()

        for pdf_file in documents_dir.rglob("*.pdf"):
            current_files.add(str(pdf_file))
            logger.info(f"Found PDF: {pdf_file.name}")

            if str(pdf_file) not in self._indexed_files:
                await self._index_document(pdf_file)

        logger.info(f"Total indexed files: {len(self._indexed_files)}")

        removed_files = self._indexed_files - current_files
        for removed_file in removed_files:
            await self._remove_document(removed_file)

    async def _index_document(self, file_path: Path) -> None:
        try:
            logger.info(f"Indexing document: {file_path.name}")
            chunks = await self._processor.process_document(str(file_path))
            logger.info(f"Created {len(chunks)} chunks from {file_path.name}")

            document_id = file_path.stem
            await self._vector_store.add_documents(chunks, document_id)
            self._indexed_files.add(str(file_path))
            logger.info(f"✓ Successfully indexed: {file_path.name}")
        except Exception as e:
            logger.error(
                f"✗ Failed to index {file_path.name}: {e}", exc_info=True
            )

    async def _remove_document(self, file_path: str) -> None:
        try:
            document_id = Path(file_path).stem
            await self._vector_store.delete_documents(document_id)
            self._indexed_files.remove(file_path)
            logger.info(f"Removed from index: {Path(file_path).name}")
        except Exception as e:
            logger.error(f"Failed to remove {file_path}: {e}", exc_info=True)

"""Use case for extracting PDF content."""

from pdf_digest.application.ports import PDFReaderPort
from pdf_digest.domain.entities.document import Document
from pdf_digest.domain.value_objects.extraction_mode import ExtractionMode


class ExtractPDFContentUseCase:
    """Use case for extracting content from PDF files."""

    def __init__(self, pdf_reader: PDFReaderPort) -> None:
        self._pdf_reader = pdf_reader

    def execute(self, file_path: str) -> Document:
        """Execute the use case to extract PDF content."""
        return self._pdf_reader.read(file_path)


class GenerateDigestUseCase:
    """Use case for generating digest from extracted document."""

    def __init__(self, pdf_reader: PDFReaderPort) -> None:
        self._pdf_reader = pdf_reader

    def execute(
        self,
        file_path: str,
        mode: ExtractionMode = ExtractionMode.STANDARD,
    ) -> str:
        """Execute the use case to generate a digest."""
        document = self._pdf_reader.read(file_path)

        return {
            ExtractionMode.BRIEF: document.to_brief,
            ExtractionMode.STANDARD: document.to_standard,
            ExtractionMode.DETAILED: document.to_detailed,
        }[mode]()

    def generate_json(
        self,
        file_path: str,
        mode: ExtractionMode = ExtractionMode.STANDARD,
    ) -> dict[str, object]:
        """Generate a JSON digest of the document."""
        document = self._pdf_reader.read(file_path)

        return {
            "title": document.title,
            "metadata": {
                "page_count": document.metadata.page_count,
                "file_size": document.metadata.file_size,
                "author": document.metadata.author,
                "creation_date": document.metadata.creation_date,
            },
            "mode": mode.value,
            "content": {
                "sections": [
                    {
                        "level": s.level,
                        "title": s.title,
                        "content": s.content,
                    }
                    for s in document.sections
                ],
            },
        }
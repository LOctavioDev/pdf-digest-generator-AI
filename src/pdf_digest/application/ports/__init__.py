"""Ports (interfaces) for the application layer."""

from typing import Protocol

from pdf_digest.domain.entities.document import Document


class PDFReaderPort(Protocol):
    """Port for PDF reading operations."""

    def read(self, file_path: str) -> Document:
        """Read and extract content from a PDF file."""
        ...


class OutputWriterPort(Protocol):
    """Port for output writing operations."""

    def write(self, content: str, output_path: str | None) -> None:
        """Write content to file or stdout."""
        ...

    def write_json(self, data: dict[str, object], output_path: str | None) -> None:
        """Write JSON data to file or stdout."""
        ...
"""Infrastructure implementation for PDF reading using PyMuPDF."""

import fitz
from pathlib import Path

from pdf_digest.application.ports import PDFReaderPort
from pdf_digest.domain.entities.document import Document, Metadata, Section
from pdf_digest.domain.value_objects.extraction_mode import ExtractionMode


class PyMuPDFReader:
    """PDF reader implementation using PyMuPDF (fitz)."""

    def read(self, file_path: str) -> Document:
        """Read and extract content from a PDF file."""
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"PDF file not found: {file_path}")

        if not path.suffix.lower() == ".pdf":
            raise ValueError(f"File is not a PDF: {file_path}")

        try:
            doc = fitz.open(file_path)
        except Exception as e:
            raise ValueError(f"Cannot open PDF: {e}")

        if doc.is_encrypted:
            raise ValueError(f"PDF is password-protected: {file_path}")

        if doc.page_count == 0:
            doc.close()
            raise ValueError(f"PDF has no pages: {file_path}")

        metadata = self._extract_metadata(doc, path)
        title = self._extract_title(doc, metadata)
        sections = self._extract_sections(doc)

        raw_text = "\n".join(page.get_text() for page in doc)
        doc.close()

        return Document(
            title=title,
            metadata=metadata,
            sections=sections,
            raw_text=raw_text,
            file_path=file_path,
        )

    def _extract_metadata(self, doc: fitz.Document, path: Path) -> Metadata:
        """Extract metadata from PDF document."""
        pdf_meta = doc.metadata

        return Metadata(
            page_count=doc.page_count,
            file_size=path.stat().st_size,
            author=pdf_meta.get("author") or None,
            creator=pdf_meta.get("creator") or None,
            creation_date=pdf_meta.get("creationDate") or None,
            modification_date=pdf_meta.get("modDate") or None,
        )

    def _extract_title(self, doc: fitz.Document, metadata: Metadata) -> str:
        """Extract document title from metadata or first page."""
        if metadata.author:
            return metadata.author

        for page_num in range(min(2, doc.page_count)):
            page = doc[page_num]
            text: str = page.get_text()
            if text.strip():
                first_line = text.strip().split("\n")[0]
                if len(first_line) < 100:
                    return first_line

        return "Untitled Document"

    def _extract_sections(self, doc: fitz.Document) -> list[Section]:
        """Extract sections and headings from PDF."""
        sections: list[Section] = []

        for page_num in range(doc.page_count):
            page = doc[page_num]
            blocks = page.get_text("blocks")

            for block in blocks:
                block_tuple: tuple = block  # type: ignore[type-arg]
                block_text = block_tuple[4].strip()
                if not block_text:
                    continue

                is_heading = self._is_heading(block)
                level = self._detect_heading_level(block_text, is_heading)

                if level > 0:
                    sections.append(
                        Section(
                            level=level,
                            title=block_text[:200],
                            content="",
                        )
                    )
                elif sections and block_text:
                    if sections[-1].content:
                        sections[-1].content += "\n" + block_text
                    else:
                        sections[-1].content = block_text

        return sections

    def _is_heading(self, block: tuple[object, ...]) -> bool:
        """Determine if a block is a heading based on properties."""
        x0, y0, x1, y1, text, block_type, block_no = block[:7]
        return block_type == 0

    def _detect_heading_level(self, text: str, is_heading: bool) -> int:
        """Detect heading level based on text analysis."""
        if not is_heading:
            return 0

        lines = text.split("\n")
        if not lines:
            return 0

        first_line = lines[0]

        if first_line.isupper() and len(first_line) < 80:
            return 1

        if first_line.title() == first_line and len(first_line) < 60:
            return 2

        if len(first_line) < 50 and not first_line.endswith((".", ",", ":")):
            return 3

        return 0


class PDFReaderAdapter:
    """Adapter implementing PDFReaderPort using PyMuPDF."""

    def __init__(self) -> None:
        self._reader = PyMuPDFReader()

    def read(self, file_path: str) -> Document:
        return self._reader.read(file_path)
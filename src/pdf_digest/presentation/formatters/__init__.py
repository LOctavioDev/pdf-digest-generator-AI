"""Formatters protocol and implementations."""

from typing import Protocol

from pdf_digest.domain.entities.document import Document


class FormatterProtocol(Protocol):
    """Protocol for document formatters."""

    def format(self, document: Document) -> str | dict[str, object]:
        """Format document to output."""
        ...


class ReadmeFormatter:
    """Formatter for README.md output."""

    def format(self, document: Document) -> str:
        """Format document as README.md."""
        lines = [
            f"# {document.title}",
            "",
            f"**Pages:** {document.metadata.page_count}",
        ]

        if document.metadata.author:
            lines.append(f"**Author:** {document.metadata.author}")

        if document.metadata.creation_date:
            lines.append(f"**Created:** {document.metadata.creation_date}")

        lines.append("")

        headings = [s for s in document.sections if s.title and s.level > 0]
        if headings:
            lines.append("## Sections\n")
            for section in headings[:15]:
                indent = "  " * (section.level - 1)
                lines.append(f"{indent}- {section.title}")

        lines.append("")
        lines.append("## Content Summary\n")

        content_sections = [s for s in document.sections if s.content]
        for section in content_sections:
            lines.append(f"### {section.title}\n")
            lines.append(section.content)
            lines.append("")

        return "\n".join(lines)


class TxtFormatter:
    """Formatter for plain TXT output."""

    def format(self, document: Document) -> str:
        """Format document as plain text."""
        lines = [
            document.title.upper(),
            "=" * len(document.title),
            "",
        ]

        lines.append(f"Pages: {document.metadata.page_count}")

        if document.metadata.author:
            lines.append(f"Author: {document.metadata.author}")

        lines.append("")
        lines.append("-" * 40)
        lines.append("")

        for section in document.sections:
            if section.title:
                prefix = "#" * section.level
                lines.append(f"{prefix} {section.title}")

            if section.content:
                lines.append(section.content)

            lines.append("")

        return "\n".join(lines)


class JsonFormatter:
    """Formatter for JSON output."""

    def format(self, document: Document) -> dict[str, object]:
        """Format document as JSON."""
        return {
            "title": document.title,
            "metadata": {
                "page_count": document.metadata.page_count,
                "file_size": document.metadata.file_size,
                "author": document.metadata.author,
                "creator": document.metadata.creator,
                "creation_date": document.metadata.creation_date,
                "modification_date": document.metadata.modification_date,
                "file_path": str(document.file_path),
            },
            "content": {
                "total_sections": document.total_sections,
                "sections": [
                    {
                        "level": s.level,
                        "title": s.title,
                        "content": s.content,
                        "is_heading_only": s.is_heading_only(),
                    }
                    for s in document.sections
                ],
            },
        }
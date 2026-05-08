"""Domain entities for PDF document representation."""

from dataclasses import dataclass, field
from pathlib import Path

from pdf_digest.domain.value_objects.extraction_mode import ExtractionMode


@dataclass(frozen=True)
class Metadata:
    """Metadata extracted from a PDF document."""

    page_count: int
    file_size: int
    author: str | None = None
    creator: str | None = None
    creation_date: str | None = None
    modification_date: str | None = None


@dataclass
class Section:
    """A section or heading within a PDF document."""

    level: int
    title: str
    content: str

    def is_heading_only(self) -> bool:
        """Check if this section contains only a heading with no content."""
        return not self.content.strip()


@dataclass
class Document:
    """A PDF document with its extracted content and metadata."""

    title: str
    metadata: Metadata
    sections: list[Section] = field(default_factory=list)
    raw_text: str = ""
    file_path: str = ""

    @property
    def total_sections(self) -> int:
        """Return the total number of sections."""
        return len(self.sections)

    @property
    def headings(self) -> list[str]:
        """Return all section titles."""
        return [s.title for s in self.sections if s.title]

    def get_sections_by_level(self, level: int) -> list[Section]:
        """Return sections at a specific heading level."""
        return [s for s in self.sections if s.level == level]

    def to_brief(self) -> str:
        """Generate a brief digest of the document."""
        lines = [f"# {self.title}\n"]
        lines.append(f"**Pages:** {self.metadata.page_count}\n")

        if self.headings:
            lines.append("\n## Sections\n")
            for heading in self.headings[:10]:
                lines.append(f"- {heading}")

        return "\n".join(lines)

    def to_standard(self) -> str:
        """Generate a standard digest of the document."""
        lines = [f"# {self.title}\n"]

        lines.append(f"**Pages:** {self.metadata.page_count}")
        if self.metadata.author:
            lines.append(f"**Author:** {self.metadata.author}")
        lines.append("")

        for section in self.sections:
            prefix = "#" * min(section.level, 6)
            lines.append(f"\n{prefix} {section.title}\n")
            if section.content:
                lines.append(section.content)

        return "\n".join(lines)

    def to_detailed(self) -> str:
        """Generate a detailed digest of the document."""
        lines = [
            f"# {self.title}",
            "",
            f"**Pages:** {self.metadata.page_count}",
            f"**File Size:** {self.metadata.file_size} bytes",
        ]

        if self.metadata.author:
            lines.append(f"**Author:** {self.metadata.author}")
        if self.metadata.creation_date:
            lines.append(f"**Created:** {self.metadata.creation_date}")

        lines.append("\n---\n")

        for section in self.sections:
            prefix = "#" * min(section.level, 6)
            lines.append(f"{prefix} {section.title}")
            if section.content:
                lines.append(section.content)
            lines.append("")

        return "\n".join(lines)
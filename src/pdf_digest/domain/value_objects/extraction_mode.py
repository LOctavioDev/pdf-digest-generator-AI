"""Value objects for extraction modes."""

from enum import Enum


class ExtractionMode(str, Enum):
    """Extraction mode for PDF content processing."""

    BRIEF = "brief"
    STANDARD = "standard"
    DETAILED = "detailed"

    @classmethod
    def from_string(cls, value: str) -> "ExtractionMode":
        """Create extraction mode from string value."""
        normalized = value.lower().strip()
        for mode in cls:
            if mode.value == normalized:
                return mode
        raise ValueError(f"Invalid extraction mode: {value}. Valid modes: {', '.join(m.value for m in cls)}")

    @property
    def compression_ratio(self) -> float:
        """Approximate compression ratio for this mode."""
        return {
            ExtractionMode.BRIEF: 0.15,
            ExtractionMode.STANDARD: 0.35,
            ExtractionMode.DETAILED: 0.75,
        }[self]


class OutputFormat(str, Enum):
    """Output format for generated digest."""

    README = "readme"
    TXT = "txt"
    JSON = "json"
    ALL = "all"

    @classmethod
    def from_string(cls, value: str) -> "OutputFormat":
        """Create output format from string value."""
        normalized = value.lower().strip()
        for fmt in cls:
            if fmt.value == normalized:
                return fmt
        raise ValueError(f"Invalid output format: {value}. Valid formats: {', '.join(f.value for f in cls)}")


class Language(str, Enum):
    """Supported languages for output headers."""

    EN = "en"
    ES = "es"

    @classmethod
    def from_string(cls, value: str) -> "Language":
        """Create language from string value."""
        normalized = value.lower().strip()
        for lang in cls:
            if lang.value == normalized:
                return lang
        raise ValueError(f"Invalid language: {value}. Valid languages: {', '.join(l.value for l in cls)}")
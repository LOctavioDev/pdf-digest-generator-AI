"""CLI application entry point."""

import sys
from pathlib import Path

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from typing_extensions import Annotated

from pdf_digest.application.usecases import ExtractPDFContentUseCase, GenerateDigestUseCase
from pdf_digest.application.ports import PDFReaderPort, OutputWriterPort
from pdf_digest.domain.entities.document import Document
from pdf_digest.domain.value_objects.extraction_mode import ExtractionMode, OutputFormat
from pdf_digest.infrastructure.pdf.pymupdf_reader import PDFReaderAdapter
from pdf_digest.infrastructure.output.file_writer import OutputWriterAdapter
from pdf_digest.presentation.formatters import (
    ReadmeFormatter,
    TxtFormatter,
    JsonFormatter,
)

Formatter = ReadmeFormatter | TxtFormatter | JsonFormatter

app = typer.Typer(help="PDF Digest Generator - Extract and condense PDF information")
console = Console()


class AppDependencies:
    """Dependency container for the application."""

    def __init__(self) -> None:
        self._pdf_reader: PDFReaderPort | None = None
        self._output_writer: OutputWriterPort | None = None

    @property
    def pdf_reader(self) -> PDFReaderPort:
        if self._pdf_reader is None:
            self._pdf_reader = PDFReaderAdapter()
        return self._pdf_reader

    @property
    def output_writer(self) -> OutputWriterPort:
        if self._output_writer is None:
            self._output_writer = OutputWriterAdapter()
        return self._output_writer


dependencies = AppDependencies()


def validate_input_file(file_path: str) -> Path:
    """Validate that input file exists and is a PDF."""
    path = Path(file_path)

    if not path.exists():
        raise typer.BadParameter(f"File not found: {file_path}")

    if not path.is_file():
        raise typer.BadParameter(f"Not a file: {file_path}")

    if path.suffix.lower() != ".pdf":
        raise typer.BadParameter(f"File must be a PDF: {file_path}")

    return path


@app.command()
def main(
    input_pdf: Annotated[str, typer.Argument(help="Path to input PDF file", callback=validate_input_file)],
    output: Annotated[str | None, typer.Option("-o", "--output", help="Output file path (default: stdout)")] = None,
    format: Annotated[str, typer.Option("-f", "--format", help="Output format: [readme, txt, json, all]")] = "readme",
    mode: Annotated[str, typer.Option("-m", "--mode", help="Extraction mode: [brief, standard, detailed]")] = "standard",
    verbose: Annotated[bool, typer.Option("-v", "--verbose", help="Enable verbose logging")] = False,
) -> None:
    """
    PDF Digest Generator - Extract and condense PDF information into AI-friendly formats.

    Examples:

    \b
        pdf-digest document.pdf
        pdf-digest document.pdf -o digest.md
        pdf-digest document.pdf -f json -o digest.json
        pdf-digest document.pdf -m brief
    """
    try:
        output_format = OutputFormat.from_string(format)
        extraction_mode = ExtractionMode.from_string(mode)
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(code=1)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task("Extracting PDF content...", total=None)

        use_case = ExtractPDFContentUseCase(dependencies.pdf_reader)
        document = use_case.execute(input_pdf)

        progress.update(task, description="Generating digest...")

        if output_format == OutputFormat.ALL:
            _generate_all_formats(document, input_pdf, verbose)
        else:
            _generate_single_format(document, output_format, input_pdf, output, verbose)

        progress.update(task, description="Done!")

    if output:
        console.print(f"[green]Output written to:[/green] {output}")
    else:
        console.print("[dim]Output written to stdout[/dim]")


def _generate_single_format(
    document: "Document",
    output_format: OutputFormat,
    input_pdf: str,
    output_path: str | None,
    verbose: bool,
) -> None:
    """Generate a single format output."""
    if output_path and not output_format == OutputFormat.JSON:
        output_path = _get_output_path(input_pdf, output_path, output_format)
    elif output_path and output_format == OutputFormat.JSON:
        output_path = output_path if output_path.endswith(".json") else f"{output_path}.json"

    formatter = _get_formatter(output_format)

    if output_format == OutputFormat.JSON or isinstance(formatter, JsonFormatter):
        data = formatter.format(document)
        if isinstance(data, dict):
            dependencies.output_writer.write_json(data, output_path)
    else:
        content = formatter.format(document)
        if isinstance(content, str):
            dependencies.output_writer.write(content, output_path)

    if verbose:
        console.print(f"[dim]Extracted {len(document.sections)} sections from {document.metadata.page_count} pages[/dim]")


def _generate_all_formats(
    document: Document,
    input_pdf: str,
    verbose: bool,
) -> None:
    """Generate all format outputs."""
    base_path = Path(input_pdf).with_suffix("")

    for fmt in [OutputFormat.README, OutputFormat.TXT, OutputFormat.JSON]:
        output_path = str(base_path) + f".{fmt.value}"
        formatter = _get_formatter(fmt)

        if isinstance(formatter, JsonFormatter):
            data = formatter.format(document)
            if isinstance(data, dict):
                dependencies.output_writer.write_json(data, output_path)
        else:
            content = formatter.format(document)
            if isinstance(content, str):
                dependencies.output_writer.write(content, output_path)

        console.print(f"[green]Created:[/green] {output_path}")

    if verbose:
        console.print(f"[dim]Extracted {len(document.sections)} sections from {document.metadata.page_count} pages[/dim]")


def _get_output_path(input_pdf: str, output_path: str | None, output_format: OutputFormat) -> str:
    """Get output path with correct extension."""
    if output_path:
        return output_path

    base = Path(input_pdf).with_suffix("")
    return f"{base}.{output_format.value}"


def _get_formatter(output_format: OutputFormat) -> Formatter:
    """Get formatter for output format."""
    formatters: dict[OutputFormat, Formatter] = {
        OutputFormat.README: ReadmeFormatter(),
        OutputFormat.TXT: TxtFormatter(),
        OutputFormat.JSON: JsonFormatter(),
    }
    return formatters[output_format]


if __name__ == "__main__":
    app()
# PDF Digest Generator - Specification Document

## 1. Project Overview

**Project Name:** pdf-digest-generator  
**Project Type:** Cross-platform CLI tool  
**Core Functionality:** Extract and condense information from PDF files into lightweight, AI-friendly formats (README, TXT, JSON) to reduce token consumption while preserving essential information.  
**Target Users:** Developers and data scientists who need to feed PDF content into LLMs for analysis, summarization, or extraction tasks.

---

## 2. Technical Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.12+ |
| PDF Parsing | `PyMuPDF` (fitz) - fast, reliable, cross-platform |
| CLI Framework | `typer` - modern, type-safe, auto-generates CLI |
| Rich Output | `rich` - colored terminal output |
| Type Safety | `mypy` + `pydantic` for validation |

---

## 3. UI/UX Specification

### 3.1 CLI Interface

```
pdf-digest [OPTIONS] INPUT_PDF [--output OUTPUT] [--format FORMAT] [--mode MODE]

Arguments:
  INPUT_PDF          Path to input PDF file (required)

Options:
  --output, -o        Output file path (default: stdout)
  --format, -f        Output format: [readme, txt, json, all] (default: readme)
  --mode, -m          Extraction mode: [brief, standard, detailed] (default: standard)
  --lang, -l          Output language for headers (default: en)
  --verbose, -v       Enable verbose logging
  --help              Show this help message and exit
```

### 3.2 Interaction Flow

1. User invokes CLI with PDF path and options
2. System validates PDF file exists and is readable
3. System extracts text content from PDF
4. System processes content based on mode
5. System generates output in requested format(s)
6. System writes to file or prints to stdout

### 3.3 Output Formats

| Format | Description | Use Case |
|--------|-------------|----------|
| `README` | Structured markdown with sections | LLM context, quick overview |
| `txt` | Plain text, minimal formatting | Token-efficient input |
| `json` | Structured JSON with metadata | Programmatic consumption |
| `all` | Generates all three formats | Comprehensive analysis |

### 3.4 Extraction Modes

| Mode | Description | Approximate Output Size |
|-----|-------------|------------------------|
| `brief` | Title, headings summary, key bullets only | ~10-20% of original |
| `standard` | Sections, key content, bullet points | ~30-40% of original |
| `detailed` | Full content with minor filtering | ~70-80% of original |

---

## 4. Functional Specification

### 4.1 Core Features

1. **PDF Text Extraction**
   - Extract text from all pages
   - Handle multi-column layouts
   - Preserve heading hierarchy
   - Handle scanned PDFs (with OCR if needed)

2. **Content Processing**
   - Identify document title (from metadata or first heading)
   - Detect and structure sections
   - Extract key bullet points
   - Remove redundant whitespace
   - Filter non-essential content (page numbers, headers)

3. **Output Generation**
   - Generate README.md with structured sections
   - Generate plain TXT with minimal formatting
   - Generate JSON with full metadata

4. **Error Handling**
   - Invalid file path
   - Corrupted PDF
   - Empty PDF
   - Password-protected PDF

### 4.2 Architecture (Clean Architecture)

```
pdf_digest/
├── src/
│   └── pdf_digest/
│       ├── __init__.py
│       ├── domain/           # Enterprise Business Rules
│       │   ├── entities/
│       │   │   ├── document.py
│       │   │   ├── section.py
│       │   │   └── metadata.py
│       │   └── value_objects/
│       │       └── extraction_mode.py
│       ├── application/      # Application Business Rules
│       │   ├── usecases/
│       │   │   ├── extract_pdfContent.py
│       │   │   └── generate_digest.py
│       │   ├── ports/
│       │   │   ├── pdf_reader_port.py
│       │   │   └── output_writer_port.py
│       │   └── services/
│       │       └── content_processor.py
│       ├── infrastructure/  # Frameworks & Drivers
│       │   ├── pdf/
│       │   │   └── pymupdf_reader.py
│       │   └── output/
│       │       └── file_writer.py
│       └── presentation/    # Interface Adapters
│           ├── cli/
│           │   ├── app.py
│           │   └── commands.py
│           └── formatters/
│               ├── readme_formatter.py
│               ├── txt_formatter.py
│               └── json_formatter.py
├── tests/
│   └── ...
├── pyproject.toml
├── uv.lock
├── README.md
└── SPEC.md
```

### 4.3 Key Classes and Interfaces

```python
# Domain Layer
class Document:
    title: str
    metadata: Metadata
    sections: list[Section]

class Section:
    level: int
    title: str
    content: str

class Metadata:
    page_count: int
    author: str | None
    creation_date: str | None

# Application Layer
class PDFReaderPort(Protocol):
    def read(self, path: str) -> Document: ...

class OutputWriterPort(Protocol):
    def write(self, content: str, path: str | None) -> None: ...
```

---

## 5. Acceptance Criteria

### 5.1 Functional Criteria

| ID | Criterion | Test Scenario |
|----|-----------|--------------|
| AC1 | PDF extraction works | Provide valid PDF, verify text extracted |
| AC2 | All formats generated | Run with `--format all`, verify 3 files created |
| AC3 | Cross-platform CLI | Run on Linux, verify working |
| AC4 | Error handling | Provide invalid path, verify error message |
| AC5 | JSON output valid | Run with `--format json`, verify valid JSON |
| AC6 | Type safety | Run mypy, verify no errors |

### 5.2 Non-Functional Criteria

| ID | Criterion |
|----|-----------|
| NF1 | CLI responds in < 2 seconds for typical PDF |
| NF2 | Output size < 50% of original PDF text |
| NF3 | Zero runtime dependencies beyond pip install |

---

## 6. Future Enhancements (Out of Scope)

- OCR support for scanned PDFs
- Table extraction
- Image extraction
- Multi-language support
- GUI version
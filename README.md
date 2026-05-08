# PDF Digest Generator

Extract and condense PDF information into lightweight, AI-friendly formats (README, TXT, JSON) to reduce token consumption when feeding content to LLMs.

## Quick Start

```bash
# 1. Clone or download the project
cd pdf-digest-generator

# 2. Run setup (creates venv and installs dependencies)
bash setup.sh
# Or manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Run with sample PDF
./pdf-digest input/CVLMLO.pdf -o output.md
```

## Installation

### Option A: Automated (Recommended)
```bash
bash setup.sh
```

### Option B: Manual
```bash
# Create virtual environment
python3 -m venv venv

# Activate
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Basic Usage
```bash
# Output to stdout
./pdf-digest input.pdf

# Save to file
./pdf-digest input.pdf -o output.md
```

### CLI Options

| Option | Description | Default |
|--------|------------|---------|
| `-o, --output` | Output file path | stdout |
| `-f, --format` | Format: readme, txt, json, all | readme |
| `-m, --mode` | Mode: brief, standard, detailed | standard |
| `-v, --verbose` | Show verbose output | false |

### Examples

```bash
# From input folder to output folder
./pdf-digest input/CVLMLO.pdf -o output/cv_readme.md

# Or use stdin/stdout
./pdf-digest input/CVLMLO.pdf > output/cv.txt

## Extraction Modes

| Mode | Description | Size |
|------|------------|------|
| `brief` | Title, headings, key bullets only | ~10-20% |
| `standard` | Sections with content | ~30-40% |
| `detailed` | Full content | ~70-80% |

## Output Formats

### README (Default)
```markdown
# Document Title

**Pages:** 5

## Sections
- Section 1
- Section 2

## Content Summary
### Section 1
Content preview...
```

### TXT
```
DOCUMENT TITLE
==============

Pages: 5
Author: John Doe

-------------------

# Section 1
Content...
```

### JSON
```json
{
  "title": "...",
  "metadata": {...},
  "content": {
    "sections": [...]
  }
}
```

## Project Structure

```
pdf-digest-generator/
├── src/pdf_digest/
│   ├── domain/           # Entities, value objects
│   ├── application/      # Use cases, ports
│   ├── infrastructure # PDF reader, file writer
│   └── presentation  # CLI, formatters
├── input/             # PDFs to process
├── output/            # Generated output files
├── venv/             # Virtual environment
├── pdf-digest        # CLI entry point
├── requirements.txt
├── setup.sh         # Setup script
├── pyproject.toml
└── README.md
```
pdf-digest-generator/
├── src/pdf_digest/
│   ├── domain/           # Entities, value objects
│   ├── application/      # Use cases, ports
│   ├── infrastructure # PDF reader, file writer
│   └── presentation  # CLI, formatters
├── tests/             # Test PDF files
├── venv/             # Virtual environment
├── pdf-digest        # CLI entry point
├── requirements.txt
├── setup.sh         # Setup script
├── pyproject.toml
└── README.md
```

## Development

```bash
# Type checking
source venv/bin/activate
mypy src/pdf_digest

# Format code
ruff check src/
ruff format src/
```

## Requirements

- Python 3.12+
- pymupdf
- typer
- rich
- pydantic

## License

MIT
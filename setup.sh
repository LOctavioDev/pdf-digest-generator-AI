#!/bin/bash
# PDF Digest Generator - Quick Setup Script

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$PROJECT_DIR/venv"

echo "Setting up PDF Digest Generator"

# Create virtual environment
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment"
    python3 -m venv "$VENV_DIR"
fi

# Activate and install dependencies
echo "Installing dependencies..."
source "$VENV_DIR/bin/activate"
pip install --upgrade pip
pip install -r "$PROJECT_DIR/requirements.txt"

echo "Setup complete :)"
echo ""
echo "Usage:"
echo "  source venv/bin/activate"
echo "  python pdf-digest.py input.pdf -o output.md"
#!/bin/bash

# Compile IEEE LaTeX Paper
# ========================

echo "📄 Compiling IEEE LaTeX Paper..."
echo ""

if ! command -v pdflatex &> /dev/null; then
    echo "❌ pdflatex not found"
    echo ""
    echo "Please install LaTeX:"
    echo "  macOS: brew install --cask mactex"
    echo "  or download from: https://www.tug.org/mactex/"
    echo ""
    echo "Alternatively, use Overleaf:"
    echo "  1. Go to https://www.overleaf.com"
    echo "  2. Upload term_paper.tex"
    echo "  3. Compile online"
    exit 1
fi

# Compile the paper
cd "$(dirname "$0")"

echo "Running pdflatex (1st pass)..."
pdflatex -interaction=nonstopmode term_paper.tex > /dev/null

echo "Running pdflatex (2nd pass for references)..."
pdflatex -interaction=nonstopmode term_paper.tex > /dev/null

# Clean up auxiliary files
echo "Cleaning up auxiliary files..."
rm -f term_paper.aux term_paper.log term_paper.out term_paper.bbl term_paper.blg

if [ -f "term_paper.pdf" ]; then
    echo ""
    echo "✅ Paper compiled successfully!"
    echo "📁 Output: term_paper.pdf"
    echo ""
    echo "Opening PDF..."
    open term_paper.pdf 2>/dev/null || echo "Open manually: term_paper.pdf"
else
    echo ""
    echo "❌ Compilation failed"
    echo "Check term_paper.log for errors"
fi

# PDF Generator

This folder contains the final PDF generation script for the Comprehensive MyST Document.

## Usage

Run the script from the project root:

```bash
python pdf_generator/generate_pdf.py
```

Or from within this folder:

```bash
cd pdf_generator
python generate_pdf.py
```

## What it does

1. **Builds and executes code cells** using `jupyter book build --execute`
2. **Exports to LaTeX** using `myst build --tex`
3. **Copies and converts images** (SVG/GIF → PNG)
4. **Links images to figures** in the correct order
5. **Fixes LaTeX issues** (Unicode, nested figures, etc.)
6. **Applies Springer book style** with:
   - Styled code blocks with language labels
   - Colored callout boxes for admonitions
   - Professional formatting
7. **Compiles to PDF** using `pdflatex`
8. **Copies PDF to downloads folder** for website access

## Output

The generated PDF is saved to:
- `_build/exports/Comprehensive-MyST-Document.pdf` (main output)
- `downloads/Comprehensive-MyST-Document.pdf` (for website downloads)

## Requirements

- LaTeX (pdflatex)
- ImageMagick (for image conversion)
- Python packages: See `requirements.txt` in project root

## Features

- **Robust language detection**: Automatically detects Python, Bash, YAML, JSON, Markdown
- **Ordered figure matching**: Matches code-generated figures by execution order
- **Styled code blocks**: All code blocks have language labels and syntax highlighting
- **Callout boxes**: Admonitions are styled with appropriate colors
- **Section numbering**: Starts from 1 (not 0.1)


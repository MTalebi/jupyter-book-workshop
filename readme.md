# Jupyter Book Workshop Example

Live demo of computational book features using Jupyter Book 2.0.

## Quick Start

```bash
# Clone repository
git clone https://github.com/yourusername/jupyter-book-workshop.git
cd jupyter-book-workshop

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start development server
jupyter-book start --execute
```

## Project Structure

```
├── content/          # Book chapters
├── data/            # CSV data files  
├── images/          # Figures
├── scripts/         # Python modules
├── myst.yml         # Configuration
└── requirements.txt # Dependencies
```

## Features Demonstrated

- **MyST Markdown**: Rich text with math, code, figures
- **Executable Code**: Live Python computations
- **Interactive Widgets**: Dynamic visualizations
- **Cross-references**: Linked equations, figures, tables
- **Citations**: BibTeX and DOI support
- **GitHub Pages**: Automated deployment

## Building Outputs

```bash
jupyter-book build --html       # Web version
jupyter-book build --pdf        # PDF export
jupyter-book build --tex        # LaTeX source
```

## Deployment

Push to GitHub main branch to auto-deploy via GitHub Actions.

## Workshop Materials

Created by Mohammad Talebi-Kalaleh, PhD Candidate  
Structural Engineering, University of Alberta  
Supervisor: Dr. Qipei Mei

## License

MIT
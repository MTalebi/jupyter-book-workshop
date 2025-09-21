---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.17.2
kernelspec:
  name: python3
  display_name: Python 3 (ipykernel)
  language: python
numbering:
  headings: true
  figure: true
  table: true
  equation: true
  code: true
---

# Creating Interactive Computational Books with Jupyter Book 2
---

## 1. Getting Started

### Setting Up Your Environment

First, create a project folder and set up a Python virtual environment. This keeps your project dependencies isolated and reproducible.

```bash
python -m venv .venv
```

Activate the environment:
- **Windows**: `.venv\Scripts\activate`
- **Mac/Linux**: `source .venv/bin/activate`

### Installing Jupyter Book

Install the latest Jupyter Book 2.0 and the MyST extension for JupyterLab:

```bash
pip install "jupyter-book>=2.0.0a0"
pip install jupyterlab-myst
```

### Creating requirements.txt

For reproducibility, create a `requirements.txt` file with all your dependencies:

```{code} text
:caption: requirements.txt
jupyter-book>=2.0.0a0
jupyterlab-myst
numpy
matplotlib
pandas
scipy
ipywidgets
```

Install all requirements:
```bash
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## 2. Project Configuration
We'll organize content in a `content/` folder.

### Understanding myst.yml

Creates a `myst.yml` configuration file. The `myst.yml` file controls your book's metadata and build settings. Here's a minimal configuration for an academic paper:

```{code} yaml
:caption: myst.yml for a paper
# See docs at: https://mystmd.org/guide/frontmatter
version: 1
project:
  title: Your Paper Title
  description: A computational research paper
  keywords:
    - computational-mechanics
    - jupyter-book
  github: yourusername/your-repo
  # For a single paper, list your main file
  toc:
    - file: content/paper.md
site:
  template: article-theme  # Use article-theme for papers
```

For a book with multiple chapters, adjust the `toc` section:

```{code} yaml
:caption: myst.yml additions for a book
project:
  toc:
    - file: content/intro.md
    - file: content/chapter1.md
    - file: content/chapter2.md
site:
  template: book-theme  # Use book-theme for books
```

### Starting the Live Preview

Start the development server with automatic code execution:

```bash
.\.venv\Scripts\jupyter-book.exe start --execute
```

The `--execute` flag is crucial because:
- It executes all code cells during the initial build
- It re-runs code cells automatically when you modify them
- Without it, notebooks with no outputs won't show any results

Your book will be available at `http://localhost:3000`. The page updates automatically as you edit files, and code cells re-execute on changes.

## 3. Writing Foundations & Visual Content

### File Formats

Jupyter Book supports three main formats:
- **MyST Markdown** (`.md`) - Best for narrative content
- **Jupyter Notebooks** (`.ipynb`) - For code-heavy content  
- **LaTeX** (`.tex`) - For complex mathematical documents

We'll focus on MyST Markdown as it's easiest to maintain and version control.

### Default Frontmatter Configuration

Start each MyST markdown file with this frontmatter to enable proper execution and numbering:

```markdown
---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.16.0
kernelspec:
  name: python3
  display_name: Python 3 (ipykernel)
  language: python
numbering:
  headings: true
  code_cell: true
  figures: true
  tables: true
  equations: true
---
```

This configuration:
- **jupytext**: Ensures proper parsing of MyST markdown
- **kernelspec**: Specifies Python kernel for code execution
- **numbering**: Enables automatic numbering for all elements

You can toggle numbering for specific elements by setting them to `false`.

### Document Structure

Create clear hierarchy with headings:

```markdown
# Chapter Title

## Main Section

### Subsection

#### Subsubsection

Regular paragraph text goes here.
```

### Mathematics

Write inline math using single dollars: $E = mc^2$

For display equations with labels:

$$
\frac{\partial u}{\partial t} + \nabla \cdot (u \otimes u) = -\nabla p + \nu \nabla^2 u
$$ (navier-stokes)

### Figures

Add figures with captions and labels for cross-referencing:

:::{figure} ./images/beam-deflection.png
:label: beam-fig
:align: center
:width: 60%

Deflection of a cantilever beam under point load
:::


For subfigures, use a grid structure:

:::::{figure} ./images/comparison.png
:label: comparison-fig
:align: center

::::{subfigure} 2
:width: 45%
:gap: 10px

:::{image} ./images/experimental.png
:::
Experimental results

:::{image} ./images/simulation.png
:::
Simulation results
::::

Comparison between experimental and numerical results
:::::


**Tip**: Save PowerPoint diagrams as SVG format for editability and scalability.

### Tables

Simple markdown tables:


| Material | Young's Modulus (GPa) | Poisson's Ratio |
|----------|----------------------|-----------------|
| Steel    | 200                  | 0.30            |
| Aluminum | 69                   | 0.33            |
| Concrete | 30                   | 0.20            |


For CSV data inline in your document:


:::{csv-table} Material Properties
:header: "Material", "Density (kg/m³)", "Yield Strength (MPa)"

"Steel", 7850, 250
"Aluminum", 2700, 95
"Titanium", 4500, 880
"Concrete", 2400, 3
:::


For external CSV files, use the table directive:


:::{table} Material Properties
:label: material-table
:align: center

```{include} ./data/materials.csv
```
:::


## 4. Scholarly Features

### Cross-References

Reference any labeled element using its label:


As shown in [](#beam-fig), the deflection increases linearly.

The governing equation [](#navier-stokes) describes fluid motion.

Material properties are listed in [](#material-table).

### Numbered References

Use `{numref}` for numbered references with custom text:


{numref}`Figure %s <beam-fig>` shows the beam deflection.

See {numref}`Table %s <material-table>` for material properties.

From {eq}`navier-stokes`, we can derive...


### Citations

#### Method 1: BibTeX

Create a `references.bib` file:

```{code} bibtex
:caption: references.bib
@article{smith2023,
  title={Computational Mechanics of Structures},
  author={Smith, John and Doe, Jane},
  journal={Journal of Engineering},
  year={2023}
}
```

Add to frontmatter and cite:

```markdown
---
bibliography: references.bib
---

Recent studies [@smith2023] show that...

Multiple citations [@smith2023; @doe2022] indicate...
```

#### Method 2: DOI

Cite directly using DOI:

The foundational work @10.1093/nar/22.22.4673 established...


### Abbreviations

Define abbreviations project-wide in `myst.yml` (recommended) or in individual files:

```yaml
# In myst.yml - applies to all pages
project:
  title: Structural Analysis Guide
  authors:
    - name: Mohammad Talebi-Kalaleh
      affiliations:
        - University of Alberta
  abbreviations:
    SHM: Structural Health Monitoring
    FEM: Finite Element Method
    DOF: Degrees of Freedom
    FFT: Fast Fourier Transform
    PCA: Principal Component Analysis
```

Then use abbreviations anywhere in your content:


The FEM uses DOF to analyze structures. 
SHM systems often employ FFT for signal processing.


### Frontmatter Metadata

You can set metadata in two places:

**Option 1: Project-wide in `myst.yml`** (recommended for common metadata):

```yaml
# In myst.yml
project:
  title: Computational Mechanics Book
  description: Advanced structural analysis techniques
  keywords: [structural analysis, computational mechanics, finite elements]
  authors:
    - name: Mohammad Talebi-Kalaleh
      affiliations:
        - University of Alberta
      orcid: 0000-0000-0000-0000
```

**Option 2: Page-specific in `.md` files** (for unique page metadata):

```markdown
---
title: Chapter 3: Nonlinear Analysis
date: 2024-11-19
doi: 10.1000/chapter-doi
# Page-specific metadata overrides project defaults
---
```

Best practice: Define common metadata (authors, keywords, abbreviations) in `myst.yml`, then add page-specific details (title, date, DOI) in individual files.

## 5. Code Integration

### Global Configuration

Create a hidden setup cell at the document start:


```{code-cell} python
:tags: [remove-cell]

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from matplotlib import rcParams

# Configure publication-quality plots
rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'DejaVu Sans'],
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'legend.fontsize': 10,
    'lines.linewidth': 2.0,
    'axes.linewidth': 1.2,
    'figure.facecolor': 'white',
    'figure.figsize': (8, 6),
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'grid.alpha': 0.3,
})

# Set random seed for reproducibility
np.random.seed(42)
```


### Static Code Blocks

Display code without execution:


```python
def calculate_stress(force, area):
    """Calculate engineering stress"""
    return force / area
```


With line numbers and highlighting:


```{code} python
:linenos:
:emphasize-lines: 2,3

def beam_deflection(load, length, E, I):
    # Maximum deflection for cantilever beam
    delta_max = (load * length**3) / (3 * E * I)
    return delta_max
```

### Executable Code Cells

Create executable cells that run when building:

```{code-cell} python
# Generate sample data
x = np.linspace(0, 10, 100)
y = np.sin(x) * np.exp(-x/10)

plt.plot(x, y)
plt.xlabel('Position (m)')
plt.ylabel('Displacement (mm)')
plt.title('Damped Oscillation')
plt.grid(True)
plt.show()
```

### Including External Code

Include code from separate files:

```{literalinclude} ./scripts/analysis.py
:start-at: def main
:end-before: if __name__
:lineno-match:
```

### Controlling Cell Visibility

Use tags to control what readers see:

```{code-cell} python
:tags: [hide-input]
# Code hidden, only output shown
results = perform_analysis()
print(f"Maximum stress: {results['max_stress']:.2f} MPa")
```

```{code-cell} python
:tags: [hide-output]
# Complex calculation - output hidden
for i in range(1000):
    intermediate_calc(i)
```

```{code-cell} python
:tags: [remove-input]
# Only the plot appears, no code
plot_final_results()
```

Available tags:
- `hide-input`: Collapse code (can be expanded)
- `hide-output`: Collapse output
- `remove-input`: Completely remove code
- `remove-output`: Completely remove output
- `remove-cell`: Remove entire cell

## 6. Enhanced Content

### Inline Code Results with {eval}

Display variables from code cells inline:

```{code-cell} python
:tags: [remove-cell]
max_stress = 250.5
safety_factor = 2.5
```

The maximum stress is {eval}`max_stress` MPa, 
with a safety factor of {eval}`safety_factor`.

### Interactive Widgets

Create interactive elements with ipywidgets:

```{code-cell} python
import ipywidgets as widgets
from IPython.display import display

@widgets.interact(frequency=(1, 10, 0.5))
def plot_wave(frequency=2):
    x = np.linspace(0, 2*np.pi, 100)
    y = np.sin(frequency * x)
    plt.plot(x, y)
    plt.ylim(-1.5, 1.5)
    plt.xlabel('x')
    plt.ylabel('sin(fx)')
    plt.title(f'Sine Wave: f = {frequency}')
    plt.show()
```

### Admonitions

Highlight important information:

:::{note}
This method assumes linear elastic behavior.
:::

:::{warning}
Check boundary conditions before applying this formula.
:::

:::{tip}
:class: dropdown
Use dimensionless parameters to generalize your results.
:::

:::{important}
Safety factors must comply with local building codes.
:::

### Exercise and Solution Blocks

Create teaching materials:

:::{exercise}
:label: ex1
Calculate the natural frequency of a cantilever beam with:
- Length L = 2 m
- Mass m = 10 kg at the tip
- Flexural rigidity EI = 1000 N⋅m²
:::

:::{solution} ex1
:class: dropdown

Using the formula for a cantilever with tip mass:
$$\omega_n = \sqrt{\frac{3EI}{mL^3}}$$

Substituting values:
$$\omega_n = \sqrt{\frac{3 \times 1000}{10 \times 2^3}} = 6.12 \text{ rad/s}$$
:::

### Mermaid Diagrams

Create flowcharts and diagrams:

```{mermaid}
flowchart TD
    A[Load Applied] --> B{Linear Analysis}
    B -->|Small Deformation| C[Linear Solution]
    B -->|Large Deformation| D[Nonlinear Analysis]
    D --> E[Iterative Solution]
    E --> F[Converged?]
    F -->|No| E
    F -->|Yes| G[Final Results]
```

### Videos and iFrames

Embed multimedia content:

:::{iframe} https://www.youtube.com/embed/VIDEO_ID
:width: 100%
:::

:::{figure} ./videos/experiment.mp4
:width: 80%
Experimental setup and testing procedure
:::

## 7. Exporting to LaTeX and PDF

### List Available Templates

View journal templates:

```bash
jupyter-book templates list --pdf
```

Common templates:
- `agu2019`: AGU Journal format
- `arxiv_two_column`: arXiv preprint
- `ieee`: IEEE Transactions

### Build PDF

Generate PDF using default template:

```bash
jupyter-book build --pdf
```

Use specific journal template:

```bash
jupyter-book build --pdf --template arxiv_two_column
```

### Export to LaTeX

For journal submission, export LaTeX source:

```bash
jupyter-book build --tex
```

The LaTeX files will be in `_build/tex/`.

## 8. Authoring with JupyterLab

### Accessing the Jupyter Server

When you run `jupyter book start --execute`, it automatically starts a Jupyter server. You can access JupyterLab for a better authoring experience:

1. Look for the server URL in your terminal (typically `http://localhost:8888/lab`)
2. Open this URL in your browser to access JupyterLab

### Live MyST Markdown Rendering

JupyterLab with the MyST extension provides real-time rendering:

```bash
# The MyST extension was installed earlier with:
pip install jupyterlab-myst
```

Benefits of authoring in JupyterLab:
- **Split view**: Edit markdown on left, see rendered output on right
- **Live preview**: Changes render immediately as you type
- **Execute cells**: Run code blocks directly in the editor
- **Better for teaching**: Show both source and output simultaneously

### MyST vs Jupyter Notebooks

Why use MyST Markdown (`.md`) instead of Jupyter Notebooks (`.ipynb`)?

| Aspect | MyST Markdown | Jupyter Notebook |
|--------|--------------|------------------|
| Version Control | Clean diffs, easy merge | Binary format, merge conflicts |
| Maintenance | Plain text, find/replace works | JSON structure, harder to edit |
| Collaboration | Any text editor works | Requires Jupyter |
| File Size | Compact | Large with outputs |
| Reproducibility | Outputs generated on build | Outputs stored in file |

### Workflow Tips

1. **Author content**: Write in JupyterLab with live preview
2. **Test execution**: Code cells run as you write
3. **Version control**: Commit clean `.md` files without outputs
4. **Build outputs**: Generate fresh outputs with `--execute`

This approach separates content from presentation, making your book maintainable long-term.

## 9. Web Deployment with GitHub Pages

### Create .gitignore

```{code} text
:caption: .gitignore
.venv/
_build/
.ipynb_checkpoints/
__pycache__/
*.pyc
.DS_Store
```

### GitHub Actions Workflow

Create `.github/workflows/deploy.yml`:

```{code} yaml
:caption: .github/workflows/deploy.yml
name: Deploy Jupyter Book to GitHub Pages

on:
  push:
    branches: [main]

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          
      - name: Build book
        run: |
          jupyter-book build --html
          
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: '_build/html'
          
      - name: Deploy to GitHub Pages
        uses: actions/deploy-pages@v4
```

### Enable GitHub Pages

1. Push your code to GitHub
2. Go to Settings → Pages
3. Select "GitHub Actions" as source
4. Your book deploys automatically on each push

## 10. Maintenance & Collaboration

### Version Control Workflow

```bash
# Clone repository
git clone https://github.com/yourusername/your-book.git
cd your-book

# Create feature branch
git checkout -b add-chapter-3

# Make changes and commit
git add .
git commit -m "Add analysis chapter"

# Push and create pull request
git push origin add-chapter-3
```

### Collaborative Authoring

1. Each author works on separate branches
2. Use pull requests for review
3. Maintain consistent style with shared configuration

### AI-Assisted Writing

Use VS Code with GitHub Copilot for:
- Auto-completing markdown syntax
- Generating boilerplate code cells
- Creating consistent documentation
- Suggesting citations and references

### Best Practices

1. **Keep content modular**: One chapter per file
2. **Version control data**: Store small datasets in `data/`
3. **Document dependencies**: Always update `requirements.txt`
4. **Test builds locally**: Run `jupyter-book build` before pushing
5. **Use semantic commits**: Clear commit messages for collaboration

---

## Quick Reference

### Essential Commands

```bash
jupyter book init              # Initialize project
jupyter book start --execute   # Start dev server with code execution
jupyter book build --pdf       # Build PDF
jupyter book clean             # Clean build files
```

### File Structure

```
my-book/
├── myst.yml              # Configuration
├── requirements.txt      # Dependencies
├── content/              # All content files
│   ├── intro.md         # First page
│   ├── chapter1.md      # Content chapters
│   ├── chapter2.md      
│   └── references.bib   # Bibliography
├── data/                # Data files
├── images/              # Figures
├── scripts/             # External code
├── _build/              # Build output (ignored)
└── .github/
    └── workflows/
        └── deploy.yml   # GitHub Actions
```

### Resources

- Documentation: https://jupyterbook.org
- MyST Syntax: https://mystmd.org
- Templates: https://github.com/jupyter-book/cookiecutter-jupyter-book

---

*Workshop materials by Mohammad Talebi-Kalaleh, University of Alberta*

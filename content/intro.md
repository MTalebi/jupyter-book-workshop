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

# Welcome to Jupyter Book Workshop

This interactive book demonstrates the features of Jupyter Book 2.0 for creating computational documents. 

## What You'll Learn

In this workshop, we explore:
- Writing MyST Markdown with executable code
- Creating figures, tables, and equations
- Building interactive visualizations
- Publishing to GitHub Pages

## Workshop Structure

This book contains three main sections:

1. **[](chapter1)** - Basic MyST features and formatting
2. **[](chapter2)** - Advanced computational features

:::{note}
All code examples are fully executable. Run `jupyter-book start --execute` to see live outputs.
:::

## About the Instructor

**Mohammad Talebi-Kalaleh** is a PhD Candidate in Structural Engineering at the University of Alberta, working under Dr. Qipei Mei's supervision. His research focuses on SHM and computational mechanics.

## Quick Start

```{code-cell} python
:tags: [remove-cell]

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

# Configure plots for publication
rcParams.update({
    'font.family': 'sans-serif',
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.linewidth': 1.2,
    'figure.figsize': (8, 5),
    'figure.dpi': 150,
    'grid.alpha': 0.3,
})
```

```{code-cell} python
# Welcome message with system info
import sys
print(f"Python {sys.version.split()[0]}")
print(f"Jupyter Book Workshop - Ready to build! 🚀")
```

Let's begin exploring the powerful features of MyST!

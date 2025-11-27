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
downloads:
  - id: comprehensive-myst-document-export
    title: Comprehensive MyST Documentation (PDF)
    description: Complete guide with all features, code examples, and styling
---

# Comprehensive MyST Documnet

## Getting Started

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
:filename: requirements.txt

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

## Project Configuration
We'll organize content in a `content/` folder.

### Understanding myst.yml

Creates a `myst.yml` configuration file. The `myst.yml` file controls your book's metadata and build settings. You can quickly generate a starter `myst.yml` configuration file by running the following command in your project folder:

```bash
myst init
myst init --write-toc
```

This will interactively guide you through some basic questions, then create a `myst.yml` with sensible defaults tailored for your project. You can edit the generated file to further customize settings as shown below. Here's a minimal configuration for an academic paper:

```{code} yaml
:filename: myst.yml

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
:filename: myst.yml

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

## Writing Foundations & Visual Content

### File Formats

Jupyter Book supports three main formats:
- **MyST Markdown** (`.md`) - Best for narrative content
- **Jupyter Notebooks** (`.ipynb`) - For code-heavy content  
- **LaTeX** (`.tex`) - For complex mathematical documents

We'll focus on MyST Markdown as it's easiest to maintain and version control.

### Default Frontmatter Configuration

Start each MyST markdown file with this frontmatter to enable proper execution and numbering:

```yaml
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

```markdown
$$
\frac{\partial u}{\partial t} + \nabla \cdot (u \otimes u) = -\nabla p + \nu \nabla^2 u
$$ (eq:navier-stokes)
```

$$
\frac{\partial u}{\partial t} + \nabla \cdot (u \otimes u) = -\nabla p + \nu \nabla^2 u
$$ (eq:navier-stokes)

### Figures

Add figures with captions and labels for cross-referencing:

```markdown
:::{figure} ../images/beam-deflection.svg
:label: fig:beam-fig
:align: center
:width: 60%

Deflection of a cantilever beam under point load
:::
```
:::{figure} ../images/beam-deflection.svg
:label: fig:beam-fig
:align: center
:width: 60%

Deflection of a cantilever beam under point load
:::


For subfigures, use a grid structure:
```markdown
::::{figure} ../images/comparison.svg
:label: fig:comparison-fig
:align: center

:::{image} ../images/experimental.svg
:::

:::{image} ../images/simulation.svg
:::

Experimental results
::::
```

::::{figure} ../images/comparison.svg
:label: fig:comparison-fig
:align: center

:::{image} ../images/experimental.svg
:::

:::{image} ../images/simulation.svg
:::

Experimental results
::::


:::{tip}
Save PowerPoint diagrams as SVG format for editability and scalability.
:::

### Tables

Simple markdown tables:

```markdown
:::{table} Material Properties
:label: tbl:material-table
:align: center
| Material | Young's Modulus (GPa) | Poisson's Ratio |
|----------|----------------------|-----------------|
| Steel    | 200                  | 0.30            |
| Aluminum | 69                   | 0.33            |
| Concrete | 30                   | 0.20            |
:::
```

:::{table} Material Properties
:label: tbl:material-table
:align: center
| Material | Young's Modulus (GPa) | Poisson's Ratio |
|----------|----------------------|-----------------|
| Steel    | 200                  | 0.30            |
| Aluminum | 69                   | 0.33            |
| Concrete | 30                   | 0.20            |
:::

For CSV data inline in your document:

```markdown
:::{csv-table} Material Properties
:label: tbl:material-table-csv
:align: center
:header: "Material", "Density (kg/m³)", "Yield Strength (MPa)"

"Steel", 7850, 250
"Aluminum", 2700, 95
"Titanium", 4500, 880
"Concrete", 2400, 3
:::
```

:::{csv-table} Material Properties
:label: tbl:material-table-csv
:align: center
:header: "Material", "Density (kg/m³)", "Yield Strength (MPa)"

"Steel", 7850, 250
"Aluminum", 2700, 95
"Titanium", 4500, 880
"Concrete", 2400, 3
:::


For external table files, use the `{table}` directive with the `{include}` directive nested inside. The included file should contain HTML table markup:
```markdown
::::{table} Material Properties from CSV File
:label: tbl:material-table-file
:align: center

:::{include} ../data/materials.html
:::

::::
```
::::{table} Material Properties from CSV File
:label: tbl:material-table-file
:align: center

:::{include} ../data/materials.html
:::

::::


## Scholarly Features

### Cross-References

Reference any labeled element using its label:


As shown in [](#fig:beam-fig), the deflection increases linearly.

The governing Equation [](#eq:navier-stokes) describes fluid motion.

Material properties are listed in [](#tbl:material-table).

### Numbered References

Use `{numref}` for numbered references with custom text:

```markdown
{numref}`fig:beam-fig`
{numref}`tbl:material-table`
{numref}`Equation %s <eq:navier-stokes>`
```

{numref}`fig:beam-fig` shows the beam deflection.

See {numref}`tbl:material-table` for material properties.

From {numref}`Equation %s <eq:navier-stokes>`, we can derive...


### Citations

#### Method 1: BibTeX

Create a `references.bib` file:

````markdown
```{code} bibtex
:filename: references.bib

@article{smith2023,
  title={Computational Mechanics of Structures},
  author={Smith, John and Doe, Jane},
  journal={Journal of Engineering},
  year={2023}
}
```
````

```{code} bibtex
:filename: references.bib

@article{smith2023,
  title={Computational Mechanics of Structures},
  author={Smith, John and Doe, Jane},
  journal={Journal of Engineering},
  year={2023}
}
```

Add to frontmatter and cite:

```yaml
---
bibliography: references.bib
---
```

```markdown
[@smith2023]
[@smith2023; @zhang2023]

```
Recent studies [@smith2023] show that...

Multiple citations [@smith2023; @zhang2023] indicate...


#### Method 2: DOI

Cite directly using DOI:
```markdown
@10.1016/j.jsv.2025.119289
```
The foundational work @10.1016/j.jsv.2025.119289 established...


### Abbreviations

Define abbreviations project-wide in `myst.yml` (recommended) or in individual files:

```{code} yaml
:filename: myst.yml

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

```{code} yaml
:filename: myst.yml
# In myst.yml
project:
  title: Computational Mechanics Book
  description: Advanced structural analysis techniques
  keywords: [structural analysis, computational mechanics, finite elements]
  authors:
    - name: Mohammad Talebi-Kalaleh
      affiliations:
        - University of Alberta
      orcid: 0009-0004-3754-5992
```

**Option 2: Page-specific in `.md` files** (for unique page metadata):

```yaml
---
title: Chapter 3: Nonlinear Analysis
date: 2024-11-19
doi: 10.1000/chapter-doi
# Page-specific metadata overrides project defaults
---
```

Best practice: Define common metadata (authors, keywords, abbreviations) in `myst.yml`, then add page-specific details (title, date, DOI) in individual files.

## Code Integration

### Global Configuration

Create a hidden setup cell at the document start:

````markdown
```{code-cell} python
:tags: [remove-cell]

```
````

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
````markdown
```python

```
````

```python
def calculate_stress(force, area):
    """Calculate engineering stress"""
    return force / area
```


With line numbers and highlighting:

````markdown
```{code} python
:linenos:
:emphasize-lines: 2


```
````

```{code} python
:linenos:
:emphasize-lines: 2

def beam_deflection(load, length, E, I):
    # Maximum deflection for cantilever beam
    delta_max = (load * length**3) / (3 * E * I)
    return delta_max
```

### Executable Code Cells

Create executable cells that run when building:
````markdown
```{code-cell} python
:caption: Figure Generated by Python Code Cell with Caption.
:label: fig:python-plot

```
````

```{code-cell} python
:caption: Figure Generated by Python Code Cell with Caption.
:label: fig:python-plot
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

Create and display tables using pandas:

```{code-cell} python
import pandas as pd
from IPython.display import display

# Define material properties
data = {
    "Material": ["Steel", "Aluminum", "Concrete"],
    "Density (kg/m³)": [7850, 2700, 2400],
    "Yield Strength (MPa)": [250, 95, 3]
}

# Create a DataFrame
material_df = pd.DataFrame(data)

display(material_df.style.hide(axis='index').set_properties(**{'text-align': 'left'}))
```

### Including External Code

Include code from separate files. This directive is helpful for showing code snippets without duplicating your content:

````markdown
```{literalinclude} ../scripts/analysis.py
:lineno-match:

```
````

```{literalinclude} ../scripts/analysis.py
:lineno-match:
```


````markdown
```{literalinclude} ../scripts/analysis.py
:start-at: def calculate_beam_deflection
:end-before: def natural_frequency
:lineno-match:

```
````

```{literalinclude} ../scripts/analysis.py
:start-at: def calculate_beam_deflection
:end-before: def natural_frequency
:lineno-match:
```

### Controlling Cell Visibility

Use tags to control what readers see:

Available tags:
- `hide-input`: Collapse code (can be expanded)
- `hide-output`: Collapse output
- `remove-input`: Completely remove code
- `remove-output`: Completely remove output
- `remove-cell`: Remove entire cell

First, let's define the required functions, then let's use different cell tags:

````markdown
```{code-cell} python
:tags: [remove-cell]

```
````

```{code-cell} python
:tags: [remove-cell]
import numpy as np
import matplotlib.pyplot as plt

def perform_analysis():
    """Perform structural analysis and return results."""
    # Simulate structural analysis
    stress_data = np.random.normal(150, 25, 100)  # MPa
    displacement_data = np.random.normal(2.5, 0.5, 100)  # mm
    
    results = {
        'max_stress': np.max(stress_data),
        'avg_stress': np.mean(stress_data),
        'max_displacement': np.max(displacement_data),
        'stress_data': stress_data,
        'displacement_data': displacement_data
    }
    return results

def intermediate_calc(i):
    """Perform intermediate calculations."""
    # Simulate complex calculations
    result = np.sin(i/100) * np.exp(-i/1000)
    return result

def plot_final_results():
    """Generate final results plot."""
    # Generate sample data
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x) * np.exp(-x/5)
    y2 = np.cos(x) * np.exp(-x/8)
    
    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(x, y1, 'b-', label='Stress Response', linewidth=2)
    plt.plot(x, y2, 'r--', label='Displacement Response', linewidth=2)
    plt.xlabel('Time (s)')
    plt.ylabel('Response')
    plt.title('Structural Response Analysis')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

```

````markdown
```{code-cell} python
:tags: [hide-input]

```
````

```{code-cell} python
:tags: [hide-input]
# Code hidden, only output shown
results = perform_analysis()
print(f"Maximum stress: {results['max_stress']:.2f} MPa")
print(f"Average stress: {results['avg_stress']:.2f} MPa")
print(f"Maximum displacement: {results['max_displacement']:.2f} mm")
```

````markdown
```{code-cell} python
:tags: [hide-output]

```
````

```{code-cell} python
:tags: [hide-output]
# Complex calculation - output hidden
calculation_results = []
for i in range(1000):
    result = intermediate_calc(i)
    calculation_results.append(result)
print(f"Completed {len(calculation_results)} calculations")
```

```{code-cell} python
:tags: [remove-input]
# Only the plot appears, no code
plot_final_results()
```

## Enhanced Content

### Inline Code Results with `{eval}`

Display variables from code cells inline:

```{code-cell} python
:tags: [remove-cell]
max_stress = 250.5
safety_factor = 2.5
```

```markdown
{eval}`max_stress`
{eval}`safety_factor`
```

The maximum stress is {eval}`max_stress` MPa, 
with a safety factor of {eval}`safety_factor`.

### Interactive Widgets

Create interactive visualizations and controls using ipywidgets:

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

Advanced Widget Dashboard:

```{code-cell} python
import ipywidgets as widgets
from IPython.display import display

# Text widgets
text_input = widgets.Text(
    value='Hello World',
    placeholder='Type something',
    description='Text Input:',
    disabled=False
)

textarea = widgets.Textarea(
    value='Multi-line\ntext input',
    placeholder='Type something',
    description='Text Area:',
    disabled=False
)

# Numeric widgets
int_slider = widgets.IntSlider(
    value=7,
    min=0,
    max=10,
    step=1,
    description='Int Slider:'
)

float_slider = widgets.FloatSlider(
    value=7.5,
    min=0,
    max=10.0,
    step=0.1,
    description='Float Slider:'
)

int_range_slider = widgets.IntRangeSlider(
    value=[5, 7],
    min=0,
    max=10,
    step=1,
    description='Range:'
)

# Selection widgets
dropdown = widgets.Dropdown(
    options=['Option 1', 'Option 2', 'Option 3'],
    value='Option 1',
    description='Dropdown:'
)

radio_buttons = widgets.RadioButtons(
    options=['Option A', 'Option B', 'Option C'],
    description='Radio:'
)

select_multiple = widgets.SelectMultiple(
    options=['Apple', 'Banana', 'Cherry', 'Date'],
    value=['Apple'],
    description='Multi-Select:'
)

# Boolean widgets
checkbox = widgets.Checkbox(
    value=False,
    description='Checkbox',
    disabled=False
)

toggle_button = widgets.ToggleButton(
    value=False,
    description='Toggle Me',
    disabled=False,
    button_style='info',
    tooltip='Click me'
)

# Button widgets
button = widgets.Button(
    description='Click Me!',
    disabled=False,
    button_style='success',
    tooltip='Click me',
    icon='check'
)

# Date and time widgets
date_picker = widgets.DatePicker(
    description='Pick a Date',
    disabled=False
)

# Color picker
color_picker = widgets.ColorPicker(
    concise=False,
    description='Pick a color',
    value='blue',
    disabled=False
)

# File upload
file_upload = widgets.FileUpload(
    accept='',  # Accepted file extension
    multiple=False  # True to accept multiple files
)

# Progress bar
progress = widgets.IntProgress(
    value=7,
    min=0,
    max=10,
    description='Loading:',
    bar_style='info',
    style={'bar_color': 'maroon'},
    orientation='horizontal'
)

# Display all widgets in organized layout
display(widgets.HTML('<h3>Widget Types Demonstration</h3>'))

display(widgets.HTML('<h4>Text Input Widgets</h4>'))
display(widgets.HBox([text_input, textarea]))

display(widgets.HTML('<h4>Numeric Widgets</h4>'))
display(widgets.VBox([int_slider, float_slider, int_range_slider]))

display(widgets.HTML('<h4>Selection Widgets</h4>'))
display(widgets.HBox([
    widgets.VBox([dropdown, radio_buttons]), 
    select_multiple
]))

display(widgets.HTML('<h4>Boolean and Button Widgets</h4>'))
display(widgets.HBox([checkbox, toggle_button, button]))

display(widgets.HTML('<h4>Specialized Widgets</h4>'))
display(widgets.HBox([date_picker, color_picker]))
display(widgets.VBox([file_upload, progress]))

# Add event handling example
def on_button_clicked(b):
    with widgets.Output():
        print("Button clicked!")

button.on_click(on_button_clicked)
```

### Admonitions

Highlight important information:

```markdown
:::{note}
This method assumes linear elastic behavior.
:::
```

:::{note}
This method assumes linear elastic behavior.
:::

```markdown
:::{attention}
Ensure all units are consistent before performing calculations.
:::
```

:::{attention}
Ensure all units are consistent before performing calculations.
:::

```markdown
:::{important}
Safety factors must comply with local building codes.
:::
```

:::{important}
Safety factors must comply with local building codes.
:::

```markdown
:::{caution}
Avoid using this formula for non-linear materials.
:::
```

:::{caution}
Avoid using this formula for non-linear materials.
:::

```markdown
:::{hint}
Consider using a numerical solver for complex systems.
:::
```

:::{hint}
Consider using a numerical solver for complex systems.
:::

```markdown
:::{warning}
Check boundary conditions before applying this formula.
:::
```

:::{warning}
Check boundary conditions before applying this formula.
:::

```markdown
:::{seealso}
Refer to the appendix for detailed derivations.
:::
```

:::{seealso}
Refer to the appendix for detailed derivations.
:::

```markdown
:::{danger}
Incorrect application of this method can lead to structural failure.
:::
```

:::{danger}
Incorrect application of this method can lead to structural failure.
:::

```markdown
:::{tip}
:class: dropdown
Use dimensionless parameters to generalize your results.
:::
```

:::{tip}
:class: dropdown
Use dimensionless parameters to generalize your results.
:::

```markdown
:::{error}
Calculation error detected: please review input values.
:::
```

:::{error}
Calculation error detected: please review input values.
:::

### Exercise and Solution Blocks

Create teaching materials:

```markdown
:::{exercise}
:label: ex1
Calculate the natural frequency of a cantilever beam with:

- Length L = 2 m
- Mass m = 10 kg at the tip
- Flexural rigidity EI = 1000 N⋅m²
:::
```

:::{exercise}
:label: ex1
Calculate the natural frequency of a cantilever beam with:

- Length L = 2 m
- Mass m = 10 kg at the tip
- Flexural rigidity EI = 1000 N⋅m²
:::

```markdown
:::{solution} ex1
:class: dropdown

Using the formula for a cantilever with tip mass:
$$\omega_n = \sqrt{\frac{3EI}{mL^3}}$$

Substituting values:
$$\omega_n = \sqrt{\frac{3 \times 1000}{10 \times 2^3}} = 6.12 \text{ rad/s}$$

:::
```

:::{solution} ex1
:class: dropdown

Using the formula for a cantilever with tip mass:
$$\omega_n = \sqrt{\frac{3EI}{mL^3}}$$

Substituting values:
$$\omega_n = \sqrt{\frac{3 \times 1000}{10 \times 2^3}} = 6.12 \text{ rad/s}$$

:::

````markdown
:::{exercise-start}
:label: ex2
:::

```{code-cell} python
:tags: [remove-cell]

```

:::{exercise-end}
:::
````

:::{exercise-start}
:label: ex2
:::

```{code-cell} python
:tags: [remove-cell]
import numpy as np

# Generate random parameters for the exercise
np.random.seed(42)  # For reproducible results
L_val = np.random.uniform(1.5, 3.0)  # Length between 1.5-3.0 m
m_val = np.random.uniform(8, 15)     # Mass between 8-15 kg
EI_val = np.random.uniform(800, 1200) # EI between 800-1200 N⋅m²

# Round to reasonable precision
L_val = round(L_val, 1)
m_val = round(m_val, 1)
EI_val = round(EI_val, 0)
```

Calculate the natural frequency of a cantilever beam with randomly generated parameters:

- Length L = {eval}`L_val` m
- Mass m = {eval}`m_val` kg at the tip  
- Flexural rigidity EI = {eval}`EI_val` N⋅m²

Find the natural frequency in both rad/s and Hz.

:::{exercise-end}
:::


````markdown
:::{solution-start} ex2
:class: dropdown
:::

```{code-cell} python
:tags: [remove-cell]

```

:::{solution-end}
:::
````

:::{solution-start} ex2
:class: dropdown
:::

```{code-cell} python
:tags: [remove-cell]

import sympy as sp
from sympy import symbols, sqrt, simplify, latex
import numpy as np

sp.init_printing()

# Define symbolic variables
L, m, EI, omega_n = symbols('L m EI omega_n', positive=True, real=True)

# Define the formula symbolically
formula = sqrt(3*EI/(m*L**3))

# Get the general formula in LaTeX
formula_latex = f"$$\\omega_n = {latex(formula)}$$"

# Substitute numerical values
L_sym, m_sym, EI_sym = L_val, m_val, EI_val
substituted_formula = formula.subs([(L, L_sym), (m, m_sym), (EI, EI_sym)])

# Create step-by-step LaTeX expressions
step1_latex = f"$$\\omega_n = \\sqrt{{\\frac{{3 \\times {EI_sym}}}{{{m_sym} \\times {L_sym}^3}}}}$$"

# Calculate intermediate values
numerator = 3 * EI_sym
denominator = m_sym * (L_sym**3)
fraction = numerator / denominator

step2_latex = f"$$\\omega_n = \\sqrt{{\\frac{{{numerator}}}{{{denominator}}}}}$$"
step3_latex = f"$$\\omega_n = \\sqrt{{{fraction:.4f}}}$$"

# Final calculation
omega_n_val = float(substituted_formula.evalf())
freq_hz = omega_n_val / (2 * np.pi)

step4_latex = f"$$\\omega_n = {omega_n_val:.3f} \\text{{ rad/s}}$$"

# Frequency conversion
freq_step1_latex = f"$$f = \\frac{{\\omega_n}}{{2\\pi}} = \\frac{{{omega_n_val:.3f}}}{{2\\pi}}$$"
freq_step2_latex = f"$$f = {freq_hz:.3f} \\text{{ Hz}}$$"

# Store results for inline evaluation (with formatting)
omega_result = omega_n_val
freq_result = freq_hz
omega_result_formatted = f"{omega_n_val:.3f}"
freq_result_formatted = f"{freq_hz:.3f}"
substituted_formula
```

**Solution Process:**

1. **Starting Formula:** The natural frequency of a cantilever beam with tip mass is given by:
   {eval}`formula_latex`

2. **Substituting Values:** With L = {eval}`L_val` m, m = {eval}`m_val` kg, EI = {eval}`EI_val` N⋅m²:
   {eval}`step1_latex`

3. **Numerical Calculation:**
   {eval}`step2_latex`
   {eval}`step3_latex`
   {eval}`step4_latex`

4. **Converting to Hz:**
   {eval}`freq_step1_latex`
   {eval}`freq_step2_latex`

**Final Answers:**
- Natural frequency: {eval}`omega_result_formatted` rad/s
- Frequency in Hz: {eval}`freq_result_formatted` Hz

:::{solution-end}
:::

### Mermaid Diagrams

Create flowcharts and diagrams:
````markdown
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
````

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
```markdown
:::{iframe} https://www.youtube.com/embed/CRa9djnZRu0?start=511&end=655&version=3&rel=0&autoplay=0
:width: 100%
Sample Youtube Video

:::
```

:::{iframe} https://www.youtube.com/embed/CRa9djnZRu0?start=511&end=655&version=3&rel=0&autoplay=0
:width: 100%
Sample Youtube Video

:::

```markdown
:::{figure} ../videos/experiment.mp4
:label: fig:video-local
:width: 80%
Sample Local Video: Experimental setup and testing procedure
:::
```

:::{figure} ../videos/experiment.mp4
:label: fig:video-local
:width: 80%
Sample Local Video: Experimental setup and testing procedure
:::

## Exporting to LaTeX and PDF

### List Available Templates

View journal templates:

```bash
jupyter-book templates list --pdf
```

**Common Academic Templates:**

1. **Plain LaTeX Book** (`plain_latex_book`)
   - Description: A plain latex book theme
   - Tags: book
   - Best for: Traditional academic books and comprehensive documentation

2. **LaPreprint Typst Template** (`lapreprint-typst`)
   - Description: Easily create beautiful preprints in Typst
   - Tags: preprint, article, paper
   - Best for: Academic preprints and research papers

3. **arXiv (NIPS Style)** (`arxiv_nips`)
   - Description: An arXiv compatible template based on the NIPS 2018 Style
   - Tags: paper, preprint, arxiv, bioarxiv, eartharxiv
   - Best for: Conference papers and arXiv submissions

### Configure the Exports
To define exports and templates in your `myst.yml` file, you can specify the desired output format and template under the `exports` section. This allows you to customize the export settings for your Jupyter Book. Here is an example configuration:

```{code} yaml
:filename: myst.yml

project:
  exports:
    - format: pdf
      template: lapreprint-typst
      articles: [content/intro.md, content/chapter1.md]
      line_numbers: true
```

This configuration will:
- Export to PDF format using the `lapreprint-typst` template
- Include only the `intro.md` file 
- Save outputs to the default `_build` directory structure


### Build PDF

Generate PDF using default template:

```bash
jupyter-book build --pdf
```

:::{warning} PDF exports require $\LaTeX$ or Typst to be installed

The default PDF renderer uses $\LaTeX$ to create PDFs, which means that to work locally you will need to [Install LaTeX]((https://www.latex-project.org/get/)). A warning will occur if MyST cannot find a $\LaTeX$ environment, as well as forcing the build process and reporting any errors.

As an alternative, for faster PDF builds, you may use [Install Typst](https://github.com/typst/typst?tab=readme-ov-file#installation) instead.

**For SVG graphics processing, install Inkscape:**
- **Windows**: `winget install Inkscape.Inkscape` or download from [inkscape.org](https://inkscape.org)
- **macOS**: `brew install inkscape` or download from [inkscape.org](https://inkscape.org)



**Handling Animated Images**
Animated images, such as GIFs, are not well supported by the PDF format. When exporting to PDF, MyST will convert the first frame of an animated image to a static image. To perform this conversion, you need to have [ImageMagick](https://imagemagick.org/) installed on your system. Here are the installation instructions for different operating systems:

- **Windows**: `winget install ImageMagick.ImageMagick`
- **macOS**: `brew install imagemagick`
- **Linux**: Use your package manager, e.g., `sudo apt-get install imagemagick`

:::

### Export to LaTeX

For journal submission, export LaTeX source:

```bash
jupyter-book build --tex
```

The LaTeX files will be in `_build/tex/`.

## Authoring with JupyterLab

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

## Web Deployment with GitHub Pages

### Create .gitignore

```text
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
:filename: .github/workflows/deploy.yml

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

## Maintenance & Collaboration

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
- Auto-completing markdown text
- Generating boilerplate code cells
- Creating consistent documentation

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

```markdown
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

- Documentation: https://next.jupyterbook.org/tutorial
- MyST Syntax: https://mystmd.org/guide
- Templates: https://github.com/jupyter-book/cookiecutter-jupyter-book

## Downloads

Download the complete guide as PDF:

- [📥 Comprehensive MyST Documentation (PDF)](../downloads/Comprehensive-MyST-Document.pdf){:download} - Complete guide with all features, code examples, and styling

The PDF is automatically generated when you run the script in the `pdf_generator` folder:

```bash
python pdf_generator/generate_pdf.py
```

---

*Workshop materials by Mohammad Talebi-Kalaleh, University of Alberta*

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

# Basic MyST Features

This chapter demonstrates fundamental MyST Markdown features for scientific writing.

## Mathematics

Inline math: The beam deflection $\delta = \frac{PL^3}{3EI}$ depends on load and stiffness.

Display equations with labels:

$$
\sigma = \frac{My}{I}
$$ (bending-stress)

$$
\tau = \frac{VQ}{It}
$$ (shear-stress)

## Figures and Images

:::{figure} https://github.com/rowanc1/pics/blob/main/mountains.png?raw=true
:label: fig-mountains
:width: 70%
:align: center

Beautiful mountains for inspiration while coding
:::

Reference figures: As shown in {numref}`Figure %s <fig-mountains>`, nature can be inspiring.

## Tables

### Markdown Tables

| Property | Steel | Aluminum | Concrete |
|----------|-------|----------|----------|
| Density (kg/m³) | 7850 | 2700 | 2400 |
| E (GPa) | 200 | 69 | 30 |
| Yield (MPa) | 250 | 95 | 3 |

### CSV Tables

:::{csv-table} Beam Section Properties
:header: "Section", "Area (mm²)", "Ixx (mm⁴)", "Zx (mm³)"
:widths: 30, 25, 25, 20

"W200×100", 12700, "113e6", "1130e3"
"W250×150", 19000, "257e6", "2057e3"
"W300×200", 25400, "415e6", "2767e3"
:::

## Code Examples

### Static Code Block

```python
def calculate_moment(force, distance):
    """Calculate bending moment"""
    return force * distance
```

### Executable Code

```{code-cell} python
import numpy as np
import matplotlib.pyplot as plt

# Beam analysis
L = 10  # Length (m)
w = 5   # Distributed load (kN/m)

x = np.linspace(0, L, 100)
M = (w * x * (L - x)) / 2  # Moment distribution

plt.figure(figsize=(8, 4))
plt.plot(x, M, 'b-', linewidth=2)
plt.xlabel('Position (m)')
plt.ylabel('Moment (kN⋅m)')
plt.title('Simply Supported Beam - Moment Diagram')
plt.grid(True, alpha=0.3)
plt.show()
```

## Cross-References

From equation {eq}`bending-stress`, we calculate the maximum stress.
The shear stress (Eq. {eq}`shear-stress`) is typically smaller.

## Citations

Recent studies on FEM [@smith2023] show improved accuracy.
Direct DOI citation: @10.1093/nar/22.22.4673

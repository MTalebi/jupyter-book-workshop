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

# Advanced Computational Features

```{code-cell} python
:tags: [remove-cell]
import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display
```

## Interactive Widgets

```{code-cell} python
@widgets.interact(
    frequency=(1, 5, 0.5),
    amplitude=(0.5, 2, 0.1),
    damping=(0, 0.5, 0.05)
)
def vibration_response(frequency=2, amplitude=1, damping=0.1):
    t = np.linspace(0, 10, 1000)
    response = amplitude * np.exp(-damping * t) * np.sin(2 * np.pi * frequency * t)
    
    plt.figure(figsize=(10, 4))
    plt.plot(t, response, 'b-', linewidth=2)
    plt.xlabel('Time (s)')
    plt.ylabel('Displacement (mm)')
    plt.title(f'Damped Vibration: f={frequency} Hz, ζ={damping}')
    plt.grid(True, alpha=0.3)
    plt.ylim(-2.5, 2.5)
    plt.show()
```

## Using {eval} for Inline Results

```{code-cell} python
:tags: [remove-cell]
# Calculate structural parameters
beam_length = 6.5  # meters
max_load = 125.7   # kN
safety_factor = 2.5
max_deflection = beam_length / 250  # L/250 criterion
```

The beam spans {eval}`beam_length` meters with a maximum load of {eval}`max_load` kN.
Using a safety factor of {eval}`safety_factor`, the allowable deflection is {eval}`f"{max_deflection*1000:.1f}"` mm.

## Advanced Code Features

### Hidden Setup Code

```{code-cell} python
:tags: [hide-input]
# Generate structural analysis data
np.random.seed(42)
nodes = 50
time_steps = 100

# Simulate displacement data
time = np.linspace(0, 10, time_steps)
displacement = np.random.randn(nodes, time_steps) * 0.1

# Calculate statistics
max_disp = np.max(np.abs(displacement))
mean_disp = np.mean(displacement)
std_disp = np.std(displacement)

print(f"Analysis Results:")
print(f"  Max displacement: {max_disp:.3f} mm")
print(f"  Mean: {mean_disp:.3f} mm")
print(f"  Std deviation: {std_disp:.3f} mm")
```

### Complex Visualizations

```{code-cell} python
:tags: [remove-input]
# Create publication-quality figure
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# Mode shapes
modes = 4
x = np.linspace(0, 1, 100)
for i in range(modes):
    ax = axes[i//2, i%2]
    mode_shape = np.sin((i+1) * np.pi * x)
    ax.plot(x, mode_shape, 'b-', linewidth=2)
    ax.fill_between(x, 0, mode_shape, alpha=0.3)
    ax.set_title(f'Mode {i+1}: {(i+1)**2:.1f} Hz')
    ax.set_xlabel('Normalized Length')
    ax.set_ylabel('Amplitude')
    ax.grid(True, alpha=0.3)

plt.suptitle('Cantilever Beam Mode Shapes', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()
```

## Admonitions

:::{tip}
:class: dropdown
**Performance Optimization Tips:**
- Use vectorized NumPy operations
- Pre-allocate arrays for large computations
- Profile code with `%timeit` magic
:::

:::{warning}
Always validate numerical results with analytical solutions when possible!
:::

:::{exercise}
:label: ex-beam
Calculate the first three natural frequencies of a cantilever beam with:
- Length: 3 m
- EI: 2000 N⋅m²
- Mass per length: 10 kg/m
:::

:::{solution} ex-beam
:class: dropdown
The natural frequencies are:
- $\omega_1 = 1.875^2 \sqrt{\frac{EI}{mL^4}} = 3.52$ rad/s
- $\omega_2 = 4.694^2 \sqrt{\frac{EI}{mL^4}} = 22.0$ rad/s  
- $\omega_3 = 7.855^2 \sqrt{\frac{EI}{mL^4}} = 61.7$ rad/s
:::

## Mermaid Diagrams

```{mermaid}
graph TD
    A[Structural Model] --> B[Mesh Generation]
    B --> C[Element Formulation]
    C --> D[Global Assembly]
    D --> E[Apply Boundary Conditions]
    E --> F[Solve System]
    F --> G{Converged?}
    G -->|No| H[Update]
    H --> D
    G -->|Yes| I[Post-Process Results]
    I --> J[Visualize]
```

## External Code Inclusion

```{literalinclude} ../scripts/analysis.py
:language: python
:lines: 1-10
:linenos:
:emphasize-lines: 5,6
```

## Bibliography

For comprehensive FEM theory, see [@smith2023; @johnson2022]. 
Recent advances in SHM are reviewed in @10.1016/j.engstruct.2023.115234.

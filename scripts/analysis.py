"""
Structural Analysis Module
Example code for Jupyter Book Workshop
"""

import numpy as np

def calculate_beam_deflection(load, length, E, I):
    """Calculate maximum deflection of a simply supported beam"""
    return (5 * load * length**4) / (384 * E * I)

def natural_frequency(mass, stiffness):
    """Calculate natural frequency of SDOF system"""
    return np.sqrt(stiffness / mass) / (2 * np.pi)

def stress_analysis(force, area):
    """Calculate normal stress"""
    return force / area

if __name__ == "__main__":
    # Example usage
    deflection = calculate_beam_deflection(10, 5, 200e9, 1e-4)
    print(f"Maximum deflection: {deflection*1000:.2f} mm")

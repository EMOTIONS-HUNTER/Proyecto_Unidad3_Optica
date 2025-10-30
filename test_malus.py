"""
Pruebas unitarias para el módulo de cálculos de Malus
"""

import pytest
import numpy as np
import sys
import os

# Agregar el directorio padre al path para importar el módulo
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from malus_calculations import PolarizationSimulator, calculate_transmission_angle

class TestPolarizationSimulator:
    """Pruebas para la clase PolarizationSimulator"""
    
    def setup_method(self):
        """Configuración inicial para cada prueba"""
        self.simulator = PolarizationSimulator(initial_intensity=1.0)
    
    def test_malus_law_0_degrees(self):
        """Prueba con ángulo de 0 grados (máxima transmisión)"""
        result = self.simulator.malus_law(0)
        assert abs(result - 1.0) < 1e-10
    
    def test_malus_law_90_degrees(self):
        """Prueba con ángulo de 90 grados (mínima transmisión)"""
        result = self.simulator.malus_law(90)
        assert abs(result - 0.0) < 1e-10
    
    def test_malus_law_45_degrees(self):
        """Prueba con ángulo de 45 grados"""
        result = self.simulator.malus_law(45)
        expected = 0.5  # cos²(45°) = (√2/2)² = 0.5
        assert abs(result - expected) < 1e-10
    
    def test_multiple_polarizers(self):
        """Prueba con múltiples polarizadores"""
        angles = [45, 45]  # Dos polarizadores a 45°
        intensities = self.simulator.multiple_polarizers(angles)
        
        # Después del primer polarizador: I = 1 * cos²(45) = 0.5
        # Después del segundo: I = 0.5 * cos²(45) = 0.25
        expected = [1.0, 0.5, 0.25]
        
        for calc, exp in zip(intensities, expected):
            assert abs(calc - exp) < 1e-10
    
    def test_theoretical_curve(self):
        """Prueba de generación de curva teórica"""
        angles, intensities = self.simulator.theoretical_curve(points=10)
        
        assert len(angles) == 10
        assert len(intensities) == 10
        assert angles[0] == 0
        assert angles[-1] == 360
        assert intensities[0] == 1.0  # 0°
        assert abs(intensities[4] - 0.0) < 1e-10  # 180°

def test_calculate_transmission_angle():
    """Prueba de la función calculate_transmission_angle"""
    
    # Caso: 50% de transmisión -> ángulo de 45°
    angle = calculate_transmission_angle(0.5, 1.0)
    assert abs(angle - 45.0) < 1e-10
    
    # Caso: 100% de transmisión -> ángulo de 0°
    angle = calculate_transmission_angle(1.0, 1.0)
    assert abs(angle - 0.0) < 1e-10
    
    # Caso: 0% de transmisión -> ángulo de 90°
    angle = calculate_transmission_angle(0.0, 1.0)
    assert abs(angle - 90.0) < 1e-10

def test_edge_cases():
    """Prueba de casos límite"""
    simulator = PolarizationSimulator(1.0)
    
    # Ángulos negativos (deberían funcionar por periodicidad)
    result_neg = simulator.malus_law(-45)
    result_pos = simulator.malus_law(315)  # Equivalente a -45°
    assert abs(result_neg - result_pos) < 1e-10
    
    # Ángulos mayores a 360°
    result_large = simulator.malus_law(405)  # 405° = 45°
    expected = simulator.malus_law(45)
    assert abs(result_large - expected) < 1e-10

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

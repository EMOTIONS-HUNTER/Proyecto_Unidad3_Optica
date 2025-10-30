"""
Módulo para cálculos de polarización y Ley de Malus
Autor: [Cristian Ashiel Contreras Sandoval ]
Fecha: [30/10/2025]
"""

import numpy as np
import matplotlib.pyplot as plt

class PolarizationSimulator:
    """
    Simulador de polarización y Ley de Malus
    """
    
    def __init__(self, initial_intensity=1.0):
        """
        Inicializa el simulador
        
        Args:
            initial_intensity (float): Intensidad inicial de la luz no polarizada (W/m²)
        """
        self.I0 = initial_intensity
        
    def malus_law(self, angle_degrees, I0=None):
        """
        Calcula la intensidad transmitida según la Ley de Malus
        
        Args:
            angle_degrees (float): Ángulo entre polarizadores en grados
            I0 (float): Intensidad incidente (opcional)
            
        Returns:
            float: Intensidad transmitida
        """
        if I0 is None:
            I0 = self.I0
            
        # Convertir a radianes y aplicar Ley de Malus
        angle_rad = np.radians(angle_degrees)
        return I0 * (np.cos(angle_rad) ** 2)
    
    def multiple_polarizers(self, angles_degrees, I0=None):
        """
        Calcula la intensidad a través de múltiples polarizadores
        
        Args:
            angles_degrees (list): Lista de ángulos entre polarizadores consecutivos
            I0 (float): Intensidad inicial
            
        Returns:
            list: Intensidades en cada etapa
        """
        if I0 is None:
            I0 = self.I0
            
        intensities = [I0]
        current_I = I0
        
        for angle in angles_degrees:
            current_I = self.malus_law(angle, current_I)
            intensities.append(current_I)
            
        return intensities
    
    def theoretical_curve(self, points=360):
        """
        Genera curva teórica de la Ley de Malus
        
        Args:
            points (int): Número de puntos en la curva
            
        Returns:
            tuple: (ángulos, intensidades)
        """
        angles = np.linspace(0, 360, points)
        intensities = [self.malus_law(angle) for angle in angles]
        
        return angles, intensities
    
    def validate_with_reference(self, reference_data):
        """
        Valida los cálculos con datos de referencia
        
        Args:
            reference_data (dict): Datos de referencia {ángulo: intensidad}
            
        Returns:
            dict: Resultados de validación
        """
        validation_results = {}
        
        for angle, ref_intensity in reference_data.items():
            calculated = self.malus_law(angle)
            error = abs(calculated - ref_intensity)
            error_percent = (error / ref_intensity) * 100
            
            validation_results[angle] = {
                'reference': ref_intensity,
                'calculated': calculated,
                'absolute_error': error,
                'percent_error': error_percent
            }
            
        return validation_results

# Funciones de utilidad
def calculate_transmission_angle(I_transmitted, I0):
    """
    Calcula el ángulo necesario para una transmisión específica
    
    Args:
        I_transmitted (float): Intensidad transmitida deseada
        I0 (float): Intensidad incidente
        
    Returns:
        float: Ángulo en grados
    """
    if I_transmitted > I0:
        raise ValueError("La intensidad transmitida no puede ser mayor que la incidente")
    
    transmission_ratio = I_transmitted / I0
    if transmission_ratio < 0:
        raise ValueError("La intensidad no puede ser negativa")
    
    angle_rad = np.arccos(np.sqrt(transmission_ratio))
    return np.degrees(angle_rad)

def generate_sample_data():
    """
    Genera datos de muestra para demostración
    """
    angles = [0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180]
    simulator = PolarizationSimulator(initial_intensity=1.0)
    
    data = []
    for angle in angles:
        intensity = simulator.malus_law(angle)
        data.append({
            'angle': angle,
            'intensity': intensity,
            'transmission_percent': intensity * 100
        })
    
    return data

if __name__ == "__main__":
    # Ejemplo de uso
    simulator = PolarizationSimulator(1.0)
    
    # Prueba con ángulo de 45 grados
    test_angle = 45
    result = simulator.malus_law(test_angle)
    print(f"Intensidad transmitida a {test_angle}°: {result:.4f}")
    
    # Curva teórica
    angles, intensities = simulator.theoretical_curve()
    print("Curva teórica generada correctamente")

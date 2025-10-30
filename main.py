"""
Simulador Interactivo de Polarización y Ley de Malus
Autor: [Cristian Ashiel Contreras Sandoval ]
Fecha: [30/10/2025]

Este simulador permite visualizar la Ley de Malus y experimentar con 
diferentes configuraciones de polarizadores.
"""

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from malus_calculations import PolarizationSimulator, calculate_transmission_angle

# Configuración de la página
st.set_page_config(
    page_title="Simulador de Polarización - Ley de Malus",
    page_icon="🔅",
    layout="wide",
    initial_sidebar_state="expanded"
)

def setup_sidebar():
    """Configura los controles en la barra lateral"""
    st.sidebar.title("🔅 Controles del Simulador")
    
    st.sidebar.markdown("### Parámetros de Simulación")
    
    # Intensidad inicial
    I0 = st.sidebar.slider(
        "Intensidad inicial I₀ (W/m²)",
        min_value=0.1,
        max_value=10.0,
        value=1.0,
        step=0.1,
        help="Intensidad de la luz incidente no polarizada"
    )
    
    # Número de polarizadores
    num_polarizers = st.sidebar.selectbox(
        "Número de polarizadores",
        options=[2, 3, 4],
        index=0,
        help="Selecciona cuántos polarizadores incluir en la simulación"
    )
    
    # Ángulos de los polarizadores
    angles = []
    st.sidebar.markdown("### Configuración de Ángulos")
    
    for i in range(1, num_polarizers):
        angle = st.sidebar.slider(
            f"Ángulo del polarizador {i+1} (°)",
            min_value=0,
            max_value=180,
            value=45 if i == 1 else 90,
            step=5,
            help=f"Ángulo entre el polarizador {i} y {i+1}"
        )
        angles.append(angle)
    
    return I0, num_polarizers, angles

def plot_malus_curve(I0, current_angle=None):
    """Genera la gráfica de la Ley de Malus"""
    simulator = PolarizationSimulator(I0)
    angles, intensities = simulator.theoretical_curve()
    
    fig = go.Figure()
    
    # Curva teórica
    fig.add_trace(go.Scatter(
        x=angles, 
        y=intensities,
        mode='lines',
        name='Ley de Malus',
        line=dict(color='blue', width=3),
        hovertemplate='Ángulo: %{x}°<br>Intensidad: %{y:.3f} W/m²<extra></extra>'
    ))
    
    # Punto actual si se proporciona
    if current_angle is not None:
        current_intensity = simulator.malus_law(current_angle)
        fig.add_trace(go.Scatter(
            x=[current_angle],
            y=[current_intensity],
            mode='markers+text',
            name='Configuración actual',
            marker=dict(size=12, color='red'),
            text=[f'{current_intensity:.3f} W/m²'],
            textposition='top center'
        ))
    
    fig.update_layout(
        title='Ley de Malus - Intensidad Transmitida vs Ángulo',
        xaxis_title='Ángulo entre polarizadores (°)',
        yaxis_title='Intensidad transmitida (W/m²)',
        hovermode='x unified',
        height=400
    )
    
    return fig

def visualize_polarizer_system(angles, intensities):
    """Visualiza el sistema de polarizadores"""
    num_polarizers = len(intensities)
    
    fig = go.Figure()
    
    # Polarizadores como barras
    for i in range(num_polarizers):
        fig.add_trace(go.Bar(
            x=[f'P{i+1}'],
            y=[intensities[i]],
            name=f'Después de P{i+1}',
            text=[f'{intensities[i]:.3f} W/m²'],
            textposition='auto',
        ))
    
    fig.update_layout(
        title='Intensidad en Cada Etapa del Sistema',
        xaxis_title='Polarizador',
        yaxis_title='Intensidad (W/m²)',
        showlegend=False,
        height=400
    )
    
    return fig

def show_educational_content():
    """Muestra contenido educativo"""
    st.markdown("""
    ## 📚 Marco Teórico - Polarización y Ley de Malus
    
    ### ¿Qué es la polarización?
    La polarización es un fenómeno donde las ondas de luz oscilan predominantemente 
    en una dirección específica. Los polarizadores son dispositivos que solo permiten 
    el paso de luz que vibra en una dirección particular.
    
    ### Ley de Malus
    La **Ley de Malus**, descubierta por Étienne-Louis Malus en 1809, establece que 
    cuando la luz polarizada pasa a través de un segundo polarizador (analizador), 
    la intensidad transmitida viene dada por:
    
    """)
    
    st.latex(r"I = I_0 \cdot \cos^2(\theta)")
    
    st.markdown("""
    Donde:
    - \( I \) = Intensidad transmitida
    - \( I_0 \) = Intensidad incidente
    - \( \theta \) = Ángulo entre los ejes de transmisión de los polarizadores
    
    ### Aplicaciones en Ingeniería
    - **Pantallas LCD**: Uso de polarizadores para controlar píxeles
    - **Gafas de sol polarizadas**: Reducen reflejos
    - **Fotografía**: Mejora de contrastes y eliminación de reflejos
    - **Comunicaciones ópticas**: Modulación de señales
    - **Sensores**: Medición de tensiones en materiales
    """)

def calculate_efficiency(angles, intensities):
    """Calcula métricas de eficiencia del sistema"""
    initial_I = intensities[0]
    final_I = intensities[-1]
    
    efficiency = (final_I / initial_I) * 100
    total_angle = sum(angles)
    
    return {
        'eficiencia_transmision': efficiency,
        'intensidad_inicial': initial_I,
        'intensidad_final': final_I,
        'perdida_total': initial_I - final_I,
        'angulo_total': total_angle
    }

def main():
    """Función principal de la aplicación"""
    
    # Header
    st.title("🔅 Simulador Interactivo de Polarización y Ley de Malus")
    st.markdown("---")
    
    # Sidebar con controles
    I0, num_polarizers, angles = setup_sidebar()
    
    # Inicializar simulador
    simulator = PolarizationSimulator(I0)
    
    # Calcular intensidades
    if num_polarizers == 2:
        current_intensity = simulator.malus_law(angles[0])
        intensities = [I0, current_intensity]
    else:
        intensities = simulator.multiple_polarizers(angles)
    
    # Layout principal
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Gráfica de Ley de Malus
        current_angle = angles[0] if angles else 0
        malus_fig = plot_malus_curve(I0, current_angle)
        st.plotly_chart(malus_fig, use_container_width=True)
        
        # Sistema de polarizadores
        system_fig = visualize_polarizer_system(angles, intensities)
        st.plotly_chart(system_fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📊 Resultados Actuales")
        
        # Mostrar resultados numéricos
        results_df = pd.DataFrame({
            'Etapa': [f'P{i+1}' for i in range(len(intensities))],
            'Intensidad (W/m²)': [f'{I:.4f}' for I in intensities],
            'Porcentaje': [f'{(I/I0)*100:.1f}%' for I in intensities]
        })
        
        st.dataframe(results_df, use_container_width=True)
        
        # Métricas de eficiencia
        if len(angles) > 0:
            metrics = calculate_efficiency(angles, intensities)
            
            st.metric(
                label="Eficiencia de Transmisión",
                value=f"{metrics['eficiencia_transmision']:.1f}%"
            )
            
            st.metric(
                label="Pérdida Total",
                value=f"{metrics['perdida_total']:.4f} W/m²"
            )
        
        # Calculadora de ángulo
        st.markdown("### 🧮 Calculadora de Ángulo")
        target_intensity = st.number_input(
            "Intensidad deseada (W/m²)",
            min_value=0.0,
            max_value=float(I0),
            value=float(I0/2),
            step=0.1
        )
        
        if target_intensity > 0:
            try:
                required_angle = calculate_transmission_angle(target_intensity, I0)
                st.info(f"**Ángulo requerido:** {required_angle:.1f}°")
            except ValueError as e:
                st.error(str(e))
    
    # Contenido educativo
    st.markdown("---")
    show_educational_content()
    
    # Validación teórica
    st.markdown("---")
    st.markdown("### 🔍 Validación Teórica")
    
    col_val1, col_val2 = st.columns(2)
    
    with col_val1:
        st.markdown("**Datos de Referencia (Ángulos comunes)**")
        reference_data = {
            0: I0,
            30: I0 * (np.cos(np.radians(30)) ** 2),
            45: I0 * (np.cos(np.radians(45)) ** 2),
            60: I0 * (np.cos(np.radians(60)) ** 2),
            90: 0.0
        }
        
        reference_df = pd.DataFrame.from_dict(
            reference_data, 
            orient='index',
            columns=['Intensidad Teórica (W/m²)']
        )
        reference_df.index.name = 'Ángulo (°)'
        st.dataframe(reference_df)
    
    with col_val2:
        st.markdown("**Comparación con Configuración Actual**")
        if angles:
            current_result = simulator.malus_law(angles[0])
            theoretical = I0 * (np.cos(np.radians(angles[0])) ** 2)
            error = abs(current_result - theoretical)
            
            st.metric("Resultado Simulado", f"{current_result:.4f} W/m²")
            st.metric("Valor Teórico Esperado", f"{theoretical:.4f} W/m²")
            st.metric("Error Absoluto", f"{error:.6f} W/m²")

    # Información técnica
    with st.expander("📋 Información Técnica del Simulador"):
        st.markdown("""
        **Especificaciones técnicas:**
        - Precisión numérica: 64-bit floating point
        - Rango de ángulos: 0° - 180°
        - Resolución angular: 0.1°
        - Validación: Comparación con solución analítica
        - Algoritmo: Implementación directa de Ley de Malus
        
        **Límites físicos:**
        - Intensidad no puede ser negativa
        - Intensidad transmitida ≤ Intensidad incidente
        - Conservación de energía verificada
        """)

if __name__ == "__main__":
    main()

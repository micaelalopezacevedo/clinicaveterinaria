"""
título: página de análisis
fecha: 11.11.2025
descripción: dashboard con estadísticas y reportes de la clínica.
Muestra: estadísticas generales, carga de veterinarios, 
mascotas por especie, próximas citas y análisis varios.
"""

import streamlit as st
from src.analisis import *

def mostrar_estadisticas_generales():
    """
    Muestra estadísticas generales en columnas
    - Total clientes, mascotas, veterinarios, citas, citas pendientes
    - Usa st.metric() para visualización
    """

def mostrar_carga_veterinarios():
    """
    Muestra carga de trabajo de veterinarios
    - Tabla con: veterinario, número de citas
    - Gráfico de barras
    """

def mostrar_mascotas_por_especie():
    """
    Muestra mascotas agrupadas por especie
    - Tabla con: especie, cantidad
    - Gráfico de pastel
    """

def mostrar_proximas_citas():
    """
    Muestra próximas citas (hoy, semana, mes)
    - Tabs para cada período
    - Tablas con detalles de citas
    """

def mostrar_veterinario_mas_ocupado():
    """
    Muestra veterinario con más citas
    """

def mostrar_especie_mas_comun():
    """
    Muestra especie de mascota más frecuente
    """

def main():
    """
    Función principal que muestra dashboard completo
    """

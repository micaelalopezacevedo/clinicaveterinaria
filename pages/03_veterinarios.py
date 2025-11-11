"""
título: página de veterinarios
fecha: 11.11.2025
descripción: interfaz Streamlit para gestión completa de personal.
Registrar, listar, ver carga de trabajo y eliminar veterinarios.
Cubre requisitos RF9-RF12.
"""

import streamlit as st
from src.veterinarios import *

def tab_registrar_veterinario():
    """
    Tab: Formulario para registrar nuevo veterinario
    - Input: nombre, dni, cargo, especialidad, telefono, email
    - Botón: Registrar
    - Output: Mensaje de éxito o error
    """

def tab_lista_veterinarios():
    """
    Tab: Mostrar lista de todos los veterinarios
    - Muestra tabla/lista con: ID, nombre, cargo, especialidad, teléfono
    - Filtro por cargo/especialidad (opcional)
    - Para cada veterinario: botón ver detalles, eliminar, ver citas
    """

def tab_carga_trabajo():
    """
    Tab: Mostrar carga de trabajo de veterinarios
    - Tabla con: veterinario, número de citas, citas próximas
    - Gráfico de barras con carga de trabajo
    """

def tab_eliminar_veterinario():
    """
    Tab: Eliminar veterinario
    - Input: ID del veterinario
    - Confirmación
    - Output: Mensaje de éxito o error
    """

def main():
    """
    Función principal que organiza los tabs
    """

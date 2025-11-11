"""
título: página de citas
fecha: 11.11.2025
descripción: interfaz Streamlit para gestión completa de citas veterinarias.
Crear, listar, ver próximas, editar, marcar realizada y cancelar.
Cubre requisitos RF13-RF16.
"""

import streamlit as st
from src.citas import *
from src.mascotas import listar_mascotas
from src.veterinarios import listar_veterinarios
from datetime import datetime

def tab_crear_cita():
    """
    Tab: Formulario para crear nueva cita
    - Seleccionar mascota (dropdown)
    - Seleccionar veterinario (dropdown)
    - Input: fecha, hora, motivo
    - Botón: Crear cita
    - Output: Mensaje de éxito o error
    """

def tab_lista_citas():
    """
    Tab: Mostrar lista de todas las citas
    - Tabla con: ID, fecha, hora, mascota, cliente, veterinario, motivo, estado
    - Filtros: por fecha, veterinario, mascota, estado
    - Para cada cita: botón detalles, editar, cancelar, marcar realizada
    """

def tab_proximas_citas():
    """
    Tab: Ver próximas citas
    - Mostrar citas de hoy/semana/mes
    - Ordenadas por fecha y hora
    - Tabla con información relevante
    """

def tab_editar_cita():
    """
    Tab: Editar cita existente
    - Input: ID de cita
    - Mostrar datos actuales
    - Permitir modificar: fecha, hora, motivo
    - Botón: Guardar cambios
    """

def tab_marcar_realizada():
    """
    Tab: Marcar cita como realizada
    - Input: ID de cita
    - Input: diagnóstico/notas
    - Botón: Guardar
    - Output: Confirmación
    """

def tab_cancelar_cita():
    """
    Tab: Cancelar cita
    - Input: ID de cita
    - Confirmación
    - Output: Mensaje de éxito
    """

def main():
    """
    Función principal que organiza los tabs
    """

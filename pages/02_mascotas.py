"""
título: página de mascotas
fecha: 11.11.2025
descripción: interfaz Streamlit para gestión completa de mascotas.
Registrar, listar, ver historial y editar mascotas.
Cubre requisitos RF5-RF8.
"""

import streamlit as st
from src.mascotas import *
from src.clientes import listar_clientes

def tab_registrar_mascota():
    """
    Tab: Formulario para registrar nueva mascota
    - Seleccionar cliente (dropdown)
    - Input: nombre, especie, raza, edad, peso, sexo
    - Botón: Registrar
    - Output: Mensaje de éxito o error
    """

def tab_lista_mascotas():
    """
    Tab: Mostrar lista de todas las mascotas
    - Muestra tabla/lista con: ID, nombre, especie, raza, cliente, edad
    - Filtro por cliente (opcional)
    - Para cada mascota: botón ver detalles, editar, eliminar, historial
    """

def tab_ver_historial():
    """
    Tab: Ver historial de citas de una mascota
    - Input: ID de mascota o seleccionar de lista
    - Output: Listado de citas (fecha, hora, motivo, veterinario, estado)
    """

def tab_editar_mascota():
    """
    Tab: Editar datos de mascota existente
    - Input: ID de mascota
    - Mostrar datos actuales
    - Permitir modificar: nombre, raza, edad, peso, sexo
    - Botón: Guardar cambios
    """

def main():
    """
    Función principal que organiza los tabs
    """

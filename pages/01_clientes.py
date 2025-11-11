"""
título: página de clientes
fecha: 11.11.2025
descripción: interfaz Streamlit para gestión completa de clientes.
Registrar, listar, buscar y editar clientes.
Cubre requisitos RF1-RF4.
"""

import streamlit as st
from src.clientes import *
from src.mascotas import obtener_mascotas_por_cliente

def tab_registrar_cliente():
    """
    Tab: Formulario para registrar nuevo cliente
    - Input: nombre, dni, telefono, email
    - Botón: Registrar
    - Output: Mensaje de éxito o error
    """

def tab_lista_clientes():
    """
    Tab: Mostrar lista de todos los clientes
    - Muestra tabla/lista con: ID, nombre, DNI, teléfono
    - Para cada cliente: botón para ver detalles, editar, eliminar
    - Mostrar mascotas asociadas
    """

def tab_buscar_cliente():
    """
    Tab: Buscar cliente por nombre o DNI
    - Input: nombre o DNI
    - Botón: Buscar
    - Output: Resultados encontrados
    """

def tab_editar_cliente():
    """
    Tab: Editar datos de cliente existente
    - Input: ID del cliente
    - Mostrar datos actuales
    - Permitir modificar: nombre, teléfono, email
    - Botón: Guardar cambios
    """

def main():
    """
    Función principal que organiza los tabs y ejecuta la interfaz
    """

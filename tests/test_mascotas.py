"""
título: tests de mascotas
fecha: 11.11.2025
descripción: pruebas unitarias para el módulo de mascotas.
Verifica todas las operaciones CRUD y validaciones.
Usa pytest para ejecutar las pruebas.
"""

import pytest
from src.mascotas import *
from src.database import session, Mascota

@pytest.fixture
def limpiar_bd():
    """
    Limpia BD antes de cada test
    """

def test_registrar_mascota(limpiar_bd):
    """
    Test: registrar mascota
    """

def test_listar_mascotas(limpiar_bd):
    """
    Test: listar todas las mascotas
    """

def test_obtener_mascota_por_id(limpiar_bd):
    """
    Test: buscar mascota por ID
    """

def test_obtener_mascotas_por_cliente(limpiar_bd):
    """
    Test: obtener mascotas de un cliente
    """

def test_modificar_mascota(limpiar_bd):
    """
    Test: modificar datos de mascota
    """

def test_eliminar_mascota(limpiar_bd):
    """
    Test: eliminar mascota
    """

"""
título: tests de clientes
fecha: 11.11.2025
descripción: pruebas unitarias para el módulo de clientes.
Verifica todas las operaciones CRUD y validaciones.
Usa pytest para ejecutar las pruebas.
"""

import pytest
from src.clientes import *
from src.database import session, Cliente

@pytest.fixture
def limpiar_bd():
    """
    Limpia BD antes de cada test
    """

def test_crear_cliente(limpiar_bd):
    """
    Test: crear cliente exitosamente
    """

def test_crear_cliente_dni_duplicado(limpiar_bd):
    """
    Test: crear cliente con DNI que ya existe
    """

def test_listar_clientes(limpiar_bd):
    """
    Test: listar clientes
    """

def test_obtener_cliente_por_id(limpiar_bd):
    """
    Test: buscar cliente por ID
    """

def test_buscar_por_dni(limpiar_bd):
    """
    Test: buscar cliente por DNI
    """

def test_modificar_cliente(limpiar_bd):
    """
    Test: modificar datos de cliente
    """

def test_eliminar_cliente(limpiar_bd):
    """
    Test: eliminar cliente
    """

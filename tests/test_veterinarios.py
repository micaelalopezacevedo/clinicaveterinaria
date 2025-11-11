"""
título: tests de veterinarios
fecha: 11.11.2025
descripción: pruebas unitarias para el módulo de veterinarios.
Verifica registro, consulta, eliminación y análisis de carga de trabajo.
Usa pytest para ejecutar las pruebas.
"""

import pytest
from src.veterinarios import *
from src.database import session, Veterinario

@pytest.fixture
def limpiar_bd():
    """
    Limpia BD antes de cada test
    """

def test_registrar_veterinario(limpiar_bd):
    """
    Test: registrar veterinario exitosamente
    """

def test_registrar_veterinario_dni_duplicado(limpiar_bd):
    """
    Test: registrar veterinario con DNI que ya existe
    """

def test_listar_veterinarios(limpiar_bd):
    """
    Test: listar todos los veterinarios
    """

def test_obtener_veterinario_por_id(limpiar_bd):
    """
    Test: buscar veterinario por ID
    """

def test_obtener_veterinarios_por_especialidad(limpiar_bd):
    """
    Test: buscar veterinarios por especialidad
    """

def test_obtener_carga_veterinario(limpiar_bd):
    """
    Test: obtener carga de trabajo de un veterinario
    """

def test_eliminar_veterinario(limpiar_bd):
    """
    Test: eliminar veterinario
    """

def test_contar_veterinarios(limpiar_bd):
    """
    Test: contar total de veterinarios
    """

def test_veterinario_existe(limpiar_bd):
    """
    Test: verificar si existe veterinario
    """

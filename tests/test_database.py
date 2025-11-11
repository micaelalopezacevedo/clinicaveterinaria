"""
título: tests de base de datos
fecha: 11.11.2025
descrición: pruebas unitarias para la capa de base de datos.
Verifica la creación de modelos, relaciones y conexión a SQLite.
Usa pytest para ejecutar las pruebas.
"""

import pytest
from src.database import session, Base, engine, Cliente, Mascota, Veterinario, Cita
from sqlalchemy import inspect

@pytest.fixture
def limpiar_bd():
    """
    Limpia todas las tablas antes de cada test
    """

class TestModelos:
    """Pruebas para los modelos (tablas)"""
    
    def test_tabla_clientes_existe(self):
        """
        Test: verificar que tabla clientes existe
        """
    
    def test_tabla_mascotas_existe(self):
        """
        Test: verificar que tabla mascotas existe
        """
    
    def test_tabla_veterinarios_existe(self):
        """
        Test: verificar que tabla veterinarios existe
        """
    
    def test_tabla_citas_existe(self):
        """
        Test: verificar que tabla citas existe
        """


class TestColumnas:
    """Pruebas para las columnas de los modelos"""
    
    def test_cliente_tiene_columnas_requeridas(self):
        """
        Test: verificar que Cliente tiene todas las columnas necesarias
        (id, nombre, dni, telefono, email)
        """
    
    def test_mascota_tiene_columnas_requeridas(self):
        """
        Test: verificar que Mascota tiene todas las columnas necesarias
        (id, nombre, especie, raza, edad, peso, sexo, cliente_id)
        """
    
    def test_veterinario_tiene_columnas_requeridas(self):
        """
        Test: verificar que Veterinario tiene todas las columnas necesarias
        (id, nombre, dni, cargo, especialidad, telefono, email)
        """
    
    def test_cita_tiene_columnas_requeridas(self):
        """
        Test: verificar que Cita tiene todas las columnas necesarias
        (id, fecha, hora, motivo, diagnostico, estado, mascota_id, veterinario_id)
        """


class TestRelaciones:
    """Pruebas para las relaciones entre modelos"""
    
    def test_cliente_tiene_relacion_mascotas(self):
        """
        Test: verificar que Cliente tiene relación con Mascotas
        """
    
    def test_mascota_tiene_relacion_cliente(self):
        """
        Test: verificar que Mascota tiene relación con Cliente
        """
    
    def test_mascota_tiene_relacion_citas(self):
        """
        Test: verificar que Mascota tiene relación con Citas
        """
    
    def test_veterinario_tiene_relacion_citas(self):
        """
        Test: verificar que Veterinario tiene relación con Citas
        """


class TestRestricciones:
    """Pruebas para restricciones de BD"""
    
    def test_cliente_dni_unico(self):
        """
        Test: verificar que DNI de cliente es único (no puede repetirse)
        """
    
    def test_veterinario_dni_unico(self):
        """
        Test: verificar que DNI de veterinario es único
        """
    
    def test_cliente_nombre_no_vacio(self):
        """
        Test: verificar que nombre de cliente no puede estar vacío
        """
    
    def test_mascota_nombre_no_vacio(self):
        """
        Test: verificar que nombre de mascota no puede estar vacío
        """

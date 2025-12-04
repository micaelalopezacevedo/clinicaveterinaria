"""
título: tests de clientes (TDD)
fecha: 11.11.2025
descripción: pruebas unitarias para el módulo de clientes.
Verifica comportamiento esperado en CRUD, validaciones y duplicados.
"""

import pytest
from src.clientes import (
    crear_cliente,
    listar_clientes,
    obtener_cliente_por_id,
    buscar_cliente_por_dni,
    buscar_cliente_por_nombre,
    modificar_cliente,
    eliminar_cliente,
    contar_clientes
)
from src.database import session, Cliente
from src.exceptions import (
    ClienteNoEncontradoException,
    DNIDuplicadoException,
    ValidacionException
)

# ===========================================================
# FIXTURE: LIMPIAR BD (GIVEN)
# ===========================================================

@pytest.fixture
def limpiar_bd():
    session.query(Cliente).delete()
    session.commit()
    yield
    session.query(Cliente).delete()
    session.commit()


# ===========================================================
# CREACIÓN DE CLIENTES (TDD)
# ===========================================================

def test_cuando_creo_un_cliente_entonces_se_guarda(limpiar_bd):
    # WHEN
    cliente = crear_cliente("Mica", "123A")

    # THEN
    assert cliente.nombre == "Mica"
    assert cliente.dni == "123A"
    assert contar_clientes() == 1


def test_no_puedo_crear_cliente_sin_campos_obligatorios(limpiar_bd):
    # WHEN + THEN
    with pytest.raises(ValidacionException):
        crear_cliente("", "")


def test_no_puedo_crear_cliente_con_dni_duplicado(limpiar_bd):
    # GIVEN
    crear_cliente("Mica", "123A")

    # WHEN + THEN
    with pytest.raises(DNIDuplicadoException):
        crear_cliente("Alex", "123A")


# ===========================================================
# LISTAR / BUSCAR
# ===========================================================

def test_listar_clientes_devuelve_todos(limpiar_bd):
    # GIVEN
    crear_cliente("Mica", "1A")
    crear_cliente("Ana", "2A")

    # WHEN
    clientes = listar_clientes()

    # THEN
    assert len(clientes) == 2


def test_buscar_por_dni_devuelve_el_cliente_correcto(limpiar_bd):
    # GIVEN
    crear_cliente("Mica", "123A")

    # WHEN
    c = buscar_cliente_por_dni("123A")

    # THEN
    assert c.nombre == "Mica"


def test_buscar_por_nombre_devuelve_coincidencias(limpiar_bd):
    # GIVEN
    crear_cliente("Mica López", "1A")
    crear_cliente("Micaela Ruiz", "2A")

    # WHEN
    resultados = buscar_cliente_por_nombre("Mica")

    # THEN
    assert len(resultados) == 2


# ===========================================================
# OBTENER POR ID
# ===========================================================

def test_puedo_obtener_cliente_por_id(limpiar_bd):
    # GIVEN
    c = crear_cliente("Mica", "1A")

    # WHEN
    encontrado = obtener_cliente_por_id(c.id)

    # THEN
    assert encontrado.id == c.id


def test_no_puedo_obtener_cliente_inexistente(limpiar_bd):
    # WHEN + THEN
    with pytest.raises(ClienteNoEncontradoException):
        obtener_cliente_por_id(999)


# ===========================================================
# MODIFICAR CLIENTE
# ===========================================================

def test_modificar_cliente_actualiza_datos(limpiar_bd):
    # GIVEN
    c = crear_cliente("Mica", "123A")

    # WHEN
    mod = modificar_cliente(c.id, nombre="Nuevo")

    # THEN
    assert mod.nombre == "Nuevo"


def test_no_puedo_modificar_cliente_con_nombre_vacio(limpiar_bd):
    # GIVEN
    c = crear_cliente("Mica", "123A")

    # WHEN + THEN
    with pytest.raises(ValidacionException):
        modificar_cliente(c.id, nombre="")


# ===========================================================
# ELIMINAR CLIENTE
# ===========================================================

def test_eliminar_cliente_lo_quita_de_la_bd(limpiar_bd):
    # GIVEN
    c = crear_cliente("Mica", "1A")

    # WHEN
    eliminar_cliente(c.id)

    # THEN
    assert contar_clientes() == 0


def test_no_puedo_eliminar_cliente_inexistente(limpiar_bd):
    # WHEN + THEN
        with pytest.raises(ClienteNoEncontradoException):
            eliminar_cliente(999)
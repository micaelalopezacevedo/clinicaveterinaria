"""
título: tests de mascotas
fecha: 11.11.2025
descripción: pruebas unitarias para el módulo de mascotas.
Verifica todas las operaciones CRUD y validaciones.
Usa pytest para ejecutar las pruebas.
"""

import pytest
from src.mascotas import (
    registrar_mascota, listar_mascotas, obtener_mascota_por_id,
    obtener_mascotas_por_cliente, modificar_mascota,
    eliminar_mascota, contar_mascotas
)
from src.database import session, Mascota, Cliente
from src.exceptions import MascotaNoEncontradaException, ClienteNoEncontradoException, ValidacionException


# =======================================================
# FIXTURE: LIMPIAR BD ANTES DE CADA TEST
# =======================================================

@pytest.fixture
def limpiar_bd():
    """Deja la base de datos totalmente limpia antes de cada test"""
    session.query(Mascota).delete()
    session.query(Cliente).delete()
    session.commit()
    yield
    # Limpieza después también (por si un test falla)
    session.query(Mascota).delete()
    session.query(Cliente).delete()
    session.commit()


# =======================================================
# HELPERS
# =======================================================

def crear_cliente(nombre="Mica", dni="000A"):
    cliente = Cliente(nombre=nombre, dni=dni)
    session.add(cliente)
    session.commit()
    return cliente


# =======================================================
# TEST: REGISTRAR MASCOTA
# =======================================================

def test_registrar_mascota(limpiar_bd):
    cliente = crear_cliente()

    mascota = registrar_mascota(
        nombre="Luna",
        especie="Perro",
        cliente_id=cliente.id
    )

    assert mascota.id is not None
    assert mascota.nombre == "Luna"
    assert mascota.especie == "Perro"
    assert mascota.cliente_id == cliente.id


def test_registrar_mascota_sin_campos_obligatorios(limpiar_bd):
    cliente = crear_cliente()

    with pytest.raises(ValidacionException):
        registrar_mascota(
            nombre="",
            especie="Perro",
            cliente_id=cliente.id
        )


def test_registrar_mascota_cliente_no_existe(limpiar_bd):
    with pytest.raises(ClienteNoEncontradoException):
        registrar_mascota("Luna", "Perro", cliente_id=999)


# =======================================================
# TEST: LISTAR MASCOTAS
# =======================================================

def test_listar_mascotas(limpiar_bd):
    cliente = crear_cliente()

    registrar_mascota("Luna", "Perro", cliente.id)
    registrar_mascota("Michi", "Gato", cliente.id)

    mascotas = listar_mascotas()

    assert len(mascotas) == 2
    assert sorted([m.nombre for m in mascotas]) == ["Luna", "Michi"]


# =======================================================
# TEST: OBTENER MASCOTA POR ID
# =======================================================

def test_obtener_mascota_por_id(limpiar_bd):
    cliente = crear_cliente()
    m = registrar_mascota("Luna", "Perro", cliente.id)

    mascota = obtener_mascota_por_id(m.id)

    assert mascota.id == m.id
    assert mascota.nombre == "Luna"


def test_obtener_mascota_por_id_inexistente(limpiar_bd):
    with pytest.raises(MascotaNoEncontradaException):
        obtener_mascota_por_id(999)


# =======================================================
# TEST: OBTENER MASCOTAS POR CLIENTE
# =======================================================

def test_obtener_mascotas_por_cliente(limpiar_bd):
    cliente = crear_cliente()
    registrar_mascota("Luna", "Perro", cliente.id)
    registrar_mascota("Michi", "Gato", cliente.id)

    mascotas = obtener_mascotas_por_cliente(cliente.id)

    assert len(mascotas) == 2
    assert {m.nombre for m in mascotas} == {"Luna", "Michi"}


# =======================================================
# TEST: MODIFICAR MASCOTA
# =======================================================

def test_modificar_mascota(limpiar_bd):
    cliente = crear_cliente()
    m = registrar_mascota("Luna", "Perro", cliente.id)

    modificada = modificar_mascota(m.id, nombre="Luna Nueva")

    assert modificada.nombre == "Luna Nueva"
    assert modificada.id == m.id


def test_modificar_mascota_inexistente(limpiar_bd):
    with pytest.raises(MascotaNoEncontradaException):
        modificar_mascota(999, nombre="Nuevo")


def test_modificar_mascota_nombre_invalido(limpiar_bd):
    cliente = crear_cliente()
    m = registrar_mascota("Luna", "Perro", cliente.id)

    with pytest.raises(ValidacionException):
        modificar_mascota(m.id, nombre="")


# =======================================================
# TEST: ELIMINAR MASCOTA
# =======================================================

def test_eliminar_mascota(limpiar_bd):
    cliente = crear_cliente()
    m = registrar_mascota("Luna", "Perro", cliente.id)

    assert eliminar_mascota(m.id) == True
    assert contar_mascotas() == 0


def test_eliminar_mascota_inexistente(limpiar_bd):
    with pytest.raises(MascotaNoEncontradaException):
        eliminar_mascota(999)


# =======================================================
# TEST: CONTAR MASCOTAS
# =======================================================

def test_contar_mascotas(limpiar_bd):
    cliente = crear_cliente()
    registrar_mascota("Luna", "Perro", cliente.id)

    assert contar_mascotas() == 1
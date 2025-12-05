import pytest
from src.mascotas import (
    registrar_mascota, listar_mascotas, obtener_mascota_por_id,
    obtener_mascotas_por_cliente, obtener_mascotas_por_especie, # <-- Nueva importación
    modificar_mascota, eliminar_mascota, contar_mascotas,
    ver_historial_mascota # <-- Nueva importación
)
from src.exceptions import MascotaNoEncontradaException, ClienteNoEncontradoException, ValidacionException

# Nota: pytest inyecta automáticamente 'session', 'cliente_default' y 'mascota_default' desde conftest.py

# =======================================================
# TESTS DE REGISTRO (CREATE)
# =======================================================

def test_registrar_mascota(session, cliente_default):
    mascota = registrar_mascota(
        nombre="Luna",
        especie="Perro",
        cliente_id=cliente_default.id,
        raza="Labrador",
        edad=3
    )

    assert mascota.id is not None
    assert mascota.nombre == "Luna"
    assert mascota.especie == "Perro"
    assert mascota.raza == "Labrador"
    assert mascota.edad == 3
    assert mascota.cliente_id == cliente_default.id

def test_registrar_mascota_sin_campos_obligatorios(session, cliente_default):
    with pytest.raises(ValidacionException):
        registrar_mascota(nombre="", especie="Perro", cliente_id=cliente_default.id)

def test_registrar_mascota_cliente_no_existe(session):
    with pytest.raises(ClienteNoEncontradoException):
        registrar_mascota("Luna", "Perro", cliente_id=999)

# =======================================================
# TESTS DE LECTURA (READ)
# =======================================================

def test_listar_mascotas(session, cliente_default):
    registrar_mascota("Luna", "Perro", cliente_default.id)
    registrar_mascota("Michi", "Gato", cliente_default.id)

    mascotas = listar_mascotas()
    assert len(mascotas) == 2
    # Verifica que ordena por nombre según tu Repositorio
    assert [m.nombre for m in mascotas] == ["Luna", "Michi"] 

def test_obtener_mascota_por_id(session, mascota_default):
    mascota = obtener_mascota_por_id(mascota_default.id)
    assert mascota.id == mascota_default.id
    assert mascota.nombre == "Luna"

def test_obtener_mascota_por_id_inexistente(session):
    with pytest.raises(MascotaNoEncontradaException):
        obtener_mascota_por_id(999)

def test_obtener_mascotas_por_cliente(session, cliente_default):
    registrar_mascota("Rex", "Perro", cliente_default.id)
    registrar_mascota("Simba", "Gato", cliente_default.id)

    mascotas = obtener_mascotas_por_cliente(cliente_default.id)
    assert len(mascotas) == 2
    assert {m.nombre for m in mascotas} == {"Rex", "Simba"}

def test_obtener_mascotas_por_especie(session, cliente_default):
    """(NUEVO) Verifica el filtrado por especie."""
    registrar_mascota("Rex", "Perro", cliente_default.id)
    registrar_mascota("Simba", "Gato", cliente_default.id)
    registrar_mascota("Firulais", "Perro", cliente_default.id)

    perros = obtener_mascotas_por_especie("Perro")
    gatos = obtener_mascotas_por_especie("Gato")

    assert len(perros) == 2
    assert len(gatos) == 1
    assert perros[0].especie == "Perro"

def test_ver_historial_mascota_vacio(session, mascota_default):
    """(NUEVO) Verifica que devuelva una lista (vacía al inicio)."""
    # Como aún no creamos Citas en este test, debe devolver lista vacía
    historial = ver_historial_mascota(mascota_default.id)
    assert isinstance(historial, list)
    assert len(historial) == 0

# =======================================================
# TESTS DE MODIFICACIÓN (UPDATE)
# =======================================================

def test_modificar_mascota_nombre(session, mascota_default):
    modificada = modificar_mascota(mascota_default.id, nombre="Luna Nueva")
    assert modificada.nombre == "Luna Nueva"
    assert modificada.id == mascota_default.id

def test_modificar_mascota_campos_opcionales(session, mascota_default):
    """(NUEVO) Verifica que se pueden actualizar raza, peso, edad, sexo."""
    modificada = modificar_mascota(
        mascota_default.id,
        raza="Mestizo",
        edad=10,
        peso=15.5,
        sexo="Hembra"
    )
    
    assert modificada.raza == "Mestizo"
    assert modificada.edad == 10
    assert modificada.peso == 15.5
    assert modificada.sexo == "Hembra"
    # El nombre no debió cambiar
    assert modificada.nombre == "Luna"

def test_modificar_mascota_inexistente(session):
    with pytest.raises(MascotaNoEncontradaException):
        modificar_mascota(999, nombre="Nuevo")

def test_modificar_mascota_nombre_invalido(session, mascota_default):
    with pytest.raises(ValidacionException):
        modificar_mascota(mascota_default.id, nombre="")

# =======================================================
# TESTS DE ELIMINACIÓN (DELETE) Y CONTEO
# =======================================================

def test_eliminar_mascota(session, mascota_default):
    assert eliminar_mascota(mascota_default.id) is True
    assert contar_mascotas() == 0

def test_eliminar_mascota_inexistente(session):
    with pytest.raises(MascotaNoEncontradaException):
        eliminar_mascota(999)

def test_contar_mascotas(session, mascota_default):
    assert contar_mascotas() == 1
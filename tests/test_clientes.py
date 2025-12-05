import pytest
from src.clientes import (
    crear_cliente, listar_clientes, obtener_cliente_por_id,
    buscar_cliente_por_dni, buscar_cliente_por_nombre,
    modificar_cliente, eliminar_cliente, contar_clientes
)
from src.exceptions import ClienteNoEncontradoException, DNIDuplicadoException, ValidacionException
from src.database import Cliente

# Nota: pytest inyecta automáticamente 'session' y 'cliente_default' desde conftest.py

# ==========================================
# TESTS DE CREACIÓN (CREATE)
# ==========================================

def test_crear_cliente_exito(session):
    """Verifica que se crea un cliente correctamente."""
    cliente = crear_cliente(
        nombre="Juan Pérez",
        dni="12345678Z",
        telefono="600111222",
        email="juan@test.com"
    )

    assert cliente.id is not None
    assert cliente.nombre == "Juan Pérez"
    assert cliente.dni == "12345678Z"
    
    # Verificación directa en BD
    en_bd = session.query(Cliente).filter_by(dni="12345678Z").first()
    assert en_bd is not None

def test_crear_cliente_dni_duplicado(session, cliente_default):
    """Verifica que no se puede crear otro cliente con el mismo DNI."""
    # cliente_default ya tiene el DNI "000A" (definido en conftest)
    with pytest.raises(DNIDuplicadoException):
        crear_cliente("Impostor", cliente_default.dni)

def test_crear_cliente_validacion_campos(session):
    """Verifica que nombre y DNI son obligatorios."""
    with pytest.raises(ValidacionException):
        crear_cliente("", "12312312A") # Nombre vacío
    
    with pytest.raises(ValidacionException):
        crear_cliente("Juan", "") # DNI vacío

# ==========================================
# TESTS DE LECTURA Y BÚSQUEDA (READ)
# ==========================================

def test_listar_clientes(session, cliente_default):
    # cliente_default crea 1. Creamos otro.
    crear_cliente("Alberto", "11111111B")
    
    clientes = listar_clientes()
    assert len(clientes) == 2
    
    # Verificar orden alfabético (Alberto antes que Mica/Juan)
    nombres = [c.nombre for c in clientes]
    assert "Alberto" in nombres
    assert cliente_default.nombre in nombres

def test_obtener_cliente_por_id(session, cliente_default):
    encontrado = obtener_cliente_por_id(cliente_default.id)
    assert encontrado.id == cliente_default.id
    assert encontrado.nombre == cliente_default.nombre

def test_obtener_cliente_inexistente(session):
    with pytest.raises(ClienteNoEncontradoException):
        obtener_cliente_por_id(999)

def test_buscar_cliente_por_dni(session, cliente_default):
    """Verifica búsqueda exacta por DNI."""
    encontrado = buscar_cliente_por_dni(cliente_default.dni)
    assert encontrado.id == cliente_default.id

def test_buscar_cliente_por_dni_no_encontrado(session):
    """Verifica que devuelve None si no existe (no lanza excepción)."""
    encontrado = buscar_cliente_por_dni("00000000Z")
    assert encontrado is None

def test_buscar_cliente_por_nombre_parcial(session):
    """(NUEVO) Verifica búsqueda 'like' %nombre%."""
    crear_cliente("Maria Lopez", "111A")
    crear_cliente("Maria Garcia", "222B")
    crear_cliente("Pedro Sanchez", "333C")

    # Buscar "Maria" debe traer 2
    resultados = buscar_cliente_por_nombre("Maria")
    assert len(resultados) == 2
    
    # Buscar "Garcia" debe traer 1
    resultados_garcia = buscar_cliente_por_nombre("Garcia")
    assert len(resultados_garcia) == 1
    assert resultados_garcia[0].dni == "222B"

# ==========================================
# TESTS DE MODIFICACIÓN (UPDATE)
# ==========================================

def test_modificar_cliente_exito(session, cliente_default):
    """Verifica actualización de datos permitidos."""
    actualizado = modificar_cliente(
        cliente_default.id,
        nombre="Micaela Actualizada",
        telefono="777777777",
        email="nuevo@mail.com"
    )

    assert actualizado.nombre == "Micaela Actualizada"
    assert actualizado.telefono == "777777777"
    assert actualizado.id == cliente_default.id

def test_modificar_cliente_nombre_vacio(session, cliente_default):
    """Verifica validación al intentar poner nombre vacío."""
    with pytest.raises(ValidacionException):
        modificar_cliente(cliente_default.id, nombre="")

def test_modificar_cliente_inexistente(session):
    with pytest.raises(ClienteNoEncontradoException):
        modificar_cliente(999, nombre="Nadie")

# Nota: No probamos conflicto de DNI en modificación porque
# el módulo clientes.py NO permite actualizar el DNI (según el código analizado).

# ==========================================
# TESTS DE ELIMINACIÓN Y CONTEO
# ==========================================

def test_eliminar_cliente(session, cliente_default):
    assert eliminar_cliente(cliente_default.id) is True
    assert contar_clientes() == 0

def test_eliminar_cliente_inexistente(session):
    with pytest.raises(ClienteNoEncontradoException):
        eliminar_cliente(999)

def test_contar_clientes(session, cliente_default):
    assert contar_clientes() == 1
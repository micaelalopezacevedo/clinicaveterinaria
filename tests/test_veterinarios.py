# test_veterinarios.py
import pytest
from src.veterinarios import *
from src.exceptions import DNIDuplicadoException, VeterinarioNoEncontradoException, ValidacionException
from src.database import Veterinario

# ==========================================
# TESTS DE CREACIÓN
# ==========================================

def test_registrar_veterinario_exito(session):
    """Verifica que se crea un veterinario correctamente en la BD."""
    # Act
    vet = crear_veterinario("Ana García", "12345678A", "Cirujana", "Cirugía", "600", "a@a.com")
    
    # Assert
    assert vet.id is not None
    assert vet.nombre == "Ana García"
    
    # Verificación extra: Consultar directamete a la BD para asegurar persistencia
    en_bd = session.query(Veterinario).filter_by(dni="12345678A").first()
    assert en_bd is not None

def test_registrar_veterinario_dni_duplicado(session):
    """Verifica que NO se pueden crear dos veterinarios con el mismo DNI."""
    # Arrange
    crear_veterinario("Ana García", "11111111X")
    
    # Act & Assert
    with pytest.raises(DNIDuplicadoException):
        crear_veterinario("Pedro Lopez", "11111111X") # Mismo DNI

def test_registrar_veterinario_campos_vacios(session):
    """(NUEVO) Verifica validaciones de campos obligatorios."""
    with pytest.raises(ValidacionException):
        crear_veterinario("", "12345678Z") # Nombre vacío
    
    with pytest.raises(ValidacionException):
        crear_veterinario("Juan", "") # DNI vacío

# ==========================================
# TESTS DE LECTURA
# ==========================================

def test_listar_veterinarios(session):
    """Verifica que se listan todos los registros."""
    crear_veterinario("Ana", "111A")
    crear_veterinario("Beto", "222B")
    
    lista = listar_veterinarios()
    assert len(lista) == 2

def test_obtener_veterinario_por_id_y_dni(session):
    """Verifica búsquedas por ID y por DNI."""
    vet_creado = crear_veterinario("Carlos", "333C")
    
    # Por ID
    encontrado_id = obtener_veterinario_por_id(vet_creado.id)
    assert encontrado_id.nombre == "Carlos"
    
    # Por DNI (NUEVO TEST IMPORTANTE)
    encontrado_dni = buscar_veterinario_por_dni("333C")
    assert encontrado_dni.id == vet_creado.id

def test_obtener_no_existente_lanza_excepcion(session):
    """Verifica que buscar un ID que no existe lanza error."""
    with pytest.raises(VeterinarioNoEncontradoException):
        obtener_veterinario_por_id(99999)

def test_obtener_veterinarios_por_especialidad(session):
    """Verifica el filtro por especialidad."""
    crear_veterinario("V1", "111", especialidad="Cirugía")
    crear_veterinario("V2", "222", especialidad="Dermatología")
    
    cirujanos = obtener_veterinarios_por_especialidad("Cirugía")
    assert len(cirujanos) == 1
    assert cirujanos[0].dni == "111"

# ==========================================
# TESTS DE MODIFICACIÓN (LOS QUE FALTABAN)
# ==========================================

def test_modificar_veterinario_exito(session):
    """(NUEVO) Verifica que se pueden actualizar datos."""
    vet = crear_veterinario("Eduardo", "555E", cargo="Junior")
    
    # Modificamos cargo y nombre
    vet_upd = modificar_veterinario(vet.id, nombre="Eduardo Pro", cargo="Senior")
    
    assert vet_upd.cargo == "Senior"
    assert vet_upd.nombre == "Eduardo Pro"
    # El DNI no debería haber cambiado
    assert vet_upd.dni == "555E"

def test_modificar_veterinario_conflicto_dni(session):
    """(NUEVO) Verifica que no puedes cambiar tu DNI al de otro usuario existente."""
    v1 = crear_veterinario("Vet 1", "DNI1")
    v2 = crear_veterinario("Vet 2", "DNI2")
    
    # Intentamos cambiar el DNI de v1 para que sea igual al de v2
    with pytest.raises(DNIDuplicadoException):
        modificar_veterinario(v1.id, dni="DNI2")

# ==========================================
# TESTS DE ELIMINACIÓN Y UTILIDADES
# ==========================================

def test_eliminar_veterinario(session):
    """Verifica la eliminación correcta."""
    vet = crear_veterinario("Felipe", "666F")
    
    resultado = eliminar_veterinario(vet.id)
    assert resultado is True
    
    # Verificar que ya no existe
    assert veterinario_existe(vet.id) is False

def test_contar_veterinarios(session):
    """Verifica el conteo total."""
    assert contar_veterinarios() == 0
    crear_veterinario("Gabi", "777G")
    assert contar_veterinarios() == 1
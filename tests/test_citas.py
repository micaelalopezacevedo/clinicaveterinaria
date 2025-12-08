import pytest
from datetime import date, timedelta, time
from sqlalchemy.exc import IntegrityError
from src.citas import *
from src.database import Cita, Veterinario, Mascota, Cliente
from src.exceptions import CitaNoEncontradaException, ValidacionException

# ==========================================
# FIXTURE: DATOS BASE
# ==========================================

@pytest.fixture
def datos_base(session):
    # Crear Veterinario
    vet = Veterinario(nombre="Dr. Test", dni="111V", especialidad="General", email="vet@test.com")
    session.add(vet)
    
    # Crear Cliente
    cliente = Cliente(nombre="Juan Dueño", dni="222C", telefono="600000000", email="juan@test.com")
    session.add(cliente)
    session.flush()
    
    # Crear Mascota
    mascota = Mascota(nombre="Firulais", especie="Perro", raza="Mestizo", edad=5, cliente_id=cliente.id)
    session.add(mascota)
    session.commit()
    
    return {
        "vet_id": vet.id,
        "cliente_id": cliente.id,
        "mascota_id": mascota.id,
        "mascota_obj": mascota 
    }

# ==========================================
# 1. TESTS DE CREACIÓN
# ==========================================

def test_crear_cita_exito(session, datos_base):
    # Usamos mañana a las 10:00 (siempre futuro)
    manana = date.today() + timedelta(days=1)
    cita = crear_cita(
        mascota_id=datos_base["mascota_id"], 
        veterinario_id=datos_base["vet_id"], 
        fecha=manana, 
        hora=time(10, 0), 
        motivo="Vacunación"
    )
    assert cita.id is not None
    assert cita.estado == "Pendiente"

def test_crear_cita_fecha_pasada_error(session, datos_base):
    ayer = date.today() - timedelta(days=1)
    with pytest.raises(ValidacionException):
        crear_cita(datos_base["mascota_id"], datos_base["vet_id"], ayer, time(10, 0), "Fallo")

def test_crear_cita_entidades_no_existentes(session):
    manana = date.today() + timedelta(days=1)
    with pytest.raises((IntegrityError, ValidacionException)):
        crear_cita(999, 999, manana, time(9, 0), "Fallo") 

# ==========================================
# 2. TESTS DE LECTURA
# ==========================================

def test_listar_citas(session, datos_base):
    manana = date.today() + timedelta(days=1)
    crear_cita(datos_base["mascota_id"], datos_base["vet_id"], manana, time(10,0), "Cita 1")
    crear_cita(datos_base["mascota_id"], datos_base["vet_id"], manana, time(11,0), "Cita 2")
    assert len(listar_citas()) == 2

def test_obtener_cita_por_id(session, datos_base):
    manana = date.today() + timedelta(days=1)
    cita_creada = crear_cita(datos_base["mascota_id"], datos_base["vet_id"], manana, time(10,0), "Test ID")
    encontrada = obtener_cita_por_id(cita_creada.id)
    assert encontrada.motivo == "Test ID"
    
    with pytest.raises(CitaNoEncontradaException):
        obtener_cita_por_id(99999)

def test_obtener_citas_por_fecha(session, datos_base):
    dia_1 = date.today() + timedelta(days=1)
    dia_2 = date.today() + timedelta(days=2)
    
    crear_cita(datos_base["mascota_id"], datos_base["vet_id"], dia_1, time(10,0), "Cita Dia 1")
    crear_cita(datos_base["mascota_id"], datos_base["vet_id"], dia_2, time(10,0), "Cita Dia 2")
    
    resultados = obtener_citas_por_fecha(dia_1)
    assert len(resultados) == 1
    assert resultados[0].motivo == "Cita Dia 1"

def test_obtener_citas_por_mascota(session, datos_base):
    # Crear otra mascota para probar filtros
    otra_mascota = Mascota(nombre="Gato", especie="Gato", cliente_id=datos_base["cliente_id"])
    session.add(otra_mascota)
    session.commit()
    
    manana = date.today() + timedelta(days=1)
    
    # Cita 1: Perro a las 10:00
    crear_cita(datos_base["mascota_id"], datos_base["vet_id"], manana, time(10,0), "Perro")
    
    # Cita 2: Gato a las 11:00 (Importante: hora diferente para no chocar horario vet)
    crear_cita(otra_mascota.id, datos_base["vet_id"], manana, time(11,0), "Gato")
    
    citas_perro = obtener_citas_por_mascota(datos_base["mascota_id"])
    assert len(citas_perro) == 1
    assert citas_perro[0].motivo == "Perro"

# ==========================================
# 3. TESTS DE LÓGICA Y ESTADOS
# ==========================================

def test_modificar_cita(session, datos_base):
    manana = date.today() + timedelta(days=1)
    cita = crear_cita(datos_base["mascota_id"], datos_base["vet_id"], manana, time(10,0), "Original")
    
    modificar_cita(cita.id, motivo="Nuevo Motivo")
    actualizada = obtener_cita_por_id(cita.id)
    assert actualizada.motivo == "Nuevo Motivo"

def test_ciclo_vida_cita(session, datos_base):
    manana = date.today() + timedelta(days=1)
    cita = crear_cita(datos_base["mascota_id"], datos_base["vet_id"], manana, time(10,0), "Checkeo")
    
    marcar_cita_realizada(cita.id)
    
    actualizada = obtener_cita_por_id(cita.id)
    assert actualizada.estado == "Realizada"

def test_cancelar_cita(session, datos_base):
    manana = date.today() + timedelta(days=1)
    cita = crear_cita(datos_base["mascota_id"], datos_base["vet_id"], manana, time(10,0), "A Cancelar")
    
    cancelar_cita(cita.id)
    assert obtener_cita_por_id(cita.id).estado == "Cancelada"

def test_error_cancelar_cita_realizada(session, datos_base):
    """Prueba que NO se puede cancelar una cita ya realizada."""
    manana = date.today() + timedelta(days=1)
    cita = crear_cita(datos_base["mascota_id"], datos_base["vet_id"], manana, time(10,0), "Ya hecha")
    
    marcar_cita_realizada(cita.id)
    
    # Esto DEBE fallar (lanzar excepción) si la lógica está bien implementada
    with pytest.raises(ValidacionException):
        cancelar_cita(cita.id)

# ==========================================
# 4. TESTS DE ELIMINACIÓN
# ==========================================

def test_eliminar_cita(session, datos_base):
    manana = date.today() + timedelta(days=1)
    cita = crear_cita(datos_base["mascota_id"], datos_base["vet_id"], manana, time(10,0), "Borrar")
    
    eliminar_cita(cita.id)
    assert cita_existe(cita.id) is False

def test_obtener_proximas_citas(session, datos_base):
    hoy = date.today()
    futuro_lejano = hoy + timedelta(days=10)
    futuro_cercano = hoy + timedelta(days=2)
    
    crear_cita(datos_base["mascota_id"], datos_base["vet_id"], futuro_lejano, time(10,0), "Lejana")
    crear_cita(datos_base["mascota_id"], datos_base["vet_id"], futuro_cercano, time(10,0), "Cercana")
    
    proximas = obtener_proximas_citas()
    # Deben venir ordenadas por fecha
    assert proximas[0].motivo == "Cercana"
    assert proximas[1].motivo == "Lejana"
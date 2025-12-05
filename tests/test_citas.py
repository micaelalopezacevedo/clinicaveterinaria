import pytest
from datetime import date, timedelta
from sqlalchemy.exc import IntegrityError
from src.citas import *
from src.database import Cita, Veterinario, Mascota, Cliente
# Ajusta estas importaciones según como hayas nombrado tus excepciones
from src.exceptions import CitaNoEncontradaException, ValidacionException

# ==========================================
# FIXTURE: DATOS BASE (Pre-requisitos)
# ==========================================

@pytest.fixture
def datos_base(session):
    """
    Crea automáticamente 1 Veterinario, 1 Cliente y 1 Mascota.
    Necesario porque no puedes crear una Cita sin que existan estos antes.
    Devuelve un diccionario con los IDs generados.
    """
    # 1. Crear Veterinario
    vet = Veterinario(nombre="Dr. Test", dni="111V", especialidad="General", email="vet@test.com")
    session.add(vet)
    
    # 2. Crear Cliente
    cliente = Cliente(nombre="Juan Dueño", dni="222C", telefono="600000000", email="juan@test.com")
    session.add(cliente)
    session.flush() # Forzamos para obtener el ID del cliente
    
    # 3. Crear Mascota asociada al cliente
    mascota = Mascota(nombre="Firulais", especie="Perro", raza="Mestizo", edad=5, cliente_id=cliente.id)
    session.add(mascota)
    
    session.commit()
    
    return {
        "vet_id": vet.id,
        "cliente_id": cliente.id,
        "mascota_id": mascota.id,
        "mascota_obj": mascota # Por si necesitamos el objeto
    }

# ==========================================
# 1. TESTS DE CREACIÓN Y VALIDACIÓN (CRÍTICOS)
# ==========================================

def test_crear_cita_exito(session, datos_base):
    """Happy Path: Crear una cita correctamente."""
    fecha_futura = date.today() + timedelta(days=5)
    
    cita = crear_cita(
        mascota_id=datos_base["mascota_id"],
        veterinario_id=datos_base["vet_id"],
        fecha=fecha_futura,
        motivo="Vacunación Anual"
    )
    
    assert cita.id is not None
    assert cita.estado == "Pendiente"
    assert cita.motivo == "Vacunación Anual"

def test_crear_cita_fecha_pasada_error(session, datos_base):
    """
    (AÑADIDO IMPORTANTE)
    No se debería poder agendar una cita para ayer.
    """
    ayer = date.today() - timedelta(days=1)
    
    with pytest.raises(ValidacionException):
        crear_cita(
            mascota_id=datos_base["mascota_id"],
            veterinario_id=datos_base["vet_id"],
            fecha=ayer,
            motivo="Intento cita pasada"
        )

def test_crear_cita_entidades_no_existentes(session):
    """
    (AÑADIDO IMPORTANTE)
    No se puede crear cita para un perro o veterinario que no existen.
    """
    fecha = date.today() + timedelta(days=1)
    
    # Intentamos usar IDs falsos (999)
    # Dependiendo de tu implementación, esto lanza IntegrityError (BD) o ValidacionException (Lógica)
    with pytest.raises((IntegrityError, ValidacionException)):
        crear_cita(999, 999, fecha, "Fallo")

# ==========================================
# 2. TESTS DE LECTURA Y FILTROS
# ==========================================

def test_listar_citas(session, datos_base):
    """Listar todas las citas."""
    crear_cita(datos_base["mascota_id"], datos_base["vet_id"], date.today(), "Cita 1")
    crear_cita(datos_base["mascota_id"], datos_base["vet_id"], date.today(), "Cita 2")
    
    assert len(listar_citas()) == 2

def test_obtener_cita_por_id(session, datos_base):
    """Buscar por ID."""
    cita_creada = crear_cita(datos_base["mascota_id"], datos_base["vet_id"], date.today(), "Test ID")
    
    encontrada = obtener_cita_por_id(cita_creada.id)
    assert encontrada.motivo == "Test ID"
    
    with pytest.raises(CitaNoEncontradaException):
        obtener_cita_por_id(99999)

def test_obtener_citas_por_fecha(session, datos_base):
    """Filtrar citas por fecha exacta."""
    hoy = date.today()
    manana = hoy + timedelta(days=1)
    
    crear_cita(datos_base["mascota_id"], datos_base["vet_id"], hoy, "Hoy")
    crear_cita(datos_base["mascota_id"], datos_base["vet_id"], manana, "Mañana")
    
    resultados = obtener_citas_por_fecha(hoy)
    assert len(resultados) == 1
    assert resultados[0].motivo == "Hoy"

def test_obtener_citas_por_mascota(session, datos_base):
    """Filtrar citas por ID de mascota."""
    # Necesitamos otra mascota para comparar
    otra_mascota = Mascota(nombre="Gato", especie="Gato", cliente_id=datos_base["cliente_id"])
    session.add(otra_mascota)
    session.commit()
    
    crear_cita(datos_base["mascota_id"], datos_base["vet_id"], date.today(), "Perro")
    crear_cita(otra_mascota.id, datos_base["vet_id"], date.today(), "Gato")
    
    citas_perro = obtener_citas_por_mascota(datos_base["mascota_id"])
    assert len(citas_perro) == 1
    assert citas_perro[0].motivo == "Perro"

# ==========================================
# 3. TESTS DE LÓGICA DE NEGOCIO (Estados)
# ==========================================

def test_modificar_cita(session, datos_base):
    """Modificar motivo o fecha."""
    cita = crear_cita(datos_base["mascota_id"], datos_base["vet_id"], date.today(), "Original")
    
    modificar_cita(cita.id, motivo="Nuevo Motivo")
    
    actualizada = obtener_cita_por_id(cita.id)
    assert actualizada.motivo == "Nuevo Motivo"

def test_ciclo_vida_cita(session, datos_base):
    """
    Prueba el ciclo completo: Pendiente -> Realizada.
    """
    cita = crear_cita(datos_base["mascota_id"], datos_base["vet_id"], date.today(), "Checkeo")
    assert cita.estado == "Pendiente"
    
    marcar_cita_realizada(cita.id)
    
    actualizada = obtener_cita_por_id(cita.id)
    assert actualizada.estado == "Realizada"

def test_cancelar_cita(session, datos_base):
    """Prueba cancelación."""
    cita = crear_cita(datos_base["mascota_id"], datos_base["vet_id"], date.today(), "A Cancelar")
    cancelar_cita(cita.id)
    assert obtener_cita_por_id(cita.id).estado == "Cancelada"

def test_error_cancelar_cita_realizada(session, datos_base):
    """
    (AÑADIDO IMPORTANTE)
    No se debe poder cancelar una cita que ya ocurrió.
    """
    cita = crear_cita(datos_base["mascota_id"], datos_base["vet_id"], date.today(), "Ya hecha")
    marcar_cita_realizada(cita.id)
    
    # Intentar cancelar ahora debería fallar
    with pytest.raises(ValidacionException):
        cancelar_cita(cita.id)

# ==========================================
# 4. TESTS DE ELIMINACIÓN Y CONTEO
# ==========================================

def test_eliminar_cita(session, datos_base):
    """Eliminación física de la BD."""
    cita = crear_cita(datos_base["mascota_id"], datos_base["vet_id"], date.today(), "Borrar")
    assert cita_existe(cita.id) is True
    
    eliminar_cita(cita.id)
    assert cita_existe(cita.id) is False

def test_obtener_proximas_citas(session, datos_base):
    """Verifica que trae citas futuras ordenadas."""
    hoy = date.today()
    futuro_lejano = hoy + timedelta(days=10)
    futuro_cercano = hoy + timedelta(days=2)
    
    crear_cita(datos_base["mascota_id"], datos_base["vet_id"], futuro_lejano, "Lejana")
    crear_cita(datos_base["mascota_id"], datos_base["vet_id"], futuro_cercano, "Cercana")
    
    proximas = obtener_proximas_citas()
    
    # Deberían venir ordenadas por fecha ascendente
    assert proximas[0].motivo == "Cercana"
    assert proximas[1].motivo == "Lejana"
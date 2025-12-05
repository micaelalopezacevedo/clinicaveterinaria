import pytest
from datetime import date, timedelta
from src.analisis import *
from src.database import Cliente, Mascota, Veterinario, Cita

# ==========================================
# FIXTURE: DATOS DE ESCENARIO COMPLEJO
# ==========================================

@pytest.fixture
def datos_analisis(session):
    """
    Crea un escenario rico en datos para probar estadísticas:
    - 2 Veterinarios
    - 3 Mascotas (2 Perros, 1 Gato)
    - Citas: Hoy, Mañana, Próxima Semana, Mes que viene, Pasadas.
    """
    # 1. Veterinarios
    v1 = Veterinario(nombre="Vet A", dni="V01", especialidad="Cirujano")
    v2 = Veterinario(nombre="Vet B", dni="V02", especialidad="General")
    session.add_all([v1, v2])
    
    # 2. Clientes y Mascotas
    c1 = Cliente(nombre="Cliente 1", dni="C01")
    session.add(c1)
    session.flush()
    
    m1 = Mascota(nombre="Perro1", especie="Perro", cliente_id=c1.id)
    m2 = Mascota(nombre="Perro2", especie="Perro", cliente_id=c1.id)
    m3 = Mascota(nombre="Gato1", especie="Gato", cliente_id=c1.id)
    session.add_all([m1, m2, m3])
    session.flush()
    
    # 3. Fechas clave
    hoy = date.today()
    manana = hoy + timedelta(days=1)
    semana_prox = hoy + timedelta(days=5) # Dentro de la semana
    mes_prox = hoy + timedelta(days=20)   # Dentro del mes
    futuro_lejano = hoy + timedelta(days=60)
    
    # 4. Citas
    citas = [
        # Vet A tiene 2 citas (1 hoy, 1 mes prox)
        Cita(fecha=hoy, hora="10:00", motivo="Hoy Vet A", mascota_id=m1.id, veterinario_id=v1.id, estado="Pendiente"),
        Cita(fecha=mes_prox, hora="10:00", motivo="Mes Prox Vet A", mascota_id=m1.id, veterinario_id=v1.id, estado="Confirmada"),
        
        # Vet B tiene 3 citas (1 mañana, 1 semana prox, 1 futuro)
        Cita(fecha=manana, hora="11:00", motivo="Mañana Vet B", mascota_id=m2.id, veterinario_id=v2.id, estado="Pendiente"),
        Cita(fecha=semana_prox, hora="12:00", motivo="Semana Vet B", mascota_id=m3.id, veterinario_id=v2.id, estado="Pendiente"),
        Cita(fecha=futuro_lejano, hora="09:00", motivo="Lejana Vet B", mascota_id=m2.id, veterinario_id=v2.id, estado="Pendiente"),
    ]
    session.add_all(citas)
    session.commit()
    
    return {"v1": v1, "v2": v2}

# ==========================================
# TESTS DE ESTADÍSTICAS GENERALES
# ==========================================

def test_obtener_estadisticas_generales(session, datos_analisis):
    """Test: Verifica que cuenta correctamente todas las entidades."""
    stats = obtener_estadisticas_generales()
    
    assert stats["total_clientes"] == 1
    assert stats["total_veterinarios"] == 2
    assert stats["total_mascotas"] == 3
    assert stats["total_citas"] == 5
    # De las 5 citas, 4 son 'Pendiente' y 1 'Confirmada'
    assert stats["citas_pendientes"] == 4

def test_estadisticas_vacias(session):
    """(Edge Case): Verificar que no falla si la BD está vacía."""
    stats = obtener_estadisticas_generales()
    assert stats["total_clientes"] == 0
    assert stats["total_citas"] == 0

# ==========================================
# TESTS DE CARGA DE TRABAJO
# ==========================================

def test_obtener_carga_veterinarios(session, datos_analisis):
    """Test: Verificar conteo de citas por veterinario."""
    carga = obtener_carga_veterinarios()
    # Esperamos una lista de dicts o tuplas
    
    # Vet B tiene 3 citas
    vet_b = next(c for c in carga if c["nombre"] == "Vet B")
    assert vet_b["num_citas"] == 3
    
    # Vet A tiene 2 citas
    vet_a = next(c for c in carga if c["nombre"] == "Vet A")
    assert vet_a["num_citas"] == 2

def test_obtener_veterinario_con_mas_citas(session, datos_analisis):
    """Test: Identificar al 'empleado del mes'."""
    top = obtener_veterinario_con_mas_citas()
    assert top["nombre"] == "Vet B"
    assert top["num_citas"] == 3

# ==========================================
# TESTS DE MASCOTAS Y ESPECIES
# ==========================================

def test_obtener_mascotas_por_especie(session, datos_analisis):
    """Test: Agrupar mascotas por especie."""
    conteo = obtener_mascotas_por_especie()
    # Tenemos 2 Perros y 1 Gato
    assert conteo["Perro"] == 2
    assert conteo["Gato"] == 1

def test_obtener_especie_mas_comun(session, datos_analisis):
    """Test: Especie más frecuente (Moda)."""
    especie = obtener_especie_mas_comun()
    assert especie == "Perro"

# ==========================================
# TESTS DE FECHAS (PRÓXIMAS CITAS)
# ==========================================

def test_obtener_proximas_citas_hoy(session, datos_analisis):
    """Test: Citas SOLO de hoy."""
    citas = obtener_proximas_citas_hoy()
    assert len(citas) == 1
    assert citas[0].motivo == "Hoy Vet A"

def test_obtener_proximas_citas_semana(session, datos_analisis):
    """
    Test: Citas de hoy + próximos 7 días.
    En fixture: Hoy(1) + Mañana(1) + SemanaProx(1) = 3 citas.
    (Mes prox y Lejana quedan fuera)
    """
    citas = obtener_proximas_citas_semana()
    assert len(citas) == 3

def test_obtener_proximas_citas_mes(session, datos_analisis):
    """
    Test: Citas de hoy + próximos 30 días.
    En fixture: 3 de semana + 1 del mes que viene = 4 citas.
    (La 'Lejana' de 60 días queda fuera)
    """
    citas = obtener_proximas_citas_mes()
    assert len(citas) == 4
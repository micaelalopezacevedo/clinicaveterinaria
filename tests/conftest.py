import pytest
from src.database import session as db_session_obj
from src.database import Cliente, Mascota, Veterinario

# Si ya tienes el modelo Cita, descomenta la siguiente línea:
# from src.database import Cita 

# =======================================================
# 1. GESTIÓN DE LA BASE DE DATOS (SETUP & TEARDOWN)
# =======================================================

@pytest.fixture(scope="function")
def session():
    """
    Fixture principal. Entrega una sesión de base de datos limpia para cada test.
    Realiza una limpieza antes y después de cada ejecución.
    """
    limpiar_base_de_datos()
    
    yield db_session_obj
    
    limpiar_base_de_datos()
    # Opcional: db_session_obj.close() si usas pool de conexiones

def limpiar_base_de_datos():
    """
    Borra todos los datos de las tablas.
    IMPORTANTE: El orden es vital para evitar errores de Foreign Key.
    Primero se borran los hijos (Mascotas, Citas), luego los padres (Clientes, Vets).
    """
    try:
        # 1. Si tienes citas, descomenta esto primero (son las que más dependencias tienen)
        # db_session_obj.query(Cita).delete()
        
        # 2. Borrar Mascotas (dependen de Cliente)
        db_session_obj.query(Mascota).delete()
        
        # 3. Borrar Entidades Principales
        db_session_obj.query(Cliente).delete()
        db_session_obj.query(Veterinario).delete()
        
        db_session_obj.commit()
    except Exception as e:
        db_session_obj.rollback()
        print(f"Error limpiando BD de test: {e}")

# =======================================================
# 2. FIXTURES DE DATOS (FACTORIES)
# =======================================================

@pytest.fixture
def cliente_default(session):
    """Crea un Cliente estándar para pruebas."""
    cliente = Cliente(
        nombre="Cliente Test",
        dni="00000000A",
        telefono="600000000",
        email="cliente@test.com"
    )
    session.add(cliente)
    session.commit()
    return cliente

@pytest.fixture
def mascota_default(session, cliente_default):
    """
    Crea una Mascota estándar.
    Automáticamente pide 'cliente_default' para asignarle un dueño.
    """
    mascota = Mascota(
        nombre="Firulais",
        especie="Perro",
        raza="Mestizo",
        edad=5,
        peso=12.5,
        sexo="Macho",
        cliente_id=cliente_default.id
    )
    session.add(mascota)
    session.commit()
    return mascota

@pytest.fixture
def veterinario_default(session):
    """Crea un Veterinario estándar para pruebas."""
    vet = Veterinario(
        nombre="Dra. Ana",
        dni="11111111V",
        cargo="Cirujana",
        especialidad="Cirugía",
        telefono="611111111",
        email="ana@vet.com"
    )
    session.add(vet)
    session.commit()
    return vet
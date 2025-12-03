"""
título: módulo de mascotas
fecha: 03.12.2025
descripción: lógica completa de gestión de mascotas.

CÓMO FUNCIONA:
===============

1. _RepositorioMascota: Acceso a BD (CRUD)
   └─ crear(), obtener_por_id(), listar_todos(), etc.
   └─ NUNCA tiene lógica de negocio

2. _ServicioMascota: Lógica de negocio
   └─ registrar_mascota(): valida + verifica cliente + crea
   └─ Usa Utilidades para validaciones
   └─ Usa _RepositorioMascota para BD

3. Interfaz pública: 9 funciones
   └─ Lo único que importa Streamlit
   └─ Wrappers simples que deleguen a ServicioMascota o RepositorioMascota
"""

from src.database import session, Mascota
from src.exceptions import MascotaNoEncontradaException, ClienteNoEncontradoException, ValidacionException
from src.logger import Logger
from sqlalchemy.exc import IntegrityError

# ========================
# REPOSITORIO (PRIVADO)
# ========================
# RESPONSABILIDAD: SOLO acceso a datos (CRUD)
# No hay lógica de negocio aquí

class _RepositorioMascota:
    """Encapsula acceso a BD - CRUD básico sin lógica"""
    
    @staticmethod
    def crear(nombre: str, especie: str, cliente_id: int, raza: str = None, edad: int = None, peso: float = None, sexo: str = None):
        """CRUD: CREATE"""
        mascota = Mascota(
            nombre=nombre,
            especie=especie,
            cliente_id=cliente_id,
            raza=raza,
            edad=edad,
            peso=peso,
            sexo=sexo
        )
        session.add(mascota)
        session.commit()
        Logger.info(f"Mascota creada con ID: {mascota.id}")
        return mascota
    
    @staticmethod
    def obtener_por_id(mascota_id: int):
        """CRUD: READ por ID"""
        mascota = session.query(Mascota).filter_by(id=mascota_id).first()
        if not mascota:
            raise MascotaNoEncontradaException(mascota_id)
        return mascota
    
    @staticmethod
    def listar_todos():
        """CRUD: READ todos"""
        return session.query(Mascota).order_by(Mascota.nombre).all()
    
    @staticmethod
    def obtener_por_cliente(cliente_id: int):
        """CRUD: READ por cliente_id"""
        return session.query(Mascota).filter_by(cliente_id=cliente_id).order_by(Mascota.nombre).all()
    
    @staticmethod
    def obtener_por_especie(especie: str):
        """CRUD: READ por especie"""
        return session.query(Mascota).filter_by(especie=especie).order_by(Mascota.nombre).all()
    
    @staticmethod
    def actualizar(mascota: Mascota, **campos) -> Mascota:
        """CRUD: UPDATE"""
        for campo, valor in campos.items():
            if valor is not None:
                setattr(mascota, campo, valor)
        session.commit()
        session.refresh(mascota)
        Logger.info(f"Mascota {mascota.id} actualizada")
        return mascota
    
    @staticmethod
    def eliminar(mascota: Mascota) -> bool:
        """CRUD: DELETE"""
        nombre = mascota.nombre
        session.delete(mascota)
        session.commit()
        Logger.info(f"Mascota {nombre} eliminada")
        return True
    
    @staticmethod
    def contar_total():
        """CRUD: COUNT todos"""
        try:
            return session.query(Mascota).count()
        except Exception as e:
            Logger.log_excepcion(e, "contar_total")
            return 0
    
    @staticmethod
    def existe(mascota_id: int) -> bool:
        """CRUD: READ para verificar existencia"""
        try:
            return session.query(Mascota).filter_by(id=mascota_id).first() is not None
        except Exception as e:
            Logger.log_excepcion(e, "existe")
            return False
    
    @staticmethod
    def obtener_historial_citas(mascota_id: int):
        """CRUD: READ relación citas"""
        try:
            mascota = session.query(Mascota).filter_by(id=mascota_id).first()
            if mascota:
                return mascota.citas
            return []
        except Exception as e:
            Logger.log_excepcion(e, "obtener_historial_citas")
            return []


# ========================
# SERVICIO (PRIVADO)
# ========================
# RESPONSABILIDAD: Lógica de negocio
# Usa Utilidades (validaciones) + _RepositorioMascota (BD)

class _ServicioMascota:
    """Orquesta validaciones + acceso a BD"""
    
    @staticmethod
    def registrar_mascota(nombre: str, especie: str, cliente_id: int, raza: str = None, edad: int = None, peso: float = None, sexo: str = None):
        """
        Registra una mascota: 1) Valida 2) Verifica cliente 3) Crea
        
        Puede lanzar ValidacionException o ClienteNoEncontradoException
        """
        try:
            # PASO 1: VALIDAR CAMPOS OBLIGATORIOS
            if not nombre or not especie or not cliente_id:
                raise ValidacionException("nombre, especie y cliente_id", "son campos obligatorios")
            
            # PASO 2: VERIFICAR QUE CLIENTE EXISTE
            # Importar aquí para evitar circular imports
            from src.clientes import obtener_cliente_por_id
            cliente = obtener_cliente_por_id(cliente_id)
            if not cliente:
                raise ClienteNoEncontradoException(cliente_id)
            
            # PASO 3: CREAR EN BD (delegado al repositorio)
            return _RepositorioMascota.crear(nombre, especie, cliente_id, raza, edad, peso, sexo)
        
        except (ValidacionException, ClienteNoEncontradoException):
            session.rollback()
            raise
        except IntegrityError:
            session.rollback()
            Logger.error("Error de integridad al registrar mascota")
            raise
        except Exception as e:
            session.rollback()
            Logger.log_excepcion(e, "registrar_mascota")
            raise
    
    @staticmethod
    def modificar_mascota(mascota_id: int, nombre: str = None, raza: str = None, edad: int = None, peso: float = None, sexo: str = None):
        """
        Modifica una mascota: 1) Obtiene 2) Valida cambios 3) Actualiza
        """
        try:
            # PASO 1: OBTENER MASCOTA
            mascota = _RepositorioMascota.obtener_por_id(mascota_id)
            
            # PASO 2: VALIDAR CAMBIOS (opcionales pero si se proporcionan, validar)
            if nombre is not None and not nombre:
                raise ValidacionException("nombre", "no puede estar vacío")
            
            # PASO 3: ACTUALIZAR (delegado al repositorio)
            return _RepositorioMascota.actualizar(
                mascota,
                nombre=nombre,
                raza=raza,
                edad=edad,
                peso=peso,
                sexo=sexo
            )
        
        except (MascotaNoEncontradaException, ValidacionException):
            session.rollback()
            raise
        except Exception as e:
            session.rollback()
            Logger.log_excepcion(e, "modificar_mascota")
            raise


# ========================
# INTERFAZ PÚBLICA (9 funciones)
# ========================
# Lo ÚNICO que usa Streamlit
# Todo está aquí, NADA en las clases privadas

def registrar_mascota(nombre: str, especie: str, cliente_id: int, raza: str = None, edad: int = None, peso: float = None, sexo: str = None):
    """Registra una nueva mascota"""
    return _ServicioMascota.registrar_mascota(nombre, especie, cliente_id, raza, edad, peso, sexo)

def listar_mascotas():
    """Devuelve todas las mascotas"""
    return _RepositorioMascota.listar_todos()

def obtener_mascota_por_id(mascota_id: int):
    """Obtiene una mascota por ID"""
    return _RepositorioMascota.obtener_por_id(mascota_id)

def obtener_mascotas_por_cliente(cliente_id: int):
    """Devuelve todas las mascotas de un cliente"""
    return _RepositorioMascota.obtener_por_cliente(cliente_id)

def obtener_mascotas_por_especie(especie: str):
    """Devuelve todas las mascotas de una especie"""
    return _RepositorioMascota.obtener_por_especie(especie)

def modificar_mascota(mascota_id: int, nombre: str = None, raza: str = None, edad: int = None, peso: float = None, sexo: str = None):
    """Modifica una mascota existente"""
    return _ServicioMascota.modificar_mascota(mascota_id, nombre, raza, edad, peso, sexo)

def eliminar_mascota(mascota_id: int):
    """Elimina una mascota"""
    try:
        mascota = _RepositorioMascota.obtener_por_id(mascota_id)
        return _RepositorioMascota.eliminar(mascota)
    except Exception as e:
        Logger.log_excepcion(e, "eliminar_mascota")
        raise

def contar_mascotas():
    """Cuenta total de mascotas"""
    return _RepositorioMascota.contar_total()

def ver_historial_mascota(mascota_id: int):
    """Ver historial de citas de una mascota"""
    try:
        return _RepositorioMascota.obtener_historial_citas(mascota_id)
    except Exception as e:
        Logger.log_excepcion(e, "ver_historial_mascota")
        return []

"""
Título: Módulo de Mascotas
Fecha: 19.11.2025
Descripción: Implementa toda la lógica relacionada con la gestión de mascotas.
Cubre los requisitos funcionales RF5-RF8
"""

from src.database import session, Mascota
from src.exceptions import (
    MascotaNoEncontradaException,
    ClienteNoEncontradoException,
    ValidacionException
)
from src.logger import Logger
from sqlalchemy.exc import IntegrityError


def registrar_mascota(nombre: str, especie: str, cliente_id: int, raza: str = None, edad: int = None, peso: float = None, sexo: str = None):
    """Registra nueva mascota asociada a cliente"""
    try:
        Logger.info(f"Intentando registrar mascota: {nombre} para cliente ID: {cliente_id}")
        
        if not nombre or not especie or not cliente_id:
            Logger.warning("Intento de registrar mascota sin datos obligatorios")
            raise ValidacionException("nombre, especie y cliente_id", "son campos obligatorios")
        
        nueva_mascota = Mascota(
            nombre=nombre,
            especie=especie,
            cliente_id=cliente_id,
            raza=raza,
            edad=edad,
            peso=peso,
            sexo=sexo
        )
        
        session.add(nueva_mascota)
        session.commit()
        Logger.info(f"Mascota registrada: {nombre} (ID: {nueva_mascota.id})")
        return nueva_mascota
    
    except ValidacionException:
        session.rollback()
        raise
    except IntegrityError:
        session.rollback()
        Logger.error(f"Error de integridad al registrar mascota")
        raise
    except Exception as e:
        session.rollback()
        Logger.log_excepcion(e, "registrar_mascota")
        raise


def listar_mascotas():
    """Devuelve todas las mascotas"""
    try:
        Logger.debug("Listando todas las mascotas")
        mascotas = session.query(Mascota).all()
        Logger.info(f"Se encontraron {len(mascotas)} mascotas")
        return mascotas
    except Exception as e:
        Logger.log_excepcion(e, "listar_mascotas")
        return []


def obtener_mascota_por_id(mascota_id: int):
    """Busca mascota por ID"""
    try:
        Logger.debug(f"Buscando mascota con ID: {mascota_id}")
        mascota = session.query(Mascota).filter_by(id=mascota_id).first()
        
        if not mascota:
            Logger.warning(f"No se encontró mascota con ID: {mascota_id}")
            raise MascotaNoEncontradaException(mascota_id)
        
        Logger.info(f"Mascota encontrada: {mascota.nombre}")
        return mascota
    
    except MascotaNoEncontradaException:
        raise
    except Exception as e:
        Logger.log_excepcion(e, "obtener_mascota_por_id")
        raise


def obtener_mascotas_por_cliente(cliente_id: int):
    """Devuelve todas las mascotas de un cliente"""
    try:
        Logger.debug(f"Buscando mascotas del cliente ID: {cliente_id}")
        mascotas = session.query(Mascota).filter_by(cliente_id=cliente_id).all()
        Logger.info(f"Cliente ID {cliente_id} tiene {len(mascotas)} mascotas")
        return mascotas
    except Exception as e:
        Logger.log_excepcion(e, "obtener_mascotas_por_cliente")
        return []


def ver_historial_mascota(mascota_id: int):
    """Ver historial de citas de una mascota"""
    try:
        Logger.debug(f"Obteniendo historial de mascota ID: {mascota_id}")
        mascota = obtener_mascota_por_id(mascota_id)
        
        if not mascota:
            raise MascotaNoEncontradaException(mascota_id)
        
        citas = mascota.citas
        Logger.info(f"Mascota {mascota.nombre} tiene {len(citas)} citas")
        return citas
    
    except MascotaNoEncontradaException:
        raise
    except Exception as e:
        Logger.log_excepcion(e, "ver_historial_mascota")
        return []


def modificar_mascota(mascota_id: int, nombre: str = None, raza: str = None, edad: int = None, peso: float = None, sexo: str = None):
    """Modifica datos de mascota existente"""
    try:
        Logger.info(f"Intentando modificar mascota ID: {mascota_id}")
        
        mascota = obtener_mascota_por_id(mascota_id)
        
        if not mascota:
            raise MascotaNoEncontradaException(mascota_id)
        
        if nombre is not None:
            Logger.debug(f"Actualizando nombre mascota: {mascota.nombre} -> {nombre}")
            mascota.nombre = nombre
        if raza is not None:
            Logger.debug(f"Actualizando raza mascota ID {mascota_id}")
            mascota.raza = raza
        if edad is not None:
            Logger.debug(f"Actualizando edad mascota ID {mascota_id}")
            mascota.edad = edad
        if peso is not None:
            Logger.debug(f"Actualizando peso mascota ID {mascota_id}")
            mascota.peso = peso
        if sexo is not None:
            Logger.debug(f"Actualizando sexo mascota ID {mascota_id}")
            mascota.sexo = sexo
        
        session.commit()
        Logger.info(f"Mascota ID {mascota_id} modificada correctamente")
        return mascota
    
    except MascotaNoEncontradaException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        Logger.log_excepcion(e, "modificar_mascota")
        raise


def eliminar_mascota(mascota_id: int):
    """Elimina mascota"""
    try:
        Logger.info(f"Intentando eliminar mascota ID: {mascota_id}")
        
        mascota = obtener_mascota_por_id(mascota_id)
        
        if not mascota:
            raise MascotaNoEncontradaException(mascota_id)
        
        nombre_mascota = mascota.nombre
        session.delete(mascota)
        session.commit()
        
        Logger.info(f"Mascota eliminada: {nombre_mascota} (ID: {mascota_id})")
        return True
    
    except MascotaNoEncontradaException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        Logger.log_excepcion(e, "eliminar_mascota")
        raise


def contar_mascotas():
    """Cuenta total de mascotas"""
    try:
        total = session.query(Mascota).count()
        Logger.debug(f"Total de mascotas: {total}")
        return total
    except Exception as e:
        Logger.log_excepcion(e, "contar_mascotas")
        return 0


def mascota_existe(mascota_id: int):
    """Verifica si existe mascota con ese ID"""
    try:
        existe = session.query(Mascota).filter_by(id=mascota_id).first() is not None
        Logger.debug(f"Mascota ID {mascota_id} existe: {existe}")
        return existe
    except Exception as e:
        Logger.log_excepcion(e, "mascota_existe")
        return False
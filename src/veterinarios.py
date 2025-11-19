"""
Título: Módulo de Veterinarios
Fecha: 19.11.2025
Descripción: Implementa toda la lógica relacionada con la gestión de veterinarios.
Cubre los requisitos funcionales RF9-RF12
"""

from src.database import session, Veterinario
from src.exceptions import (
    VeterinarioNoEncontradoException,
    DNIDuplicadoException,
    ValidacionException
)
from src.logger import Logger
from sqlalchemy.exc import IntegrityError


def crear_veterinario(nombre: str, dni: str, cargo: str = None, especialidad: str = None, telefono: str = None, email: str = None):
    """Crea un nuevo veterinario"""
    try:
        Logger.info(f"Intentando crear veterinario: {nombre} con DNI: {dni}")
        
        if not nombre or not dni:
            Logger.warning("Intento de crear veterinario sin nombre o DNI")
            raise ValidacionException("nombre y DNI", "son campos obligatorios")
        
        if session.query(Veterinario).filter_by(dni=dni).first():
            Logger.error(f"DNI duplicado {dni}")
            raise DNIDuplicadoException(dni, "Veterinario")
        
        veterinario = Veterinario(
            nombre=nombre,
            dni=dni,
            cargo=cargo,
            especialidad=especialidad,
            telefono=telefono,
            email=email
        )
        
        session.add(veterinario)
        session.commit()
        Logger.info(f"Veterinario creado correctamente: {veterinario.nombre} (ID: {veterinario.id})")
        return veterinario
    
    except (DNIDuplicadoException, ValidacionException):
        session.rollback()
        raise
    except IntegrityError:
        session.rollback()
        Logger.error("Error de integridad, probablemente DNI duplicado")
        raise
    except Exception as e:
        session.rollback()
        Logger.log_excepcion(e, "crear_veterinario")
        raise


def listar_veterinarios():
    """Devuelve todos los veterinarios"""
    try:
        Logger.debug("Listando todos los veterinarios")
        veterinarios = session.query(Veterinario).all()
        Logger.info(f"Se encontraron {len(veterinarios)} veterinarios")
        return veterinarios
    except Exception as e:
        Logger.log_excepcion(e, "listar_veterinarios")
        return []


def obtener_veterinario_por_id(veterinario_id: int):
    """Busca veterinario por ID"""
    try:
        Logger.debug(f"Buscando veterinario con ID: {veterinario_id}")
        veterinario = session.query(Veterinario).filter_by(id=veterinario_id).first()
        
        if not veterinario:
            Logger.warning(f"No se encontró veterinario con ID: {veterinario_id}")
            raise VeterinarioNoEncontradoException(veterinario_id)
        
        Logger.info(f"Veterinario encontrado: {veterinario.nombre}")
        return veterinario
    
    except VeterinarioNoEncontradoException:
        raise
    except Exception as e:
        Logger.log_excepcion(e, "obtener_veterinario_por_id")
        raise


def buscar_veterinario_por_dni(dni: str):
    """Busca veterinario por DNI"""
    try:
        Logger.debug(f"Buscando veterinario con DNI: {dni}")
        veterinario = session.query(Veterinario).filter_by(dni=dni).first()
        
        if not veterinario:
            Logger.warning(f"No se encontró veterinario con DNI: {dni}")
            return None
        
        Logger.info(f"Veterinario encontrado: {veterinario.nombre}")
        return veterinario
    except Exception as e:
        Logger.log_excepcion(e, "buscar_veterinario_por_dni")
        return None


def buscar_veterinario_por_nombre(nombre: str):
    """Busca veterinarios por nombre (búsqueda parcial)"""
    try:
        Logger.debug(f"Buscando veterinarios con nombre: {nombre}")
        veterinarios = session.query(Veterinario).filter(
            Veterinario.nombre.like(f"%{nombre}%")
        ).all()
        Logger.info(f"Se encontraron {len(veterinarios)} veterinarios con nombre similar a '{nombre}'")
        return veterinarios
    except Exception as e:
        Logger.log_excepcion(e, "buscar_veterinario_por_nombre")
        return []


def modificar_veterinario(veterinario_id: int, nombre: str = None, cargo: str = None, especialidad: str = None, telefono: str = None, email: str = None):
    """Modifica veterinario existente"""
    try:
        Logger.info(f"Intentando modificar veterinario ID: {veterinario_id}")
        
        veterinario = obtener_veterinario_por_id(veterinario_id)
        
        if not veterinario:
            raise VeterinarioNoEncontradoException(veterinario_id)
        
        if nombre is not None:
            Logger.debug(f"Actualizando nombre veterinario: {veterinario.nombre} -> {nombre}")
            veterinario.nombre = nombre
        if cargo is not None:
            Logger.debug(f"Actualizando cargo veterinario ID {veterinario_id}")
            veterinario.cargo = cargo
        if especialidad is not None:
            Logger.debug(f"Actualizando especialidad veterinario ID {veterinario_id}")
            veterinario.especialidad = especialidad
        if telefono is not None:
            Logger.debug(f"Actualizando teléfono veterinario ID {veterinario_id}")
            veterinario.telefono = telefono
        if email is not None:
            Logger.debug(f"Actualizando email veterinario ID {veterinario_id}")
            veterinario.email = email
        
        session.commit()
        Logger.info(f"Veterinario ID {veterinario_id} modificado correctamente")
        return veterinario
    
    except VeterinarioNoEncontradoException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        Logger.log_excepcion(e, "modificar_veterinario")
        raise


def eliminar_veterinario(veterinario_id: int):
    """Elimina veterinario"""
    try:
        Logger.info(f"Intentando eliminar veterinario ID: {veterinario_id}")
        
        veterinario = obtener_veterinario_por_id(veterinario_id)
        
        if not veterinario:
            raise VeterinarioNoEncontradoException(veterinario_id)
        
        nombre_veterinario = veterinario.nombre
        session.delete(veterinario)
        session.commit()
        
        Logger.info(f"Veterinario eliminado: {nombre_veterinario} (ID: {veterinario_id})")
        return True
    
    except VeterinarioNoEncontradoException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        Logger.log_excepcion(e, "eliminar_veterinario")
        raise


def contar_veterinarios():
    """Cuenta total de veterinarios"""
    try:
        total = session.query(Veterinario).count()
        Logger.debug(f"Total de veterinarios: {total}")
        return total
    except Exception as e:
        Logger.log_excepcion(e, "contar_veterinarios")
        return 0


def veterinario_existe(veterinario_id: int):
    """Verifica si existe veterinario con ese ID"""
    try:
        existe = session.query(Veterinario).filter_by(id=veterinario_id).first() is not None
        Logger.debug(f"Veterinario ID {veterinario_id} existe: {existe}")
        return existe
    except Exception as e:
        Logger.log_excepcion(e, "veterinario_existe")
        return False
"""
título: módulo de citas
fecha: 11.11.2025
descripción: implementa toda la lógica relacionada con gestión de citas veterinarias.
Cubre los requisitos funcionales RF13-RF16:
- RF13: Crear citas
- RF14: Filtrar citas por criterios
- RF15: Modificar y cancelar citas
- RF16: Mostrar próximas citas
"""

from src.database import session, Cita
from src.exceptions import (
    CitaNoEncontradaException,
    MascotaNoEncontradaException,
    VeterinarioNoEncontradoException,
    ValidacionException
)
from src.logger import Logger
from datetime import datetime, date, time


def validar_horario_laboral(hora: time) -> bool:
    """Valida que la hora esté dentro del horario laboral (9:00 - 17:00)"""
    hora_inicio = time(9, 0)  # 9:00 AM
    hora_fin = time(17, 0)    # 5:00 PM
    return hora_inicio <= hora <= hora_fin


def verificar_disponibilidad(veterinario_id: int, fecha: date, hora_str: str, cita_id: int = None) -> bool:
    """
    Verifica si el veterinario está disponible en esa fecha y hora.
    Args:
        veterinario_id: ID del veterinario
        fecha: Fecha de la cita
        hora_str: Hora en formato "HH:MM"
        cita_id: ID de la cita actual (para excluirla al editar)
    Returns:
        True si está disponible, False si ya tiene una cita
    """
    try:
        query = session.query(Cita).filter_by(
            veterinario_id=veterinario_id,
            fecha=fecha,
            hora=hora_str
        )
        
        # Si estamos editando una cita, excluirla de la búsqueda
        if cita_id:
            query = query.filter(Cita.id != cita_id)
        
        cita_existente = query.first()
        
        if cita_existente:
            Logger.warning(f"Conflicto de horario: Veterinario {veterinario_id} ya tiene cita el {fecha} a las {hora_str}")
            return False
        
        return True
    except Exception as e:
        Logger.log_excepcion(e, "verificar_disponibilidad")
        return True  # En caso de error, permitir la cita


def crear_cita(mascota_id: int, veterinario_id: int, fecha: date, hora: time, 
               motivo: str = None, estado: str = "Pendiente"):
    """Crea una nueva cita"""
    try:
        Logger.info(f"Intentando crear cita para mascota ID: {mascota_id} con veterinario ID: {veterinario_id}")
        
        if not mascota_id or not veterinario_id or not fecha or not hora:
            Logger.warning("Intento de crear cita sin datos obligatorios")
            raise ValidacionException("Mascota, veterinario, fecha y hora", "son campos obligatorios")
        
        # Validar que la fecha no sea pasada
        fecha_hora_cita = datetime.combine(fecha, hora)
        if fecha_hora_cita < datetime.now():
            Logger.warning(f"Intento de crear cita en fecha pasada: {fecha_hora_cita}")
            raise ValidacionException("Fecha/hora", "no puede ser en el pasado")
        
        # Validar horario laboral (9:00 - 17:00)
        if not validar_horario_laboral(hora):
            Logger.warning(f"Intento de crear cita fuera del horario laboral: {hora}")
            raise ValidacionException("Hora", "debe estar entre 09:00 y 17:00")
        
        # Convertir hora a string formato HH:MM
        hora_str = hora.strftime('%H:%M')
        
        # Verificar disponibilidad del veterinario
        if not verificar_disponibilidad(veterinario_id, fecha, hora_str):
            raise ValidacionException("Horario", "el veterinario ya tiene una cita a esa hora")
        
        cita = Cita(
            mascota_id=mascota_id,
            veterinario_id=veterinario_id,
            fecha=fecha,
            hora=hora_str,  # Guardar como string
            motivo=motivo,
            estado=estado,
            diagnostico=None
        )
        
        session.add(cita)
        session.commit()
        Logger.info(f"Cita creada correctamente con ID: {cita.id}")
        return cita
    
    except ValidacionException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        Logger.log_excepcion(e, "crear_cita")
        raise


def listar_citas():
    """Devuelve todas las citas ordenadas por fecha y hora"""
    try:
        Logger.debug("Listando todas las citas")
        citas = session.query(Cita).order_by(Cita.fecha.desc(), Cita.hora.desc()).all()
        Logger.info(f"Se encontraron {len(citas)} citas")
        return citas
    except Exception as e:
        Logger.log_excepcion(e, "listar_citas")
        return []


def obtener_cita_por_id(cita_id: int):
    """Busca cita por ID"""
    try:
        Logger.debug(f"Buscando cita con ID: {cita_id}")
        cita = session.query(Cita).filter_by(id=cita_id).first()
        
        if not cita:
            Logger.warning(f"No se encontró cita con ID: {cita_id}")
            raise CitaNoEncontradaException(cita_id)
        
        Logger.info(f"Cita encontrada: ID {cita.id}")
        return cita
    
    except CitaNoEncontradaException:
        raise
    except Exception as e:
        Logger.log_excepcion(e, "obtener_cita_por_id")
        raise


def obtener_citas_por_mascota(mascota_id: int):
    """Busca todas las citas de una mascota"""
    try:
        Logger.debug(f"Buscando citas de mascota ID: {mascota_id}")
        citas = session.query(Cita).filter_by(mascota_id=mascota_id).order_by(Cita.fecha.desc()).all()
        Logger.info(f"Se encontraron {len(citas)} citas para mascota ID: {mascota_id}")
        return citas
    except Exception as e:
        Logger.log_excepcion(e, "obtener_citas_por_mascota")
        return []


def obtener_citas_por_veterinario(veterinario_id: int):
    """Busca todas las citas de un veterinario"""
    try:
        Logger.debug(f"Buscando citas de veterinario ID: {veterinario_id}")
        citas = session.query(Cita).filter_by(veterinario_id=veterinario_id).order_by(Cita.fecha.desc()).all()
        Logger.info(f"Se encontraron {len(citas)} citas para veterinario ID: {veterinario_id}")
        return citas
    except Exception as e:
        Logger.log_excepcion(e, "obtener_citas_por_veterinario")
        return []


def obtener_citas_por_fecha(fecha: date):
    """Busca todas las citas de una fecha específica"""
    try:
        Logger.debug(f"Buscando citas para fecha: {fecha}")
        citas = session.query(Cita).filter_by(fecha=fecha).order_by(Cita.hora).all()
        Logger.info(f"Se encontraron {len(citas)} citas para la fecha {fecha}")
        return citas
    except Exception as e:
        Logger.log_excepcion(e, "obtener_citas_por_fecha")
        return []


def obtener_citas_por_estado(estado: str):
    """Busca citas por estado"""
    try:
        Logger.debug(f"Buscando citas con estado: {estado}")
        citas = session.query(Cita).filter_by(estado=estado).order_by(Cita.fecha.desc()).all()
        Logger.info(f"Se encontraron {len(citas)} citas con estado: {estado}")
        return citas
    except Exception as e:
        Logger.log_excepcion(e, "obtener_citas_por_estado")
        return []


def modificar_cita(cita_id: int, fecha: date = None, hora: time = None, 
                   motivo: str = None, estado: str = None, diagnostico: str = None):
    """Modifica cita existente"""
    try:
        Logger.info(f"Intentando modificar cita ID: {cita_id}")
        
        cita = obtener_cita_por_id(cita_id)
        
        if not cita:
            raise CitaNoEncontradaException(cita_id)
        
        if fecha is not None:
            Logger.debug(f"Actualizando fecha cita ID {cita_id}")
            cita.fecha = fecha
        
        if hora is not None:
            Logger.debug(f"Actualizando hora cita ID {cita_id}")
            
            # Validar horario laboral
            if not validar_horario_laboral(hora):
                raise ValidacionException("Hora", "debe estar entre 09:00 y 17:00")
            
            # Convertir hora a string
            hora_str = hora.strftime('%H:%M') if isinstance(hora, time) else hora
            
            # Verificar disponibilidad (excluyendo esta cita)
            fecha_a_validar = fecha if fecha is not None else cita.fecha
            if not verificar_disponibilidad(cita.veterinario_id, fecha_a_validar, hora_str, cita_id):
                raise ValidacionException("Horario", "el veterinario ya tiene una cita a esa hora")
            
            cita.hora = hora_str
        
        if motivo is not None:
            Logger.debug(f"Actualizando motivo cita ID {cita_id}")
            cita.motivo = motivo
        
        if estado is not None:
            Logger.debug(f"Actualizando estado cita ID {cita_id}: {estado}")
            cita.estado = estado
        
        if diagnostico is not None:
            Logger.debug(f"Actualizando diagnóstico cita ID {cita_id}")
            cita.diagnostico = diagnostico
        
        session.commit()
        # Refrescar el objeto para obtener los datos actualizados
        session.refresh(cita)
        Logger.info(f"Cita ID {cita_id} modificada correctamente")
        return cita
    
    except (CitaNoEncontradaException, ValidacionException):
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        Logger.log_excepcion(e, "modificar_cita")
        raise


def cancelar_cita(cita_id: int):
    """Cancela una cita (cambia estado a Cancelada)"""
    try:
        Logger.info(f"Intentando cancelar cita ID: {cita_id}")
        cita = modificar_cita(cita_id, estado="Cancelada")
        Logger.info(f"Cita ID {cita_id} cancelada correctamente")
        return cita
    except Exception as e:
        Logger.log_excepcion(e, "cancelar_cita")
        raise


def eliminar_cita(cita_id: int):
    """Elimina una cita"""
    try:
        Logger.info(f"Intentando eliminar cita ID: {cita_id}")
        
        cita = obtener_cita_por_id(cita_id)
        
        if not cita:
            raise CitaNoEncontradaException(cita_id)
        
        session.delete(cita)
        session.commit()
        
        Logger.info(f"Cita eliminada: ID {cita_id}")
        return True
    
    except CitaNoEncontradaException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        Logger.log_excepcion(e, "eliminar_cita")
        raise


def contar_citas():
    """Cuenta total de citas"""
    try:
        total = session.query(Cita).count()
        Logger.debug(f"Total de citas: {total}")
        return total
    except Exception as e:
        Logger.log_excepcion(e, "contar_citas")
        return 0


def contar_citas_por_estado(estado: str):
    """Cuenta citas por estado"""
    try:
        total = session.query(Cita).filter_by(estado=estado).count()
        Logger.debug(f"Total de citas con estado '{estado}': {total}")
        return total
    except Exception as e:
        Logger.log_excepcion(e, "contar_citas_por_estado")
        return 0

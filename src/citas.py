"""
título: módulo de citas
fecha: 11.11.2025
descripción: lógica completa de gestión de citas veterinarias.

CÓMO FUNCIONA:
===============

1. _RepositorioCita: Acceso a BD (CRUD)
   └─ crear(), obtener_por_id(), listar_todas(), contar_todas(), etc.
   └─ NUNCA tiene lógica de negocio

2. _ServicioCita: Lógica de negocio
   └─ crear_cita(): valida + verifica + crea
   └─ modificar_cita(): valida cambios + actualiza
   └─ Usa Utilidades para validaciones
   └─ Usa _RepositorioCita para BD

3. Interfaz pública: 14 funciones
   └─ Lo único que importa Streamlit
   └─ Wrappers simples que deleguen a ServicioCita
   └─ Ejemplo: def crear_cita(...) → return _ServicioCita.crear_cita(...)
"""

from src.database import session, Cita
from src.utils import Utilidades
from src.exceptions import CitaNoEncontradaException, ValidacionException
from src.logger import Logger
from datetime import date, time

# ========================
# REPOSITORIO (PRIVADO)
# ========================
# RESPONSABILIDAD: Acceso a datos (CRUD básico)
# Aquí SOLO van queries a BD, nada de validaciones

class _RepositorioCita:
    """
    Encapsula acceso a BD
    Métodos: crear, leer, actualizar, eliminar (CRUD)
    """
    
    @staticmethod
    def crear(mascota_id: int, vet_id: int, fecha: date, hora: time, motivo: str = None, estado: str = "Pendiente"):
        """
        CRUD: CREATE
        Guarda una cita en la BD
        """
        # Convertir hora (objeto time) a string "HH:MM"
        hora_str = Utilidades.convertir_hora_a_string(hora)
        
        # Crear objeto Cita
        cita = Cita(
            mascota_id=mascota_id,
            veterinario_id=vet_id,
            fecha=fecha,
            hora=hora_str,
            motivo=motivo,
            estado=estado,
            diagnostico=None
        )
        
        # Guardar en BD
        session.add(cita)
        session.commit()
        Logger.info(f"Cita creada con ID: {cita.id}")
        return cita
    
    @staticmethod
    def obtener_por_id(cita_id: int):
        """
        CRUD: READ por ID
        Busca una cita en la BD
        Lanza excepción si no existe
        """
        cita = session.query(Cita).filter_by(id=cita_id).first()
        if not cita:
            raise CitaNoEncontradaException(cita_id)
        return cita
    
    @staticmethod
    def listar_todas():
        """CRUD: READ todos - devuelve lista ordenada por fecha descendente"""
        return session.query(Cita).order_by(Cita.fecha.desc(), Cita.hora.desc()).all()
    
    @staticmethod
    def obtener_por_mascota(mascota_id: int):
        """CRUD: READ filtrado por mascota"""
        return session.query(Cita).filter_by(mascota_id=mascota_id).order_by(Cita.fecha.desc()).all()
    
    @staticmethod
    def obtener_por_veterinario(vet_id: int):
        """CRUD: READ filtrado por veterinario"""
        return session.query(Cita).filter_by(veterinario_id=vet_id).order_by(Cita.fecha.desc()).all()
    
    @staticmethod
    def obtener_por_fecha(fecha: date):
        """CRUD: READ filtrado por fecha"""
        return session.query(Cita).filter_by(fecha=fecha).order_by(Cita.hora).all()
    
    @staticmethod
    def obtener_por_estado(estado: str):
        """CRUD: READ filtrado por estado (Pendiente, Confirmada, Realizada, Cancelada)"""
        return session.query(Cita).filter_by(estado=estado).order_by(Cita.fecha.desc()).all()
    
    @staticmethod
    def actualizar(cita: Cita, **campos) -> Cita:
        """
        CRUD: UPDATE
        Modifica campos específicos de una cita
        campos: diccionario con los campos a actualizar
        """
        for campo, valor in campos.items():
            if valor is not None:  # Solo actualizar si el valor no es None
                setattr(cita, campo, valor)
        session.commit()
        session.refresh(cita)  # Recargar objeto para tener datos actualizados
        Logger.info(f"Cita {cita.id} actualizada")
        return cita
    
    @staticmethod
    def eliminar(cita: Cita) -> bool:
        """CRUD: DELETE - elimina una cita de la BD"""
        session.delete(cita)
        session.commit()
        Logger.info(f"Cita {cita.id} eliminada")
        return True
    
    @staticmethod
    def contar_todas():
        """CRUD: COUNT - cuenta total de citas"""
        try:
            return session.query(Cita).count()
        except Exception as e:
            Logger.log_excepcion(e, "contar_todas")
            return 0
    
    @staticmethod
    def contar_por_estado(estado: str):
        """CRUD: COUNT - cuenta citas por estado"""
        try:
            return session.query(Cita).filter_by(estado=estado).count()
        except Exception as e:
            Logger.log_excepcion(e, "contar_por_estado")
            return 0
    
    @staticmethod
    def verificar_disponibilidad(vet_id: int, fecha: date, hora_str: str, cita_id: int = None) -> bool:
        """
        CRUD: READ para verificar si hay conflicto
        Verifica si el veterinario ya tiene cita a esa hora
        Si cita_id se proporciona, excluye esa cita (útil para ediciones)
        """
        q = session.query(Cita).filter_by(veterinario_id=vet_id, fecha=fecha, hora=hora_str)
        if cita_id:
            q = q.filter(Cita.id != cita_id)  # Excluir esta cita de la búsqueda
        return not q.first()  # True si NO hay conflicto, False si hay


# ========================
# SERVICIO (PRIVADO)
# ========================
# RESPONSABILIDAD: Lógica de negocio
# Aquí va: validaciones + coordinación + reglas de negocio

class _ServicioCita:
    """
    Orquesta validaciones (utils.py) + acceso a BD (Repositorio)
    Implementa la lógica de negocio
    """
    
    @staticmethod
    def crear_cita(mascota_id: int, veterinario_id: int, fecha: date, hora: time, motivo: str = None, estado: str = "Pendiente"):
        """
        Crea una cita con TODAS las validaciones y reglas de negocio
        
        FLUJO:
        1. Validar campos (mascota, vet, fecha, hora)
        2. Validar que hora no sea pasada
        3. Validar que hora esté en horario laboral (09:00-17:00)
        4. Verificar que vet no tenga conflicto de horario
        5. Crear en BD
        
        Puede lanzar ValidacionException si algo falla
        """
        # PASO 1: VALIDAR TODOS LOS CAMPOS
        # Utilidades.validar_campos_cita() hace todo: campos obligatorios, fecha no pasada, hora laboral
        es_valido, mensaje = Utilidades.validar_campos_cita(mascota_id, veterinario_id, fecha, hora)
        if not es_valido:
            raise ValidacionException("Cita", mensaje)
        
        # PASO 2: CONVERTIR HORA A STRING
        hora_str = Utilidades.convertir_hora_a_string(hora)
        
        # PASO 3: VERIFICAR DISPONIBILIDAD DEL VETERINARIO
        # Si devuelve False = hay conflicto = lanzar excepción
        if not _RepositorioCita.verificar_disponibilidad(veterinario_id, fecha, hora_str):
            raise ValidacionException("Horario", "el veterinario ya tiene una cita a esa hora")
        
        # PASO 4: CREAR EN BD (delegado al repositorio)
        return _RepositorioCita.crear(mascota_id, veterinario_id, fecha, hora, motivo, estado)
    
    @staticmethod
    def modificar_cita(cita_id: int, fecha: date = None, hora: time = None, motivo: str = None, estado: str = None, diagnostico: str = None):
        """
        Modifica una cita existente con validaciones
        
        FLUJO:
        1. Obtener cita actual
        2. SI se cambia hora → validar como si fuera nueva cita
        3. Actualizar en BD
        
        Los parámetros son opcionales (None = no cambiar)
        """
        # PASO 1: OBTENER CITA ACTUAL
        cita = _RepositorioCita.obtener_por_id(cita_id)
        
        # PASO 2: SI SE CAMBIA HORA, VALIDAR
        if hora is not None:
            # Usar fecha nueva si se proporciona, si no usar la actual
            fecha_val = fecha or cita.fecha
            
            # Validar como si fuera una nueva cita
            es_valido, mensaje = Utilidades.validar_campos_cita(cita.mascota_id, cita.veterinario_id, fecha_val, hora)
            if not es_valido:
                raise ValidacionException("Cita", mensaje)
            
            # Convertir hora a string
            hora_str = Utilidades.convertir_hora_a_string(hora)
            
            # Verificar disponibilidad (excluyendo ESTA cita, por eso pasamos cita_id)
            if not _RepositorioCita.verificar_disponibilidad(cita.veterinario_id, fecha_val, hora_str, cita_id):
                raise ValidacionException("Horario", "el veterinario ya tiene una cita a esa hora")
            
            # Actualizar con los nuevos valores
            return _RepositorioCita.actualizar(cita, fecha=fecha_val, hora=hora_str, motivo=motivo, estado=estado, diagnostico=diagnostico)
        else:
            # Si NO se cambia hora, solo actualizar otros campos (sin validaciones extra)
            return _RepositorioCita.actualizar(cita, fecha=fecha, motivo=motivo, estado=estado, diagnostico=diagnostico)


# ========================
# INTERFAZ PÚBLICA (14 funciones)
# ========================
# Lo ÚNICO que Streamlit importa y usa
# Cada función es un wrapper simple que delega a ServicioCita o RepositorioCita

def crear_cita(mascota_id: int, veterinario_id: int, fecha: date, hora: time, motivo: str = None, estado: str = "Pendiente"):
    """Crea una nueva cita"""
    return _ServicioCita.crear_cita(mascota_id, veterinario_id, fecha, hora, motivo, estado)

def listar_citas():
    """Devuelve todas las citas"""
    return _RepositorioCita.listar_todas()

def obtener_cita_por_id(cita_id: int):
    """Obtiene una cita por ID"""
    return _RepositorioCita.obtener_por_id(cita_id)

def obtener_citas_por_mascota(mascota_id: int):
    """Devuelve todas las citas de una mascota"""
    return _RepositorioCita.obtener_por_mascota(mascota_id)

def obtener_citas_por_veterinario(veterinario_id: int):
    """Devuelve todas las citas de un veterinario"""
    return _RepositorioCita.obtener_por_veterinario(veterinario_id)

def obtener_citas_por_fecha(fecha: date):
    """Devuelve todas las citas de una fecha"""
    return _RepositorioCita.obtener_por_fecha(fecha)

def obtener_citas_por_estado(estado: str):
    """Devuelve todas las citas de un estado"""
    return _RepositorioCita.obtener_por_estado(estado)

def modificar_cita(cita_id: int, fecha: date = None, hora: time = None, motivo: str = None, estado: str = None, diagnostico: str = None):
    """Modifica una cita existente"""
    return _ServicioCita.modificar_cita(cita_id, fecha, hora, motivo, estado, diagnostico)

def cancelar_cita(cita_id: int):
    """Cancela una cita (cambia estado a Cancelada)"""
    return modificar_cita(cita_id, estado="Cancelada")

def eliminar_cita(cita_id: int):
    """Elimina una cita completamente"""
    cita = _RepositorioCita.obtener_por_id(cita_id)
    return _RepositorioCita.eliminar(cita)

def contar_citas():
    """Cuenta total de citas"""
    return _RepositorioCita.contar_todas()

def contar_citas_por_estado(estado: str):
    """Cuenta citas por estado"""
    return _RepositorioCita.contar_por_estado(estado)

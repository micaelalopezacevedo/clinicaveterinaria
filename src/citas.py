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
from datetime import date

# CREATE
def crear_cita(fecha: date, hora: str, motivo: str, mascota_id: int, veterinario_id: int, diagnostico: str = None) -> Cita:
    """
    Crea nueva cita (RF13)
    Args: fecha (date), hora (str), motivo (str), mascota_id (int), 
          veterinario_id (int), diagnostico (str, opcional)
    Return: Cita creada o None si error
    """

# READ
def listar_citas() -> list:
    """
    Devuelve todas las citas
    Args: ninguno
    Return: Lista de citas
    """

def obtener_cita_por_id(cita_id: int) -> Cita:
    """
    Busca cita por ID
    Args: cita_id (int)
    Return: Cita encontrada o None
    """

def obtener_citas_por_fecha(fecha: date) -> list:
    """
    Devuelve citas de una fecha específica (RF14)
    Args: fecha (date)
    Return: Lista de citas de esa fecha
    """

def obtener_citas_por_mascota(mascota_id: int) -> list:
    """
    Devuelve todas las citas de una mascota (RF14)
    Args: mascota_id (int)
    Return: Lista de citas de la mascota
    """

def obtener_citas_por_veterinario(veterinario_id: int) -> list:
    """
    Devuelve todas las citas de un veterinario (RF14)
    Args: veterinario_id (int)
    Return: Lista de citas del veterinario
    """

def obtener_citas_por_cliente(cliente_id: int) -> list:
    """
    Devuelve citas de todas las mascotas de un cliente (RF14)
    Args: cliente_id (int)
    Return: Lista de citas del cliente
    """

def obtener_proximas_citas(dias: int = 7) -> list:
    """
    Devuelve citas próximas en los próximos N días (RF16)
    Args: dias (int, por defecto 7)
    Return: Lista de próximas citas
    """

def obtener_citas_pendientes() -> list:
    """
    Devuelve todas las citas con estado 'pendiente'
    Args: ninguno
    Return: Lista de citas pendientes
    """

# UPDATE
def modificar_cita(cita_id: int, fecha: date = None, hora: str = None, motivo: str = None, diagnostico: str = None) -> Cita:
    """
    Modifica cita existente (RF15)
    Args: cita_id (int), fecha (date, opcional), hora (str, opcional), 
          motivo (str, opcional), diagnostico (str, opcional)
    Return: Cita modificada o None si no existe
    """

def marcar_cita_realizada(cita_id: int, diagnostico: str) -> Cita:
    """
    Marca cita como realizada y añade diagnóstico
    Args: cita_id (int), diagnostico (str)
    Return: Cita actualizada o None
    """

def cancelar_cita(cita_id: int) -> Cita:
    """
    Cancela una cita (cambia estado a 'cancelada') (RF15)
    Args: cita_id (int)
    Return: Cita cancelada o None si no existe
    """

# DELETE
def eliminar_cita(cita_id: int) -> bool:
    """
    Elimina una cita
    Args: cita_id (int)
    Return: True si éxito, False si error/no existe
    """

# AUXILIAR
def contar_citas() -> int:
    """
    Cuenta total de citas
    Args: ninguno
    Return: Número de citas (int)
    """

def cita_existe(cita_id: int) -> bool:
    """
    Verifica si existe cita con ese ID
    Args: cita_id (int)
    Return: True si existe, False si no
    """
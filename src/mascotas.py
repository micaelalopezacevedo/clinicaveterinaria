"""
título: módulo de mascotas
fecha: 11.11.2025
descrición: implementa toda la lógica relacionada con la gestión de mascotas.
Cubre los requisitos funcionales RF5-RF8:
- RF5: Registrar nuevas mascotas
- RF6: Modificar mascotas
- RF7: Eliminar mascotas
- RF8: Listar mascotas y ver historial
"""

from src.database import session, Mascota

# CREATE
def registrar_mascota(nombre: str, especie: str, cliente_id: int, raza: str = None, edad: int = None, peso: float = None, sexo: str = None) -> Mascota:
    """
    Registra nueva mascota asociada a cliente
    Args: nombre (str), especie (str), cliente_id (int), raza (str, opcional), 
          edad (int, opcional), peso (float, opcional), sexo (str, opcional)
    Return: Mascota creada o None si error
    """

# READ
def listar_mascotas() -> list:
    """
    Devuelve todas las mascotas
    Args: ninguno
    Return: Lista de mascotas
    """

def obtener_mascota_por_id(mascota_id: int) -> Mascota:
    """
    Busca mascota por ID
    Args: mascota_id (int)
    Return: Mascota encontrada o None
    """

def obtener_mascotas_por_cliente(cliente_id: int) -> list:
    """
    Devuelve todas las mascotas de un cliente
    Args: cliente_id (int)
    Return: Lista de mascotas del cliente
    """

def ver_historial_mascota(mascota_id: int) -> list:
    """
    Ver historial de citas de una mascota (RF8)
    Args: mascota_id (int)
    Return: Lista de citas de la mascota
    """

# UPDATE
def modificar_mascota(mascota_id: int, nombre: str = None, raza: str = None, edad: int = None, peso: float = None, sexo: str = None) -> Mascota:
    """
    Modifica datos de mascota existente
    Args: mascota_id (int), nombre (str, opcional), raza (str, opcional), 
          edad (int, opcional), peso (float, opcional), sexo (str, opcional)
    Return: Mascota modificada o None si no existe
    """

# DELETE
def eliminar_mascota(mascota_id: int) -> bool:
    """
    Elimina mascota (y sus citas asociadas)
    Args: mascota_id (int)
    Return: True si éxito, False si error/no existe
    """

# AUXILIAR
def contar_mascotas() -> int:
    """
    Cuenta total de mascotas
    Args: ninguno
    Return: Número de mascotas (int)
    """

def mascota_existe(mascota_id: int) -> bool:
    """
    Verifica si existe mascota con ese ID
    Args: mascota_id (int)
    Return: True si existe, False si no
    """
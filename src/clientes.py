"""
título: módulo de clientes
fecha: 11.11.2025
descripción: implementa toda la lógica relacionada con la gestión de clientes.
Cubre los requisitos funcionales RF1-RF4:
- RF1: Registrar nuevos clientes
- RF2: Consultar, editar y eliminar clientes
- RF3: Buscar clientes por nombre o DNI
- RF4: Listar todos los clientes
"""

from src.database import session, Cliente

# CREATE
def crear_cliente(nombre: str, dni: str, telefono: str = None, email: str = None) -> Cliente:
    """
    Crea nuevo cliente
    Args: nombre (str), dni (str), telefono (str, opcional), email (str, opcional)
    Return: Cliente creado o None si error
    """

# READ
def listar_clientes() -> list:
    """
    Devuelve todos los clientes
    Args: ninguno
    Return: Lista de clientes (vacía si no hay)
    """

def obtener_cliente_por_id(cliente_id: int) -> Cliente:
    """
    Busca cliente por ID
    Args: cliente_id (int)
    Return: Cliente encontrado o None
    """

def buscar_cliente_por_dni(dni: str) -> Cliente:
    """
    Busca cliente por DNI (búsqueda exacta)
    Args: dni (str)
    Return: Cliente encontrado o None
    """

def buscar_cliente_por_nombre(nombre: str) -> list:
    """
    Busca clientes por nombre (búsqueda parcial)
    Args: nombre (str)
    Return: Lista de clientes que coinciden
    """

# UPDATE
def modificar_cliente(cliente_id: int, nombre: str = None, telefono: str = None, email: str = None) -> Cliente:
    """
    Modifica datos de cliente existente
    Args: cliente_id (int), nombre (str, opcional), telefono (str, opcional), email (str, opcional)
    Return: Cliente modificado o None si no existe
    """

# DELETE
def eliminar_cliente(cliente_id: int) -> bool:
    """
    Elimina cliente (y sus mascotas asociadas)
    Args: cliente_id (int)
    Return: True si éxito, False si error/no existe
    """

# AUXILIAR
def contar_clientes() -> int:
    """
    Cuenta total de clientes
    Args: ninguno
    Return: Número de clientes (int)
    """

def cliente_existe(cliente_id: int) -> bool:
    """
    Verifica si existe cliente con ese ID
    Args: cliente_id (int)
    Return: True si existe, False si no
    """
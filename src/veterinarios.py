"""
título: módulo de veterinarios
fecha: 11.11.2025
descripción: implementa toda la lógica relacionada con la gestión de empleados.
Cubre los requisitos funcionales RF9-RF12:
- RF9: Registrar veterinarios
- RF10: Consultar veterinarios
- RF11: Eliminar veterinarios
- RF12: Analizar carga de trabajo
"""

from src.database import session, Veterinario

# CREATE
def registrar_veterinario(nombre: str, dni: str, cargo: str = None, especialidad: str = None, telefono: str = None, email: str = None) -> Veterinario:
    """
    Registra nuevo veterinario
    Args: nombre (str), dni (str), cargo (str, opcional), especialidad (str, opcional), 
          telefono (str, opcional), email (str, opcional)
    Return: Veterinario creado o None si error
    """

# READ
def listar_veterinarios() -> list:
    """
    Devuelve todos los veterinarios
    Args: ninguno
    Return: Lista de veterinarios
    """

def obtener_veterinario_por_id(veterinario_id: int) -> Veterinario:
    """
    Busca veterinario por ID
    Args: veterinario_id (int)
    Return: Veterinario encontrado o None
    """

def obtener_veterinarios_por_especialidad(especialidad: str) -> list:
    """
    Busca veterinarios por especialidad
    Args: especialidad (str)
    Return: Lista de veterinarios con esa especialidad
    """

def obtener_carga_veterinario(veterinario_id: int) -> int:
    """
    Devuelve número de citas asignadas a veterinario (RF12)
    Args: veterinario_id (int)
    Return: Número de citas (int)
    """

# DELETE
def eliminar_veterinario(veterinario_id: int) -> bool:
    """
    Elimina veterinario
    Args: veterinario_id (int)
    Return: True si éxito, False si error/no existe
    """

# AUXILIAR
def contar_veterinarios() -> int:
    """
    Cuenta total de veterinarios
    Args: ninguno
    Return: Número de veterinarios (int)
    """

def veterinario_existe(veterinario_id: int) -> bool:
    """
    Verifica si existe veterinario con ese ID
    Args: veterinario_id (int)
    Return: True si existe, False si no
    """
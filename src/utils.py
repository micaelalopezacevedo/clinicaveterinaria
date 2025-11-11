"""
título: módulo de utilidades
fecha: 11.11.2025
descripción: funciones auxiliares y validaciones para toda la aplicación.
Incluye validaciones de formato (DNI, email, teléfono),
formateo de datos y funciones de búsqueda.
"""

# VALIDACIONES
def validar_dni(dni: str) -> bool:
    """
    Valida formato de DNI español
    Args: dni (str)
    Return: True si válido, False si no (bool)
    """

def validar_email(email: str) -> bool:
    """
    Valida formato de email
    Args: email (str)
    Return: True si válido, False si no (bool)
    """

def validar_telefono(telefono: str) -> bool:
    """
    Valida formato de teléfono
    Args: telefono (str)
    Return: True si válido, False si no (bool)
    """

def validar_fecha(fecha_str: str) -> tuple:
    """
    Valida formato de fecha (YYYY-MM-DD)
    Args: fecha_str (str)
    Return: Tupla (es_válida (bool), mensaje_error (str))
    """

def validar_hora(hora_str: str) -> tuple:
    """
    Valida formato de hora (HH:MM)
    Args: hora_str (str)
    Return: Tupla (es_válida (bool), mensaje_error (str))
    """

# FORMATEO
def formatear_telefono(telefono: str) -> str:
    """
    Formatea teléfono a formato estándar
    Args: telefono (str)
    Return: Teléfono formateado (str)
    """

def formatear_dni(dni: str) -> str:
    """
    Convierte DNI a mayúsculas
    Args: dni (str)
    Return: DNI formateado (str)
    """

# BÚSQUEDAS Y FILTROS
def limpiar_busqueda(texto: str) -> str:
    """
    Limpia texto para búsquedas (trim, minúsculas)
    Args: texto (str)
    Return: Texto limpio (str)
    """
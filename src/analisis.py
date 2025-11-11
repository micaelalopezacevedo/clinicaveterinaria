"""
título: módulo de análisis
fecha: 11.11.2025
descripción: implementa estadísticas y reportes de la clínica.
Cubre los requisitos funcionales RF12 (carga de trabajo) y RF16 (próximas citas).
Proporciona dashboards y análisis de datos.
"""

# ESTADÍSTICAS GENERALES
def obtener_estadisticas_generales() -> dict:
    """
    Devuelve estadísticas generales de la clínica
    Args: ninguno
    Return: dict con total_clientes, total_mascotas, total_veterinarios, 
            total_citas, citas_pendientes
    """

def obtener_total_clientes() -> int:
    """
    Cuenta total de clientes
    Args: ninguno
    Return: Número de clientes (int)
    """

def obtener_total_mascotas() -> int:
    """
    Cuenta total de mascotas
    Args: ninguno
    Return: Número de mascotas (int)
    """

def obtener_total_citas() -> int:
    """
    Cuenta total de citas
    Args: ninguno
    Return: Número de citas (int)
    """

def obtener_citas_pendientes() -> int:
    """
    Cuenta citas con estado 'pendiente'
    Args: ninguno
    Return: Número de citas pendientes (int)
    """

# ANÁLISIS DE VETERINARIOS
def obtener_carga_veterinarios() -> list:
    """
    Devuelve carga de trabajo de cada veterinario (RF12)
    Args: ninguno
    Return: Lista de dicts con: veterinario_id (int), nombre (str), num_citas (int)
    """

def obtener_veterinario_con_mas_citas() -> dict:
    """
    Encuentra veterinario con más citas asignadas
    Args: ninguno
    Return: dict con id (int), nombre (str), num_citas (int)
    """

# ANÁLISIS DE MASCOTAS
def obtener_especie_mas_comun() -> str:
    """
    Devuelve la especie de mascota más registrada
    Args: ninguno
    Return: Nombre de la especie (str)
    """

def obtener_mascotas_por_especie() -> dict:
    """
    Cuenta mascotas agrupadas por especie
    Args: ninguno
    Return: dict con especie (str): cantidad (int)
    """

# PRÓXIMAS CITAS
def obtener_proximas_citas_hoy() -> list:
    """
    Devuelve citas programadas para hoy (RF16)
    Args: ninguno
    Return: Lista de citas de hoy
    """

def obtener_proximas_citas_semana() -> list:
    """
    Devuelve citas de la próxima semana (RF16)
    Args: ninguno
    Return: Lista de citas de los próximos 7 días
    """

def obtener_proximas_citas_mes() -> list:
    """
    Devuelve citas del próximo mes (RF16)
    Args: ninguno
    Return: Lista de citas de los próximos 30 días
    """
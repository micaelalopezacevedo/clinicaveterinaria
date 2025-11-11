"""
título: módulo de utilidades
fecha: 11.11.2025
descripción: clase estática Utilidades que agrupa funciones auxiliares.
Todos los métodos son estáticos.
Incluye validaciones, formateo y funciones auxiliares.
"""

class Utilidades:
    """
    Clase estática con funciones de utilidad para la aplicación
    Agrupa validaciones, formateos y funciones auxiliares
    """
    
    # VALIDACIONES
    @staticmethod
    def validar_dni(dni: str) -> bool:
        """
        Valida formato de DNI español (8 números + 1 letra)
        Args: dni (str)
        Return: True si válido, False si no (bool)
        Formato esperado: 12345678A
        """
    
    @staticmethod
    def validar_email(email: str) -> bool:
        """
        Valida formato básico de email
        Args: email (str)
        Return: True si válido, False si no (bool)
        Verifica: presencia de @ y dominio
        """
    
    @staticmethod
    def validar_telefono(telefono: str) -> bool:
        """
        Valida formato de teléfono español (9 dígitos)
        Args: telefono (str)
        Return: True si válido, False si no (bool)
        Formato esperado: 600123456 o 600-123-456
        """
    
    @staticmethod
    def validar_fecha(fecha_str: str) -> tuple:
        """
        Valida formato de fecha (YYYY-MM-DD)
        Args: fecha_str (str)
        Return: Tupla (es_válida (bool), mensaje_error (str))
        Ejemplo: ("2025-11-15") -> (True, "")
        """
    
    @staticmethod
    def validar_hora(hora_str: str) -> tuple:
        """
        Valida formato de hora (HH:MM)
        Args: hora_str (str)
        Return: Tupla (es_válida (bool), mensaje_error (str))
        Ejemplo: ("14:30") -> (True, "")
        """
    
    @staticmethod
    def validar_edad(edad: int) -> bool:
        """
        Valida que edad esté en rango lógico (0-50 años para mascotas)
        Args: edad (int)
        Return: True si válido, False si no (bool)
        """
    
    @staticmethod
    def validar_peso(peso: float) -> bool:
        """
        Valida que peso sea positivo y mayor a 0
        Args: peso (float)
        Return: True si válido, False si no (bool)
        """
    
    # FORMATEO
    @staticmethod
    def formatear_dni(dni: str) -> str:
        """
        Formatea DNI: convierte a mayúsculas y elimina espacios
        Args: dni (str)
        Return: DNI formateado (str)
        Ejemplo: "12345678 a" -> "12345678A"
        """
    
    @staticmethod
    def formatear_telefono(telefono: str) -> str:
        """
        Formatea teléfono: elimina guiones y espacios
        Args: telefono (str)
        Return: Teléfono formateado (str)
        Ejemplo: "600-123-456" -> "600123456"
        """
    
    @staticmethod
    def formatear_nombre(nombre: str) -> str:
        """
        Formatea nombre: capitaliza primera letra de cada palabra
        Args: nombre (str)
        Return: Nombre formateado (str)
        Ejemplo: "juan pérez" -> "Juan Pérez"
        """
    
    @staticmethod
    def formatear_email(email: str) -> str:
        """
        Formatea email: convierte a minúsculas y elimina espacios
        Args: email (str)
        Return: Email formateado (str)
        Ejemplo: "JUAN@EMAIL.COM " -> "juan@email.com"
        """
    
    # BÚSQUEDAS Y FILTROS
    @staticmethod
    def limpiar_busqueda(texto: str) -> str:
        """
        Limpia texto para búsquedas: minúsculas, sin espacios extra
        Args: texto (str)
        Return: Texto limpio (str)
        Uso: Para búsquedas insensibles a mayúsculas
        """
    
    @staticmethod
    def truncar_texto(texto: str, longitud: int) -> str:
        """
        Trunca texto a una longitud máxima con puntos suspensivos
        Args: texto (str), longitud (int)
        Return: Texto truncado (str)
        Ejemplo: ("Descripción larga", 10) -> "Descripci..."
        """
    
    # CONVERSIONES
    @staticmethod
    def edad_a_meses(edad_anos: int) -> int:
        """
        Convierte edad de años a meses
        Args: edad_anos (int)
        Return: Edad en meses (int)
        """
    
    @staticmethod
    def meses_a_edad(meses: int) -> float:
        """
        Convierte edad de meses a años
        Args: meses (int)
        Return: Edad en años (float)
        """
    
    # UTILIDADES GENERALES
    @staticmethod
    def es_vacio(valor: str) -> bool:
        """
        Verifica si un valor es vacío o solo contiene espacios
        Args: valor (str)
        Return: True si está vacío, False si no (bool)
        """
    
    @staticmethod
    def obtener_edad_desde_fecha(fecha_nacimiento: str) -> int:
        """
        Calcula edad a partir de fecha de nacimiento
        Args: fecha_nacimiento (str, formato YYYY-MM-DD)
        Return: Edad en años (int)
        """

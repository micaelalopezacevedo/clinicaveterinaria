"""
título: módulo de utilidades
fecha: 11.11.2025
descripción: clase estática Utilidades que agrupa funciones auxiliares.
Todos los métodos son estáticos.
Incluye validaciones, formateo, búsquedas, conversiones y funciones auxiliares.

CAMBIOS:
- Se mantienen TODOS los métodos originales
- Se añaden nuevos métodos específicos para citas
- Organización clara por categorías de funcionalidad
"""

import re
from datetime import datetime, time, date


class Utilidades:
    """
    Clase estática con funciones de utilidad para la aplicación
    Agrupa validaciones, formateos, búsquedas, conversiones y funciones auxiliares
    """
    
    # ====== VALIDACIONES GENÉRICAS ======
    
    @staticmethod
    def validar_nombre(nombre: str) -> bool:
        """Valida que nombre solo contenga letras"""
        nombre = nombre.lower().strip()
        patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ -]+$"
        return re.match(patron, nombre)
    
    @staticmethod
    def validar_dni(dni: str) -> bool:
        """
        Valida formato de DNI español (8 números + 1 letra)
        Args: dni (str)
        Return: True si válido, False si no (bool)
        Formato esperado: 12345678A
        """
        # FORMATEO
        dni = dni.upper().strip()
        
        # CONSTRUIR UN PATRÓN CON RE
        patron = r"^\d{8}[A-Z]$"
        return re.match(patron, dni) is not None
    
    @staticmethod
    def validar_email(email: str) -> bool:
        """
        Valida formato básico de email
        Args: email (str)
        Return: True si válido, False si no (bool)
        Verifica: presencia de @ y dominio
        """
        # FORMATEO
        email = email.lower().strip()
        
        patron = r"^[\w\.-]+@[\w\.-]+\.[A-Za-z]{2,}$"
        
        return re.match(patron, email) is not None
    
    @staticmethod
    def validar_telefono(telefono: str) -> bool:
        """
        Valida formato de teléfono español (9 dígitos)
        Args: telefono (str)
        Return: True si válido, False si no (bool)
        Formato esperado: 600123456 o 600-123-456
        """
        # FORMATEO - CONTEMPLAR SI HAY ESPACIOS
        telefono = telefono.split()  # Separar en lista por espacios
        separator = ""
        telefono = separator.join(telefono)  # Juntar en un mismo string
        telefono = telefono.strip()
        
        patron = r"^\d{9}$"
        return re.match(patron, telefono) is not None
    
    @staticmethod
    def validar_fecha(fecha_str: str) -> tuple:
        """
        Valida formato de fecha (YYYY-MM-DD)
        Args: fecha_str (str)
        Return: Tupla (es_válida (bool), mensaje_error (str))
        Ejemplo: ("2025-11-15") -> (True, "")
        """
        try:
            datetime.strptime(fecha_str, "%Y-%m-%d")
            return True, ""
        except ValueError:
            return False, "Formato de fecha inválido. Use YYYY-MM-DD"
    
    @staticmethod
    def validar_hora(hora_str: str) -> tuple:
        """
        Valida formato de hora (HH:MM)
        Args: hora_str (str)
        Return: Tupla (es_válida (bool), mensaje_error (str))
        Ejemplo: ("14:30") -> (True, "")
        """
        try:
            datetime.strptime(hora_str, "%H:%M")
            return True, ""
        except ValueError:
            return False, "Formato de hora inválido. Use HH:MM"
    
    @staticmethod
    def validar_edad(edad: int) -> bool:
        """
        Valida que edad esté en rango lógico (0-50 años para mascotas)
        Args: edad (int)
        Return: True si válido, False si no (bool)
        """
        return 0 <= edad <= 50
    
    @staticmethod
    def validar_peso(peso: float) -> bool:
        """
        Valida que peso sea positivo y mayor a 0
        Args: peso (float)
        Return: True si válido, False si no (bool)
        """
        return peso > 0
    
    @staticmethod
    def es_vacio(valor: str) -> bool:
        """
        Verifica si un valor es vacío o solo contiene espacios
        Args: valor (str)
        Return: True si está vacío, False si no (bool)
        """
        return not valor or len(valor.strip()) == 0
    
    # ====== VALIDACIONES ESPECÍFICAS PARA CITAS ======
    
    @staticmethod
    def validar_hora_laboral(hora: time) -> bool:
        """Valida que hora esté en horario laboral (09:00 - 17:00)"""
        hora_inicio = time(9, 0)
        hora_fin = time(17, 0)
        return hora_inicio <= hora <= hora_fin
    
    @staticmethod
    def validar_fecha_no_pasada(fecha: date, hora: time) -> bool:
        """Valida que fecha/hora no sea en el pasado"""
        fecha_hora_cita = datetime.combine(fecha, hora)
        return fecha_hora_cita >= datetime.now()
    
    @staticmethod
    def validar_campos_cita(mascota_id: int, veterinario_id: int, fecha: date, hora: time) -> tuple:
        """
        Valida TODOS los campos de una cita de forma centralizada
        Return: (es_válido: bool, mensaje_error: str)
        """
        if not mascota_id or not veterinario_id or not fecha or not hora:
            return False, "Mascota, veterinario, fecha y hora son campos obligatorios"
        
        if not Utilidades.validar_fecha_no_pasada(fecha, hora):
            return False, "No se pueden crear citas en el pasado"
        
        if not Utilidades.validar_hora_laboral(hora):
            return False, "La hora debe estar entre 09:00 y 17:00"
        
        return True, ""
    
    # ====== FORMATEO ======
    # SUPUESTO: AL FORMATEAR UN DATO; SE ASUME QUE YA HA PASADO POR VALIDACIONES
    
    @staticmethod
    def formatear_dni(dni: str) -> str:
        """
        Formatea DNI: convierte a mayúsculas y elimina espacios
        Args: dni (str)
        Return: DNI formateado (str)
        Ejemplo: "12345678 a" -> "12345678A"
        """
        dni = dni.upper().strip()
        return dni
    
    @staticmethod
    def formatear_telefono(telefono: str) -> str:
        """
        Formatea teléfono: elimina guiones y espacios
        Args: telefono (str)
        Return: Teléfono formateado (str)
        Ejemplo: "600-123-456" -> "600123456"
        """
        # CONTEMPLAR SI HAY ESPACIOS
        telefono = telefono.split()  # Separar en lista por espacios
        separator = ""
        telefono = separator.join(telefono)  # Juntar en un mismo string
        telefono = telefono.strip()
        
        return telefono
    
    @staticmethod
    def formatear_nombre(nombre: str) -> str:
        """
        Formatea nombre: capitaliza primera letra de cada palabra
        Args: nombre (str)
        Return: Nombre formateado (str)
        Ejemplo: "juan pérez" -> "Juan Pérez"
        """
        nombre = nombre.strip().lower()
        return nombre.title()
    
    @staticmethod
    def formatear_email(email: str) -> str:
        """
        Formatea email: convierte a minúsculas y elimina espacios
        Args: email (str)
        Return: Email formateado (str)
        Ejemplo: "JUAN@EMAIL.COM " -> "juan@email.com"
        """
        email = email.lower().strip()
        return email
    
    # ====== FORMATEO ESPECÍFICO PARA CITAS ======
    
    @staticmethod
    def convertir_hora_a_string(hora: time) -> str:
        """Convierte objeto time a string formato HH:MM"""
        if isinstance(hora, time):
            return hora.strftime('%H:%M')
        return hora
    
    @staticmethod
    def convertir_string_a_hora(hora_str: str) -> time:
        """Convierte string formato HH:MM a objeto time"""
        return datetime.strptime(hora_str, '%H:%M').time()
    
    @staticmethod
    def formatear_fecha(fecha: date) -> str:
        """Formatea fecha a DD/MM/YYYY"""
        return fecha.strftime('%d/%m/%Y')
    
    @staticmethod
    def obtener_icono_estado_cita(estado: str) -> str:
        """Devuelve emoji según estado de cita"""
        iconos = {
            "Pendiente": "🕐",
            "Confirmada": "✅",
            "Realizada": "✔️",
            "Cancelada": "❌"
        }
        return iconos.get(estado, "📋")
    
    # ====== BÚSQUEDAS Y FILTROS ======
    
    @staticmethod
    def limpiar_busqueda(texto: str) -> str:
        """
        Limpia texto para búsquedas: minúsculas, sin espacios extra
        Args: texto (str)
        Return: Texto limpio (str)
        Uso: Para búsquedas insensibles a mayúsculas
        """
        return texto.lower().strip()
    
    @staticmethod
    def truncar_texto(texto: str, longitud: int) -> str:
        """
        Trunca texto a una longitud máxima con puntos suspensivos
        Args: texto (str), longitud (int)
        Return: Texto truncado (str)
        Ejemplo: ("Descripción larga", 10) -> "Descripci..."
        """
        if len(texto) > longitud:
            return texto[:longitud] + "..."
        return texto
    
    # ====== CONVERSIONES ======
    
    @staticmethod
    def edad_a_meses(edad_anos: int) -> int:
        """
        Convierte edad de años a meses
        Args: edad_anos (int)
        Return: Edad en meses (int)
        """
        return edad_anos * 12
    
    @staticmethod
    def meses_a_edad(meses: int) -> float:
        """
        Convierte edad de meses a años
        Args: meses (int)
        Return: Edad en años (float)
        """
        return round(meses / 12, 1)
    
    @staticmethod
    def computarEmoticonoEspecie(especie):
        return("🐶" if especie == "Perro" 
                                 else "🐱" if especie == "Gato" 
                                 else "🐦" if especie == "Pájaro"
                                 else "🐇" if especie == "Conejo"
                                 else "🐾")

    
    @staticmethod
    def obtener_edad_desde_fecha(fecha_nacimiento: str) -> int:
        """
        Calcula edad a partir de fecha de nacimiento
        Args: fecha_nacimiento (str, formato YYYY-MM-DD)
        Return: Edad en años (int)
        """
        try:
            fecha_nac = datetime.strptime(fecha_nacimiento, "%Y-%m-%d").date()
            hoy = date.today()
            edad = hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))
            return edad
        except ValueError:
            return 0

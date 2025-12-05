import pytest
from datetime import date, time, datetime, timedelta
from src.utils import Utilidades

class TestValidaciones:
    """Pruebas para funciones de validación genéricas"""

    def test_validar_dni_correcto(self):
        """Test: validar DNI con formato correcto (8 números + Letra)."""
        assert Utilidades.validar_dni("12345678A") is True
        assert Utilidades.validar_dni("87654321Z") is True
        # Prueba minúsculas que deberían ser válidas por el .upper() interno
        assert Utilidades.validar_dni("12345678a") is True

    def test_validar_dni_incorrecto(self):
        """Test: validar DNI con formato incorrecto."""
        assert Utilidades.validar_dni("1234567") is False   # Falta número
        assert Utilidades.validar_dni("12345678") is False  # Falta letra
        assert Utilidades.validar_dni("ABC45678A") is False # Letras al inicio

    def test_validar_email_correcto(self):
        """Test: validar email con formato correcto."""
        assert Utilidades.validar_email("test@dominio.com") is True
        assert Utilidades.validar_email("nombre.apellido@empresa.es") is True

    def test_validar_email_incorrecto(self):
        """Test: validar email con formato incorrecto."""
        assert Utilidades.validar_email("correo_sin_arroba.com") is False
        assert Utilidades.validar_email("juan@dominio") is False # Falta .com/.es
        assert Utilidades.validar_email("@dominio.com") is False # Falta usuario

    def test_validar_telefono_correcto(self):
        """Test: validar teléfono con formato correcto (9 dígitos)."""
        assert Utilidades.validar_telefono("600123456") is True
        # El código contempla separadores porque hace split y join
        assert Utilidades.validar_telefono("600 123 456") is True

    def test_validar_telefono_incorrecto(self):
        """Test: validar teléfono con formato incorrecto."""
        assert Utilidades.validar_telefono("12345") is False # Muy corto
        assert Utilidades.validar_telefono("60012345678") is False # Muy largo
        assert Utilidades.validar_telefono("teléfono") is False # Letras

    def test_validar_fecha_correcta(self):
        """Test: validar fecha con formato correcto (YYYY-MM-DD)."""
        valido, msg = Utilidades.validar_fecha("2025-11-15")
        assert valido is True
        assert msg == ""

    def test_validar_fecha_incorrecta(self):
        """Test: validar fecha con formato incorrecto."""
        valido, msg = Utilidades.validar_fecha("15-11-2025") # Formato al revés
        assert valido is False
        assert "inválido" in msg
        
        valido, msg = Utilidades.validar_fecha("2025/11/15") # Separador incorrecto
        assert valido is False

    def test_validar_hora_correcta(self):
        """Test: validar hora con formato correcto (HH:MM)."""
        valido, msg = Utilidades.validar_hora("14:30")
        assert valido is True
        
        valido, msg = Utilidades.validar_hora("09:05")
        assert valido is True

    def test_validar_hora_incorrecta(self):
        """Test: validar hora con formato incorrecto."""
        valido, msg = Utilidades.validar_hora("25:00") # Hora imposible
        assert valido is False
        
        valido, msg = Utilidades.validar_hora("14-30") # Separador incorrecto
        assert valido is False

class TestFormateo:
    """Pruebas para funciones de formateo"""

    def test_formatear_telefono(self):
        """Test: formatear teléfono a formato estándar (sin espacios/guiones)."""
        assert Utilidades.formatear_telefono("600 123 456") == "600123456"
        assert Utilidades.formatear_telefono("  666-777-888  ") == "666777888"

    def test_formatear_dni(self):
        """Test: convertir DNI a mayúsculas y quitar espacios."""
        assert Utilidades.formatear_dni("  12345678z  ") == "12345678Z"

    def test_formatear_nombre(self):
        """Test: Capitalizar nombres."""
        assert Utilidades.formatear_nombre("juan perez") == "Juan Perez"
        assert Utilidades.formatear_nombre("ANA GARCIA") == "Ana Garcia"

class TestBusquedas:
    """Pruebas para funciones de búsqueda y filtros"""

    def test_limpiar_busqueda(self):
        """Test: limpiar texto para búsquedas (lowercase + trim)."""
        assert Utilidades.limpiar_busqueda("  BusCando  ") == "buscando"

    def test_truncar_texto(self):
        """Test: cortar textos largos."""
        texto = "Hola Mundo"
        assert Utilidades.truncar_texto(texto, 4) == "Hola..."
        assert Utilidades.truncar_texto(texto, 20) == "Hola Mundo" # No corta si es corto

# ==========================================
# NUEVAS CLASES (Faltaban en tu esqueleto)
# ==========================================

class TestValidacionesCitas:
    """Pruebas específicas para la lógica de Citas"""
    
    def test_validar_hora_laboral(self):
        """Test: Verificar rango 09:00 - 17:00."""
        assert Utilidades.validar_hora_laboral(time(9, 0)) is True  # Límite inferior
        assert Utilidades.validar_hora_laboral(time(17, 0)) is True # Límite superior
        assert Utilidades.validar_hora_laboral(time(12, 30)) is True # Medio
        
        assert Utilidades.validar_hora_laboral(time(8, 59)) is False # Muy pronto
        assert Utilidades.validar_hora_laboral(time(17, 0o1)) is False # Muy tarde

    def test_validar_fecha_no_pasada(self):
        """Test: No permitir fechas anteriores a hoy."""
        hoy = date.today()
        ayer = hoy - timedelta(days=1)
        manana = hoy + timedelta(days=1)
        hora = time(10, 0)
        
        assert Utilidades.validar_fecha_no_pasada(manana, hora) is True
        assert Utilidades.validar_fecha_no_pasada(ayer, hora) is False
    
    def test_validar_campos_cita_completo(self):
        """Test: Validación integradora de campos de cita."""
        # Caso correcto
        valido, msg = Utilidades.validar_campos_cita(
            mascota_id=1, 
            veterinario_id=1, 
            fecha=date.today() + timedelta(days=1), 
            hora=time(10, 0)
        )
        assert valido is True
        
        # Caso falta dato
        valido, msg = Utilidades.validar_campos_cita(None, 1, date.today(), time(10,0))
        assert valido is False
        assert "obligatorios" in msg

class TestConversiones:
    """Pruebas para cálculos de edad y conversiones"""
    
    def test_edad_a_meses(self):
        assert Utilidades.edad_a_meses(2) == 24
        
    def test_obtener_edad_desde_fecha(self):
        """Test: Calcular edad basada en nacimiento."""
        # Calculamos una fecha de hace exactamente 10 años
        hace_10_anos = date.today().replace(year=date.today().year - 10)
        fecha_str = hace_10_anos.strftime("%Y-%m-%d")
        
        assert Utilidades.obtener_edad_desde_fecha(fecha_str) == 10
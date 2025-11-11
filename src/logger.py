"""
título: módulo de logger (registro de eventos)
fecha: 11.11.2025
descripción: clase estática para logging centralizado de la aplicación.
Registra eventos en consola y en archivo logs/clinica.log.
Todos los métodos son estáticos.
"""

import logging
from datetime import datetime

class Logger:
    """
    Clase estática para manejar el logging de la aplicación
    Registra eventos en consola y archivo
    """
    
    # CONFIGURACIÓN INICIAL
    @staticmethod
    def configurar_logger() -> None:
        """
        Configura el sistema de logging de la aplicación
        Args: ninguno
        Return: None
        Crea archivo logs/clinica.log y configura formato
        """
    
    # MÉTODOS DE LOGGING
    @staticmethod
    def debug(mensaje: str) -> None:
        """
        Registra mensaje de DEBUG (información detallada para diagnosticar)
        Args: mensaje (str)
        Return: None
        Nivel: DEBUG (más bajo, muy detallado)
        """
    
    @staticmethod
    def info(mensaje: str) -> None:
        """
        Registra mensaje INFO (información general de ejecución)
        Args: mensaje (str)
        Return: None
        Nivel: INFO (confirmaciones de eventos normales)
        """
    
    @staticmethod
    def warning(mensaje: str) -> None:
        """
        Registra mensaje WARNING (advertencia, algo podría ir mal)
        Args: mensaje (str)
        Return: None
        Nivel: WARNING (algo inusual pero no es error)
        """
    
    @staticmethod
    def error(mensaje: str) -> None:
        """
        Registra mensaje ERROR (error grave, algo falló)
        Args: mensaje (str)
        Return: None
        Nivel: ERROR (algo falló pero el programa continúa)
        """
    
    @staticmethod
    def critical(mensaje: str) -> None:
        """
        Registra mensaje CRITICAL (error crítico, situación grave)
        Args: mensaje (str)
        Return: None
        Nivel: CRITICAL (más alto, algo muy grave pasó)
        """
    
    # MÉTODO ESPECIAL PARA EXCEPCIONES
    @staticmethod
    def log_excepcion(excepcion: Exception, contexto: str = "") -> None:
        """
        Registra una excepción con traceback completo
        Args: excepcion (Exception), contexto (str, opcional)
        Return: None
        Uso: Llamar en bloques except para registrar error con traceback
        """
    
    # MÉTODOS AUXILIARES
    @staticmethod
    def obtener_timestamp() -> str:
        """
        Devuelve timestamp actual formateado
        Args: ninguno
        Return: timestamp (str, formato: YYYY-MM-DD HH:MM:SS)
        """
    
    @staticmethod
    def limpiar_logs() -> None:
        """
        Limpia el archivo de logs (borra todo el contenido)
        Args: ninguno
        Return: None
        """
    
    @staticmethod
    def obtener_tamaño_logs() -> int:
        """
        Obtiene tamaño del archivo de logs en bytes
        Args: ninguno
        Return: tamaño (int, en bytes)
        """

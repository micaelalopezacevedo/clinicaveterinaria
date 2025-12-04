"""
título: módulo de logger (registro de eventos)
fecha: 11.11.2025
descripción: clase estática para logging centralizado de la aplicación.
Registra eventos en consola y en archivo logs/clinica.log.
Todos los métodos son estáticos.
"""

import logging
import os
from datetime import datetime


class Logger:
    """
    Clase estática para manejar el logging de la aplicación.
    Registra eventos en consola y archivo.

    Arquitectura:
    - Singleton pattern: un logger global para toda la app
    - DEBUG en archivo (máxima información)
    - WARNING en consola (solo problemas)
    - Archivo: logs/app.log
    """

    _logger = None
    _logfile = "logs/app.log"

    @classmethod
    def _get_logger(cls):
        """Obtiene o crea la instancia global del logger."""
        if cls._logger is None:

            # Crear carpeta logs si no existe
            os.makedirs('logs', exist_ok=True)

            # Crear logger global
            cls._logger = logging.getLogger("clinica_veterinaria")
            cls._logger.setLevel(logging.DEBUG)

            # Evitar añadir handlers duplicados
            if cls._logger.hasHandlers():
                cls._logger.handlers.clear()

            # Formato de salida
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )

            # Handler archivo (DEBUG – máximo detalle)
            try:
                file_handler = logging.FileHandler(cls._logfile, encoding="utf-8")
                file_handler.setLevel(logging.DEBUG)
                file_handler.setFormatter(formatter)
                cls._logger.addHandler(file_handler)
            except Exception as e:
                print(f"[Logger] Error configurando file handler: {e}")

            # Handler consola (WARNING+)
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.WARNING)
            console_handler.setFormatter(formatter)
            cls._logger.addHandler(console_handler)

        return cls._logger

    # ================================
    # CONFIGURACIÓN
    # ================================

    @staticmethod
    def configurar_logger() -> None:
        """
        Configura el logger explícitamente.
        (Recomendación: llamar desde main.py)
        """
        logger = Logger._get_logger()
        logger.info("Logger configurado correctamente")

    # ================================
    # MÉTODOS DE LOGGING
    # ================================

    @staticmethod
    def debug(mensaje: str) -> None:
        Logger._get_logger().debug(f"🔍 {mensaje}")

    @staticmethod
    def info(mensaje: str) -> None:
        Logger._get_logger().info(f"✅ {mensaje}")

    @staticmethod
    def warning(mensaje: str) -> None:
        Logger._get_logger().warning(f"⚠ {mensaje}")

    @staticmethod
    def error(mensaje: str) -> None:
        Logger._get_logger().error(f"❌ {mensaje}")

    @staticmethod
    def critical(mensaje: str) -> None:
        Logger._get_logger().critical(f"🔴 {mensaje}")

    # ================================
    # LOG DE EXCEPCIONES
    # ================================

    @staticmethod
    def log_excepcion(excepcion: Exception, contexto: str = "") -> None:
        """
        Registra una excepción con traceback completo.
        """
        logger = Logger._get_logger()
        if contexto:
            logger.error(f"❌ Error en {contexto}: {excepcion}", exc_info=True)
        else:
            logger.error(f"❌ Excepción: {excepcion}", exc_info=True)

    # ================================
    # MÉTODOS AUXILIARES
    # ================================

    @staticmethod
    def obtener_timestamp() -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def limpiar_logs() -> None:
        """Borra el contenido del archivo de logs."""
        try:
            if os.path.exists(Logger._logfile):
                with open(Logger._logfile, "w"):
                    pass
                Logger.info("Logs limpios")
        except Exception as e:
            Logger.error(f"Error limpiando logs: {e}")

    @staticmethod
    def obtener_tamaño_logs() -> int:
        """Devuelve el tamaño de logs en bytes."""
        try:
            if os.path.exists(Logger._logfile):
                return os.path.getsize(Logger._logfile)
            return 0
        except Exception as e:
            Logger.warning(f"Error obteniendo tamaño logs: {e}")
            return 0


# ⚠️ IMPORTANTE:
# Se debe llamar desde main.py:
#
#   from src.logger import Logger
#   Logger.configurar_logger()
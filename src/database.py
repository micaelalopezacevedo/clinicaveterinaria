"""
título: capa de base de datos
fecha: 11.11.2025
descripcion: clase DatabaseConnector que gestiona la conexión a SQLite.
Gestiona engine, sesiones, creación de tablas y relaciones.
Define también los 4 modelos: Cliente, Mascota, Veterinario, Cita.
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Base declarativa
Base = declarative_base()

class Cliente(Base):
    """
    TABLA: clientes
    Almacena información de los dueños de mascotas
    Campos: id, nombre, dni, teléfono, email
    Relación: mascotas (1:N)
    """
    __tablename__ = 'clientes'
    # Define aquí: id, nombre, dni, teléfono, email, relación mascotas

class Mascota(Base):
    """
    TABLA: mascotas
    Almacena información de los animales
    Campos: id, nombre, especie, raza, edad, peso, sexo, cliente_id
    Relaciones: cliente (N:1), citas (1:N)
    """
    __tablename__ = 'mascotas'
    # Define aquí: id, nombre, especie, raza, edad, peso, sexo, cliente_id, relaciones

class Veterinario(Base):
    """
    TABLA: veterinarios
    Almacena información del personal
    Campos: id, nombre, dni, cargo, especialidad, teléfono, email
    Relación: citas (1:N)
    """
    __tablename__ = 'veterinarios'
    # Define aquí: id, nombre, dni, cargo, especialidad, teléfono, email, relación citas

class Cita(Base):
    """
    TABLA: citas
    Almacena información de las citas veterinarias
    Campos: id, fecha, hora, motivo, diagnóstico, estado, mascota_id, veterinario_id
    Relaciones: mascota (N:1), veterinario (N:1)
    """
    __tablename__ = 'citas'
    # Define aquí: id, fecha, hora, motivo, diagnóstico, estado, mascota_id, veterinario_id, relaciones

class DatabaseConnector:
    """
    Clase que gestiona la conexión a la base de datos SQLite
    Centraliza todas las operaciones de BD
    """
    
    def __init__(self, db_path: str = 'clinica.db'):
        """
        Constructor del DatabaseConnector
        Args: db_path (str, ruta del archivo .db, por defecto 'clinica.db')
        Return: Objeto DatabaseConnector
        Inicializa: engine, Base, Session, ruta BD
        """
    
    def conectar(self) -> bool:
        """
        Conecta a la base de datos y crea las tablas si no existen
        Args: ninguno
        Return: True si conexión exitosa, False si error
        Lanza: DatabaseConnectionException si falla la conexión
        """
    
    def desconectar(self) -> None:
        """
        Cierra la sesión y desconecta de la BD
        Args: ninguno
        Return: None
        Limpia: Cierra session y libera recursos
        """
    
    def crear_tablas(self) -> bool:
        """
        Crea todas las tablas en la base de datos
        Args: ninguno
        Return: True si éxito, False si error
        Usa: Base.metadata.create_all(engine)
        """
    
    def obtener_sesion(self):
        """
        Devuelve la sesión actual de la BD
        Args: ninguno
        Return: objeto sesión (SQLAlchemy Session)
        Uso: Para realizar operaciones CRUD
        """
    
    def verificar_conexion(self) -> bool:
        """
        Verifica que la conexión a la BD es válida y está activa
        Args: ninguno
        Return: True si está conectado, False si no
        """
    
    def obtener_engine(self):
        """
        Devuelve el engine de SQLAlchemy
        Args: ninguno
        Return: objeto engine (Engine)
        Uso: Operaciones avanzadas con SQLAlchemy
        """
    
    def vaciar_tablas(self) -> None:
        """
        Elimina todos los datos de todas las tablas (DESTRUCTIVO)
        Args: ninguno
        Return: None
        CUIDADO: Solo usar en testing, NUNCA en producción
        """
    
    def obtener_tamaño_bd(self) -> int:
        """
        Devuelve el tamaño del archivo BD en bytes
        Args: ninguno
        Return: Tamaño en bytes (int)
        """

# Crear instancia global del conector
db = DatabaseConnector()
db.conectar()

# Exportar sesión global para usar en otros módulos
session = db.obtener_sesion()
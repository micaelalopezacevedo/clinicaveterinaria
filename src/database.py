"""
título: capa de base de datos
fecha: 03.12.2025
descripcion: clase DatabaseConnector que gestiona la conexión a SQLite.

Gestiona engine, sesiones, creación de tablas y relaciones.
Define también los 4 modelos: Cliente, Mascota, Veterinario, Cita.
"""

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    Date,
    ForeignKey,
    event,
)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# ==========================================
# 1. MOTOR DE BASE DE DATOS (ENGINE)
# ==========================================

# echo=False para que no saque SQL por consola
engine = create_engine("sqlite:///clinica.db", echo=False)

# 🔐 Activar claves foráneas en SQLite (IMPORTANTE para CASCADE)
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON;")
    cursor.close()

# ==========================================
# 2. BASE DECLARATIVA
# ==========================================

Base = declarative_base()

# ==========================================
# 3. MODELOS (TABLAS)
# ==========================================

class Cliente(Base):
    """
    TABLA: clientes
    ===============
    Almacena información de los dueños de las mascotas.
    """
    __tablename__ = "clientes"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    dni = Column(String(20), unique=True, nullable=False)
    telefono = Column(String(20))
    email = Column(String(100))
    
    # CASCADE REAL hacia Mascota (y de ahí a Cita)
    # ❌ PROBLEMA: passive_deletes=True desactiva el cascade de SQLAlchemy
    # ✅ SOLUCIÓN: Quitarlo para que SQLAlchemy maneje el cascade
    mascotas = relationship(
        "Mascota",
        back_populates="cliente",
        cascade="all, delete-orphan",
    )
    
    def __repr__(self):
        return f"<Cliente id={self.id} nombre={self.nombre}>"


class Mascota(Base):
    """
    TABLA: mascotas
    ===============
    Almacena información de los animales.
    """
    __tablename__ = "mascotas"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    especie = Column(String(50), nullable=False)
    raza = Column(String(50))
    edad = Column(Integer)
    peso = Column(Float)
    sexo = Column(String(10))  # 'Macho' / 'Hembra' / etc.
    
    # FK con CASCADE REAL hacia Cliente
    cliente_id = Column(
        Integer,
        ForeignKey("clientes.id", ondelete="CASCADE"),
        nullable=False,
    )
    
    # Relaciones
    cliente = relationship("Cliente", back_populates="mascotas")
    
    # Al borrar mascota → borrar sus citas
    citas = relationship(
        "Cita",
        back_populates="mascota",
        cascade="all, delete-orphan",
    )
    
    def __repr__(self):
        return f"<Mascota id={self.id} nombre={self.nombre}>"


class Veterinario(Base):
    """
    TABLA: veterinarios
    ===================
    Almacena información del personal de la clínica.
    """
    __tablename__ = "veterinarios"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    dni = Column(String(20), unique=True, nullable=False)
    cargo = Column(String(50))  # 'Veterinario', 'Auxiliar', ...
    especialidad = Column(String(100))  # 'Cirugía', 'Felinos', ...
    telefono = Column(String(20))
    email = Column(String(100))
    
    # NO ponemos cascade aquí porque queremos que las citas sigan existiendo
    # y solo se quede veterinario_id = NULL (SET NULL en la FK de Cita)
    citas = relationship("Cita", back_populates="veterinario")
    
    def __repr__(self):
        return f"<Veterinario id={self.id} nombre={self.nombre}>"


class Cita(Base):
    """
    TABLA: citas
    ============
    Almacena información de las citas veterinarias.
    """
    __tablename__ = "citas"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(Date, nullable=False)
    hora = Column(String(5), nullable=False)  # 'HH:MM'
    motivo = Column(String(200))
    diagnostico = Column(String(500))
    estado = Column(String(20), default="Pendiente")
    
    # Si se borra la mascota → borrar la cita (CASCADE)
    mascota_id = Column(
        Integer,
        ForeignKey("mascotas.id", ondelete="CASCADE"),
        nullable=False,
    )
    
    # Si se borra el veterinario → mantener la cita pero sin veterinario (SET NULL)
    veterinario_id = Column(
        Integer,
        ForeignKey("veterinarios.id", ondelete="SET NULL"),
        nullable=True,
    )
    
    mascota = relationship("Mascota", back_populates="citas")
    veterinario = relationship("Veterinario", back_populates="citas")
    
    def __repr__(self):
        return (
            f"<Cita id={self.id} fecha={self.fecha} "
            f"mascota_id={self.mascota_id} veterinario_id={self.veterinario_id}>"
        )


# ==========================================
# 4. CREAR TABLAS Y SESIÓN
# ==========================================

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

print("✅ Base de datos configurada correctamente")

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

# ==========================================
# 1. MOTOR DE BASE DE DATOS (ENGINE)
# ==========================================
engine = create_engine('sqlite:///clinica.db', echo=False)

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
    
    Campos:
    - id: Identificador único (autoincremental)
    - nombre: Nombre completo del cliente
    - dni: DNI único del cliente
    - telefono: Teléfono de contacto
    - email: Correo electrónico
    
    Relaciones:
    - mascotas: Lista de mascotas que posee este cliente (1:N)
    """
    __tablename__ = 'clientes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    dni = Column(String(20), unique=True, nullable=False)
    telefono = Column(String(20))
    email = Column(String(100))
    
    # Relación con Mascotas
    mascotas = relationship("Mascota", back_populates="cliente", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Cliente(id={self.id}, nombre='{self.nombre}', dni='{self.dni}')>"


class Mascota(Base):
    """
    TABLA: mascotas
    ===============
    Almacena información de los animales.
    
    Campos:
    - id: Identificador único
    - nombre: Nombre del animal
    - especie: Tipo de animal (Perro, Gato, Conejo, etc.)
    - raza: Raza del animal
    - edad: Edad en años
    - peso: Peso en kilogramos
    - sexo: Macho o Hembra
    - cliente_id: Clave foránea que vincula con Cliente
    
    Relaciones:
    - cliente: El Cliente propietario de esta mascota
    - citas: Todas las citas de esta mascota
    """
    __tablename__ = 'mascotas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    especie = Column(String(50), nullable=False)
    raza = Column(String(50))
    edad = Column(Integer)
    peso = Column(Float)
    sexo = Column(String(10))  # 'Macho' o 'Hembra'
    
    # Clave foránea
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    
    # Relaciones
    cliente = relationship("Cliente", back_populates="mascotas")
    citas = relationship("Cita", back_populates="mascota", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Mascota(id={self.id}, nombre='{self.nombre}', especie='{self.especie}')>"


class Veterinario(Base):
    """
    TABLA: veterinarios
    ===================
    Almacena información del personal de la clínica.
    
    Campos:
    - id: Identificador único
    - nombre: Nombre completo del veterinario
    - dni: DNI único
    - cargo: Tipo de empleado (Veterinario, Auxiliar, Administrativo)
    - especialidad: Especialización (Cirugía, Felinos, Diagnóstico, etc.)
    - telefono: Teléfono de contacto
    - email: Correo electrónico
    
    Relaciones:
    - citas: Todas las citas asignadas a este veterinario
    """
    __tablename__ = 'veterinarios'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    dni = Column(String(20), unique=True, nullable=False)
    cargo = Column(String(50))  # 'Veterinario', 'Auxiliar', 'Administrativo'
    especialidad = Column(String(100))  # 'Cirugía', 'Felinos', etc.
    telefono = Column(String(20))
    email = Column(String(100))
    
    # Relaciones
    citas = relationship("Cita", back_populates="veterinario")
    
    def __repr__(self):
        return f"<Veterinario(id={self.id}, nombre='{self.nombre}', especialidad='{self.especialidad}')>"


class Cita(Base):
    """
    TABLA: citas
    ============
    Almacena información de las citas veterinarias.
    
    Campos:
    - id: Identificador único
    - fecha: Fecha de la cita (formato: YYYY-MM-DD)
    - hora: Hora de la cita (formato: HH:MM)
    - motivo: Razón de la consulta
    - diagnostico: Diagnóstico o notas del veterinario
    - estado: Estado de la cita ('pendiente', 'realizada', 'cancelada')
    - mascota_id: Clave foránea a Mascota
    - veterinario_id: Clave foránea a Veterinario
    
    Relaciones:
    - mascota: La mascota de esta cita
    - veterinario: El veterinario responsable
    """
    __tablename__ = 'citas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(Date, nullable=False)
    hora = Column(String(10), nullable=False)  # Formato: HH:MM
    motivo = Column(String(200), nullable=False)
    diagnostico = Column(String(500))
    estado = Column(String(20), default='pendiente')  # 'pendiente', 'realizada', 'cancelada'
    
    # Claves foráneas
    mascota_id = Column(Integer, ForeignKey('mascotas.id'), nullable=False)
    veterinario_id = Column(Integer, ForeignKey('veterinarios.id'), nullable=False)
    
    # Relaciones
    mascota = relationship("Mascota", back_populates="citas")
    veterinario = relationship("Veterinario", back_populates="citas")
    
    def __repr__(self):
        return f"<Cita(id={self.id}, fecha={self.fecha}, estado='{self.estado}')>"


# ==========================================
# 4. CREAR TABLAS Y SESIÓN
# ==========================================

# Crea todas las tablas en la base de datos si no existen
Base.metadata.create_all(engine)

# Configurar sesión para operaciones CRUD
Session = sessionmaker(bind=engine)
session = Session()

print("✅ Base de datos configurada correctamente")
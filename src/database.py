"""
título: capa de base de datos
fecha: 11.11.2025
descripcion: configura SQLAlchemy y define los modelos (clases) que representan
las tablas de la base de datos SQLite. Define las 4 tablas principales:
cliente, mascota, veterinario y cita, con sus relaciones.
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///clinica.db', echo=False)
Base = declarative_base()

class Cliente(Base):
    __tablename__ = 'clientes'
    # id, nombre, dni, telefono, email
    # Relación: mascotas (1:N)

class Mascota(Base):
    __tablename__ = 'mascotas'
    # id, nombre, especie, raza, edad, peso, sexo, cliente_id
    # Relaciones: cliente (N:1), citas (1:N)

class Veterinario(Base):
    __tablename__ = 'veterinarios'
    # id, nombre, dni, cargo, especialidad, telefono, email
    # Relación: citas (1:N)

class Cita(Base):
    __tablename__ = 'citas'
    # id, fecha, hora, motivo, diagnostico, estado, mascota_id, veterinario_id
    # Relaciones: mascota (N:1), veterinario (N:1)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()



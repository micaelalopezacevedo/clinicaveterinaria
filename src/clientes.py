"""
título: módulo de clientes
fecha: 03.12.2025
descripción: lógica completa de gestión de clientes.

CÓMO FUNCIONA:
===============

1. _RepositorioCliente: Acceso a BD (CRUD)
   └─ crear(), obtener_por_id(), listar_todos(), etc.
   └─ NUNCA tiene lógica de negocio

2. _ServicioCliente: Lógica de negocio
   └─ crear_cliente(): valida + verifica DNI + crea
   └─ Usa Utilidades para validaciones
   └─ Usa _RepositorioCliente para BD

3. Interfaz pública: 8 funciones
   └─ Lo único que importa Streamlit
   └─ Wrappers simples que deleguen a ServicioCliente o RepositorioCliente
"""

from src.database import session, Cliente
from src.exceptions import ClienteNoEncontradoException, DNIDuplicadoException, ValidacionException
from src.logger import Logger
from sqlalchemy.exc import IntegrityError

# ========================
# REPOSITORIO (PRIVADO)
# ========================
# RESPONSABILIDAD: SOLO acceso a datos (CRUD)
# No hay lógica de negocio aquí

class _RepositorioCliente:
    """Encapsula acceso a BD - CRUD básico sin lógica"""
    
    @staticmethod
    def crear(nombre: str, dni: str, telefono: str = None, email: str = None):
        """CRUD: CREATE"""
        cliente = Cliente(
            nombre=nombre,
            dni=dni,
            telefono=telefono,
            email=email
        )
        session.add(cliente)
        session.commit()
        Logger.info(f"Cliente creado con ID: {cliente.id}")
        return cliente
    
    @staticmethod
    def obtener_por_id(cliente_id: int):
        """CRUD: READ por ID"""
        cliente = session.query(Cliente).filter_by(id=cliente_id).first()
        if not cliente:
            raise ClienteNoEncontradoException(cliente_id)
        return cliente
    
    @staticmethod
    def listar_todos():
        """CRUD: READ todos"""
        return session.query(Cliente).order_by(Cliente.nombre).all()
    
    @staticmethod
    def obtener_por_dni(dni: str):
        """CRUD: READ por DNI"""
        return session.query(Cliente).filter_by(dni=dni).first()
    
    @staticmethod
    def obtener_por_nombre(nombre: str):
        """CRUD: READ búsqueda parcial por nombre"""
        return session.query(Cliente).filter(
            Cliente.nombre.like(f"%{nombre}%")
        ).order_by(Cliente.nombre).all()
    
    @staticmethod
    def actualizar(cliente: Cliente, **campos) -> Cliente:
        """CRUD: UPDATE"""
        for campo, valor in campos.items():
            if valor is not None:
                setattr(cliente, campo, valor)
        session.commit()
        session.refresh(cliente)
        Logger.info(f"Cliente {cliente.id} actualizado")
        return cliente
    
    @staticmethod
    def eliminar(cliente: Cliente) -> bool:
        """CRUD: DELETE"""
        nombre = cliente.nombre
        session.delete(cliente)
        session.commit()
        Logger.info(f"Cliente {nombre} eliminado")
        return True
    
    @staticmethod
    def contar_total():
        """CRUD: COUNT todos"""
        try:
            return session.query(Cliente).count()
        except Exception as e:
            Logger.log_excepcion(e, "contar_total")
            return 0
    
    @staticmethod
    def existe(cliente_id: int) -> bool:
        """CRUD: READ para verificar existencia"""
        try:
            return session.query(Cliente).filter_by(id=cliente_id).first() is not None
        except Exception as e:
            Logger.log_excepcion(e, "existe")
            return False
    
    @staticmethod
    def dni_existe(dni: str, excluir_id: int = None) -> bool:
        """CRUD: READ para verificar DNI duplicado (excluyendo un ID si se proporciona)"""
        q = session.query(Cliente).filter_by(dni=dni)
        if excluir_id:
            q = q.filter(Cliente.id != excluir_id)
        return q.first() is not None


# ========================
# SERVICIO (PRIVADO)
# ========================
# RESPONSABILIDAD: Lógica de negocio
# Usa Utilidades (validaciones) + _RepositorioCliente (BD)

class _ServicioCliente:
    """Orquesta validaciones + acceso a BD"""
    
    @staticmethod
    def crear_cliente(nombre: str, dni: str, telefono: str = None, email: str = None):
        """
        Crea un cliente: 1) Valida 2) Verifica DNI 3) Crea
        
        Puede lanzar ValidacionException o DNIDuplicadoException
        """
        try:
            # PASO 1: VALIDAR CAMPOS OBLIGATORIOS
            if not nombre or not dni:
                raise ValidacionException("nombre y DNI", "son campos obligatorios")
            
            # PASO 2: VERIFICAR DNI DUPLICADO
            if _RepositorioCliente.dni_existe(dni):
                raise DNIDuplicadoException(dni, "Cliente")
            
            # PASO 3: CREAR EN BD (delegado al repositorio)
            return _RepositorioCliente.crear(nombre, dni, telefono, email)
        
        except (DNIDuplicadoException, ValidacionException):
            session.rollback()
            raise
        except IntegrityError:
            session.rollback()
            Logger.error("Error de integridad, probablemente DNI duplicado")
            raise
        except Exception as e:
            session.rollback()
            Logger.log_excepcion(e, "crear_cliente")
            raise
    
    @staticmethod
    def modificar_cliente(cliente_id: int, nombre: str = None, telefono: str = None, email: str = None):
        """
        Modifica un cliente: 1) Obtiene 2) Valida cambios 3) Actualiza
        """
        try:
            # PASO 1: OBTENER CLIENTE
            cliente = _RepositorioCliente.obtener_por_id(cliente_id)
            
            # PASO 2: VALIDAR CAMBIOS (opcionales pero si se proporcionan, validar)
            if nombre is not None and not nombre:
                raise ValidacionException("nombre", "no puede estar vacío")
            
            # PASO 3: ACTUALIZAR (delegado al repositorio)
            return _RepositorioCliente.actualizar(
                cliente,
                nombre=nombre,
                telefono=telefono,
                email=email
            )
        
        except (ClienteNoEncontradoException, ValidacionException):
            session.rollback()
            raise
        except Exception as e:
            session.rollback()
            Logger.log_excepcion(e, "modificar_cliente")
            raise


# ========================
# INTERFAZ PÚBLICA (8 funciones)
# ========================
# Lo ÚNICO que usa Streamlit
# Todo está aquí, NADA en las clases privadas

def crear_cliente(nombre: str, dni: str, telefono: str = None, email: str = None):
    """Crea un nuevo cliente"""
    return _ServicioCliente.crear_cliente(nombre, dni, telefono, email)

def listar_clientes():
    """Devuelve todos los clientes"""
    return _RepositorioCliente.listar_todos()

def obtener_cliente_por_id(cliente_id: int):
    """Obtiene un cliente por ID"""
    return _RepositorioCliente.obtener_por_id(cliente_id)

def buscar_cliente_por_dni(dni: str):
    """Busca un cliente por DNI"""
    return _RepositorioCliente.obtener_por_dni(dni)

def buscar_cliente_por_nombre(nombre: str):
    """Busca clientes por nombre (búsqueda parcial)"""
    return _RepositorioCliente.obtener_por_nombre(nombre)

def modificar_cliente(cliente_id: int, nombre: str = None, telefono: str = None, email: str = None):
    """Modifica un cliente existente"""
    return _ServicioCliente.modificar_cliente(cliente_id, nombre, telefono, email)

def eliminar_cliente(cliente_id: int):
    """Elimina un cliente"""
    try:
        cliente = _RepositorioCliente.obtener_por_id(cliente_id)
        return _RepositorioCliente.eliminar(cliente)
    except Exception as e:
        Logger.log_excepcion(e, "eliminar_cliente")
        raise

def contar_clientes():
    """Cuenta total de clientes"""
    return _RepositorioCliente.contar_total()

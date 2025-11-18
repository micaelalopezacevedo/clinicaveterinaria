"""
título: módulo de clientes
fecha: 11.11.2025
descripción: implementa toda la lógica relacionada con la gestión de clientes.
Cubre los requisitos funcionales RF1-RF4:
- RF1: Registrar nuevos clientes
- RF2: Consultar, editar y eliminar clientes
- RF3: Buscar clientes por nombre o DNI
- RF4: Listar todos los clientes
"""

"""
========================================
TÍTULO: Módulo de Clientes
FECHA: 18.11.2025
DESCRIPCIÓN:
Implementa toda la lógica relacionada con gestión de clientes.
Cubre los requisitos funcionales RF1-RF4
========================================
"""

from src.database import session, Cliente
from sqlalchemy.exc import IntegrityError

# ===================================
# CREAR (CREATE)
# ===================================

def crear_cliente(nombre: str, dni: str, telefono: str = None, email: str = None) -> Cliente:
    """
    Crea nuevo cliente
    Args: nombre (str), dni (str), telefono (str, opcional), email (str, opcional)
    Return: Cliente creado o None si error
    """
    try:
        # Validar campos obligatorios
        if not nombre or not dni:
            print("Error: Nombre y DNI son obligatorios")
            return None
        
        # Crear objeto Cliente
        nuevo_cliente = Cliente(
            nombre=nombre,
            dni=dni,
            telefono=telefono,
            email=email
        )
        
        # Añadir a la sesión
        session.add(nuevo_cliente)
        
        # Confirmar cambios
        session.commit()
        
        print(f"✅ Cliente creado: {nombre} (ID: {nuevo_cliente.id})")
        return nuevo_cliente
    
    except IntegrityError:
        session.rollback()
        print(f"❌ Error: DNI {dni} ya existe")
        return None
    
    except Exception as e:
        session.rollback()
        print(f"❌ Error al crear cliente: {str(e)}")
        return None


# ===================================
# LEER (READ)
# ===================================

def listar_clientes() -> list:
    """
    Devuelve todos los clientes
    Args: ninguno
    Return: Lista de clientes
    """
    try:
        clientes = session.query(Cliente).all()
        return clientes
    except Exception as e:
        print(f"❌ Error al listar clientes: {str(e)}")
        return []


def obtener_cliente_por_id(cliente_id: int) -> Cliente:
    """
    Busca cliente por ID
    Args: cliente_id (int)
    Return: Cliente encontrado o None
    """
    try:
        cliente = session.query(Cliente).filter_by(id=cliente_id).first()
        return cliente
    except Exception as e:
        print(f"❌ Error al buscar cliente: {str(e)}")
        return None


def buscar_cliente_por_dni(dni: str) -> Cliente:
    """
    Busca cliente por DNI (búsqueda exacta)
    Args: dni (str)
    Return: Cliente encontrado o None
    """
    try:
        cliente = session.query(Cliente).filter_by(dni=dni).first()
        return cliente
    except Exception as e:
        print(f"❌ Error al buscar por DNI: {str(e)}")
        return None


def buscar_cliente_por_nombre(nombre: str) -> list:
    """
    Busca clientes por nombre (búsqueda parcial)
    Args: nombre (str)
    Return: Lista de clientes que coinciden
    """
    try:
        clientes = session.query(Cliente).filter(
            Cliente.nombre.like(f"%{nombre}%")
        ).all()
        return clientes
    except Exception as e:
        print(f"❌ Error al buscar por nombre: {str(e)}")
        return []


# ===================================
# ACTUALIZAR (UPDATE)
# ===================================

def modificar_cliente(cliente_id: int, nombre: str = None, telefono: str = None, email: str = None) -> Cliente:
    """
    Modifica datos de cliente existente
    Args: cliente_id (int), nombre (str, opcional), telefono (str, opcional), email (str, opcional)
    Return: Cliente modificado o None si no existe
    """
    try:
        # Buscar cliente
        cliente = obtener_cliente_por_id(cliente_id)
        
        if not cliente:
            print(f"❌ No existe cliente con ID: {cliente_id}")
            return None
        
        # Actualizar solo campos proporcionados
        if nombre is not None:
            cliente.nombre = nombre
        if telefono is not None:
            cliente.telefono = telefono
        if email is not None:
            cliente.email = email
        
        # Confirmar cambios
        session.commit()
        
        print(f"✅ Cliente actualizado: {cliente.nombre}")
        return cliente
    
    except Exception as e:
        session.rollback()
        print(f"❌ Error al modificar cliente: {str(e)}")
        return None


# ===================================
# ELIMINAR (DELETE)
# ===================================

def eliminar_cliente(cliente_id: int) -> bool:
    """
    Elimina cliente (y sus mascotas asociadas)
    Args: cliente_id (int)
    Return: True si éxito, False si error/no existe
    """
    try:
        # Buscar cliente
        cliente = obtener_cliente_por_id(cliente_id)
        
        if not cliente:
            print(f"❌ No existe cliente con ID: {cliente_id}")
            return False
        
        nombre = cliente.nombre
        
        # Eliminar
        session.delete(cliente)
        session.commit()
        
        print(f"✅ Cliente eliminado: {nombre}")
        return True
    
    except Exception as e:
        session.rollback()
        print(f"❌ Error al eliminar cliente: {str(e)}")
        return False


# ===================================
# AUXILIARES
# ===================================

def contar_clientes() -> int:
    """
    Cuenta total de clientes
    Args: ninguno
    Return: Número de clientes (int)
    """
    try:
        return session.query(Cliente).count()
    except Exception as e:
        print(f"❌ Error al contar clientes: {str(e)}")
        return 0


def cliente_existe(cliente_id: int) -> bool:
    """
    Verifica si existe cliente con ese ID
    Args: cliente_id (int)
    Return: True si existe, False si no
    """
    return obtener_cliente_por_id(cliente_id) is not None

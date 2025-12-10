"""
título: módulo de veterinarios
fecha: 03.12.2025
descripción: lógica completa de gestión de veterinarios.

CÓMO FUNCIONA:
===============

1. _RepositorioVeterinario: Acceso a BD (CRUD)
   └─ crear(), obtener_por_id(), listar_todos(), contar_total(), etc.
   └─ NUNCA tiene lógica de negocio

2. _ServicioVeterinario: Lógica de negocio
   └─ crear_veterinario(): valida + verifica DNI + crea
   └─ Usa Utilidades para validaciones
   └─ Usa _RepositorioVeterinario para BD

3. Interfaz pública: 10 funciones
   └─ Lo único que importa Streamlit
   └─ Wrappers simples que deleguen a ServicioVeterinario o RepositorioVeterinario
"""

from src.database import session, Veterinario
from src.exceptions import VeterinarioNoEncontradoException, DNIDuplicadoException, ValidacionException
from src.logger import Logger
from sqlalchemy.exc import IntegrityError

# ========================
# REPOSITORIO (PRIVADO)
# ========================
# RESPONSABILIDAD: SOLO acceso a datos (CRUD)
# No hay lógica de negocio aquí

class _RepositorioVeterinario:
    """Encapsula acceso a BD - CRUD básico sin lógica"""
    
    @staticmethod
    def crear(nombre: str, dni: str, cargo: str = None, especialidad: str = None, telefono: str = None, email: str = None):
        """CRUD: CREATE"""
        veterinario = Veterinario(
            nombre=nombre,
            dni=dni,
            cargo=cargo,
            especialidad=especialidad,
            telefono=telefono,
            email=email
        )
        session.add(veterinario)
        session.commit()
        Logger.info(f"Veterinario creado con ID: {veterinario.id}")
        return veterinario
    
    @staticmethod
    def obtener_por_id(veterinario_id: int):
        """CRUD: READ por ID"""
        veterinario = session.query(Veterinario).filter_by(id=veterinario_id).first()
        if not veterinario:
            raise VeterinarioNoEncontradoException(veterinario_id)
        return veterinario
    
    @staticmethod
    def listar_todos():
        """CRUD: READ todos"""
        return session.query(Veterinario).order_by(Veterinario.nombre).all()
    
    @staticmethod
    def obtener_por_dni(dni: str):
        """CRUD: READ por DNI"""
        return session.query(Veterinario).filter_by(dni=dni).first()
    
    @staticmethod
    def obtener_por_nombre(nombre: str):
        """CRUD: READ búsqueda parcial por nombre"""
        return session.query(Veterinario).filter(
            Veterinario.nombre.like(f"%{nombre}%")
        ).order_by(Veterinario.nombre).all()
    
    @staticmethod
    def actualizar(veterinario: Veterinario, **campos) -> Veterinario:
        """CRUD: UPDATE"""
        for campo, valor in campos.items():
            if valor is not None:
                setattr(veterinario, campo, valor)
        session.commit()
        session.refresh(veterinario)
        Logger.info(f"Veterinario {veterinario.id} actualizado")
        return veterinario
    
    @staticmethod
    def eliminar(veterinario: Veterinario) -> bool:
        """CRUD: DELETE"""
        nombre = veterinario.nombre
        session.delete(veterinario)
        session.commit()
        Logger.info(f"Veterinario {nombre} eliminado")
        return True
    
    @staticmethod
    def contar_total():
        """CRUD: COUNT todos"""
        try:
            return session.query(Veterinario).count()
        except Exception as e:
            Logger.log_excepcion(e, "contar_total")
            return 0
    
    @staticmethod
    def existe(veterinario_id: int) -> bool:
        """CRUD: READ para verificar existencia"""
        try:
            return session.query(Veterinario).filter_by(id=veterinario_id).first() is not None
        except Exception as e:
            Logger.log_excepcion(e, "existe")
            return False
    
    @staticmethod
    def dni_existe(dni: str, excluir_id: int = None) -> bool:
        """CRUD: READ para verificar DNI duplicado (excluyendo un ID si se proporciona)"""
        q = session.query(Veterinario).filter_by(dni=dni)
        if excluir_id:
            q = q.filter(Veterinario.id != excluir_id)
        return q.first() is not None


# ========================
# SERVICIO (PRIVADO)
# ========================
# RESPONSABILIDAD: Lógica de negocio
# Usa Utilidades (validaciones) + _RepositorioVeterinario (BD)

class _ServicioVeterinario:
    """Orquesta validaciones + acceso a BD"""
    
    @staticmethod
    def crear_veterinario(nombre: str, dni: str, cargo: str = None, especialidad: str = None, telefono: str = None, email: str = None):
        """
        Crea un veterinario: 1) Valida 2) Verifica DNI 3) Crea
        
        Puede lanzar ValidacionException o DNIDuplicadoException
        """
        try:
            # PASO 1: VALIDAR CAMPOS OBLIGATORIOS
            if not nombre or not dni:
                raise ValidacionException("nombre y DNI", "son campos obligatorios")
            
            # PASO 2: VERIFICAR DNI DUPLICADO
            if _RepositorioVeterinario.dni_existe(dni):
                raise DNIDuplicadoException(dni, "Veterinario")
            
            # PASO 3: CREAR EN BD (delegado al repositorio)
            return _RepositorioVeterinario.crear(nombre, dni, cargo, especialidad, telefono, email)
        
        except (DNIDuplicadoException, ValidacionException):
            session.rollback()
            raise
        except IntegrityError:
            session.rollback()
            Logger.error("Error de integridad, probablemente DNI duplicado")
            raise
        except Exception as e:
            session.rollback()
            Logger.log_excepcion(e, "crear_veterinario")
            raise
    
    @staticmethod
    def modificar_veterinario(veterinario_id: int, nombre: str = None, dni: str = None, cargo: str = None, especialidad: str = None, telefono: str = None, email: str = None):
        """
        Modifica un veterinario: 1) Obtiene 2) Valida si cambia DNI 3) Actualiza
        
        Si se cambia DNI, verifica que no exista otro con ese DNI
        """
        try:
            # PASO 1: OBTENER VETERINARIO
            veterinario = _RepositorioVeterinario.obtener_por_id(veterinario_id)
            
            # PASO 2: SI CAMBIA DNI, VALIDAR QUE NO EXISTA OTRO
            if dni is not None and dni != veterinario.dni:
                if _RepositorioVeterinario.dni_existe(dni, excluir_id=veterinario_id):
                    raise DNIDuplicadoException(dni, "Veterinario")
            
            # PASO 3: ACTUALIZAR (delegado al repositorio)
            return _RepositorioVeterinario.actualizar(
                veterinario, 
                nombre=nombre, 
                dni=dni, 
                cargo=cargo, 
                especialidad=especialidad, 
                telefono=telefono, 
                email=email
            )
        
        except (DNIDuplicadoException, VeterinarioNoEncontradoException):
            session.rollback()
            raise
        except Exception as e:
            session.rollback()
            Logger.log_excepcion(e, "modificar_veterinario")
            raise


# ========================
# INTERFAZ PÚBLICA (10 funciones)
# ========================
# Lo ÚNICO que usa Streamlit
# Todo está aquí, NADA en las clases privadas

def crear_veterinario(nombre: str, dni: str, cargo: str = None, especialidad: str = None, telefono: str = None, email: str = None):
    """Crea un nuevo veterinario"""
    return _ServicioVeterinario.crear_veterinario(nombre, dni, cargo, especialidad, telefono, email)

def listar_veterinarios():
    """Devuelve todos los veterinarios"""
    return _RepositorioVeterinario.listar_todos()

def obtener_veterinario_por_id(veterinario_id: int):
    """Obtiene un veterinario por ID"""
    return _RepositorioVeterinario.obtener_por_id(veterinario_id)

def buscar_veterinario_por_dni(dni: str):
    """Busca un veterinario por DNI"""
    return _RepositorioVeterinario.obtener_por_dni(dni)

def buscar_veterinario_por_nombre(nombre: str):
    """Busca veterinarios por nombre (búsqueda parcial)"""
    return _RepositorioVeterinario.obtener_por_nombre(nombre)

def modificar_veterinario(veterinario_id: int, nombre: str = None, dni: str = None, cargo: str = None, especialidad: str = None, telefono: str = None, email: str = None):
    """Modifica un veterinario existente"""
    return _ServicioVeterinario.modificar_veterinario(veterinario_id, nombre, dni, cargo, especialidad, telefono, email)

def eliminar_veterinario(veterinario_id: int):
    """Elimina un veterinario"""
    try:
        veterinario = _RepositorioVeterinario.obtener_por_id(veterinario_id)
        return _RepositorioVeterinario.eliminar(veterinario)
    except Exception as e:
        Logger.log_excepcion(e, "eliminar_veterinario")
        raise

def contar_veterinarios():
    """Cuenta total de veterinarios"""
    return _RepositorioVeterinario.contar_total()

def veterinario_existe(veterinario_id: int):
    """Verifica si existe un veterinario con ese ID"""
    return _RepositorioVeterinario.existe(veterinario_id)

def obtener_veterinarios_por_especialidad(especialidad: str):
    """Devuelve veterinarios de una especialidad (búsqueda parcial)"""
    try:
        return session.query(Veterinario).filter(
            Veterinario.especialidad.like(f"%{especialidad}%")
        ).order_by(Veterinario.nombre).all()
    except Exception as e:
        Logger.log_excepcion(e, "obtener_veterinarios_por_especialidad")
        return []
#
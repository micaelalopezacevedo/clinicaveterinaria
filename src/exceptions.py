"""
título: módulo de excepciones personalizadas
fecha: 11.11.2025
descripción: define todas las excepciones personalizadas para el proyecto.
Cada excepción hereda de ClinicaException (base personalizada).
Se lanzan en operaciones CRUD y validaciones cuando algo falla.
"""

# EXCEPCIÓN BASE
class ClinicaException(Exception):
    """
    Excepción base para todas las excepciones del proyecto
    Args: mensaje (str)
    Return: Objeto excepción
    """

# EXCEPCIONES DE ENTIDADES NO ENCONTRADAS
class ClienteNoEncontradoException(ClinicaException):
    """
    Se lanza cuando se intenta acceder a un cliente que no existe
    Args: cliente_id (int)
    Return: Mensaje de error descriptivo
    """

class MascotaNoEncontradaException(ClinicaException):
    """
    Se lanza cuando se intenta acceder a una mascota que no existe
    Args: mascota_id (int)
    Return: Mensaje de error descriptivo
    """

class VeterinarioNoEncontradoException(ClinicaException):
    """
    Se lanza cuando se intenta acceder a un veterinario que no existe
    Args: veterinario_id (int)
    Return: Mensaje de error descriptivo
    """

class CitaNoEncontradaException(ClinicaException):
    """
    Se lanza cuando se intenta acceder a una cita que no existe
    Args: cita_id (int)
    Return: Mensaje de error descriptivo
    """

# EXCEPCIONES DE VALIDACIÓN Y DUPLICADOS
class DNIDuplicadoException(ClinicaException):
    """
    Se lanza cuando se intenta crear un cliente/veterinario con DNI duplicado
    Args: dni (str), entidad (str, ej: "Cliente" o "Veterinario")
    Return: Mensaje de error descriptivo
    """

class ClienteSinMascotasException(ClinicaException):
    """
    Se lanza cuando se intenta acceder a mascotas de un cliente que no tiene ninguna
    Args: cliente_id (int)
    Return: Mensaje de error descriptivo
    """

class ValidacionException(ClinicaException):
    """
    Se lanza cuando un campo no cumple con las validaciones requeridas
    Args: campo (str), motivo (str), valor (str, opcional)
    Return: Mensaje de error descriptivo
    """

# EXCEPCIONES DE BASE DE DATOS
class DatabaseConnectionException(ClinicaException):
    """
    Se lanza cuando hay un problema al conectar con la base de datos
    Args: mensaje (str)
    Return: Mensaje de error descriptivo
    """

class DatabaseOperationException(ClinicaException):
    """
    Se lanza cuando una operación en la base de datos falla
    Args: operacion (str), motivo (str)
    Return: Mensaje de error descriptivo
    """

# EXCEPCIONES DE LÓGICA
class CitaConflictoException(ClinicaException):
    """
    Se lanza cuando hay conflicto de citas (misma hora, veterinario, etc)
    Args: motivo (str)
    Return: Mensaje de error descriptivo
    """

class VeterinarioSobreCargadoException(ClinicaException):
    """
    Se lanza cuando un veterinario tiene demasiadas citas programadas
    Args: veterinario_id (int), num_citas (int)
    Return: Mensaje de error descriptivo
    """

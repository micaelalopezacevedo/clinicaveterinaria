"""
título: módulo de excepciones personalizadas
fecha: 11.11.2025
descripción: define todas las excepciones personalizadas para el proyecto.
Cada excepción hereda de ClinicaException (base personalizada).
Se lanzan en operaciones CRUD y validaciones cuando algo falla.
"""

# =====================================
# EXCEPCIÓN BASE (Abstracción SOLID)
# =====================================

class ClinicaException(Exception):
    """
    Excepción base para todas las excepciones del proyecto.
    """

    def __init__(self, mensaje: str):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.mensaje}"


# =====================================
# EXCEPCIONES: ENTIDADES NO ENCONTRADAS
# =====================================

class ClienteNoEncontradoException(ClinicaException):
    def __init__(self, cliente_id: int):
        super().__init__(f"Cliente con ID {cliente_id} no encontrado")


class MascotaNoEncontradaException(ClinicaException):
    def __init__(self, mascota_id: int):
        super().__init__(f"Mascota con ID {mascota_id} no encontrada")


class VeterinarioNoEncontradoException(ClinicaException):
    def __init__(self, veterinario_id: int):
        super().__init__(f"Veterinario con ID {veterinario_id} no encontrado")


class CitaNoEncontradaException(ClinicaException):
    def __init__(self, cita_id: int):
        super().__init__(f"Cita con ID {cita_id} no encontrada")


# =====================================
# EXCEPCIONES: VALIDACIÓN Y DUPLICADOS
# =====================================

class DNIDuplicadoException(ClinicaException):
    def __init__(self, dni: str, entidad: str = "Cliente"):
        super().__init__(f"Ya existe un {entidad} con DNI {dni}")


class ClienteSinMascotasException(ClinicaException):
    def __init__(self, cliente_id: int):
        super().__init__(f"Cliente {cliente_id} no tiene mascotas registradas")


class ValidacionException(ClinicaException):
    def __init__(self, campo: str, motivo: str, valor: str = None):
        if valor:
            mensaje = f"Validación en '{campo}': {motivo} (valor: {valor})"
        else:
            mensaje = f"Validación en '{campo}': {motivo}"
        super().__init__(mensaje)


# =====================================
# EXCEPCIONES: BASE DE DATOS
# =====================================

class DatabaseConnectionException(ClinicaException):
    def __init__(self, mensaje: str):
        super().__init__(f"Error de conexión a la BD: {mensaje}")


class DatabaseOperationException(ClinicaException):
    def __init__(self, operacion: str, motivo: str):
        super().__init__(f"Error en operación '{operacion}': {motivo}")


# =====================================
# EXCEPCIONES: LÓGICA DE NEGOCIO
# =====================================

class CitaConflictoException(ClinicaException):
    def __init__(self, motivo: str):
        super().__init__(f"Conflicto de citas: {motivo}")


class VeterinarioSobreCargadoException(ClinicaException):
    def __init__(self, veterinario_id: int, num_citas: int):
        super().__init__(
            f"Veterinario {veterinario_id} tiene {num_citas} citas. Límite superado."
        )
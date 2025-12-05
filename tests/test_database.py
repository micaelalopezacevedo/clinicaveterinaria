import pytest
from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError
from datetime import date
from src.database import Cliente, Mascota, Veterinario, Cita

# ==========================================
# 1. TESTS DE ESTRUCTURA (MODELOS Y COLUMNAS)
# ==========================================

class TestModelos:
    """Verifica que las tablas se crean correctamente en la BD"""

    def test_tablas_existen(self, session):
        """Verifica que las 4 tablas principales existen en el esquema."""
        inspector = inspect(session.bind)
        tablas = inspector.get_table_names()
        
        assert "clientes" in tablas
        assert "mascotas" in tablas
        assert "veterinarios" in tablas
        assert "citas" in tablas

class TestColumnas:
    """Verifica que las columnas requeridas están presentes"""

    def _check_columns(self, model, expected_columns):
        """Helper para inspeccionar columnas de un modelo"""
        inspector = inspect(model)
        # Obtenemos los nombres de las columnas del modelo
        columns = {c.key for c in inspector.columns}
        for col in expected_columns:
            assert col in columns, f"Falta la columna '{col}' en el modelo {model._name_}"

    def test_cliente_tiene_columnas_requeridas(self):
        self._check_columns(Cliente, ["id", "nombre", "dni", "telefono", "email"])

    def test_mascota_tiene_columnas_requeridas(self):
        self._check_columns(Mascota, ["id", "nombre", "especie", "raza", "edad", "peso", "sexo", "cliente_id"])

    def test_veterinario_tiene_columnas_requeridas(self):
        self._check_columns(Veterinario, ["id", "nombre", "dni", "cargo", "especialidad", "telefono", "email"])

    def test_cita_tiene_columnas_requeridas(self):
        self._check_columns(Cita, ["id", "fecha", "hora", "motivo", "diagnostico", "estado", "mascota_id", "veterinario_id"])

# ==========================================
# 2. TESTS DE RELACIONES Y CASCADES (CRÍTICO)
# ==========================================

class TestRelaciones:
    """
    Pruebas de integración para verificar Foreign Keys y efectos en cadena (Cascade)
    """

    def test_relacion_cliente_mascota_cascade(self, session):
        """
        Test IMPORTANTE: Verificar que al borrar un Cliente, 
        se borran automáticamente sus Mascotas (Cascade Delete).
        """
        # 1. Crear Cliente
        cliente = Cliente(nombre="Juan", dni="111A")
        session.add(cliente)
        session.commit()

        # 2. Crear Mascota asociada
        mascota = Mascota(nombre="Fido", especie="Perro", cliente_id=cliente.id)
        session.add(mascota)
        session.commit()

        # Pre-check: Existen ambos
        assert session.query(Cliente).count() == 1
        assert session.query(Mascota).count() == 1

        # 3. Borrar Cliente
        session.delete(cliente)
        session.commit()

        # Assert: La mascota debe haber desaparecido
        assert session.query(Cliente).count() == 0
        assert session.query(Mascota).count() == 0

    def test_relacion_mascota_cita_cascade(self, session):
        """
        Test IMPORTANTE: Verificar que al borrar una Mascota,
        se borran sus Citas.
        """
        # Setup
        c = Cliente(nombre="Ana", dni="222B")
        v = Veterinario(nombre="Vet", dni="333C")
        session.add_all([c, v])
        session.commit()

        m = Mascota(nombre="Mishi", especie="Gato", cliente_id=c.id)
        session.add(m)
        session.commit()

        cita = Cita(fecha=date.today(), hora="10:00", mascota_id=m.id, veterinario_id=v.id)
        session.add(cita)
        session.commit()

        # Borrar Mascota
        session.delete(m)
        session.commit()

        # Assert: Cita eliminada
        assert session.query(Cita).count() == 0

    def test_relacion_veterinario_cita_set_null(self, session):
        """
        Test IMPORTANTE: Verificar que al borrar un Veterinario,
        la Cita NO se borra, pero veterinario_id pasa a ser NULL.
        (Principio: No queremos perder el historial médico si echamos a un médico).
        """
        # Setup
        c = Cliente(nombre="Luis", dni="444D")
        v = Veterinario(nombre="Dr. House", dni="555E")
        session.add_all([c, v])
        session.commit()

        m = Mascota(nombre="Rex", especie="Perro", cliente_id=c.id)
        session.add(m)
        session.commit()

        cita = Cita(fecha=date.today(), hora="12:00", mascota_id=m.id, veterinario_id=v.id)
        session.add(cita)
        session.commit()

        # Borrar Veterinario
        session.delete(v)
        session.commit()

        # Assert: La cita SIGUE existiendo
        cita_db = session.query(Cita).first()
        assert cita_db is not None
        # Pero no tiene veterinario asignado
        assert cita_db.veterinario_id is None

# ==========================================
# 3. TESTS DE RESTRICCIONES (INTEGRIDAD)
# ==========================================

class TestRestricciones:
    """Verifica Constraints (Unique, Not Null)"""

    def test_cliente_dni_unico(self, session):
        """Verificar que salta error si repetimos DNI de cliente."""
        c1 = Cliente(nombre="Cliente 1", dni="DNI_DUPLICADO")
        session.add(c1)
        session.commit()

        c2 = Cliente(nombre="Cliente 2", dni="DNI_DUPLICADO")
        session.add(c2)

        # Al hacer commit debe explotar
        with pytest.raises(IntegrityError):
            session.commit()

    def test_veterinario_dni_unico(self, session):
        """Verificar unique constraint en veterinarios."""
        v1 = Veterinario(nombre="V1", dni="123")
        session.add(v1)
        session.commit()

        v2 = Veterinario(nombre="V2", dni="123")
        session.add(v2)

        with pytest.raises(IntegrityError):
            session.commit()

    def test_campos_obligatorios_cliente(self, session):
        """Verificar que 'nombre' y 'dni' no pueden ser Null."""
        # Cliente sin nombre ni DNI
        c = Cliente() 
        session.add(c)
        
        with pytest.raises(IntegrityError):
            session.commit()

    def test_campos_obligatorios_cita(self, session):
        """Cita sin fecha ni hora debe fallar."""
        c = Cliente(nombre="C", dni="C")
        session.add(c)
        session.commit()
        m = Mascota(nombre="M", especie="X", cliente_id=c.id)
        session.add(m)
        session.commit()

        # Cita vacía (sin fecha, hora, mascota)
        cita = Cita()
        session.add(cita)

        with pytest.raises(IntegrityError):
            session.commit()
"""
título: página de veterinarios
fecha: 03.12.2025
descripción: interfaz Streamlit para gestión completa de veterinarios.

CÓMO FUNCIONA:
===============

1. RegistrarVeterinario: Formulario para crear nuevos veterinarios
   └─ Input: nombre, DNI, cargo, especialidad, teléfono, email
   └─ Valida con utils.py → Llama a crear_veterinario()

2. ListarVeterinarios: Muestra listado de todos los veterinarios
   └─ Métrica de total
   └─ Expanders con información completa

3. BuscadorVeterinario: Busca por DNI o nombre
   └─ Dos opciones: búsqueda exacta (DNI) o parcial (nombre)
   └─ Muestra resultados en expanders

4. EditorVeterinario: Edita o elimina veterinarios
   └─ Busca por ID o DNI
   └─ Formulario de edición
   └─ Botones para actualizar o eliminar

ARQUITECTURA:
- 4 clases independientes: una por tab
- Cada clase es INDEPENDIENTE
- Usa session_state para persistir datos entre reruns
"""

import streamlit as st
from src.veterinarios import (
    crear_veterinario, listar_veterinarios, obtener_veterinario_por_id,
    buscar_veterinario_por_dni, buscar_veterinario_por_nombre,
    modificar_veterinario, eliminar_veterinario, veterinario_existe,
    obtener_veterinarios_por_especialidad
)
from src.clientes import obtener_cliente_por_id

from src.citas import obtener_citas_por_veterinario

from src.utils import Utilidades
from src.exceptions import DNIDuplicadoException, ValidacionException, VeterinarioNoEncontradoException

# ✅ PROTECCIÓN DE LOGIN
if not st.session_state.get("logged_in", False):
    st.warning("⚠ Debes iniciar sesión para acceder")
    st.stop()


# Configurar página
st.set_page_config(page_title="Gestión de Veterinarios", page_icon="🩺", layout="wide")

st.title("🩺 Gestión de Veterinarios")
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to top, rgb(194, 211, 255), rgb(255, 255, 255));
</style>
""", unsafe_allow_html=True)
st.markdown("---")

# ========================
# CLASE 1: REGISTRAR VETERINARIO
# ========================

class RegistrarVeterinario:
    """Responsabilidad: Mostrar formulario para registrar nuevos veterinarios"""
    
    @staticmethod
    def mostrar():
        """Renderiza el tab de registro"""
        st.header("Registrar nuevo veterinario")
        
        # Formulario con st.form
        with st.form("form_registrar_veterinario"):
            col1, col2 = st.columns(2)
            
            with col1:
                # TEXT_INPUT: Nombre
                nombre = st.text_input("Nombre completo *", placeholder="Ej: Dr. Juan Pérez García", key="reg_nombre")
                # TEXT_INPUT: DNI
                dni = st.text_input("DNI *", placeholder="Ej: 12345678A", key="reg_dni")
                # TEXT_INPUT: Cargo
                cargo = st.text_input("Cargo", placeholder="Ej: Veterinario", key="reg_cargo")
            
            with col2:
                # TEXT_INPUT: Especialidad
                especialidad = st.text_input("Especialidad", placeholder="Ej: Cirugía", key="reg_especialidad")
                # TEXT_INPUT: Teléfono
                telefono = st.text_input("Teléfono", placeholder="Ej: 600123456", key="reg_telefono")
                # TEXT_INPUT: Email
                email = st.text_input("Email", placeholder="Ej: juan@clinica.com", key="reg_email")
            
            st.markdown("*Los campos marcados con * son obligatorios*")
            
            # Botón SUBMIT
            if st.form_submit_button("Registrar veterinario", use_container_width=True):
                RegistrarVeterinario._procesar_registro(nombre, dni, cargo, especialidad, telefono, email)
    
    @staticmethod
    def _procesar_registro(nombre: str, dni: str, cargo: str, especialidad: str, telefono: str, email: str):
        """Valida y llama a crear_veterinario()"""
        # VALIDAR CAMPOS OBLIGATORIOS
        if not nombre or not dni:
            st.error("❌ El nombre y DNI son obligatorios")
            return
        
        # VALIDAR NOMBRE (solo letras)
        if not Utilidades.validar_nombre(nombre):
            st.error("❌ El nombre solo puede contener letras y espacios")
            return
        
        # VALIDAR DNI
        if not Utilidades.validar_dni(dni):
            st.error("❌ El DNI debe tener formato: 12345678A")
            return
        
        # VALIDAR EMAIL (si se proporciona)
        if email and not Utilidades.validar_email(email):
            st.error("❌ El email debe tener formato: juan@email.com")
            return
        
        # VALIDAR TELÉFONO (si se proporciona)
        if telefono and not Utilidades.validar_telefono(telefono):
            st.error("❌ El teléfono debe tener formato: 600123456")
            return
        
        # FORMATEAR DATOS
        nombre = Utilidades.formatear_nombre(nombre)
        dni = Utilidades.formatear_dni(dni)
        telefono = Utilidades.formatear_telefono(telefono) if telefono else None
        email = Utilidades.formatear_email(email) if email else None
        
        # CREAR VETERINARIO
        try:
            veterinario = crear_veterinario(nombre, dni, cargo or None, especialidad or None, telefono, email)
            st.success(f"✅ Veterinario {nombre} registrado con ID: {veterinario.id}")
        except DNIDuplicadoException as e:
            st.error(f"⚠ {str(e)}")
        except ValidacionException as e:
            st.error(f"⚠ {str(e)}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")


# ========================
# CLASE 2: LISTAR VETERINARIOS
# ========================

class ListarVeterinarios:
    """Responsabilidad: Mostrar listado de todos los veterinarios"""
    
    @staticmethod
    def mostrar():
        """Renderiza el tab de listado"""
        st.header("Lista de todos los veterinarios")
        
        try:
            # OBTENER TODOS LOS VETERINARIOS
            veterinarios = listar_veterinarios()
            
            if not veterinarios:
                st.info("ℹ No hay veterinarios registrados")
                return
            
            # MÉTRICA: Total
            st.metric("Total de veterinarios", len(veterinarios))
            
            # OPCIONALES: Filtro por especialidad
            especialidades = list(set([v.especialidad for v in veterinarios if v.especialidad]))
            if especialidades:
                filtro_especialidad = st.selectbox(
                    "Filtrar por especialidad:", 
                    ["Todas"] + especialidades, 
                    key="filtro_esp"
                )
                if filtro_especialidad != "Todas":
                    veterinarios = [v for v in veterinarios if v.especialidad == filtro_especialidad]
            
            st.markdown("---")
            ListarVeterinarios._mostrar_veterinarios(veterinarios)
        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    @staticmethod
    def _mostrar_veterinarios(veterinarios):
        """Renderiza cada veterinario en un expander"""
        for veterinario in veterinarios:
            with st.expander(f"🔹 {veterinario.nombre} - {veterinario.especialidad}"):
                tab1, tab2 = st.tabs(["Ficha del veterinario", "Citas"])
                with tab1: 
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**ID:** {veterinario.id}")
                        st.markdown(f"**Nombre:** {veterinario.nombre}")
                        st.markdown(f"**DNI:** {veterinario.dni}")
                        st.markdown(f"**Cargo:** {veterinario.cargo or 'N/A'}")

                    with col2:
                        st.markdown(f"**Especialidad:** {veterinario.especialidad or 'N/A'}")
                        st.markdown(f"**Teléfono:** {veterinario.telefono or 'N/A'}")
                        st.markdown(f"**Email:** {veterinario.email or 'N/A'}")
                with tab2:
                    citas = obtener_citas_por_veterinario(veterinario.id)
                    if citas:
                        for cita in citas:
                            st.subheader(f"{Utilidades.computarEmoticonoEspecie(cita.mascota.especie)} {Utilidades.formatear_fecha(cita.fecha)} - {cita.estado}")
                        
                            tab1, tab2 = st.tabs(["Información de la mascota", "Información de la cita"])
                            with tab1:
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.markdown(f"**ID:** {cita.mascota.id}")
                                    st.markdown(f"**Nombre:** {cita.mascota.nombre}")
                                    st.markdown(f"**Especie:** {cita.mascota.especie}")
                                    st.markdown(f"**Raza:** {cita.mascota.raza or 'No registrada'}")

                                with col2:
                                    st.markdown(f"**Edad:** {cita.mascota.edad or 'N/A'} años")
                                    st.markdown(f"**Peso:** {cita.mascota.peso or 'N/A'} kg")
                                    st.markdown(f"**Sexo:** {cita.mascota.sexo or 'No registrado'}")
                            with tab2:
                                st.markdown(f"**Fecha y hora**: el **{Utilidades.formatear_fecha(cita.fecha)}** a las **{cita.hora}**")
                                st.markdown(f"**Motivo:** {cita.motivo}")
                            st.divider()
                    else:
                        st.info("No hay citas registradas en este momento para este veterinario")


# ========================
# CLASE 3: BUSCADOR VETERINARIO
# ========================

class BuscadorVeterinario:
    """Responsabilidad: Buscar veterinarios por múltiples criterios"""
    
    @staticmethod
    def mostrar():
        """Renderiza el tab de búsqueda"""
        st.header("Buscar veterinarios")
        
        tipo = st.selectbox(
            "Buscar por:", 
            ["DNI", "Nombre", "Especialidad"],
            key="tipo_busqueda_vet"
        )
        
        if tipo == "DNI":
            BuscadorVeterinario._buscar_por_dni()
        elif tipo == "Nombre":
            BuscadorVeterinario._buscar_por_nombre()
        else:
            BuscadorVeterinario._buscar_por_especialidad()
    
    @staticmethod
    def _buscar_por_dni():
        dni = st.text_input("Introduce el DNI", placeholder="Ej: 12345678A", key="buscar_dni")
        
        if st.button("🔍 Buscar", use_container_width=True, key="btn_buscar_dni"):
            if not dni:
                st.warning("⚠ Introduce un DNI")
                return
            try:
                veterinario = buscar_veterinario_por_dni(dni)
                if veterinario:
                    st.success("✅ Encontrado")
                    with st.expander(f"🔹 {veterinario.nombre} - DNI: {veterinario.dni}"):
                        BuscadorVeterinario._mostrar_detalle(veterinario)
                else:
                    st.error(f"❌ No encontrado: {dni}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    @staticmethod
    def _buscar_por_nombre():
        nombre = st.text_input("Introduce el nombre (o parte)", placeholder="Ej: Juan", key="buscar_nombre")
        
        if st.button("🔍 Buscar", use_container_width=True, key="btn_buscar_nombre"):
            if not nombre:
                st.warning("⚠ Introduce un nombre")
                return
            try:
                veterinarios = buscar_veterinario_por_nombre(nombre)
                if veterinarios:
                    st.success(f"✅ {len(veterinarios)} encontrado(s)")
                    for vet in veterinarios:
                        with st.expander(f"🔹 {vet.nombre} - DNI: {vet.dni}"):
                            BuscadorVeterinario._mostrar_detalle(vet)
                else:
                    st.info(f"ℹ Sin resultados para: {nombre}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    @staticmethod
    def _buscar_por_especialidad():
        especialidad = st.text_input("Introduce la especialidad", placeholder="Ej: Cirugía", key="buscar_esp")
        
        if st.button("🔍 Buscar", use_container_width=True, key="btn_buscar_esp"):
            if not especialidad:
                st.warning("⚠ Introduce una especialidad")
                return
            try:
                veterinarios = obtener_veterinarios_por_especialidad(especialidad)
                if veterinarios:
                    st.success(f"✅ {len(veterinarios)} encontrado(s)")
                    for vet in veterinarios:
                        with st.expander(f"🔹 {vet.nombre} - {vet.especialidad or 'N/A'}"):
                            BuscadorVeterinario._mostrar_detalle(vet)
                else:
                    st.info(f"ℹ Sin resultados para: {especialidad}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    @staticmethod
    def _mostrar_detalle(veterinario):
        tab1, tab2 = st.tabs(["Ficha del veterinario", "Citas"])
        with tab1: 
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**ID:** {veterinario.id}")
                st.markdown(f"**Nombre:** {veterinario.nombre}")
                st.markdown(f"**DNI:** {veterinario.dni}")
                st.markdown(f"**Cargo:** {veterinario.cargo or 'N/A'}")

            with col2:
                st.markdown(f"**Especialidad:** {veterinario.especialidad or 'N/A'}")
                st.markdown(f"**Teléfono:** {veterinario.telefono or 'N/A'}")
                st.markdown(f"**Email:** {veterinario.email or 'N/A'}")
        with tab2:
            citas = obtener_citas_por_veterinario(veterinario.id)
            if citas:
                for cita in citas:
                    st.subheader(f"{Utilidades.computarEmoticonoEspecie(cita.mascota.especie)} {Utilidades.formatear_fecha(cita.fecha)} - {cita.estado}")
                   
                    tab1, tab2 = st.tabs(["Información de la mascota", "Información de la cita"])
                    with tab1:
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**ID:** {cita.mascota.id}")
                            st.markdown(f"**Nombre:** {cita.mascota.nombre}")
                            st.markdown(f"**Especie:** {cita.mascota.especie}")
                            st.markdown(f"**Raza:** {cita.mascota.raza or 'No registrada'}")

                        with col2:
                            st.markdown(f"**Edad:** {cita.mascota.edad or 'N/A'} años")
                            st.markdown(f"**Peso:** {cita.mascota.peso or 'N/A'} kg")
                            st.markdown(f"**Sexo:** {cita.mascota.sexo or 'No registrado'}")
                    with tab2:
                        st.markdown(f"**Fecha y hora**: el **{Utilidades.formatear_fecha(cita.fecha)}** a las **{cita.hora}**")
                        st.markdown(f"**Motivo:** {cita.motivo}")
                    st.divider()




# ========================
# CLASE 4: EDITOR VETERINARIO
# ========================

class EditorVeterinario:
    """Responsabilidad: Editar o eliminar veterinarios"""
    
    @staticmethod
    def mostrar():
        st.header("Editar o eliminar veterinario")
        
        tipo = st.selectbox("Buscar por:", ["ID", "DNI"], key="tipo_editar_vet")
        
        if tipo == "ID":
            EditorVeterinario._buscar_por_id()
        else:
            EditorVeterinario._buscar_por_dni()
        
        EditorVeterinario._mostrar_formulario_edicion()
    
    @staticmethod
    def _buscar_por_id():
        vet_id = st.number_input("ID", min_value=1, key="id_editar_vet")
        
        if st.button("🔍 Buscar", use_container_width=True, key="btn_editar_id_vet"):
            try:
                veterinario = obtener_veterinario_por_id(vet_id)
                st.session_state.veterinario_seleccionado = veterinario
                st.success(f"✅ {veterinario.nombre}")
            except VeterinarioNoEncontradoException:
                st.error(f"❌ No encontrado: {vet_id}")
                st.session_state.veterinario_seleccionado = None
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.session_state.veterinario_seleccionado = None
    
    @staticmethod
    def _buscar_por_dni():
        dni = st.text_input("DNI", placeholder="Ej: 12345678A", key="dni_editar_vet")
        
        if st.button("🔍 Buscar", use_container_width=True, key="btn_editar_dni_vet"):
            if not dni:
                st.warning("⚠ Introduce un DNI")
                return
            try:
                veterinario = buscar_veterinario_por_dni(dni)
                if veterinario:
                    st.session_state.veterinario_seleccionado = veterinario
                    st.success(f"✅ {veterinario.nombre}")
                else:
                    st.error(f"❌ No encontrado: {dni}")
                    st.session_state.veterinario_seleccionado = None
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.session_state.veterinario_seleccionado = None
    
    @staticmethod
    def _mostrar_formulario_edicion():
            """Formulario para editar o eliminar el veterinario seleccionado"""
            if "veterinario_seleccionado" not in st.session_state or not st.session_state.veterinario_seleccionado:
                return

            veterinario = st.session_state.veterinario_seleccionado

            # Flag para controlar si estamos en modo "confirmar eliminación"
            if "confirmar_elim_vet" not in st.session_state:
                st.session_state.confirmar_elim_vet = False

            st.markdown("---")
            st.subheader(f"✏ Editando: {veterinario.nombre} (ID: {veterinario.id})")

            if st.button("⬅ Volver"):
                st.session_state.veterinario_seleccionado = None
                st.session_state.confirmar_elim_vet = False
                st.rerun()

            # ===== FORMULARIO PRINCIPAL =====
            with st.form("form_editar_veterinario"):
                col1, col2 = st.columns(2)

                with col1:
                    nuevo_nombre = st.text_input("Nombre", value=veterinario.nombre, key="edit_nombre_vet")
                    nuevo_dni = st.text_input("DNI", value=veterinario.dni, key="edit_dni_vet")
                    nuevo_cargo = st.text_input("Cargo", value=veterinario.cargo or "", key="edit_cargo_vet")

                with col2:
                    nueva_especialidad = st.text_input("Especialidad", value=veterinario.especialidad or "", key="edit_esp_vet")
                    nuevo_telefono = st.text_input("Teléfono", value=veterinario.telefono or "", key="edit_tel_vet")
                    nuevo_email = st.text_input("Email", value=veterinario.email or "", key="edit_email_vet")

                # LOS TRES BOTONES EN LA MISMA FILA
                col_btn1, col_btn2, col_btn3 = st.columns(3)
                with col_btn1:
                    actualizar = st.form_submit_button("💾 Actualizar", use_container_width=True)
                with col_btn2:
                    pedir_eliminar = st.form_submit_button("🗑 Eliminar", use_container_width=True)
                with col_btn3:
                    cancelar = st.form_submit_button("❌ Cancelar edición", use_container_width=True)

            # ===== LÓGICA DE ACTUALIZAR =====
            if actualizar:
                try:
                    if nuevo_nombre and not Utilidades.validar_nombre(nuevo_nombre):
                        st.error("❌ Nombre inválido")
                    elif nuevo_dni and not Utilidades.validar_dni(nuevo_dni):
                        st.error("❌ DNI inválido")
                    elif nuevo_email and not Utilidades.validar_email(nuevo_email):
                        st.error("❌ Email inválido")
                    elif nuevo_telefono and not Utilidades.validar_telefono(nuevo_telefono):
                        st.error("❌ Teléfono inválido")
                    else:
                        # Formatear datos
                        nuevo_nombre_fmt = Utilidades.formatear_nombre(nuevo_nombre) if nuevo_nombre else None
                        nuevo_dni_fmt = Utilidades.formatear_dni(nuevo_dni) if nuevo_dni else None
                        nuevo_tel_fmt = Utilidades.formatear_telefono(nuevo_telefono) if nuevo_telefono else None
                        nuevo_email_fmt = Utilidades.formatear_email(nuevo_email) if nuevo_email else None

                        vet_act = modificar_veterinario(
                            veterinario.id,
                            nombre=nuevo_nombre_fmt if nuevo_nombre_fmt != veterinario.nombre else None,
                            dni=nuevo_dni_fmt if nuevo_dni_fmt != veterinario.dni else None,
                            cargo=nuevo_cargo if nuevo_cargo != (veterinario.cargo or "") else None,
                            especialidad=nueva_especialidad if nueva_especialidad != (veterinario.especialidad or "") else None,
                            telefono=nuevo_tel_fmt if nuevo_tel_fmt != (veterinario.telefono or "") else None,
                            email=nuevo_email_fmt if nuevo_email_fmt != (veterinario.email or "") else None
                        )
                        st.success("✅ Actualizado")
                        st.session_state.veterinario_seleccionado = vet_act
                except DNIDuplicadoException as e:
                    st.error(f"⚠ {str(e)}")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

            # ===== ENTRAR EN MODO CONFIRMACIÓN DE ELIMINACIÓN =====
            if pedir_eliminar:
                st.session_state.confirmar_elim_vet = True

            # ===== BOTONES DE CONFIRMACIÓN (FUERA DEL FORM) =====
            if st.session_state.confirmar_elim_vet:
                st.markdown("### 🗑 Eliminar este veterinario")
                st.warning(f"Esta acción eliminará al veterinario **{veterinario.nombre}**. No se puede deshacer.")

                col_conf1, col_conf2 = st.columns(2)
                with col_conf1:
                    if st.button("✅ Sí, eliminar definitivamente", use_container_width=True, key="vet_confirmar_elim"):
                        try:
                            eliminar_veterinario(veterinario.id)
                            st.success(f"✅ {veterinario.nombre} eliminado")
                            st.session_state.veterinario_seleccionado = None
                            st.session_state.confirmar_elim_vet = False
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")

                with col_conf2:
                    if st.button("❌ No, conservar veterinario", use_container_width=True, key="vet_cancelar_elim"):
                        st.session_state.confirmar_elim_vet = False
                        st.info("Eliminación cancelada")

            # ===== CANCELAR EDICIÓN =====
            if cancelar:
                st.session_state.veterinario_seleccionado = None
                st.session_state.confirmar_elim_vet = False
                st.rerun()


# ========================
# MAIN - RENDERIZACIÓN
# ========================

tab1, tab2, tab3, tab4 = st.tabs(["Registrar", "Listar", "Buscar", "Editar/Eliminar"])

with tab1:
    RegistrarVeterinario.mostrar()
with tab2:
    ListarVeterinarios.mostrar()
with tab3:
    BuscadorVeterinario.mostrar()
with tab4:
    EditorVeterinario.mostrar()
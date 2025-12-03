"""
título: página de mascotas
fecha: 03.12.2025
descripción: interfaz Streamlit para gestión completa de mascotas.
"""

import streamlit as st
from src.mascotas import (
    registrar_mascota, listar_mascotas, obtener_mascota_por_id,
    obtener_mascotas_por_cliente, obtener_mascotas_por_especie,
    modificar_mascota, eliminar_mascota, contar_mascotas,
    ver_historial_mascota
)
from src.clientes import buscar_cliente_por_dni, obtener_cliente_por_id
from src.utils import Utilidades
from src.exceptions import MascotaNoEncontradaException, ClienteNoEncontradoException, ValidacionException

# Configurar página
st.set_page_config(page_title="Gestión de Mascotas", page_icon="🐶", layout="wide")

st.title("🐶 Gestión de Mascotas")
st.markdown("---")

# ========================
# CLASE 1: REGISTRAR MASCOTA
# ========================

class RegistrarMascota:
    """Responsabilidad: Mostrar formulario para registrar nuevas mascotas"""
    
    ESPECIES = ["Perro", "Gato", "Conejo", "Pájaro", "Otros"]
    SEXOS = ["Macho", "Hembra", "No especificado"]
    
    @staticmethod
    def mostrar():
        """Renderiza el tab de registro"""
        st.header("Registrar nueva mascota")
        
        with st.form("form_registrar_mascota"):
            col1, col2 = st.columns(2)
            
            with col1:
                cliente_dni = st.text_input("DNI Cliente *", placeholder="Ej: 12345678A", key="reg_dni_cliente")
                nombre = st.text_input("Nombre mascota *", placeholder="Ej: Rex", key="reg_nombre")
                especie = st.selectbox("Especie *", RegistrarMascota.ESPECIES, key="reg_especie")
            
            with col2:
                raza = st.text_input("Raza", placeholder="Ej: Labrador", key="reg_raza")
                edad = st.number_input("Edad (años)", min_value=0, max_value=50, step=1, key="reg_edad")
                peso = st.number_input("Peso (kg)", min_value=0.0, step=0.1, key="reg_peso")
                sexo = st.selectbox("Sexo", RegistrarMascota.SEXOS, key="reg_sexo")
            
            st.markdown("Los campos marcados con * son obligatorios")
            
            if st.form_submit_button("Registrar mascota", use_container_width=True):
                RegistrarMascota._procesar_registro(cliente_dni, nombre, especie, raza, edad, peso, sexo)
    
    @staticmethod
    def _procesar_registro(cliente_dni: str, nombre: str, especie: str, raza: str, edad: int, peso: float, sexo: str):
        """Valida y llama a registrar_mascota()"""
        if not cliente_dni or not nombre or not especie:
            st.error("❌ DNI cliente, nombre y especie son obligatorios")
            return
        
        if not Utilidades.validar_dni(cliente_dni):
            st.error("❌ El DNI debe tener formato: 12345678A")
            return
        
        if not Utilidades.validar_nombre(nombre):
            st.error("❌ El nombre solo puede contener letras")
            return
        
        cliente_dni = Utilidades.formatear_dni(cliente_dni)
        nombre = Utilidades.formatear_nombre(nombre)
        
        try:
            cliente = buscar_cliente_por_dni(cliente_dni)
            if not cliente:
                st.error(f"❌ No existe cliente con DNI: {cliente_dni}")
                return
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            return
        
        try:
            mascota = registrar_mascota(
                nombre=nombre,
                especie=especie,
                cliente_id=cliente.id,
                raza=raza or None,
                edad=edad if edad > 0 else None,
                peso=peso if peso > 0 else None,
                sexo=sexo if sexo != "No especificado" else None
            )
            st.success(f"✅ Mascota {nombre} registrada con ID: {mascota.id}")
        except ClienteNoEncontradoException as e:
            st.error(f"⚠ {str(e)}")
        except ValidacionException as e:
            st.error(f"⚠ {str(e)}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")


# ========================
# CLASE 2: LISTAR MASCOTAS
# ========================

class ListarMascotas:
    """Responsabilidad: Mostrar listado de todas las mascotas"""
    
    @staticmethod
    def mostrar():
        """Renderiza el tab de listado"""
        st.header("Lista de todas las mascotas")
        
        try:
            mascotas = listar_mascotas()
            
            if not mascotas:
                st.info("ℹ No hay mascotas registradas")
                return
            
            st.metric("Total de mascotas", len(mascotas))
            
            especies = list(set([m.especie for m in mascotas if m.especie]))
            if especies:
                filtro_especie = st.selectbox(
                    "Filtrar por especie:",
                    ["Todas"] + sorted(especies),
                    key="filtro_esp"
                )
                if filtro_especie != "Todas":
                    mascotas = [m for m in mascotas if m.especie == filtro_especie]
            
            st.markdown("---")
            ListarMascotas._mostrar_mascotas(mascotas)
        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    @staticmethod
    def _mostrar_mascotas(mascotas):
        """Renderiza cada mascota en un expander"""
        for mascota in mascotas:
            try:
                titulo = f"🐾 {mascota.nombre} - {mascota.especie}"
                
                with st.expander(titulo):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"ID: {mascota.id}")
                        st.write(f"Nombre: {mascota.nombre}")
                        st.write(f"Especie: {mascota.especie}")
                        st.write(f"Raza: {mascota.raza or 'No registrada'}")
                    
                    with col2:
                        st.write(f"Edad: {mascota.edad or 'N/A'} años")
                        st.write(f"Peso: {mascota.peso or 'N/A'} kg")
                        st.write(f"Sexo: {mascota.sexo or 'No registrado'}")
                    
                    try:
                        cliente = obtener_cliente_por_id(mascota.cliente_id)
                        if cliente:
                            st.write(f"Propietario: {cliente.nombre} ({cliente.dni})")
                    except:
                        pass
            
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")


# ========================
# CLASE 3: BUSCADOR MASCOTA
# ========================

class BuscadorMascota:
    """Responsabilidad: Buscar mascotas por múltiples criterios"""
    
    @staticmethod
    def mostrar():
        """Renderiza el tab de búsqueda"""
        st.header("Buscar mascotas")
        
        tipo = st.selectbox(
            "Buscar por:",
            ["ID Mascota", "DNI Cliente", "Especie"],
            key="tipo_busqueda_masc"
        )
        
        if tipo == "ID Mascota":
            BuscadorMascota._buscar_por_id()
        elif tipo == "DNI Cliente":
            BuscadorMascota._buscar_por_cliente()
        else:
            BuscadorMascota._buscar_por_especie()
    
    @staticmethod
    def _buscar_por_id():
        mascota_id = st.number_input("ID de la mascota", min_value=1, step=1, key="buscar_id_masc")
        
        if st.button("🔍 Buscar", use_container_width=True, key="btn_buscar_id_masc"):
            try:
                mascota = obtener_mascota_por_id(mascota_id)
                st.success("✅ Encontrada")
                BuscadorMascota._mostrar_detalle(mascota)
            except MascotaNoEncontradaException:
                st.error(f"❌ No encontrada: {mascota_id}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    @staticmethod
    def _buscar_por_cliente():
        cliente_dni = st.text_input("DNI del cliente", placeholder="Ej: 12345678A", key="buscar_dni_cliente_masc")
        
        if st.button("🔍 Buscar", use_container_width=True, key="btn_buscar_cliente_masc"):
            if not cliente_dni:
                st.warning("⚠ Introduce un DNI")
                return
            
            try:
                cliente = buscar_cliente_por_dni(cliente_dni)
                if not cliente:
                    st.error(f"❌ No existe cliente con DNI: {cliente_dni}")
                    return
                
                mascotas = obtener_mascotas_por_cliente(cliente.id)
                if mascotas:
                    st.success(f"✅ {len(mascotas)} mascota(s) del cliente {cliente.nombre}")
                    for m in mascotas:
                        with st.expander(f"🐾 {m.nombre} - {m.especie}"):
                            BuscadorMascota._mostrar_detalle(m)
                else:
                    st.info(f"ℹ {cliente.nombre} no tiene mascotas")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    @staticmethod
    def _buscar_por_especie():
        especie = st.selectbox("Especie", ["Perro", "Gato", "Conejo", "Pájaro", "Otros"], key="buscar_esp_masc")
        
        if st.button("🔍 Buscar", use_container_width=True, key="btn_buscar_esp_masc"):
            try:
                mascotas = obtener_mascotas_por_especie(especie)
                if mascotas:
                    st.success(f"✅ {len(mascotas)} mascota(s) encontrada(s)")
                    for m in mascotas:
                        with st.expander(f"🐾 {m.nombre}"):
                            BuscadorMascota._mostrar_detalle(m)
                else:
                    st.info(f"ℹ Sin mascotas de especie: {especie}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    @staticmethod
    def _mostrar_detalle(mascota):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"ID: {mascota.id}")
            st.write(f"Nombre: {mascota.nombre}")
            st.write(f"Especie: {mascota.especie}")
            st.write(f"Raza: {mascota.raza or 'N/A'}")
        with col2:
            st.write(f"Edad: {mascota.edad or 'N/A'} años")
            st.write(f"Peso: {mascota.peso or 'N/A'} kg")
            st.write(f"Sexo: {mascota.sexo or 'N/A'}")
        
        try:
            cliente = obtener_cliente_por_id(mascota.cliente_id)
            if cliente:
                st.write(f"Propietario: {cliente.nombre} ({cliente.dni})")
        except:
            pass


# ========================
# CLASE 4: EDITOR MASCOTA
# ========================

class EditorMascota:
    """Responsabilidad: Editar o eliminar mascotas"""
    
    SEXOS = ["Macho", "Hembra", "No especificado"]
    
    @staticmethod
    def mostrar():
        """Renderiza el tab de edición"""
        st.header("Editar o eliminar mascota")

        # inicializar flag de confirmación si no existe
        if "mostrar_confirmacion_elim_masc" not in st.session_state:
            st.session_state.mostrar_confirmacion_elim_masc = False
        
        tipo = st.selectbox("Buscar por:", ["ID", "DNI Cliente"], key="tipo_editar_masc")
        
        if tipo == "ID":
            EditorMascota._buscar_por_id()
        else:
            EditorMascota._buscar_por_cliente()
        
        EditorMascota._mostrar_formulario_edicion()
    
    @staticmethod
    def _buscar_por_id():
        masc_id = st.number_input("ID", min_value=1, key="id_editar_masc")
        
        if st.button("🔍 Buscar", use_container_width=True, key="btn_editar_id_masc"):
            try:
                mascota = obtener_mascota_por_id(masc_id)
                st.session_state.mascota_seleccionada = mascota
                st.session_state.mostrar_confirmacion_elim_masc = False
                st.success(f"✅ {mascota.nombre}")
            except MascotaNoEncontradaException:
                st.error(f"❌ No encontrada: {masc_id}")
                st.session_state.mascota_seleccionada = None
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.session_state.mascota_seleccionada = None
    
    @staticmethod
    def _buscar_por_cliente():
        cliente_dni = st.text_input("DNI Cliente", placeholder="Ej: 12345678A", key="dni_editar_masc")
        
        if st.button("🔍 Buscar", use_container_width=True, key="btn_editar_cliente_masc"):
            if not cliente_dni:
                st.warning("⚠ Introduce un DNI")
                return
            
            try:
                cliente = buscar_cliente_por_dni(cliente_dni)
                if not cliente:
                    st.error(f"❌ No existe cliente con DNI: {cliente_dni}")
                    return
                
                mascotas = obtener_mascotas_por_cliente(cliente.id)
                if mascotas:
                    st.session_state.mascotas_encontradas = mascotas
                    st.session_state.mascota_seleccionada = None
                    st.session_state.mostrar_confirmacion_elim_masc = False
                    st.success(f"✅ {len(mascotas)} mascota(s)")
                else:
                    st.info(f"ℹ {cliente.nombre} no tiene mascotas")
                    st.session_state.mascotas_encontradas = []
                    st.session_state.mascota_seleccionada = None
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                return
        
        if st.session_state.get("mascotas_encontradas") and not st.session_state.get("mascota_seleccionada"):
            opciones = {f"{m.nombre} ({m.especie})": m.id for m in st.session_state.mascotas_encontradas}
            masc_label = st.selectbox("Selecciona mascota", list(opciones.keys()), key="sel_masc_editar")
            masc_id_sel = opciones[masc_label]
            
            if st.button("Seleccionar", use_container_width=True, key="btn_sel_masc"):
                try:
                    mascota = obtener_mascota_por_id(masc_id_sel)
                    st.session_state.mascota_seleccionada = mascota
                    st.session_state.mostrar_confirmacion_elim_masc = False
                    st.success(f"✅ Seleccionada: {mascota.nombre}")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    @staticmethod
    def _mostrar_formulario_edicion():
        mascota = st.session_state.get("mascota_seleccionada")
        if not mascota:
            return
        
        st.markdown("---")
        st.subheader(f"✏ Editando: {mascota.nombre} (ID: {mascota.id})")
        
        if st.button("⬅ Volver"):
            st.session_state.mascota_seleccionada = None
            st.session_state.mostrar_confirmacion_elim_masc = False
            st.rerun()
        
        with st.form("form_editar_mascota"):
            col1, col2 = st.columns(2)
            
            with col1:
                nuevo_nombre = st.text_input("Nombre", value=mascota.nombre, key="edit_nombre_masc")
                nueva_raza = st.text_input("Raza", value=mascota.raza or "", key="edit_raza_masc")
                nueva_edad = st.number_input(
                    "Edad (años)", value=mascota.edad or 0,
                    min_value=0, max_value=50, key="edit_edad_masc"
                )
            
            with col2:
                nuevo_peso = st.number_input(
                    "Peso (kg)", value=mascota.peso or 0.0,
                    min_value=0.0, step=0.1, key="edit_peso_masc"
                )
                nuevo_sexo = st.selectbox(
                    "Sexo",
                    EditorMascota.SEXOS,
                    index=EditorMascota.SEXOS.index(mascota.sexo) if mascota.sexo in EditorMascota.SEXOS else 2,
                    key="edit_sexo_masc"
                )
            
            col_btn1, col_btn2, col_btn3 = st.columns(3)
            with col_btn1:
                actualizar = st.form_submit_button("💾 Actualizar", use_container_width=True)
            with col_btn2:
                eliminar = st.form_submit_button("🗑 Eliminar", use_container_width=True)
            with col_btn3:
                cancelar = st.form_submit_button("❌ Cancelar edición", use_container_width=True)
        
        # ACTUALIZAR
        if actualizar:
            try:
                if nuevo_nombre and not Utilidades.validar_nombre(nuevo_nombre):
                    st.error("❌ Nombre inválido")
                else:
                    nuevo_nombre_fmt = Utilidades.formatear_nombre(nuevo_nombre) if nuevo_nombre else None
                    
                    masc_act = modificar_mascota(
                        mascota.id,
                        nombre=nuevo_nombre_fmt if nuevo_nombre_fmt != mascota.nombre else None,
                        raza=nueva_raza if nueva_raza != (mascota.raza or "") else None,
                        edad=nueva_edad if nueva_edad != (mascota.edad or 0) else None,
                        peso=nuevo_peso if nuevo_peso != (mascota.peso or 0.0) else None,
                        sexo=nuevo_sexo if nuevo_sexo != (mascota.sexo or "No especificado") else None
                    )
                    st.success("✅ Mascota actualizada")
                    st.session_state.mascota_seleccionada = masc_act
                    st.session_state.mostrar_confirmacion_elim_masc = False
            except ValidacionException as e:
                st.error(f"⚠ {str(e)}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
        
        # MARCAR QUE QUEREMOS CONFIRMAR ELIMINACIÓN
        if eliminar:
            st.session_state.mostrar_confirmacion_elim_masc = True
        
        # MOSTRAR CONFIRMACIÓN PERSISTENTE ENTRE RERUNS
        if st.session_state.get("mostrar_confirmacion_elim_masc"):
            st.warning(f"⚠ ¿Seguro que deseas eliminar a {mascota.nombre}? Esta acción eliminará también sus citas relacionadas.")
            col_conf1, col_conf2 = st.columns(2)
            with col_conf1:
                if st.button("✅ Sí, eliminar", use_container_width=True, key="confirmar_elim_masc"):
                    try:
                        eliminar_mascota(mascota.id)
                        st.success(f"✅ {mascota.nombre} eliminada")
                        st.session_state.mascota_seleccionada = None
                        st.session_state.mostrar_confirmacion_elim_masc = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
            with col_conf2:
                if st.button("❌ No, cancelar", use_container_width=True, key="cancelar_elim_masc"):
                    st.info("Eliminación cancelada")
                    st.session_state.mostrar_confirmacion_elim_masc = False
        
        # CANCELAR EDICIÓN
        if cancelar:
            st.session_state.mascota_seleccionada = None
            st.session_state.mostrar_confirmacion_elim_masc = False
            st.rerun()


# ========================
# MAIN - RENDERIZACIÓN
# ========================

tab1, tab2, tab3, tab4 = st.tabs(["Registrar", "Listar", "Buscar", "Editar/Eliminar"])

with tab1:
    RegistrarMascota.mostrar()
with tab2:
    ListarMascotas.mostrar()
with tab3:
    BuscadorMascota.mostrar()
with tab4:
    EditorMascota.mostrar()
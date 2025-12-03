"""
título: página de clientes
fecha: 03.12.2025
descripción: interfaz Streamlit para gestión completa de clientes.

CÓMO FUNCIONA:
===============

1. RegistrarCliente: Formulario para crear nuevos clientes
   └─ Input: nombre, DNI, teléfono, email
   └─ Valida → Llama a crear_cliente()

2. ListarClientes: Muestra listado de todos los clientes
   └─ Métrica de total
   └─ Expanders con información completa
   └─ Muestra mascotas asociadas

3. BuscadorCliente: Busca por DNI o nombre
   └─ Dos opciones: búsqueda exacta (DNI) o parcial (nombre)
   └─ Muestra resultados en expanders

4. EditorCliente: Edita o elimina clientes
   └─ Busca por DNI
   └─ Formulario de edición
   └─ Botones para actualizar o eliminar

ARQUITECTURA:
- 4 clases independientes: una por tab
- Cada clase es INDEPENDIENTE
- Usa session_state para persistir datos entre reruns
"""

import streamlit as st
from src.clientes import (
    crear_cliente, listar_clientes, obtener_cliente_por_id,
    buscar_cliente_por_dni, buscar_cliente_por_nombre,
    modificar_cliente, eliminar_cliente, contar_clientes
)
from src.mascotas import obtener_mascotas_por_cliente
from src.utils import Utilidades
from src.exceptions import ClienteNoEncontradoException, DNIDuplicadoException, ValidacionException

# Configurar página
st.set_page_config(page_title="Gestión de Clientes", page_icon="👤", layout="wide")

st.title("👤 Gestión de Clientes")
st.markdown("---")

# ========================
# CLASE 1: REGISTRAR CLIENTE
# ========================

class RegistrarCliente:
    """Responsabilidad: Mostrar formulario para registrar nuevos clientes"""
    
    @staticmethod
    def mostrar():
        """Renderiza el tab de registro"""
        st.header("Registrar nuevo cliente")
        
        with st.form("form_registrar_cliente"):
            col1, col2 = st.columns(2)
            
            with col1:
                nombre = st.text_input("Nombre completo *", placeholder="Ej: Juan Pérez García", key="reg_nombre")
                dni = st.text_input("DNI *", placeholder="Ej: 12345678A", key="reg_dni")
            
            with col2:
                telefono = st.text_input("Teléfono", placeholder="Ej: 600123456", key="reg_telefono")
                email = st.text_input("Email", placeholder="Ej: juan@email.com", key="reg_email")
            
            st.markdown("*Los campos marcados con * son obligatorios*")
            
            if st.form_submit_button("Registrar cliente", use_container_width=True):
                RegistrarCliente._procesar_registro(nombre, dni, telefono, email)
    
    @staticmethod
    def _procesar_registro(nombre: str, dni: str, telefono: str, email: str):
        """Valida y llama a crear_cliente()"""
        if not nombre or not dni:
            st.error("❌ Nombre y DNI son obligatorios")
            return
        
        if not Utilidades.validar_nombre(nombre):
            st.error("❌ El nombre solo puede contener letras")
            return
        
        if not Utilidades.validar_dni(dni):
            st.error("❌ El DNI debe tener formato: 12345678A")
            return
        
        if email and not Utilidades.validar_email(email):
            st.error("❌ El email debe tener formato: juan@email.com")
            return
        
        if telefono and not Utilidades.validar_telefono(telefono):
            st.error("❌ El teléfono debe tener formato: 600123456")
            return
        
        nombre = Utilidades.formatear_nombre(nombre)
        dni = Utilidades.formatear_dni(dni)
        telefono = Utilidades.formatear_telefono(telefono) if telefono else None
        email = Utilidades.formatear_email(email) if email else None
        
        try:
            cliente = crear_cliente(nombre, dni, telefono, email)
            st.success(f"✅ Cliente {nombre} registrado con ID: {cliente.id}")
        except DNIDuplicadoException as e:
            st.error(f"⚠ {str(e)}")
        except ValidacionException as e:
            st.error(f"⚠ {str(e)}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")


# ========================
# CLASE 2: LISTAR CLIENTES
# ========================

class ListarClientes:
    """Responsabilidad: Mostrar listado de todos los clientes"""
    
    @staticmethod
    def mostrar():
        """Renderiza el tab de listado"""
        st.header("Lista de todos los clientes")
        
        try:
            clientes = listar_clientes()
            
            if not clientes:
                st.info("ℹ No hay clientes registrados")
                return
            
            st.metric("Total de clientes", len(clientes))
            st.markdown("---")
            ListarClientes._mostrar_clientes(clientes)
        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    @staticmethod
    def _mostrar_clientes(clientes):
        """Renderiza cada cliente en un expander"""
        for cliente in clientes:
            try:
                titulo = f"👤 {cliente.nombre} - DNI: {cliente.dni}"
                
                with st.expander(titulo):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"*ID:* {cliente.id}")
                        st.write(f"*Nombre:* {cliente.nombre}")
                        st.write(f"*DNI:* {cliente.dni}")
                    
                    with col2:
                        st.write(f"*Teléfono:* {cliente.telefono or 'No registrado'}")
                        st.write(f"*Email:* {cliente.email or 'No registrado'}")
                    
                    mascotas = obtener_mascotas_por_cliente(cliente.id)
                    if mascotas:
                        st.markdown("🐾 Mascotas:")
                        for mascota in mascotas:
                            st.write(f"- {mascota.nombre} ({mascota.especie})")
                    else:
                        st.info("Sin mascotas registradas")
            
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")


# ========================
# CLASE 3: BUSCADOR CLIENTE
# ========================

class BuscadorCliente:
    """Responsabilidad: Buscar clientes por múltiples criterios"""
    
    @staticmethod
    def mostrar():
        """Renderiza el tab de búsqueda"""
        st.header("Buscar clientes")
        
        tipo = st.selectbox(
            "Buscar por:", 
            ["DNI", "Nombre"],
            key="tipo_busqueda_cliente"
        )
        
        if tipo == "DNI":
            BuscadorCliente._buscar_por_dni()
        else:
            BuscadorCliente._buscar_por_nombre()
    
    @staticmethod
    def _buscar_por_dni():
        dni = st.text_input("Introduce el DNI", placeholder="Ej: 12345678A", key="buscar_dni_cliente")
        
        if st.button("🔍 Buscar", use_container_width=True, key="btn_buscar_dni_cliente"):
            if not dni:
                st.warning("⚠ Introduce un DNI")
                return
            
            try:
                cliente = buscar_cliente_por_dni(dni)
                if cliente:
                    st.success("✅ Encontrado")
                    BuscadorCliente._mostrar_detalle(cliente)
                else:
                    st.error(f"❌ No encontrado: {dni}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    @staticmethod
    def _buscar_por_nombre():
        nombre = st.text_input("Introduce el nombre (o parte)", placeholder="Ej: Juan", key="buscar_nombre_cliente")
        
        if st.button("🔍 Buscar", use_container_width=True, key="btn_buscar_nombre_cliente"):
            if not nombre:
                st.warning("⚠ Introduce un nombre")
                return
            
            try:
                clientes = buscar_cliente_por_nombre(nombre)
                if clientes:
                    st.success(f"✅ {len(clientes)} encontrado(s)")
                    for cliente in clientes:
                        with st.expander(f"👤 {cliente.nombre} - DNI: {cliente.dni}"):
                            BuscadorCliente._mostrar_detalle(cliente)
                else:
                    st.info(f"ℹ Sin resultados para: {nombre}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    @staticmethod
    def _mostrar_detalle(cliente):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"*ID:* {cliente.id}")
            st.write(f"*Nombre:* {cliente.nombre}")
            st.write(f"*DNI:* {cliente.dni}")
        with col2:
            st.write(f"*Teléfono:* {cliente.telefono or 'N/A'}")
            st.write(f"*Email:* {cliente.email or 'N/A'}")
        
        mascotas = obtener_mascotas_por_cliente(cliente.id)
        if mascotas:
            st.markdown("🐾 Mascotas:")
            for mascota in mascotas:
                st.write(f"- {mascota.nombre} ({mascota.especie})")


# ========================
# CLASE 4: EDITOR CLIENTE (ARREGLADO)
# ========================

class EditorCliente:
    """Responsabilidad: Editar o eliminar clientes"""
    
    @staticmethod
    def mostrar():
        st.header("Editar o eliminar cliente")

        # Flag de confirmación de borrado
        if "confirmar_eliminacion_cliente" not in st.session_state:
            st.session_state.confirmar_eliminacion_cliente = False
        
        EditorCliente._buscar_cliente()
        EditorCliente._mostrar_formulario_edicion()
    
    @staticmethod
    def _buscar_cliente():
        dni = st.text_input("DNI", placeholder="Ej: 12345678A", key="dni_editar_cliente")
        
        if st.button("🔍 Buscar", use_container_width=True, key="btn_buscar_cliente"):
            if not dni:
                st.warning("⚠ Introduce un DNI")
                return
            
            try:
                cliente = buscar_cliente_por_dni(dni)
                if cliente:
                    st.session_state.cliente_seleccionado = cliente
                    st.session_state.confirmar_eliminacion_cliente = False
                    st.success(f"✅ {cliente.nombre} encontrado")
                else:
                    st.error(f"❌ No existe cliente con DNI: {dni}")
                    st.session_state.cliente_seleccionado = None
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.session_state.cliente_seleccionado = None
    
    @staticmethod
    def _mostrar_formulario_edicion():
        cliente = st.session_state.get("cliente_seleccionado")
        if not cliente:
            return
        
        st.markdown("---")
        st.subheader(f"✏ Editando: {cliente.nombre} (ID: {cliente.id})")
        
        if st.button("⬅ Volver"):
            st.session_state.cliente_seleccionado = None
            st.session_state.confirmar_eliminacion_cliente = False
            st.rerun()

        with st.form("form_editar_cliente"):
            col1, col2 = st.columns(2)
            
            with col1:
                nuevo_nombre = st.text_input("Nombre", value=cliente.nombre, key="edit_nombre")
            
            with col2:
                nuevo_telefono = st.text_input("Teléfono", value=cliente.telefono or "", key="edit_tel")
                nuevo_email = st.text_input("Email", value=cliente.email or "", key="edit_email")
            
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
                elif nuevo_email and not Utilidades.validar_email(nuevo_email):
                    st.error("❌ Email inválido")
                elif nuevo_telefono and not Utilidades.validar_telefono(nuevo_telefono):
                    st.error("❌ Teléfono inválido")
                else:
                    cliente_act = modificar_cliente(
                        cliente.id,
                        nombre=Utilidades.formatear_nombre(nuevo_nombre),
                        telefono=Utilidades.formatear_telefono(nuevo_telefono),
                        email=Utilidades.formatear_email(nuevo_email)
                    )
                    st.success("✅ Cliente actualizado")
                    st.session_state.cliente_seleccionado = cliente_act
                    st.session_state.confirmar_eliminacion_cliente = False
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

        # MOSTRAR CONFIRMACIÓN DE BORRADO (flag persistente)
        if eliminar:
            st.session_state.confirmar_eliminacion_cliente = True
        
        if st.session_state.confirmar_eliminacion_cliente:
            st.warning(f"⚠ ¿Seguro que deseas eliminar al cliente {cliente.nombre}? "
                       f"Se eliminarán también sus mascotas y citas asociadas.")
            
            col_c1, col_c2 = st.columns(2)
            with col_c1:
                if st.button("✅ Sí, eliminar", key="btn_conf_elim_cliente", use_container_width=True):
                    try:
                        eliminar_cliente(cliente.id)
                        st.success(f"✅ Cliente {cliente.nombre} eliminado correctamente")
                        st.session_state.cliente_seleccionado = None
                        st.session_state.confirmar_eliminacion_cliente = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")

            with col_c2:
                if st.button("❌ Cancelar eliminación", key="btn_cancel_elim_cliente", use_container_width=True):
                    st.session_state.confirmar_eliminacion_cliente = False
                    st.info("Eliminación cancelada")

        # CANCELAR EDICIÓN
        if cancelar:
            st.session_state.cliente_seleccionado = None
            st.session_state.confirmar_eliminacion_cliente = False
            st.rerun()


# ========================
# MAIN - RENDERIZACIÓN
# ========================

tab1, tab2, tab3, tab4 = st.tabs(["Registrar", "Listar", "Buscar", "Editar/Eliminar"])

with tab1:
    RegistrarCliente.mostrar()
with tab2:
    ListarClientes.mostrar()
with tab3:
    BuscadorCliente.mostrar()
with tab4:
    EditorCliente.mostrar()
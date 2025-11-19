"""
título: página de clientes
fecha: 11.11.2025
descripción: interfaz Streamlit para gestión completa de clientes.
Registrar, listar, buscar y editar clientes.
Cubre requisitos RF1-RF4.
"""

import streamlit as st
from src.clientes import (
    crear_cliente,
    listar_clientes,
    obtener_cliente_por_id,
    buscar_cliente_por_dni,
    buscar_cliente_por_nombre,
    modificar_cliente,
    eliminar_cliente
)
from src.utils import Utilidades
from src.mascotas import obtener_mascotas_por_cliente
from src.exceptions import *

# Configuración de la página
st.set_page_config(
    page_title="Gestión de Clientes",
    page_icon="👤",
    layout="wide"
)

# Título principal
st.title("👤 Gestión de Clientes")
st.markdown("---")

# Crear tabs para organizar funcionalidades
tab1, tab2, tab3, tab4 = st.tabs(["Registrar", "Listar", "Buscar", "Editar/Eliminar"])

# ========================================
# TAB 1: REGISTRAR CLIENTE
# ========================================
with tab1:
    st.header("Registrar nuevo cliente")
    
    with st.form("form_registrar_cliente"):
        col1, col2 = st.columns(2)
        
        with col1:
            nombre = st.text_input("Nombre completo *", placeholder="Ej: Juan Pérez García")
            dni = st.text_input("DNI *", placeholder="Ej: 12345678A")
        
        with col2:
            telefono = st.text_input("Teléfono", placeholder="Ej: 600123456")
            email = st.text_input("Email", placeholder="Ej: juan@email.com")
        
        st.markdown("*Los campos marcados con * son obligatorios*")
        
        submitted = st.form_submit_button("Registrar cliente", use_container_width=True)

        if submitted:
            # VALIDACIONES
            if not dni or not nombre:
                st.error("El nombre y el DNI son campos obligatorios")
            # NOMBRE
            if not Utilidades.validar_nombre(nombre):
                st.error("El nombre solo puede contener letras")
            # DNI
            if not Utilidades.validar_dni(dni):
                st.error("El DNI ha de tener el siguiente formato: 12345678A")
            # EMAIL
            if email and not Utilidades.validar_email(email):
                st.error("El email ha de tener el siguiente formato: juan@email.com")
            # TELÉFONO
            if telefono and not Utilidades.validar_telefono(telefono):
                st.error("El formato de teléfono tiene que ser: 123456789")

            # SI PASA LAS VALIDACIONES...
            if Utilidades.validar_nombre(nombre) and Utilidades.validar_dni(dni):
                if (not email or Utilidades.validar_email(email)) and (not telefono or Utilidades.validar_telefono(telefono)):
                    # FORMATEO para pasar valores estándar a la base de datos
                    nombre = Utilidades.formatear_nombre(nombre)
                    dni = Utilidades.formatear_dni(dni)
                    telefono = Utilidades.formatear_telefono(telefono) if telefono else None
                    email = Utilidades.formatear_email(email) if email else None
                    #Crear el cliente
                    try:
                        cliente = crear_cliente(nombre, dni, telefono, email)
                        if cliente:
                            st.success(f"Cliente *{nombre}* registrado correctamente con ID: {cliente.id}")
                        else:
                            st.error("Error al crear el cliente. Ya existe un cliente con este DNI")
                    # Error de integridad de la base de datos
                    except Exception as e:
                        st.error(f"Error: {str(e)}")

# ========================================
# TAB 2: LISTAR CLIENTES
# ========================================
with tab2:
    st.header("Lista de todos los clientes")
    
    try:
        clientes = listar_clientes()
        
        if not clientes:
            st.info("ℹNo hay clientes registrados todavía")
        else:
            st.metric("Total de clientes", len(clientes))
            st.markdown("---")
            
            for cliente in clientes:
                with st.expander(f"👤 {cliente.nombre} - DNI: {cliente.dni}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"*ID:* {cliente.id}")
                        st.write(f"*Nombre:* {cliente.nombre}")
                        st.write(f"*DNI:* {cliente.dni}")
                    
                    with col2:
                        st.write(f"*Teléfono:* {cliente.telefono or 'No registrado'}")
                        st.write(f"*Email:* {cliente.email or 'No registrado'}")
                    
                    # Mostrar mascotas del cliente
                    mascotas = obtener_mascotas_por_cliente(cliente.id)
                    if mascotas:
                        st.markdown("🐾 Mascotas:")
                        for mascota in mascotas:
                            st.write(f"- {mascota.nombre} ({mascota.especie})")
                    else:
                        st.info("Sin mascotas registradas")
    
    except Exception as e:
        st.error(f"Error al listar clientes: {str(e)}")

# ========================================
# TAB 3: BUSCAR CLIENTE
# ========================================
with tab3:
    st.header("Buscar clientes")
    
    tipo_busqueda = st.selectbox(
        "Buscar por:",
        ["DNI", "Nombre"],
    )
    
    if tipo_busqueda == "DNI":
        dni_buscar = st.text_input("Introduce el DNI", placeholder="Ej: 12345678A")
        
        if st.button("Buscar por DNI", use_container_width=True):
            if not dni_buscar:
                st.warning("Introduce un DNI para buscar")
            else:
                try:
                    cliente = buscar_cliente_por_dni(dni_buscar)
                    
                    if cliente:
                        st.success(f"Cliente encontrado")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"*ID:* {cliente.id}")
                            st.write(f"*Nombre:* {cliente.nombre}")
                            st.write(f"*DNI:* {cliente.dni}")
                        
                        with col2:
                            st.write(f"*Teléfono:* {cliente.telefono or 'No registrado'}")
                            st.write(f"*Email:* {cliente.email or 'No registrado'}")
                    else:
                        st.error(f"No se encontró ningún cliente con DNI: {dni_buscar}")
                
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    else:  # Buscar por nombre
        nombre_buscar = st.text_input("Introduce el nombre (o parte del nombre)", placeholder="Ej: Juan")
        
        if st.button("Buscar por nombre", use_container_width=True):
            if not nombre_buscar:
                st.warning("Introduce un nombre para buscar")
            else:
                try:
                    clientes = buscar_cliente_por_nombre(nombre_buscar)
                    
                    if clientes:
                        st.success(f"Se encontraron {len(clientes)} cliente(s)")
                        
                        for cliente in clientes:
                            with st.expander(f"👤 {cliente.nombre} - DNI: {cliente.dni}"):
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    st.write(f"*ID:* {cliente.id}")
                                    st.write(f"*Nombre:* {cliente.nombre}")
                                    st.write(f"*DNI:* {cliente.dni}")
                                
                                with col2:
                                    st.write(f"*Teléfono:* {cliente.telefono or 'No registrado'}")
                                    st.write(f"*Email:* {cliente.email or 'No registrado'}")
                    else:
                        st.error(f"No se encontraron clientes con nombre: {nombre_buscar}")
                
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# ========================================
# TAB 4: EDITAR/ELIMINAR CLIENTE
# ========================================
with tab4:
    st.header("Editar o eliminar cliente")
    
    cliente_dni = st.text_input("DNI", placeholder="DNI del cliente")
    
    if st.button("Buscar cliente por DNI", use_container_width=True):
        try:
            cliente = buscar_cliente_por_dni(cliente_dni)
            
            if cliente:
                st.session_state.cliente_seleccionado = cliente
                st.success(f"Cliente encontrado: {cliente.nombre}")
            else:
                st.error(f"No existe cliente con DNI: {cliente_dni}")
                st.session_state.cliente_seleccionado = None
        
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    # Si hay un cliente seleccionado, mostrar formulario de edición
    if "cliente_seleccionado" in st.session_state and st.session_state.cliente_seleccionado:
        cliente = st.session_state.cliente_seleccionado
        
        st.markdown("---")
        st.subheader("Editar datos")
        
        with st.form("form_editar_cliente"):
            col1, col2 = st.columns(2)
            
            with col1:
                nuevo_nombre = st.text_input("Nombre completo", value=cliente.nombre)
                nuevo_telefono = st.text_input("Teléfono", value=cliente.telefono or "")
            
            with col2:
                nuevo_email = st.text_input("Email", value=cliente.email or "")
            
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                actualizar = st.form_submit_button("Actualizar datos", use_container_width=True)
            
            with col_btn2:
                eliminar = st.form_submit_button("Eliminar cliente", use_container_width=True, type="primary")
            
            if actualizar:
                # VALIDACIONES EN ACTUALIZACIÓN
                errores = []
                
                if not Utilidades.validar_nombre(nuevo_nombre):
                    errores.append("El nombre solo puede contener letras")
                
                if nuevo_email and not Utilidades.validar_email(nuevo_email):
                    errores.append("El email no tiene un formato válido")
                
                if nuevo_telefono and not Utilidades.validar_telefono(nuevo_telefono):
                    errores.append("El teléfono debe tener 9 dígitos")
                
                if errores:
                    for error in errores:
                        st.error(error)
                else:
                    # FORMATEO
                    nuevo_nombre = Utilidades.formatear_nombre(nuevo_nombre)
                    nuevo_telefono = Utilidades.formatear_telefono(nuevo_telefono) if nuevo_telefono else None
                    nuevo_email = Utilidades.formatear_email(nuevo_email) if nuevo_email else None
                    
                    try:
                        cliente_actualizado = modificar_cliente(
                            cliente.id,
                            nombre=nuevo_nombre if nuevo_nombre != cliente.nombre else None,
                            telefono=nuevo_telefono if nuevo_telefono != cliente.telefono else None,
                            email=nuevo_email if nuevo_email != cliente.email else None
                        )
                        
                        if cliente_actualizado:
                            st.success(f"Cliente actualizado correctamente")
                            st.session_state.cliente_seleccionado = cliente_actualizado
                        else:
                            st.error("Error al actualizar el cliente")
                    
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            
            if eliminar:
                try:
                    confirmacion = st.checkbox(f"Confirmo que quiero eliminar a {cliente.nombre}")
                    
                    if confirmacion:
                        resultado = eliminar_cliente(cliente.id)
                        
                        if resultado:
                            st.success(f"Cliente {cliente.nombre} eliminado correctamente")
                            st.session_state.cliente_seleccionado = None
                        else:
                            st.error("Error al eliminar el cliente")
                    else:
                        st.warning("Marca la casilla de confirmación para eliminar")
                
                except Exception as e:
                    st.error(f"Error: {str(e)}")
"""
Título: Página de Veterinarios
Fecha: 19.11.2025
Descripción: Interfaz Streamlit para gestión completa de veterinarios.
Registrar, listar, buscar y editar veterinarios.
Cubre requisitos RF9-RF12.
"""

import streamlit as st
from src.veterinarios import (
    crear_veterinario,
    listar_veterinarios,
    obtener_veterinario_por_id,
    buscar_veterinario_por_dni,
    buscar_veterinario_por_nombre,
    modificar_veterinario,
    eliminar_veterinario
)
from src.utils import Utilidades
from src.exceptions import *

st.set_page_config(
    page_title="Gestión de Veterinarios",
    page_icon="🩺",
    layout="wide"
)

st.title("🩺 Gestión de Veterinarios")
st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["Registrar", "Listar", "Buscar", "Editar/Eliminar"])

# TAB 1: REGISTRAR VETERINARIO
with tab1:
    st.header("Registrar nuevo veterinario")
    
    with st.form("form_registrar_veterinario"):
        col1, col2 = st.columns(2)
        
        with col1:
            nombre = st.text_input("Nombre completo *", placeholder="Ej: Dr. Juan Pérez García")
            dni = st.text_input("DNI *", placeholder="Ej: 12345678A")
            cargo = st.text_input("Cargo", placeholder="Ej: Veterinario")
        
        with col2:
            especialidad = st.text_input("Especialidad", placeholder="Ej: Cirugía")
            telefono = st.text_input("Teléfono", placeholder="Ej: 600123456")
            email = st.text_input("Email", placeholder="Ej: juan@clinica.com")
        
        st.markdown("*Los campos marcados con * son obligatorios*")
        
        submitted = st.form_submit_button("Registrar veterinario", use_container_width=True)
        
        if submitted:
            if not dni or not nombre:
                st.error("El nombre y el DNI son campos obligatorios")
            if not Utilidades.validar_nombre(nombre):
                st.error("El nombre solo puede contener letras")
            if not Utilidades.validar_dni(dni):
                st.error("El DNI ha de tener el siguiente formato: 12345678A")
            if email and not Utilidades.validar_email(email):
                st.error("El email ha de tener el siguiente formato: juan@email.com")
            if telefono and not Utilidades.validar_telefono(telefono):
                st.error("El formato de teléfono tiene que ser: 123456789")
            
            if Utilidades.validar_nombre(nombre) and Utilidades.validar_dni(dni):
                if (not email or Utilidades.validar_email(email)) and (not telefono or Utilidades.validar_telefono(telefono)):
                    nombre = Utilidades.formatear_nombre(nombre)
                    dni = Utilidades.formatear_dni(dni)
                    telefono = Utilidades.formatear_telefono(telefono) if telefono else None
                    email = Utilidades.formatear_email(email) if email else None
                    
                    try:
                        veterinario = crear_veterinario(nombre, dni, cargo, especialidad, telefono, email)
                        if veterinario:
                            st.success(f"Veterinario {nombre} registrado correctamente con ID: {veterinario.id}")
                        else:
                            st.error("Error al crear el veterinario. Ya existe un veterinario con este DNI")
                    except DNIDuplicadoException as e:
                        st.error(f"Error: {str(e)}")
                    except ValidacionException as e:
                        st.warning(f"Validación: {str(e)}")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")

# TAB 2: LISTAR VETERINARIOS
with tab2:
    st.header("Lista de todos los veterinarios")
    
    try:
        veterinarios = listar_veterinarios()
        
        if not veterinarios:
            st.info("No hay veterinarios registrados todavía")
        else:
            st.metric("Total de veterinarios", len(veterinarios))
            st.markdown("---")
            
            for veterinario in veterinarios:
                with st.expander(f"{veterinario.nombre} - DNI: {veterinario.dni}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"*ID:* {veterinario.id}")
                        st.write(f"*Nombre:* {veterinario.nombre}")
                        st.write(f"*DNI:* {veterinario.dni}")
                        st.write(f"*Cargo:* {veterinario.cargo or 'No registrado'}")
                    
                    with col2:
                        st.write(f"*Especialidad:* {veterinario.especialidad or 'No registrada'}")
                        st.write(f"*Teléfono:* {veterinario.telefono or 'No registrado'}")
                        st.write(f"*Email:* {veterinario.email or 'No registrado'}")
    
    except Exception as e:
        st.error(f"Error al listar veterinarios: {str(e)}")

# TAB 3: BUSCAR VETERINARIO
with tab3:
    st.header("Buscar veterinarios")
    
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
                    veterinario = buscar_veterinario_por_dni(dni_buscar)
                    
                    if veterinario:
                        st.success("Veterinario encontrado")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"*ID:* {veterinario.id}")
                            st.write(f"*Nombre:* {veterinario.nombre}")
                            st.write(f"*DNI:* {veterinario.dni}")
                            st.write(f"*Cargo:* {veterinario.cargo or 'No registrado'}")
                        
                        with col2:
                            st.write(f"*Especialidad:* {veterinario.especialidad or 'No registrada'}")
                            st.write(f"*Teléfono:* {veterinario.telefono or 'No registrado'}")
                            st.write(f"*Email:* {veterinario.email or 'No registrado'}")
                    else:
                        st.error(f"No se encontró ningún veterinario con DNI: {dni_buscar}")
                
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    else:
        nombre_buscar = st.text_input("Introduce el nombre (o parte del nombre)", placeholder="Ej: Juan")
        
        if st.button("Buscar por nombre", use_container_width=True):
            if not nombre_buscar:
                st.warning("Introduce un nombre para buscar")
            else:
                try:
                    veterinarios = buscar_veterinario_por_nombre(nombre_buscar)
                    
                    if veterinarios:
                        st.success(f"Se encontraron {len(veterinarios)} veterinario(s)")
                        
                        for veterinario in veterinarios:
                            with st.expander(f"{veterinario.nombre} - DNI: {veterinario.dni}"):
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    st.write(f"*ID:* {veterinario.id}")
                                    st.write(f"*Nombre:* {veterinario.nombre}")
                                    st.write(f"*DNI:* {veterinario.dni}")
                                    st.write(f"*Cargo:* {veterinario.cargo or 'No registrado'}")
                                
                                with col2:
                                    st.write(f"*Especialidad:* {veterinario.especialidad or 'No registrada'}")
                                    st.write(f"*Teléfono:* {veterinario.telefono or 'No registrado'}")
                                    st.write(f"*Email:* {veterinario.email or 'No registrado'}")
                    else:
                        st.error(f"No se encontraron veterinarios con nombre: {nombre_buscar}")
                
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# TAB 4: EDITAR/ELIMINAR VETERINARIO
with tab4:
    st.header("Editar o eliminar veterinario")
    
    veterinario_dni = st.text_input("DNI", placeholder="DNI del veterinario")
    
    if st.button("Buscar veterinario por DNI", use_container_width=True):
        try:
            veterinario = buscar_veterinario_por_dni(veterinario_dni)
            
            if veterinario:
                st.session_state.veterinario_seleccionado = veterinario
                st.success(f"Veterinario encontrado: {veterinario.nombre}")
            else:
                st.error(f"No existe veterinario con DNI: {veterinario_dni}")
                st.session_state.veterinario_seleccionado = None
        
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    if "veterinario_seleccionado" in st.session_state and st.session_state.veterinario_seleccionado:
        veterinario = st.session_state.veterinario_seleccionado
        
        st.markdown("---")
        st.subheader("Editar datos")
        
        with st.form("form_editar_veterinario"):
            col1, col2 = st.columns(2)
            
            with col1:
                nuevo_nombre = st.text_input("Nombre completo", value=veterinario.nombre)
                nuevo_cargo = st.text_input("Cargo", value=veterinario.cargo or "")
                nuevo_telefono = st.text_input("Teléfono", value=veterinario.telefono or "")
            
            with col2:
                nueva_especialidad = st.text_input("Especialidad", value=veterinario.especialidad or "")
                nuevo_email = st.text_input("Email", value=veterinario.email or "")
            
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                actualizar = st.form_submit_button("Actualizar datos", use_container_width=True)
            
            with col_btn2:
                eliminar = st.form_submit_button("Eliminar veterinario", use_container_width=True, type="primary")
            
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
                        veterinario_actualizado = modificar_veterinario(
                            veterinario.id,
                            nombre=nuevo_nombre if nuevo_nombre != veterinario.nombre else None,
                            cargo=nuevo_cargo if nuevo_cargo != (veterinario.cargo or "") else None,
                            especialidad=nueva_especialidad if nueva_especialidad != (veterinario.especialidad or "") else None,
                            telefono=nuevo_telefono if nuevo_telefono != veterinario.telefono else None,
                            email=nuevo_email if nuevo_email != veterinario.email else None
                        )
                        
                        if veterinario_actualizado:
                            st.success("Veterinario actualizado correctamente")
                            st.session_state.veterinario_seleccionado = veterinario_actualizado
                        else:
                            st.error("Error al actualizar el veterinario")
                    
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            
            if eliminar:
                try:
                    confirmacion = st.checkbox(f"Confirmo que quiero eliminar a {veterinario.nombre}")
                    
                    if confirmacion:
                        resultado = eliminar_veterinario(veterinario.id)
                        
                        if resultado:
                            st.success(f"Veterinario {veterinario.nombre} eliminado correctamente")
                            st.session_state.veterinario_seleccionado = None
                        else:
                            st.error("Error al eliminar el veterinario")
                    else:
                        st.warning("Marca la casilla de confirmación para eliminar")
                
                except Exception as e:
                    st.error(f"Error: {str(e)}")
"""
Título: Página de Mascotas
Fecha: 19.11.2025
Descripción: Interfaz Streamlit para gestión completa de mascotas.
Registrar, listar, buscar y editar mascotas.
Cubre requisitos RF5-RF8.
"""

import streamlit as st
from src.mascotas import (
    registrar_mascota,
    listar_mascotas,
    obtener_mascota_por_id,
    obtener_mascotas_por_cliente,
    modificar_mascota,
    eliminar_mascota
)
from src.clientes import buscar_cliente_por_dni, obtener_cliente_por_id
from src.utils import Utilidades
from src.exceptions import *

st.set_page_config(
    page_title="Gestión de Mascotas",
    page_icon="dog",
    layout="wide"
)

st.title("🐶 Gestión de Mascotas")
st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["Registrar", "Listar", "Buscar", "Editar/Eliminar"])

# TAB 1: REGISTRAR MASCOTA
with tab1:
    st.header("Registrar nueva mascota")
    with st.form("form_registrar_mascota"):
        col1, col2 = st.columns(2)
        with col1:
            cliente_dni = st.text_input("DNI Cliente *", placeholder="Ej: 12345678A")
            nombre = st.text_input("Nombre mascota *", placeholder="Ej: Rex")
            especie = st.selectbox("Especie *", ["Perro", "Gato", "Conejo", "Pajaro", "Otros"])
        with col2:
            raza = st.text_input("Raza", placeholder="Ej: Labrador")
            edad = st.number_input("Edad (años)", min_value=0, max_value=50, step=1, key="edad_registrar")
            peso = st.number_input("Peso (kg)", min_value=0.0, step=0.1, key="peso_registrar")
        sexo = st.selectbox("Sexo", ["Macho", "Hembra", "No especificado"])
        st.markdown("*Los campos marcados con * son obligatorios*")
        submitted = st.form_submit_button("Registrar mascota", use_container_width=True)
        
        if submitted:
            if not nombre or not especie or not cliente_dni:
                st.error("Nombre, especie y DNI cliente son campos obligatorios")
            if not Utilidades.validar_dni(cliente_dni):
                st.error("El DNI debe tener el siguiente formato: 12345678A")
            if not Utilidades.validar_nombre(nombre):
                st.error("El nombre solo puede contener letras")
            if Utilidades.validar_dni(cliente_dni) and Utilidades.validar_nombre(nombre):
                cliente_dni = Utilidades.formatear_dni(cliente_dni)
                nombre = Utilidades.formatear_nombre(nombre)
                try:
                    cliente = buscar_cliente_por_dni(cliente_dni)
                    if not cliente:
                        st.error(f"No existe cliente con DNI: {cliente_dni}")
                    else:
                        mascota = registrar_mascota(
                            nombre=nombre,
                            especie=especie,
                            cliente_id=cliente.id,
                            raza=raza if raza else None,
                            edad=edad if edad > 0 else None,
                            peso=peso if peso > 0 else None,
                            sexo=sexo if sexo != "No especificado" else None
                        )
                        if mascota:
                            st.success(f"Mascota {nombre} registrada correctamente con ID: {mascota.id}")
                        else:
                            st.error("Error al registrar la mascota")
                except ClienteNoEncontradoException as e:
                    st.error(f"Error: {str(e)}")
                except ValidacionException as e:
                    st.warning(f"Validacion: {str(e)}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# TAB 2: LISTAR MASCOTAS
with tab2:
    st.header("Lista de todas las mascotas")
    try:
        mascotas = listar_mascotas()
        if not mascotas:
            st.info("No hay mascotas registradas todavía")
        else:
            st.metric("Total de mascotas", len(mascotas))
            st.markdown("---")
            for mascota in mascotas:
                with st.expander(f"{mascota.nombre} - {mascota.especie}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"*ID:* {mascota.id}")
                        st.write(f"*Nombre:* {mascota.nombre}")
                        st.write(f"*Especie:* {mascota.especie}")
                        st.write(f"*Raza:* {mascota.raza or 'No registrada'}")
                    with col2:
                        st.write(f"*Edad:* {mascota.edad or 'No registrada'} años")
                        st.write(f"*Peso:* {mascota.peso or 'No registrado'} kg")
                        st.write(f"*Sexo:* {mascota.sexo or 'No registrado'}")
                    try:
                        cliente = obtener_cliente_por_id(mascota.cliente_id)
                        if cliente:
                            st.write(f"*Propietario:* {cliente.nombre} ({cliente.dni})")
                    except:
                        pass
    except Exception as e:
        st.error(f"Error al listar mascotas: {str(e)}")

# TAB 3: BUSCAR MASCOTA
with tab3:
    st.header("Buscar mascotas")
    tipo_busqueda = st.selectbox(
        "Buscar por:",
        ["ID Mascota", "DNI Cliente"],
        key="tipo_busqueda"
    )
    
    if tipo_busqueda == "ID Mascota":
        mascota_id = st.number_input("ID de la mascota", min_value=1, step=1, key="buscar_id_mascota")
        if st.button("Buscar por ID", use_container_width=True, key="btn_buscar_id"):
            try:
                mascota = obtener_mascota_por_id(mascota_id)
                if mascota:
                    st.success("Mascota encontrada")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"*ID:* {mascota.id}")
                        st.write(f"*Nombre:* {mascota.nombre}")
                        st.write(f"*Especie:* {mascota.especie}")
                        st.write(f"*Raza:* {mascota.raza or 'No registrada'}")
                    with col2:
                        st.write(f"*Edad:* {mascota.edad or 'No registrada'} años")
                        st.write(f"*Peso:* {mascota.peso or 'No registrado'} kg")
                        st.write(f"*Sexo:* {mascota.sexo or 'No registrado'}")
                else:
                    st.error(f"No se encontró mascota con ID: {mascota_id}")
            except MascotaNoEncontradaException as e:
                st.error(f"Error: {str(e)}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        cliente_dni = st.text_input("DNI del cliente", placeholder="Ej: 12345678A", key="buscar_dni_cliente")
        if st.button("Buscar mascotas del cliente", use_container_width=True, key="btn_buscar_dni"):
            if not cliente_dni:
                st.warning("Introduce un DNI para buscar")
            else:
                try:
                    cliente = buscar_cliente_por_dni(cliente_dni)
                    if not cliente:
                        st.error(f"No existe cliente con DNI: {cliente_dni}")
                    else:
                        mascotas = obtener_mascotas_por_cliente(cliente.id)
                        if mascotas:
                            st.success(f"Se encontraron {len(mascotas)} mascota(s) del cliente {cliente.nombre}")
                            for mascota in mascotas:
                                with st.expander(f"{mascota.nombre} - {mascota.especie}"):
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        st.write(f"*ID:* {mascota.id}")
                                        st.write(f"*Nombre:* {mascota.nombre}")
                                        st.write(f"*Especie:* {mascota.especie}")
                                    with col2:
                                        st.write(f"*Edad:* {mascota.edad or 'No registrada'} años")
                                        st.write(f"*Peso:* {mascota.peso or 'No registrado'} kg")
                        else:
                            st.info(f"El cliente {cliente.nombre} no tiene mascotas registradas")
                except ClienteNoEncontradoException as e:
                    st.error(f"Error: {str(e)}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# TAB 4: EDITAR/ELIMINAR MASCOTA
with tab4:
    st.header("Editar o eliminar mascota")
    
    tipo_busqueda_editar = st.selectbox(
        "Buscar mascota por:",
        ["DNI Cliente", "ID Mascota"]
    )
    
    mascotas_disponibles = []
    
    if tipo_busqueda_editar == "DNI Cliente":
        cliente_dni_editar = st.text_input("DNI del cliente", placeholder="Ej: 12345678A", key="editar_dni_cliente")
        
        if cliente_dni_editar:
            try:
                cliente = buscar_cliente_por_dni(cliente_dni_editar)
                if cliente:
                    mascotas_disponibles = obtener_mascotas_por_cliente(cliente.id)
                    if not mascotas_disponibles:
                        st.info(f"El cliente {cliente.nombre} no tiene mascotas registradas")
                else:
                    st.error(f"No existe cliente con DNI: {cliente_dni_editar}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    else:  # Buscar por ID Mascota
        mascota_id_buscar = st.number_input("ID de la mascota", min_value=1, step=1, key="editar_id_mascota")
        
        if mascota_id_buscar > 0:
            try:
                mascota_encontrada = obtener_mascota_por_id(mascota_id_buscar)
                if mascota_encontrada:
                    mascotas_disponibles = [mascota_encontrada]
                else:
                    st.error(f"No existe mascota con ID: {mascota_id_buscar}")
            except MascotaNoEncontradaException:
                st.error(f"No existe mascota con ID: {mascota_id_buscar}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    # Si hay mascotas disponibles, mostrar selector
    if mascotas_disponibles:
        mascota_seleccionada_id = st.selectbox(
            "Selecciona la mascota a editar:",
            options=[m.id for m in mascotas_disponibles],
            format_func=lambda x: f"{next(m.nombre for m in mascotas_disponibles if m.id == x)} - {next(m.especie for m in mascotas_disponibles if m.id == x)}",
            key="select_mascota_editar"
        )
        
        if st.button("Cargar mascota seleccionada", key="btn_cargar_mascota"):
            mascota = obtener_mascota_por_id(mascota_seleccionada_id)
            if mascota:
                st.session_state.mascota_seleccionada = mascota
                st.success(f"Mascota cargada: {mascota.nombre}")
    
    # Mostrar formulario si hay mascota seleccionada
    if "mascota_seleccionada" in st.session_state and st.session_state.mascota_seleccionada:
        mascota = st.session_state.mascota_seleccionada
        st.markdown("---")
        st.subheader("Editar datos")
        
        with st.form("form_editar_mascota"):
            col1, col2 = st.columns(2)
            with col1:
                nuevo_nombre = st.text_input("Nombre", value=mascota.nombre)
                nueva_raza = st.text_input("Raza", value=mascota.raza or "")
                nueva_edad = st.number_input("Edad (años)", value=mascota.edad or 0, min_value=0, key="edad_editar")
            with col2:
                nuevo_peso = st.number_input("Peso (kg)", value=mascota.peso or 0.0, min_value=0.0, step=0.1, key="peso_editar")
                nuevo_sexo = st.selectbox(
                    "Sexo",
                    ["Macho", "Hembra", "No especificado"],
                    index=0 if mascota.sexo == "Macho" else (1 if mascota.sexo == "Hembra" else 2)
                )
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                actualizar = st.form_submit_button("Actualizar datos", use_container_width=True)
            with col_btn2:
                eliminar = st.form_submit_button("Eliminar mascota", use_container_width=True, type="primary")
            
            if actualizar:
                # VALIDACIONES EN ACTUALIZACIÓN
                errores = []
                
                if not Utilidades.validar_nombre(nuevo_nombre):
                    errores.append("El nombre solo puede contener letras")
                
                if errores:
                    for error in errores:
                        st.error(error)
                else:
                    # FORMATEO
                    nuevo_nombre = Utilidades.formatear_nombre(nuevo_nombre)
                    
                    try:
                        mascota_actualizada = modificar_mascota(
                            mascota.id,
                            nombre=nuevo_nombre if nuevo_nombre != mascota.nombre else None,
                            raza=nueva_raza if nueva_raza != (mascota.raza or "") else None,
                            edad=nueva_edad if nueva_edad != (mascota.edad or 0) else None,
                            peso=nuevo_peso if nuevo_peso != (mascota.peso or 0.0) else None,
                            sexo=nuevo_sexo if nuevo_sexo != (mascota.sexo or "No especificado") else None
                        )
                        if mascota_actualizada:
                            st.success("Mascota actualizada correctamente")
                            st.session_state.mascota_seleccionada = mascota_actualizada
                        else:
                            st.error("Error al actualizar la mascota")
                    except MascotaNoEncontradaException as e:
                        st.error(f"Error: {str(e)}")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            
            if eliminar:
                try:
                    confirmacion = st.checkbox(f"Confirmo que quiero eliminar a {mascota.nombre}")
                    if confirmacion:
                        resultado = eliminar_mascota(mascota.id)
                        if resultado:
                            st.success(f"Mascota {mascota.nombre} eliminada correctamente")
                            st.session_state.mascota_seleccionada = None
                        else:
                            st.error("Error al eliminar la mascota")
                    else:
                        st.warning("Marca la casilla de confirmación para eliminar")
                except MascotaNoEncontradaException as e:
                    st.error(f"Error: {str(e)}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
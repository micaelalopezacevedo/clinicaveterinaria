"""
título: página de citas
fecha: 11.11.2025
descripción: interfaz Streamlit para gestión completa de citas veterinarias.
Crear, listar, ver próximas, editar, marcar realizada y cancelar.
Cubre requisitos RF13-RF16.
"""

import streamlit as st
from datetime import datetime, date, time, timedelta
from src.citas import (
    crear_cita,
    listar_citas,
    obtener_cita_por_id,
    obtener_citas_por_mascota,
    obtener_citas_por_veterinario,
    obtener_citas_por_fecha,
    obtener_citas_por_estado,
    modificar_cita,
    cancelar_cita,
    eliminar_cita
)
from src.mascotas import listar_mascotas, obtener_mascota_por_id
from src.veterinarios import listar_veterinarios, obtener_veterinario_por_id
from src.clientes import obtener_cliente_por_id
from src.exceptions import *

st.set_page_config(
    page_title="Gestión de Citas",
    page_icon="📅",
    layout="wide"
)

st.title("📅 Gestión de Citas")
st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["Registrar", "Listar", "Buscar", "Editar/Cancelar"])

# TAB 1: REGISTRAR CITA
with tab1:
    st.header("Registrar nueva cita")
    
    with st.form("form_registrar_cita"):
        col1, col2 = st.columns(2)
        
        with col1:
            # Selector de mascota
            mascotas = listar_mascotas()
            if not mascotas:
                st.warning("No hay mascotas registradas. Registra una mascota primero.")
                mascota_id = None
            else:
                mascota_opciones = {f"{m.nombre} (ID: {m.id})": m.id for m in mascotas}
                mascota_seleccionada = st.selectbox(
                    "Mascota *",
                    options=list(mascota_opciones.keys()),
                    key="select_mascota_registrar"
                )
                mascota_id = mascota_opciones[mascota_seleccionada]
            
            # Fecha de la cita
            fecha_cita = st.date_input(
                "Fecha de la cita *",
                min_value=date.today(),
                value=date.today(),
                key="fecha_registrar"
            )
            
            # Motivo
            motivo = st.text_area("Motivo de la consulta", placeholder="Ej: Revisión anual, vacunación...")
        
        with col2:
            # Selector de veterinario
            veterinarios = listar_veterinarios()
            if not veterinarios:
                st.warning("No hay veterinarios registrados. Registra un veterinario primero.")
                veterinario_id = None
            else:
                vet_opciones = {f"{v.nombre} - {v.especialidad or 'General'} (ID: {v.id})": v.id for v in veterinarios}
                vet_seleccionado = st.selectbox(
                    "Veterinario *",
                    options=list(vet_opciones.keys()),
                    key="select_vet_registrar"
                )
                veterinario_id = vet_opciones[vet_seleccionado]
            
            # Hora de la cita - DROPDOWN CON HORARIOS
            horas_disponibles = [
                "09:00", "09:30", "10:00", "10:30", "11:00", "11:30",
                "12:00", "12:30", "13:00", "13:30", "14:00", "14:30",
                "15:00", "15:30", "16:00", "16:30", "17:00"
            ]
            hora_seleccionada = st.selectbox(
                "Hora de la cita *",
                options=horas_disponibles,
                key="hora_registrar"
            )
            # Convertir string a objeto time
            hora_cita = datetime.strptime(hora_seleccionada, '%H:%M').time()
            
            # Estado
            estado = st.selectbox(
                "Estado",
                ["Pendiente", "Confirmada", "Realizada", "Cancelada"],
                key="estado_registrar"
            )
        
        st.markdown("**Los campos marcados con * son obligatorios**")
        
        submitted = st.form_submit_button("Registrar cita", use_container_width=True)
        
        if submitted:
            if not mascota_id or not veterinario_id:
                st.error("Debe seleccionar una mascota y un veterinario")
            else:
                try:
                    # Validar que la fecha/hora no sea pasada
                    fecha_hora_cita = datetime.combine(fecha_cita, hora_cita)
                    if fecha_hora_cita < datetime.now():
                        st.error("No se pueden crear citas en el pasado")
                    else:
                        cita = crear_cita(
                            mascota_id=mascota_id,
                            veterinario_id=veterinario_id,
                            fecha=fecha_cita,
                            hora=hora_cita,
                            motivo=motivo if motivo else None,
                            estado=estado
                        )
                        if cita:
                            st.success(f"Cita registrada correctamente con ID: {cita.id}")
                            st.success(f"Fecha: {cita.fecha.strftime('%d/%m/%Y')} a las {cita.hora}")
                        else:
                            st.error("Error al registrar la cita")
                
                except ValidacionException as e:
                    st.error(f"Error de validación: {str(e)}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# TAB 2: LISTAR CITAS
with tab2:
    st.header("Lista de todas las citas")
    
    try:
        citas = listar_citas()
        
        if not citas:
            st.info("No hay citas registradas todavía")
        else:
            st.metric("Total de citas", len(citas))
            
            # Filtro por estado
            filtro_estado = st.selectbox(
                "Filtrar por estado:",
                ["Todas", "Pendiente", "Confirmada", "Realizada", "Cancelada"],
                key="filtro_estado_listar"
            )
            
            if filtro_estado != "Todas":
                citas = [c for c in citas if c.estado == filtro_estado]
            
            st.markdown("---")
            
            for cita in citas:
                # Obtener información relacionada
                try:
                    mascota = obtener_mascota_por_id(cita.mascota_id)
                    veterinario = obtener_veterinario_por_id(cita.veterinario_id)
                    cliente = obtener_cliente_por_id(mascota.cliente_id) if mascota else None
                    
                    # Color según estado
                    if cita.estado == "Pendiente":
                        icono = "🕐"
                    elif cita.estado == "Confirmada":
                        icono = "✅"
                    elif cita.estado == "Realizada":
                        icono = "✔️"
                    else:
                        icono = "❌"
                    
                    titulo = f"{icono} Cita ID: {cita.id} - {cita.fecha.strftime('%d/%m/%Y')} {cita.hora}"
                    
                    with st.expander(titulo):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**ID Cita:** {cita.id}")
                            st.write(f"**Fecha:** {cita.fecha.strftime('%d/%m/%Y')}")
                            st.write(f"**Hora:** {cita.hora}")
                            st.write(f"**Estado:** {cita.estado}")
                            if mascota:
                                st.write(f"**Mascota:** {mascota.nombre} ({mascota.especie})")
                            if cliente:
                                st.write(f"**Propietario:** {cliente.nombre}")
                        
                        with col2:
                            if veterinario:
                                st.write(f"**Veterinario:** {veterinario.nombre}")
                                st.write(f"**Especialidad:** {veterinario.especialidad or 'General'}")
                            if cita.motivo:
                                st.write(f"**Motivo:** {cita.motivo}")
                            if cita.diagnostico:
                                st.write(f"**Diagnóstico:** {cita.diagnostico}")
                
                except Exception as e:
                    st.error(f"Error al mostrar cita: {str(e)}")
    
    except Exception as e:
        st.error(f"Error al listar citas: {str(e)}")

# TAB 3: BUSCAR CITA
with tab3:
    st.header("Buscar citas")
    
    tipo_busqueda = st.selectbox(
        "Buscar por:",
        ["ID Cita", "Fecha", "Mascota", "Veterinario", "Estado"],
        key="tipo_busqueda"
    )
    
    if tipo_busqueda == "ID Cita":
        cita_id = st.number_input("ID de la cita", min_value=1, step=1, key="buscar_id_cita")
        
        if st.button("Buscar por ID", use_container_width=True, key="btn_buscar_id"):
            try:
                cita = obtener_cita_por_id(cita_id)
                
                if cita:
                    st.success("Cita encontrada")
                    mascota = obtener_mascota_por_id(cita.mascota_id)
                    veterinario = obtener_veterinario_por_id(cita.veterinario_id)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**ID:** {cita.id}")
                        st.write(f"**Fecha:** {cita.fecha.strftime('%d/%m/%Y')}")
                        st.write(f"**Hora:** {cita.hora}")
                        st.write(f"**Estado:** {cita.estado}")
                        if mascota:
                            st.write(f"**Mascota:** {mascota.nombre}")
                    
                    with col2:
                        if veterinario:
                            st.write(f"**Veterinario:** {veterinario.nombre}")
                        if cita.motivo:
                            st.write(f"**Motivo:** {cita.motivo}")
                        if cita.diagnostico:
                            st.write(f"**Diagnóstico:** {cita.diagnostico}")
                else:
                    st.error(f"No se encontró cita con ID: {cita_id}")
            
            except CitaNoEncontradaException as e:
                st.error(f"Error: {str(e)}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    elif tipo_busqueda == "Fecha":
        fecha_buscar = st.date_input("Selecciona la fecha", key="buscar_fecha")
        
        if st.button("Buscar por fecha", use_container_width=True, key="btn_buscar_fecha"):
            try:
                citas = obtener_citas_por_fecha(fecha_buscar)
                
                if citas:
                    st.success(f"Se encontraron {len(citas)} cita(s) para {fecha_buscar.strftime('%d/%m/%Y')}")
                    
                    for cita in citas:
                        mascota = obtener_mascota_por_id(cita.mascota_id)
                        veterinario = obtener_veterinario_por_id(cita.veterinario_id)
                        
                        with st.expander(f"Cita {cita.hora} - {mascota.nombre if mascota else 'N/A'}"):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write(f"**ID:** {cita.id}")
                                st.write(f"**Hora:** {cita.hora}")
                                st.write(f"**Estado:** {cita.estado}")
                            with col2:
                                if veterinario:
                                    st.write(f"**Veterinario:** {veterinario.nombre}")
                                if cita.motivo:
                                    st.write(f"**Motivo:** {cita.motivo}")
                else:
                    st.info(f"No hay citas para la fecha {fecha_buscar.strftime('%d/%m/%Y')}")
            
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    elif tipo_busqueda == "Mascota":
        mascotas = listar_mascotas()
        if mascotas:
            mascota_opciones = {f"{m.nombre} (ID: {m.id})": m.id for m in mascotas}
            mascota_seleccionada = st.selectbox("Selecciona la mascota", options=list(mascota_opciones.keys()))
            mascota_id = mascota_opciones[mascota_seleccionada]
            
            if st.button("Buscar citas de la mascota", use_container_width=True):
                try:
                    citas = obtener_citas_por_mascota(mascota_id)
                    
                    if citas:
                        st.success(f"Se encontraron {len(citas)} cita(s)")
                        for cita in citas:
                            veterinario = obtener_veterinario_por_id(cita.veterinario_id)
                            with st.expander(f"{cita.fecha.strftime('%d/%m/%Y')} {cita.hora} - {cita.estado}"):
                                st.write(f"**ID:** {cita.id}")
                                if veterinario:
                                    st.write(f"**Veterinario:** {veterinario.nombre}")
                                if cita.motivo:
                                    st.write(f"**Motivo:** {cita.motivo}")
                    else:
                        st.info("Esta mascota no tiene citas registradas")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("No hay mascotas registradas")
    
    elif tipo_busqueda == "Veterinario":
        veterinarios = listar_veterinarios()
        if veterinarios:
            vet_opciones = {f"{v.nombre} (ID: {v.id})": v.id for v in veterinarios}
            vet_seleccionado = st.selectbox("Selecciona el veterinario", options=list(vet_opciones.keys()))
            vet_id = vet_opciones[vet_seleccionado]
            
            if st.button("Buscar citas del veterinario", use_container_width=True):
                try:
                    citas = obtener_citas_por_veterinario(vet_id)
                    
                    if citas:
                        st.success(f"Se encontraron {len(citas)} cita(s)")
                        for cita in citas:
                            mascota = obtener_mascota_por_id(cita.mascota_id)
                            with st.expander(f"{cita.fecha.strftime('%d/%m/%Y')} {cita.hora} - {mascota.nombre if mascota else 'N/A'}"):
                                st.write(f"**ID:** {cita.id}")
                                st.write(f"**Estado:** {cita.estado}")
                                if cita.motivo:
                                    st.write(f"**Motivo:** {cita.motivo}")
                    else:
                        st.info("Este veterinario no tiene citas registradas")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("No hay veterinarios registrados")
    
    else:  # Buscar por Estado
        estado_buscar = st.selectbox(
            "Selecciona el estado",
            ["Pendiente", "Confirmada", "Realizada", "Cancelada"]
        )
        
        if st.button("Buscar por estado", use_container_width=True):
            try:
                citas = obtener_citas_por_estado(estado_buscar)
                
                if citas:
                    st.success(f"Se encontraron {len(citas)} cita(s) con estado: {estado_buscar}")
                    for cita in citas:
                        mascota = obtener_mascota_por_id(cita.mascota_id)
                        veterinario = obtener_veterinario_por_id(cita.veterinario_id)
                        
                        with st.expander(f"{cita.fecha.strftime('%d/%m/%Y')} {cita.hora}"):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write(f"**ID:** {cita.id}")
                                if mascota:
                                    st.write(f"**Mascota:** {mascota.nombre}")
                            with col2:
                                if veterinario:
                                    st.write(f"**Veterinario:** {veterinario.nombre}")
                                if cita.motivo:
                                    st.write(f"**Motivo:** {cita.motivo}")
                else:
                    st.info(f"No hay citas con estado: {estado_buscar}")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# TAB 4: EDITAR/CANCELAR CITA
with tab4:
    st.header("Editar o cancelar cita")
    
    # Selector de tipo de búsqueda
    tipo_busqueda_editar = st.selectbox(
        "Buscar cita por:",
        ["ID de Cita", "Veterinario", "Mascota"],
        key="tipo_busqueda_editar"
    )
    
    if tipo_busqueda_editar == "ID de Cita":
        cita_id_editar = st.number_input("ID de la cita", min_value=1, step=1, key="id_cita_editar")
        
        if st.button("Buscar cita por ID", use_container_width=True, key="btn_buscar_editar"):
            try:
                cita = obtener_cita_por_id(cita_id_editar)
                
                if cita:
                    st.session_state.cita_seleccionada = cita
                    st.success(f"Cita encontrada: {cita.fecha.strftime('%d/%m/%Y')} {cita.hora}")
                else:
                    st.error(f"No existe cita con ID: {cita_id_editar}")
                    st.session_state.cita_seleccionada = None
            
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    elif tipo_busqueda_editar == "Veterinario":
        veterinarios = listar_veterinarios()
        if veterinarios:
            vet_opciones = {f"{v.nombre} - {v.especialidad or 'General'} (ID: {v.id})": v.id for v in veterinarios}
            vet_seleccionado = st.selectbox(
                "Selecciona el veterinario",
                options=list(vet_opciones.keys()),
                key="select_vet_editar"
            )
            vet_id = vet_opciones[vet_seleccionado]
            
            if st.button("Buscar citas del veterinario", use_container_width=True, key="btn_buscar_vet_editar"):
                try:
                    citas = obtener_citas_por_veterinario(vet_id)
                    
                    if citas:
                        st.session_state.citas_encontradas = citas
                        st.session_state.tipo_busqueda_actual = "veterinario"
                        st.success(f"Se encontraron {len(citas)} cita(s)")
                    else:
                        st.info("Este veterinario no tiene citas registradas")
                        st.session_state.citas_encontradas = None
                        st.session_state.cita_seleccionada = None
                
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            
            # Mostrar lista de citas encontradas
            if "citas_encontradas" in st.session_state and st.session_state.citas_encontradas and st.session_state.get("tipo_busqueda_actual") == "veterinario":
                st.markdown("---")
                st.subheader("📋 Citas del veterinario")
                
                for cita in st.session_state.citas_encontradas:
                    try:
                        mascota = obtener_mascota_por_id(cita.mascota_id)
                        nombre_mascota = mascota.nombre if mascota else "N/A"
                        
                        # Icono según estado
                        if cita.estado == "Pendiente":
                            icono = "🕐"
                        elif cita.estado == "Confirmada":
                            icono = "✅"
                        elif cita.estado == "Realizada":
                            icono = "✔️"
                        else:
                            icono = "❌"
                        
                        with st.expander(f"{icono} ID: {cita.id} - {cita.fecha.strftime('%d/%m/%Y')} {cita.hora} - {nombre_mascota} ({cita.estado})"):
                            col_info, col_btn = st.columns([3, 1])
                            
                            with col_info:
                                st.write(f"**Fecha:** {cita.fecha.strftime('%d/%m/%Y')}")
                                st.write(f"**Hora:** {cita.hora}")
                                st.write(f"**Mascota:** {nombre_mascota}")
                                st.write(f"**Estado:** {cita.estado}")
                                if cita.motivo:
                                    st.write(f"**Motivo:** {cita.motivo}")
                            
                            with col_btn:
                                if st.button("✏️ Editar", key=f"editar_vet_{cita.id}", use_container_width=True):
                                    st.session_state.cita_seleccionada = cita
                                    st.session_state.citas_encontradas = None
                                    st.rerun()
                    
                    except Exception as e:
                        st.error(f"Error al mostrar cita: {str(e)}")
        else:
            st.warning("No hay veterinarios registrados")
    
    else:  # Buscar por Mascota
        mascotas = listar_mascotas()
        if mascotas:
            mascota_opciones = {f"{m.nombre} - {m.especie} (ID: {m.id})": m.id for m in mascotas}
            mascota_seleccionada = st.selectbox(
                "Selecciona la mascota",
                options=list(mascota_opciones.keys()),
                key="select_mascota_editar"
            )
            mascota_id = mascota_opciones[mascota_seleccionada]
            
            if st.button("Buscar citas de la mascota", use_container_width=True, key="btn_buscar_masc_editar"):
                try:
                    citas = obtener_citas_por_mascota(mascota_id)
                    
                    if citas:
                        st.session_state.citas_encontradas = citas
                        st.session_state.tipo_busqueda_actual = "mascota"
                        st.success(f"Se encontraron {len(citas)} cita(s)")
                    else:
                        st.info("Esta mascota no tiene citas registradas")
                        st.session_state.citas_encontradas = None
                        st.session_state.cita_seleccionada = None
                
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            
            # Mostrar lista de citas encontradas
            if "citas_encontradas" in st.session_state and st.session_state.citas_encontradas and st.session_state.get("tipo_busqueda_actual") == "mascota":
                st.markdown("---")
                st.subheader("📋 Citas de la mascota")
                
                for cita in st.session_state.citas_encontradas:
                    try:
                        veterinario = obtener_veterinario_por_id(cita.veterinario_id)
                        nombre_vet = veterinario.nombre if veterinario else "N/A"
                        
                        # Icono según estado
                        if cita.estado == "Pendiente":
                            icono = "🕐"
                        elif cita.estado == "Confirmada":
                            icono = "✅"
                        elif cita.estado == "Realizada":
                            icono = "✔️"
                        else:
                            icono = "❌"
                        
                        with st.expander(f"{icono} ID: {cita.id} - {cita.fecha.strftime('%d/%m/%Y')} {cita.hora} - Dr. {nombre_vet} ({cita.estado})"):
                            col_info, col_btn = st.columns([3, 1])
                            
                            with col_info:
                                st.write(f"**Fecha:** {cita.fecha.strftime('%d/%m/%Y')}")
                                st.write(f"**Hora:** {cita.hora}")
                                st.write(f"**Veterinario:** Dr. {nombre_vet}")
                                st.write(f"**Estado:** {cita.estado}")
                                if cita.motivo:
                                    st.write(f"**Motivo:** {cita.motivo}")
                            
                            with col_btn:
                                if st.button("✏️ Editar", key=f"editar_masc_{cita.id}", use_container_width=True):
                                    st.session_state.cita_seleccionada = cita
                                    st.session_state.citas_encontradas = None
                                    st.rerun()
                    
                    except Exception as e:
                        st.error(f"Error al mostrar cita: {str(e)}")
        else:
            st.warning("No hay mascotas registradas")
    
    # FORMULARIO DE EDICIÓN (aparece cuando hay una cita seleccionada)
    if "cita_seleccionada" in st.session_state and st.session_state.cita_seleccionada:
        cita = st.session_state.cita_seleccionada
        
        # Verificar si la cita está cancelada
        if cita.estado == "Cancelada":
            st.markdown("---")
            st.warning("⚠️ Esta cita está cancelada y no se puede editar")
            
            # Mostrar información de la cita cancelada (solo lectura)
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**ID:** {cita.id}")
                st.write(f"**Fecha:** {cita.fecha.strftime('%d/%m/%Y')}")
                st.write(f"**Hora:** {cita.hora}")
                st.write(f"**Estado:** {cita.estado}")
            with col2:
                try:
                    mascota = obtener_mascota_por_id(cita.mascota_id)
                    veterinario = obtener_veterinario_por_id(cita.veterinario_id)
                    if mascota:
                        st.write(f"**Mascota:** {mascota.nombre}")
                    if veterinario:
                        st.write(f"**Veterinario:** {veterinario.nombre}")
                    if cita.motivo:
                        st.write(f"**Motivo:** {cita.motivo}")
                except:
                    pass
            
            # Botón para volver
            if st.button("⬅️ Volver a la búsqueda", key="volver_cancelada"):
                st.session_state.cita_seleccionada = None
                st.rerun()
        
        else:
            # La cita NO está cancelada, se puede editar
            st.markdown("---")
            st.subheader(f"✏️ Editando Cita ID: {cita.id}")
            
            # Botón para volver a la búsqueda
            if st.button("⬅️ Volver a la búsqueda"):
                st.session_state.cita_seleccionada = None
                st.rerun()
            
            with st.form("form_editar_cita"):
                col1, col2 = st.columns(2)
                
                with col1:
                    nueva_fecha = st.date_input("Fecha", value=cita.fecha, min_value=date.today())
                    
                    # Hora de la cita - DROPDOWN CON HORARIOS
                    horas_disponibles = [
                        "09:00", "09:30", "10:00", "10:30", "11:00", "11:30",
                        "12:00", "12:30", "13:00", "13:30", "14:00", "14:30",
                        "15:00", "15:30", "16:00", "16:30", "17:00"
                    ]
                    # Encontrar el índice de la hora actual
                    indice_hora = horas_disponibles.index(cita.hora) if cita.hora in horas_disponibles else 0
                    
                    hora_seleccionada = st.selectbox(
                        "Hora",
                        options=horas_disponibles,
                        index=indice_hora,
                        key="hora_editar"
                    )
                    # Convertir string a objeto time
                    nueva_hora = datetime.strptime(hora_seleccionada, '%H:%M').time()
                    
                    nuevo_estado = st.selectbox(
                        "Estado",
                        ["Pendiente", "Confirmada", "Realizada"],
                        index=["Pendiente", "Confirmada", "Realizada"].index(cita.estado) if cita.estado in ["Pendiente", "Confirmada", "Realizada"] else 0
                    )
                
                with col2:
                    nuevo_motivo = st.text_area("Motivo", value=cita.motivo or "")
                    nuevo_diagnostico = st.text_area("Diagnóstico", value=cita.diagnostico or "")
                
                # Solo dos botones: Actualizar y Cancelar
                col_btn1, col_btn2 = st.columns(2)
                
                with col_btn1:
                    actualizar = st.form_submit_button("💾 Actualizar", use_container_width=True)
                
                with col_btn2:
                    cancelar_btn = st.form_submit_button("❌ Cancelar cita", use_container_width=True, type="primary")
            
            # FUERA DEL FORMULARIO - Procesar acciones
            if actualizar:
                try:
                    cita_actualizada = modificar_cita(
                        cita.id,
                        fecha=nueva_fecha if nueva_fecha != cita.fecha else None,
                        hora=nueva_hora if nueva_hora.strftime('%H:%M') != cita.hora else None,
                        motivo=nuevo_motivo if nuevo_motivo != (cita.motivo or "") else None,
                        estado=nuevo_estado if nuevo_estado != cita.estado else None,
                        diagnostico=nuevo_diagnostico if nuevo_diagnostico != (cita.diagnostico or "") else None
                    )
                    
                    if cita_actualizada:
                        st.success("✅ Cita actualizada correctamente")
                        st.session_state.cita_seleccionada = cita_actualizada
                        # Mostrar datos actualizados
                        st.info(f"📅 Nueva fecha: {cita_actualizada.fecha.strftime('%d/%m/%Y')} a las {cita_actualizada.hora}")
                        st.info(f"📊 Estado: {cita_actualizada.estado}")
                    else:
                        st.error("Error al actualizar la cita")
                
                except ValidacionException as e:
                    st.error(f"⚠️ Error de validación: {str(e)}")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
            
            if cancelar_btn:
                try:
                    cita_cancelada = cancelar_cita(cita.id)
                    if cita_cancelada:
                        st.success("✅ Cita cancelada correctamente")
                        st.session_state.cita_seleccionada = cita_cancelada
                        st.rerun()  # Recargar para mostrar el estado actualizado
                    else:
                        st.error("Error al cancelar la cita")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

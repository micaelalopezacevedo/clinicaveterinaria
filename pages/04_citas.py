"""
título: página de citas
fecha: 11.11.2025
descripción: interfaz Streamlit para gestión completa de citas veterinarias.

CÓMO FUNCIONA:
===============

1. RegistrarCita: Formulario para crear nuevas citas
   └─ Selectbox de mascota, veterinario, fecha, hora, estado
   └─ Al submit → crea_cita()

2. ListarCitas: Muestra listado de todas las citas
   └─ Filtro por estado (Pendiente, Confirmada, Realizada, Cancelada)
   └─ Muestra en expanders con información completa

3. BuscadorCita: Busca citas por múltiples criterios
   └─ Por ID, Fecha, Mascota, Veterinario, Estado
   └─ Cada búsqueda es un radio button

4. EditorCita: Edita o cancela citas
   └─ Busca la cita
   └─ Muestra formulario de edición
   └─ Botones para actualizar o cancelar

ARQUITECTURA:
- 4 clases: una por tab
- Cada clase es INDEPENDIENTE
- Usa session_state para persistir datos entre reruns
"""

import streamlit as st
from datetime import datetime, date, time
from src.citas import (
    crear_cita, listar_citas, obtener_cita_por_id,
    obtener_citas_por_mascota, obtener_citas_por_veterinario,
    obtener_citas_por_fecha, obtener_citas_por_estado,
    modificar_cita, cancelar_cita, eliminar_cita
)
from src.mascotas import listar_mascotas, obtener_mascota_por_id
from src.veterinarios import listar_veterinarios, obtener_veterinario_por_id
from src.clientes import obtener_cliente_por_id
from src.utils import Utilidades
from src.exceptions import ValidacionException, CitaNoEncontradaException


# Configurar página
st.set_page_config(page_title="Gestión de Citas", page_icon="📅", layout="wide")

st.title("📅 Gestión de Citas")
st.markdown("---")

# ========================
# CLASE 1: REGISTRAR CITA
# ========================

class RegistrarCita:
    """Responsabilidad: Mostrar formulario para registrar nuevas citas"""
    
    # Horarios disponibles (09:00 a 17:00, cada 30 min)
    HORAS = ["09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", 
             "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00"]
    
    @staticmethod
    def mostrar():
        """Renderiza el tab de registro"""
        st.header("Registrar nueva cita")
        
        # Formulario con st.form (envía datos de una vez al hacer submit)
        with st.form("form_registrar_cita"):
            col1, col2 = st.columns(2)
            
            with col1:
                # SELECTBOX: Mascota
                mascota_id = RegistrarCita._seleccionar_mascota()
                # DATE_INPUT: Fecha (mínimo hoy)
                fecha = st.date_input("Fecha de la cita *", min_value=date.today(), value=date.today(), key="fecha_reg")
                # TEXT_AREA: Motivo
                motivo = st.text_area("Motivo", placeholder="Ej: Revisión anual, vacunación...")
            
            with col2:
                # SELECTBOX: Veterinario
                vet_id = RegistrarCita._seleccionar_veterinario()
                # SELECTBOX: Hora
                hora = RegistrarCita._seleccionar_hora()
                # SELECTBOX: Estado
                estado = st.selectbox("Estado", ["Pendiente", "Confirmada", "Realizada", "Cancelada"], key="estado_reg")
            
            st.markdown("**Los campos marcados con * son obligatorios**")
            
            # Botón SUBMIT (envía el formulario)
            if st.form_submit_button("Registrar cita", use_container_width=True):
                RegistrarCita._procesar_registro(mascota_id, vet_id, fecha, hora, motivo, estado)
    
    @staticmethod
    def _seleccionar_mascota():
        """Dropdown de mascotas"""
        mascotas = listar_mascotas()
        if not mascotas:
            st.warning("No hay mascotas registradas")
            return None
        # Crear diccionario: "Nombre (ID: 1)" → 1
        opciones = {f"{m.nombre} (ID: {m.id})": m.id for m in mascotas}
        seleccionado = st.selectbox("Mascota *", list(opciones.keys()), key="sel_masc_reg")
        return opciones[seleccionado]
    
    @staticmethod
    def _seleccionar_veterinario():
        """Dropdown de veterinarios"""
        veterinarios = listar_veterinarios()
        if not veterinarios:
            st.warning("No hay veterinarios registrados")
            return None
        opciones = {f"{v.nombre} - {v.especialidad or 'General'} (ID: {v.id})": v.id for v in veterinarios}
        seleccionado = st.selectbox("Veterinario *", list(opciones.keys()), key="sel_vet_reg")
        return opciones[seleccionado]
    
    @staticmethod
    def _seleccionar_hora():
        """Dropdown de horas disponibles"""
        hora_str = st.selectbox("Hora *", RegistrarCita.HORAS, key="hora_reg")
        # Convertir "14:30" → objeto time(14, 30)
        return datetime.strptime(hora_str, '%H:%M').time()
    
    @staticmethod
    def _procesar_registro(mascota_id, vet_id, fecha, hora, motivo, estado):
        """Llama a crear_cita() y muestra resultado"""
        if not mascota_id or not vet_id:
            st.error("Debe seleccionar mascota y veterinario")
            return
        
        try:
            # Llamar a crear_cita del backend
            cita = crear_cita(mascota_id, vet_id, fecha, hora, motivo or None, estado)
            # Mostrar éxito
            st.success(f"✅ Cita registrada con ID: {cita.id}")
            st.success(f"📅 {Utilidades.formatear_fecha(cita.fecha)} a las {cita.hora}")
        except ValidacionException as e:
            st.error(f"⚠️ Error de validación: {str(e)}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")


# ========================
# CLASE 2: LISTAR CITAS
# ========================

class ListarCitas:
    """Responsabilidad: Mostrar listado de todas las citas con filtrado"""
    
    @staticmethod
    def mostrar():
        """Renderiza el tab de listado"""
        st.header("Lista de todas las citas")
        
        try:
            # Obtener todas las citas
            citas = listar_citas()
            
            if not citas:
                st.info("No hay citas registradas")
                return
            
            # Métrica: total de citas
            st.metric("Total de citas", len(citas))
            
            # Selectbox para filtrar por estado
            filtro = st.selectbox("Filtrar por estado:", 
                                 ["Todas", "Pendiente", "Confirmada", "Realizada", "Cancelada"], 
                                 key="filtro_list")
            
            # Aplicar filtro (si el usuario seleccionó un estado)
            if filtro != "Todas":
                citas = [c for c in citas if c.estado == filtro]
            
            st.markdown("---")
            ListarCitas._mostrar_citas(citas)
        
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    @staticmethod
    def _mostrar_citas(citas):
        """Renderiza cada cita en un expander"""
        for cita in citas:
            try:
                # Obtener datos relacionados
                mascota = obtener_mascota_por_id(cita.mascota_id)
                veterinario = obtener_veterinario_por_id(cita.veterinario_id)
                cliente = obtener_cliente_por_id(mascota.cliente_id) if mascota else None
                
                # Obtener icono del estado (de utils)
                icono = Utilidades.obtener_icono_estado_cita(cita.estado)
                
                # Título del expander
                titulo = f"{icono} ID: {cita.id} - {Utilidades.formatear_fecha(cita.fecha)} {cita.hora}"
                
                # Expander (desplegable)
                with st.expander(titulo):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**ID:** {cita.id}")
                        st.write(f"**Fecha:** {Utilidades.formatear_fecha(cita.fecha)}")
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
                st.error(f"Error: {str(e)}")


# ========================
# CLASE 3: BUSCADOR CITA
# ========================

class BuscadorCita:
    """Responsabilidad: Buscar citas por múltiples criterios"""
    
    @staticmethod
    def mostrar():
        """Renderiza el tab de búsqueda"""
        st.header("Buscar citas")
        
        # Selector de tipo de búsqueda
        tipo = st.selectbox("Buscar por:", 
                           ["ID Cita", "Fecha", "Mascota", "Veterinario", "Estado"], 
                           key="tipo_busqueda")
        
        # Mostrar interfaz según tipo de búsqueda
        if tipo == "ID Cita":
            BuscadorCita._buscar_id()
        elif tipo == "Fecha":
            BuscadorCita._buscar_fecha()
        elif tipo == "Mascota":
            BuscadorCita._buscar_mascota()
        elif tipo == "Veterinario":
            BuscadorCita._buscar_veterinario()
        else:
            BuscadorCita._buscar_estado()
    
    @staticmethod
    def _buscar_id():
        """Búsqueda por ID"""
        cita_id = st.number_input("ID", min_value=1, key="buscar_id")
        if st.button("Buscar", key="btn_id"):
            try:
                cita = obtener_cita_por_id(cita_id)
                st.success("✅ Encontrada")
                BuscadorCita._mostrar_detalle(cita)
            except CitaNoEncontradaException:
                st.error(f"No encontrada: {cita_id}")
            except Exception as e:
                st.error(str(e))
    
    @staticmethod
    def _buscar_fecha():
        """Búsqueda por fecha"""
        fecha = st.date_input("Fecha", key="buscar_fecha")
        if st.button("Buscar", key="btn_fecha"):
            try:
                citas = obtener_citas_por_fecha(fecha)
                if citas:
                    st.success(f"✅ {len(citas)} cita(s) encontrada(s)")
                    for c in citas:
                        mascota = obtener_mascota_por_id(c.mascota_id)
                        veterinario = obtener_veterinario_por_id(c.veterinario_id)
                        with st.expander(f"{c.hora} - {mascota.nombre if mascota else 'N/A'}"):
                            st.write(f"**ID:** {c.id} | **Estado:** {c.estado}")
                            if veterinario:
                                st.write(f"**Vet:** {veterinario.nombre}")
                else:
                    st.info("Sin citas para esa fecha")
            except Exception as e:
                st.error(str(e))
    
    @staticmethod
    def _buscar_mascota():
        """Búsqueda por mascota"""
        mascotas = listar_mascotas()
        if not mascotas:
            st.warning("Sin mascotas")
            return
        opciones = {f"{m.nombre} (ID: {m.id})": m.id for m in mascotas}
        mascota_id = opciones[st.selectbox("Mascota", list(opciones.keys()), key="buscar_masc")]
        if st.button("Buscar", key="btn_masc"):
            try:
                citas = obtener_citas_por_mascota(mascota_id)
                if citas:
                    st.success(f"✅ {len(citas)} cita(s)")
                    for c in citas:
                        vet = obtener_veterinario_por_id(c.veterinario_id)
                        with st.expander(f"{Utilidades.formatear_fecha(c.fecha)} {c.hora} - {c.estado}"):
                            st.write(f"**ID:** {c.id}")
                            if vet:
                                st.write(f"**Vet:** {vet.nombre}")
                else:
                    st.info("Sin citas")
            except Exception as e:
                st.error(str(e))
    
    @staticmethod
    def _buscar_veterinario():
        """Búsqueda por veterinario"""
        vets = listar_veterinarios()
        if not vets:
            st.warning("Sin veterinarios")
            return
        opciones = {f"{v.nombre} (ID: {v.id})": v.id for v in vets}
        vet_id = opciones[st.selectbox("Veterinario", list(opciones.keys()), key="buscar_vet")]
        if st.button("Buscar", key="btn_vet"):
            try:
                citas = obtener_citas_por_veterinario(vet_id)
                if citas:
                    st.success(f"✅ {len(citas)} cita(s)")
                    for c in citas:
                        mascota = obtener_mascota_por_id(c.mascota_id)
                        with st.expander(f"{Utilidades.formatear_fecha(c.fecha)} {c.hora} - {mascota.nombre if mascota else 'N/A'}"):
                            st.write(f"**ID:** {c.id} | **Estado:** {c.estado}")
                else:
                    st.info("Sin citas")
            except Exception as e:
                st.error(str(e))
    
    @staticmethod
    def _buscar_estado():
        """Búsqueda por estado"""
        estado = st.selectbox("Estado", ["Pendiente", "Confirmada", "Realizada", "Cancelada"], key="buscar_est")
        if st.button("Buscar", key="btn_est"):
            try:
                citas = obtener_citas_por_estado(estado)
                if citas:
                    st.success(f"✅ {len(citas)} cita(s) con estado: {estado}")
                    for c in citas:
                        mascota = obtener_mascota_por_id(c.mascota_id)
                        vet = obtener_veterinario_por_id(c.veterinario_id)
                        with st.expander(f"{Utilidades.formatear_fecha(c.fecha)} {c.hora}"):
                            st.write(f"**ID:** {c.id}")
                            if mascota:
                                st.write(f"**Mascota:** {mascota.nombre}")
                            if vet:
                                st.write(f"**Vet:** {vet.nombre}")
                else:
                    st.info(f"Sin citas con estado: {estado}")
            except Exception as e:
                st.error(str(e))
    
    @staticmethod
    def _mostrar_detalle(cita):
        """Muestra detalles completos de una cita"""
        mascota = obtener_mascota_por_id(cita.mascota_id)
        vet = obtener_veterinario_por_id(cita.veterinario_id)
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**ID:** {cita.id}")
            st.write(f"**Fecha:** {Utilidades.formatear_fecha(cita.fecha)}")
            st.write(f"**Hora:** {cita.hora}")
            st.write(f"**Estado:** {cita.estado}")
            if mascota:
                st.write(f"**Mascota:** {mascota.nombre}")
        with col2:
            if vet:
                st.write(f"**Vet:** {vet.nombre}")
            if cita.motivo:
                st.write(f"**Motivo:** {cita.motivo}")
            if cita.diagnostico:
                st.write(f"**Diagnóstico:** {cita.diagnostico}")


# ========================
# CLASE 4: EDITOR CITA
# ========================

class EditorCita:
    """Responsabilidad: Editar o cancelar citas existentes"""
    
    HORAS = ["09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30",
             "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00"]
    
    @staticmethod
    def mostrar():
        """Renderiza el tab de edición"""
        st.header("Editar o cancelar cita")
        
        tipo = st.selectbox("Buscar cita por:", ["ID de Cita", "Veterinario", "Mascota"], key="tipo_editar")
        
        if tipo == "ID de Cita":
            EditorCita._buscar_por_id()
        elif tipo == "Veterinario":
            EditorCita._buscar_por_vet()
        else:
            EditorCita._buscar_por_masc()
        
        # Mostrar formulario de edición si hay cita seleccionada
        EditorCita._mostrar_formulario_edicion()
    
    @staticmethod
    def _buscar_por_id():
        """Busca cita por ID"""
        cita_id = st.number_input("ID", min_value=1, key="id_editar")
        if st.button("Buscar", use_container_width=True, key="btn_editar_id"):
            try:
                cita = obtener_cita_por_id(cita_id)
                # Guardar en session_state para que persista tras rerun
                st.session_state.cita_seleccionada = cita
                st.success(f"✅ {Utilidades.formatear_fecha(cita.fecha)} {cita.hora}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.session_state.cita_seleccionada = None
    
    @staticmethod
    def _buscar_por_vet():
        """Busca citas por veterinario"""
        vets = listar_veterinarios()
        if not vets:
            st.warning("Sin veterinarios")
            return
        opciones = {f"{v.nombre} - {v.especialidad or 'General'} (ID: {v.id})": v.id for v in vets}
        vet_id = opciones[st.selectbox("Veterinario", list(opciones.keys()), key="editar_vet")]
        
        if st.button("Buscar", use_container_width=True, key="btn_editar_vet"):
            try:
                citas = obtener_citas_por_veterinario(vet_id)
                if citas:
                    st.session_state.citas_encontradas = citas
                    st.session_state.tipo_busqueda_editar = "vet"
                    st.success(f"✅ {len(citas)} cita(s)")
                else:
                    st.info("Sin citas")
                    st.session_state.citas_encontradas = None
            except Exception as e:
                st.error(str(e))
        
        EditorCita._mostrar_lista_encontradas("vet")
    
    @staticmethod
    def _buscar_por_masc():
        """Busca citas por mascota"""
        mascotas = listar_mascotas()
        if not mascotas:
            st.warning("Sin mascotas")
            return
        opciones = {f"{m.nombre} - {m.especie} (ID: {m.id})": m.id for m in mascotas}
        masc_id = opciones[st.selectbox("Mascota", list(opciones.keys()), key="editar_masc")]
        
        if st.button("Buscar", use_container_width=True, key="btn_editar_masc"):
            try:
                citas = obtener_citas_por_mascota(masc_id)
                if citas:
                    st.session_state.citas_encontradas = citas
                    st.session_state.tipo_busqueda_editar = "masc"
                    st.success(f"✅ {len(citas)} cita(s)")
                else:
                    st.info("Sin citas")
                    st.session_state.citas_encontradas = None
            except Exception as e:
                st.error(str(e))
        
        EditorCita._mostrar_lista_encontradas("masc")
    
    @staticmethod
    def _mostrar_lista_encontradas(tipo):
        """Muestra lista de citas encontradas con botones para seleccionar"""
        if "citas_encontradas" not in st.session_state or not st.session_state.citas_encontradas:
            return
        if st.session_state.get("tipo_busqueda_editar") != tipo:
            return
        
        st.markdown("---")
        st.subheader("📋 Citas encontradas")
        
        for cita in st.session_state.citas_encontradas:
            try:
                if tipo == "vet":
                    mascota = obtener_mascota_por_id(cita.mascota_id)
                    nombre = mascota.nombre if mascota else "N/A"
                else:
                    vet = obtener_veterinario_por_id(cita.veterinario_id)
                    nombre = vet.nombre if vet else "N/A"
                
                icono = Utilidades.obtener_icono_estado_cita(cita.estado)
                titulo = f"{icono} ID: {cita.id} - {Utilidades.formatear_fecha(cita.fecha)} {cita.hora} - {nombre} ({cita.estado})"
                
                with st.expander(titulo):
                    col_info, col_btn = st.columns([3, 1])
                    with col_info:
                        st.write(f"**Fecha:** {Utilidades.formatear_fecha(cita.fecha)}")
                        st.write(f"**Hora:** {cita.hora}")
                        st.write(f"**Estado:** {cita.estado}")
                        if cita.motivo:
                            st.write(f"**Motivo:** {cita.motivo}")
                    with col_btn:
                        if st.button("✏️ Editar", key=f"edit_{cita.id}", use_container_width=True):
                            st.session_state.cita_seleccionada = cita
                            st.session_state.citas_encontradas = None
                            st.rerun()
            except Exception as e:
                st.error(str(e))
    
    @staticmethod
    def _mostrar_formulario_edicion():
        """Formulario para editar o cancelar la cita seleccionada"""
        # Si no hay cita seleccionada, no mostrar formulario
        if "cita_seleccionada" not in st.session_state or not st.session_state.cita_seleccionada:
            return
        
        cita = st.session_state.cita_seleccionada
        
        # SI LA CITA ESTÁ CANCELADA: mostrar mensaje y botón para volver
        if cita.estado == "Cancelada":
            st.markdown("---")
            st.warning("⚠️ Cita cancelada - No se puede editar")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**ID:** {cita.id}")
                st.write(f"**Fecha:** {Utilidades.formatear_fecha(cita.fecha)}")
                st.write(f"**Hora:** {cita.hora}")
                st.write(f"**Estado:** {cita.estado}")
            with col2:
                try:
                    mascota = obtener_mascota_por_id(cita.mascota_id)
                    vet = obtener_veterinario_por_id(cita.veterinario_id)
                    if mascota:
                        st.write(f"**Mascota:** {mascota.nombre}")
                    if vet:
                        st.write(f"**Vet:** {vet.nombre}")
                    if cita.motivo:
                        st.write(f"**Motivo:** {cita.motivo}")
                except:
                    pass
            
            if st.button("⬅️ Volver", key="volver_cancelada"):
                st.session_state.cita_seleccionada = None
                st.rerun()
        
        else:
            # SI LA CITA NO ESTÁ CANCELADA: mostrar formulario de edición
            st.markdown("---")
            st.subheader(f"✏️ Editando Cita ID: {cita.id}")
            
            if st.button("⬅️ Volver"):
                st.session_state.cita_seleccionada = None
                st.rerun()
            
            # Formulario
            with st.form("form_editar_cita"):
                col1, col2 = st.columns(2)
                
                with col1:
                    nueva_fecha = st.date_input("Fecha", value=cita.fecha, min_value=date.today(), key="edit_fecha")
                    
                    indice_hora = EditorCita.HORAS.index(cita.hora) if cita.hora in EditorCita.HORAS else 0
                    hora_str = st.selectbox("Hora", EditorCita.HORAS, index=indice_hora, key="edit_hora")
                    nueva_hora = datetime.strptime(hora_str, '%H:%M').time()
                    
                    nuevo_estado = st.selectbox("Estado", ["Pendiente", "Confirmada", "Realizada"],
                                               index=["Pendiente", "Confirmada", "Realizada"].index(cita.estado) if cita.estado in ["Pendiente", "Confirmada", "Realizada"] else 0,
                                               key="edit_estado")
                
                with col2:
                    nuevo_motivo = st.text_area("Motivo", value=cita.motivo or "", key="edit_motivo")
                    nuevo_diag = st.text_area("Diagnóstico", value=cita.diagnostico or "", key="edit_diag")
                
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    actualizar = st.form_submit_button("💾 Actualizar", use_container_width=True)
                with col_btn2:
                    cancelar_btn = st.form_submit_button("❌ Cancelar", use_container_width=True, type="primary")
            
            # Procesar actualización
            if actualizar:
                try:
                    cita_act = modificar_cita(
                        cita.id,
                        fecha=nueva_fecha if nueva_fecha != cita.fecha else None,
                        hora=nueva_hora if nueva_hora.strftime('%H:%M') != cita.hora else None,
                        motivo=nuevo_motivo if nuevo_motivo != (cita.motivo or "") else None,
                        estado=nuevo_estado if nuevo_estado != cita.estado else None,
                        diagnostico=nuevo_diag if nuevo_diag != (cita.diagnostico or "") else None
                    )
                    st.success("✅ Actualizada")
                    st.session_state.cita_seleccionada = cita_act
                    st.rerun()
                except ValidacionException as e:
                    st.error(f"⚠️ {str(e)}")
                except Exception as e:
                    st.error(f"❌ {str(e)}")
            
            # Procesar cancelación
            if cancelar_btn:
                try:
                    cita_canc = cancelar_cita(cita.id)
                    st.success("✅ Cancelada")
                    st.session_state.cita_seleccionada = cita_canc
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ {str(e)}")


# ========================
# MAIN
# ========================

tab1, tab2, tab3, tab4 = st.tabs(["Registrar", "Listar", "Buscar", "Editar/Cancelar"])

with tab1:
    RegistrarCita.mostrar()
with tab2:
    ListarCitas.mostrar()
with tab3:
    BuscadorCita.mostrar()
with tab4:
    EditorCita.mostrar()

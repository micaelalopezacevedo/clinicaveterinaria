"""
título: página de citas
fecha: 11.11.2025
descripción: interfaz Streamlit para gestión completa de citas veterinarias.
"""

import streamlit as st
from datetime import datetime, date
from src.citas import (
    crear_cita, listar_citas, obtener_cita_por_id,
    obtener_citas_por_mascota, obtener_citas_por_veterinario,
    obtener_citas_por_fecha, obtener_citas_por_estado,
    modificar_cita, cancelar_cita
)
from src.mascotas import listar_mascotas, obtener_mascota_por_id
from src.veterinarios import listar_veterinarios, obtener_veterinario_por_id
from src.clientes import obtener_cliente_por_id
from src.utils import Utilidades
from src.exceptions import ValidacionException

# ✅ PROTECCIÓN DE LOGIN
if not st.session_state.get("logged_in", False):
    st.warning("⚠ Debes iniciar sesión para acceder")
    st.stop()


# ============= Configuración =============
st.set_page_config(page_title="Gestión de Citas", page_icon="📅", layout="wide")
st.title("📅 Gestión de Citas")
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to top, rgb(194, 211, 255), rgb(255, 255, 255));
</style>
""", unsafe_allow_html=True)
st.markdown("---")



# =========================================================
#  CLASE 1 — REGISTRAR CITA
# =========================================================
class RegistrarCita:
    HORAS = ["09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30",
             "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00"]

    @staticmethod
    def mostrar():
        st.header("Registrar nueva cita")

        with st.form("form_registrar_cita"):
            col1, col2 = st.columns(2)

            with col1:
                mascota_id = RegistrarCita._select_mascota()
                fecha = st.date_input("Fecha *", min_value=date.today(), value=date.today())
                motivo = st.text_area("Motivo", placeholder="Ej: Vacunación, revisión...")

            with col2:
                vet_id = RegistrarCita._select_vet()
                hora = RegistrarCita._select_hora()
                estado = st.selectbox("Estado", ["Pendiente", "Confirmada", "Realizada", "Cancelada"])

            submit = st.form_submit_button("Registrar cita", use_container_width=True)

            if submit:
                RegistrarCita._procesar(mascota_id, vet_id, fecha, hora, motivo, estado)

    @staticmethod
    def _select_mascota():
        mascotas = listar_mascotas()
        if not mascotas:
            st.warning("No hay mascotas registradas")
            return None
        opciones = {f"{m.nombre} (Propietario: {obtener_cliente_por_id(m.cliente_id).nombre} ({obtener_cliente_por_id(m.cliente_id).dni}))": m.id for m in mascotas}
        return opciones[st.selectbox("Mascota *", list(opciones.keys()))]

    @staticmethod
    def _select_vet():
        vets = listar_veterinarios()
        if not vets:
            st.warning("No hay veterinarios registrados")
            return None
        opciones = {f"{v.nombre} ({v.especialidad or 'General'})": v.id for v in vets}
        return opciones[st.selectbox("Veterinario *", list(opciones.keys()))]

    @staticmethod
    def _select_hora():
        hora_str = st.selectbox("Hora *", RegistrarCita.HORAS)
        return datetime.strptime(hora_str, "%H:%M").time()

    @staticmethod
    def _procesar(mascota_id, vet_id, fecha, hora, motivo, estado):
        if not mascota_id or not vet_id:
            st.error("Debes seleccionar mascota y veterinario")
            return
        try:
            cita = crear_cita(mascota_id, vet_id, fecha, hora, motivo or None, estado)
            st.success(f"✅ Cita creada con ID {cita.id}")
        except Exception as e:
            st.error(str(e))


# =========================================================
#  CLASE 2 — LISTAR CITAS
# =========================================================
class ListarCitas:
    @staticmethod
    def mostrar():
        st.header("Listado de Citas")

        citas = listar_citas()
        if not citas:
            st.info("No hay citas registradas")
            return

        st.metric("Total citas", len(citas))

        filtro = st.selectbox("Filtrar por estado:",
                              ["Todas", "Pendiente", "Confirmada", "Realizada", "Cancelada"])

        if filtro != "Todas":
            citas = [c for c in citas if c.estado == filtro]

        st.markdown("---")

        for c in citas:
            ListarCitas._expander(c)

    @staticmethod
    def _expander(cita):
        mascota = obtener_mascota_por_id(cita.mascota_id)
        vet = obtener_veterinario_por_id(cita.veterinario_id)
        cliente = obtener_cliente_por_id(mascota.cliente_id) if mascota else None

        icono = Utilidades.obtener_icono_estado_cita(cita.estado)
        titulo = f"{icono} Cita {cita.id} — {Utilidades.formatear_fecha(cita.fecha)} {cita.hora}"

        with st.expander(titulo):
            col1, col2 = st.columns(2)

            with col1:
                st.write(f"Estado: **{cita.estado}**")
                st.write(f"Fecha: {Utilidades.formatear_fecha(cita.fecha)}")
                st.write(f"Hora: {cita.hora}")
                st.write(f"Mascota: {mascota.nombre if mascota else 'N/A'}")
                if cliente:
                    st.write(f"Cliente: {cliente.nombre}")

            with col2:
                st.write(f"Veterinario: {vet.nombre if vet else 'N/A'}")
                if cita.motivo:
                    st.write(f"Motivo: {cita.motivo}")
                if cita.diagnostico:
                    st.write(f"Diagnóstico: {cita.diagnostico}")


# =========================================================
#  CLASE 3 — BUSCADOR
# =========================================================
class BuscadorCita:
    @staticmethod
    def mostrar():
        st.header("Buscar citas")

        tipo = st.selectbox("Buscar por:",
                            ["ID Cita", "Fecha", "Mascota", "Veterinario", "Estado"])

        if tipo == "ID Cita":
            BuscadorCita._por_id()

        elif tipo == "Fecha":
            BuscadorCita._por_fecha()

        elif tipo == "Mascota":
            BuscadorCita._por_mascota()

        elif tipo == "Veterinario":
            BuscadorCita._por_vet()

        else:
            BuscadorCita._por_estado()

    @staticmethod
    def _mostrar(cita):
        mascota = obtener_mascota_por_id(cita.mascota_id)
        vet = obtener_veterinario_por_id(cita.veterinario_id)
    
        with st.expander(f"Cita {cita.id} - {Utilidades.formatear_fecha(cita.fecha)}"):
            st.write(f"### Cita {cita.id}")
            st.write(f"Fecha: {Utilidades.formatear_fecha(cita.fecha)}")
            st.write(f"Hora: {cita.hora}")
            st.write(f"Estado: {cita.estado}")
            st.write(f"Mascota: {mascota.nombre if mascota else 'N/A'}")
            st.write(f"Veterinario: {vet.nombre if vet else 'N/A'}")
            st.write(f"Motivo: {cita.motivo if cita.motivo else 'N/A'}")

    @staticmethod
    def _por_id():
        cita_id = st.number_input("ID", min_value=1)
        if st.button("Buscar ID"):
            try:
                cita = obtener_cita_por_id(cita_id)
                BuscadorCita._mostrar(cita)
            except:
                st.error("No encontrada")

    @staticmethod
    def _por_fecha():
        fecha = st.date_input("Fecha")
        if st.button("Buscar fecha"):
            citas = obtener_citas_por_fecha(fecha)
            if citas:
                for c in citas:
                    BuscadorCita._mostrar(c)
            else:
                st.info("No hay citas")

    @staticmethod
    def _por_mascota():
        mascotas = listar_mascotas()
        opciones = {f"{m.nombre} (ID {m.id})": m.id for m in mascotas}
        mascota_id = opciones[st.selectbox("Mascota", list(opciones.keys()))]

        if st.button("Buscar mascota"):
            citas = obtener_citas_por_mascota(mascota_id)
            if citas:
                for c in citas:
                    BuscadorCita._mostrar(c)
            else:
                st.info("No hay citas")

    @staticmethod
    def _por_vet():
        vets = listar_veterinarios()
        opciones = {v.nombre: v.id for v in vets}
        vet_id = opciones[st.selectbox("Veterinario", list(opciones.keys()))]

        if st.button("Buscar veterinario"):
            citas = obtener_citas_por_veterinario(vet_id)
            if citas:
                for c in citas:
                    BuscadorCita._mostrar(c)
            else:
                st.info("No hay citas")

    @staticmethod
    def _por_estado():
        estado = st.selectbox("Estado", ["Pendiente", "Confirmada", "Realizada", "Cancelada"])
        if st.button("Buscar estado"):
            citas = obtener_citas_por_estado(estado)
            if citas:
                for c in citas:
                    BuscadorCita._mostrar(c)
            else:
                st.info("No hay citas")


# =========================================================
#  CLASE 4 — EDITOR
# =========================================================
class EditorCita:
    HORAS = RegistrarCita.HORAS

    @staticmethod
    def mostrar():
        st.header("Editar o cancelar cita")

        tipo = st.selectbox("Buscar por:", ["ID", "Veterinario", "Fecha"])

        if tipo == "ID":
            EditorCita._buscar_id()

        elif tipo == "Veterinario":
            EditorCita._buscar_vet()

        elif tipo == "Fecha":
            EditorCita._buscar_fecha()

        EditorCita._formulario()

    # -------------------------
    # BÚSQUEDAS
    # -------------------------
    @staticmethod
    def _buscar_id():
        cita_id = st.number_input("ID cita", min_value=1)
        if st.button("Buscar cita ID"):
            try:
                st.session_state.cita_sel = obtener_cita_por_id(cita_id)
            except:
                st.error("Cita no encontrada")
                st.session_state.cita_sel = None

    @staticmethod
    def _buscar_vet():
        vets = listar_veterinarios()
        opciones = {v.nombre: v.id for v in vets}
        vet_id = opciones[st.selectbox("Veterinario", opciones.keys())]

        if st.button("Buscar citas vet"):
            st.session_state.citas_lista = obtener_citas_por_veterinario(vet_id)

        EditorCita._lista()

    @staticmethod
    def _buscar_masc():
        mascotas = listar_mascotas()
        opciones = {m.nombre: m.id for m in mascotas}
        masc_id = opciones[st.selectbox("Mascota", opciones.keys())]

        if st.button("Buscar citas mascota"):
            st.session_state.citas_lista = obtener_citas_por_mascota(masc_id)

        EditorCita._lista()
    
    @staticmethod
    def _buscar_fecha():
        fecha = st.date_input("Fecha")
        if st.button("Buscar fecha"):
            st.session_state.citas_lista = obtener_citas_por_fecha(fecha)
        if st.session_state.citas_lista:
            EditorCita._lista()
        else: 
            st.info("No hay citas programadas para esta fecha")

        

    @staticmethod
    def _lista():
        if "citas_lista" not in st.session_state or not st.session_state.citas_lista:
            return

        for c in st.session_state.citas_lista:
            titulo = f"ID {c.id} — {Utilidades.formatear_fecha(c.fecha)} {c.hora}"
            with st.expander(titulo):
                if st.button(f"Editar {c.id}"):
                    st.session_state.cita_sel = c
                    st.session_state.citas_lista = None
                    st.rerun()

    # -------------------------
    # FORMULARIO EDICIÓN
    # -------------------------
    @staticmethod
    def _formulario():
        if "cita_sel" not in st.session_state or not st.session_state.cita_sel:
            return

        cita = st.session_state.cita_sel

        st.markdown("---")
        st.subheader(f"Editando cita {cita.id}")

        with st.form("form_edit_cita"):
            col1, col2 = st.columns(2)

            with col1:
                nueva_fecha = st.date_input("Fecha", value=cita.fecha)
                hora_idx = EditorCita.HORAS.index(cita.hora) if cita.hora in EditorCita.HORAS else 0
                hora_str = st.selectbox("Hora", EditorCita.HORAS, index=hora_idx)
                nueva_hora = datetime.strptime(hora_str, "%H:%M").time()
                nuevo_estado = st.selectbox("Estado", ["Pendiente", "Confirmada", "Realizada"],
                                            index=["Pendiente", "Confirmada", "Realizada"].index(cita.estado))

            with col2:
                motivo = st.text_area("Motivo", value=cita.motivo or "")
                diag = st.text_area("Diagnóstico", value=cita.diagnostico or "")

            actualizar = st.form_submit_button("Actualizar cita")
            cancelar = st.form_submit_button("Cancelar cita")

        if actualizar:
            try:
                cita_mod = modificar_cita(
                    cita.id,
                    fecha=nueva_fecha if nueva_fecha != cita.fecha else None,
                    hora=nueva_hora if nueva_hora.strftime("%H:%M") != cita.hora else None,
                    motivo=motivo if motivo != (cita.motivo or "") else None,
                    estado=nuevo_estado if nuevo_estado != cita.estado else None,
                    diagnostico=diag if diag != (cita.diagnostico or "") else None
                )
                st.success("Cita actualizada")
                st.session_state.cita_sel = cita_mod
            except Exception as e:
                st.error(str(e))

        if cancelar:
            try:
                cita_canc = cancelar_cita(cita.id)
                st.success("Cita cancelada")
                st.session_state.cita_sel = cita_canc
            except Exception as e:
                st.error(str(e))


# =========================================================
#  MAIN
# =========================================================

tab1, tab2, tab3, tab4 = st.tabs(["Registrar", "Listar", "Buscar", "Editar/Cancelar"])

with tab1:
    RegistrarCita.mostrar()
with tab2:
    ListarCitas.mostrar()
with tab3:
    BuscadorCita.mostrar()
with tab4:
    EditorCita.mostrar()
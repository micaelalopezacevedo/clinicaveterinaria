"""
título: aplicación principal (streamlit)
fecha: 04.12.2025
descripción: interfaz web interactiva que navega entre módulos existentes.
"""

import streamlit as st
from src.logger import Logger
from src.clientes import contar_clientes
from src.mascotas import contar_mascotas
from src.veterinarios import listar_veterinarios
from src.citas import listar_citas

# =====================================
# CONFIGURACIÓN PÁGINA
# =====================================

st.set_page_config(
    page_title="🏥 Clínica Veterinaria",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded"
)

Logger.configurar_logger()

# =====================================
# DASHBOARD PRINCIPAL
# =====================================

st.title("🏥 Bienvenido a Clínica Veterinaria")
st.markdown("Sistema de gestión integral para clientes, mascotas, veterinarios y citas")
st.divider()

# =====================================
# MÉTRICAS PRINCIPALES
# =====================================

try:
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("👥 Clientes", contar_clientes())

    with col2:
        st.metric("🐾 Mascotas", contar_mascotas())

    with col3:
        veterinarios = listar_veterinarios()
        st.metric("🩺 Veterinarios", len(veterinarios) if veterinarios else 0)

    with col4:
        citas = listar_citas()
        st.metric("📅 Citas", len(citas) if citas else 0)

except Exception as e:
    st.error("❌ Error cargando estadísticas")
    Logger.log_excepcion(e, "Dashboard")

st.divider()

# =====================================
# DESCRIPCIÓN DE MÓDULOS
# =====================================

st.subheader("📌 Funcionalidades del sistema")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 👤 Gestión de clientes
    - Crear nuevo cliente
    - Ver lista de clientes
    - Buscar por DNI o nombre
    - Editar información
    - Eliminar cliente
    """)

with col2:
    st.markdown("""
    ### 🐾 Gestión de mascotas
    - Registrar mascota
    - Asociar a cliente
    - Ver historial
    - Filtrar por especie
    - Eliminar mascota
    """)

col3, col4 = st.columns(2)

with col3:
    st.markdown("""
    ### 🩺 Gestión de veterinarios
    - Registrar veterinario
    - Ver especialidades
    - Buscar por nombre
    - Editar datos
    - Eliminar veterinario
    """)

with col4:
    st.markdown("""
    ### 📅 Gestión de citas
    - Agendar cita
    - Ver calendario
    - Cambiar horario
    - Cancelar cita
    - Ver diagnóstico
    """)

st.divider()

# =====================================
# ANÁLISIS
# =====================================

st.subheader("📈 Dashboard")
st.markdown("""
- Gráficos de mascotas por especie  
- Citas por veterinario  
- Clientes más frecuentes  
- Reportes personalizados  
""")

st.divider()
st.caption("🐾 Clínica Veterinaria v2.0 | Streamlit")

Logger.info("Página principal cargada correctamente.")
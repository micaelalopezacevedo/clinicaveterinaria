"""
título: aplicación principal (streamlit)
fecha: 04.12.2025
descripción: interfaz web interactiva que navega entre módulos existentes.
"""

import streamlit as st
import bcrypt

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

st.markdown("""
<style>
.stApp {
    background: linear-gradient(to top, rgb(194, 211, 255), rgb(255, 255, 255));
</style>
""", unsafe_allow_html=True)

Logger.configurar_logger()

# =====================================
# CONFIGURACIÓN DE AUTENTICACIÓN
# =====================================

# Hashear contraseñas
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Base de datos de usuarios (username: password_hash)
USUARIOS = {
    "admin": hash_password("admin123"),
    "vet": hash_password("vet123")
}

# Nombres asociados a usuarios
NOMBRES = {
    "admin": "Administrador",
    "vet": "Veterinario"
}

# Verificar contraseña
def verificar_contraseña(password_ingresada, password_hash):
    return bcrypt.checkpw(password_ingresada.encode('utf-8'), password_hash.encode('utf-8'))

# =====================================
# INICIALIZAR SESIÓN
# =====================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.name = None

# =====================================
# FORMULARIO DE LOGIN
# =====================================

if not st.session_state.logged_in:
    st.title("🏥 Clínica Veterinaria")
    st.markdown("### 🔐 Iniciar Sesión")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        username = st.text_input("👤 Usuario", placeholder="admin")
        password = st.text_input("🔑 Contraseña", type="password", placeholder="Ingresa tu contraseña")
        
        if st.button("🚀 Ingresar", use_container_width=True):
            if username in USUARIOS:
                if verificar_contraseña(password, USUARIOS[username]):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.name = NOMBRES[username]
                    Logger.info(f"Login exitoso: {username}")
                    st.success("✓ Bienvenido!")
                    st.rerun()
                else:
                    st.error("❌ Contraseña incorrecta")
                    Logger.warning(f"Intento fallido con usuario: {username}")
            else:
                st.error("❌ Usuario no encontrado")
                Logger.warning(f"Usuario no existente: {username}")

else:
    # =====================================
    # DASHBOARD PRINCIPAL (Usuario autenticado)
    # =====================================
    
    # Botón logout en sidebar
    with st.sidebar:
        st.markdown(f"👤 *{st.session_state.name}* ({st.session_state.username})")
        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.name = None
            Logger.info(f"Logout: {st.session_state.username}")
            st.rerun()
    
    st.title("🏥 Bienvenido a Clínica Veterinaria")
    st.markdown(f"👤 Usuario: *{st.session_state.name}* ({st.session_state.username})")
    st.markdown("Sistema de gestión integral para clientes, mascotas, veterinarios y citas")
    st.image("./img/logo_bueno.png", width=360 )
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
    Logger.info(f"Página principal cargada correctamente. Usuario: {st.session_state.name}")
"""
título: página principal
fecha: 11.11.2025
descripción: página de inicio de la aplicación Streamlit.
Muestra bienvenida y panel de estadísticas generales.
Punto de entrada principal de la aplicación.
"""

import streamlit as st
from src.database import Session, Base, engine  # importa lo necesario


st.title("Gestión de clínica veterinaria")
st.write("Marcos García, Micaela López, Alejandro González")
st.divider()
st.write("Esta página de inicio la completaremos más adelante")

st.subheader("⚠️ Administración de datos")

# Botón para resetear base de datos
if st.button("🗑️ Resetear base de datos (borrar todo)"):
    # Abrir sesión
    session = Session()

    # Borrar todas las filas de todas las tablas
    # IMPORTANTE: usar metadata.sorted_tables para respetar claves foráneas
    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())

    session.commit()
    session.close()

    st.success("Base de datos vaciada correctamente.")
    st.rerun()
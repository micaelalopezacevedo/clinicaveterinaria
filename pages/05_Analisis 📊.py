"""
título: página de análisis
fecha: 11.11.2025
descripción: dashboard con estadísticas y reportes de la clínica.
Muestra: estadísticas generales, carga de veterinarios,
mascotas por especie, próximas citas y análisis varios.
"""

import streamlit as st
import plotly.express as px
import pandas as pd
from src.analisis import (
    obtener_estadisticas_generales,
    obtener_carga_veterinarios,
    obtener_mascotas_por_especie,
    obtener_proximas_citas_hoy,
    obtener_proximas_citas_semana,
    obtener_proximas_citas_mes,
    obtener_veterinario_con_mas_citas,
    obtener_especie_mas_comun
)

# ✅ PROTECCIÓN DE LOGIN
if not st.session_state.get("logged_in", False):
    st.warning("⚠ Debes iniciar sesión para acceder")
    st.stop()

st.markdown("""
<style>
.stApp {
    background: linear-gradient(to top, rgb(194, 211, 255), rgb(255, 255, 255));
</style>
""", unsafe_allow_html=True)
# =========================
# CLASES DE VISUALIZACIÓN (SOLID)
# =========================

class AnalisisGeneral:
    """Responsabilidad: mostrar estadísticas generales en métricas"""
    @staticmethod
    def mostrar():
        try:
            stats = obtener_estadisticas_generales()
            col1, col2, col3, col4, col5 = st.columns(5)
            
            col1.metric("👥 Clientes", stats.get('total_clientes', 0))
            col2.metric("🐾 Mascotas", stats.get('total_mascotas', 0))
            col3.metric("👨‍⚕ Veterinarios", stats.get('total_veterinarios', 0))
            col4.metric("📅 Citas", stats.get('total_citas', 0))
            col5.metric("⏳ Pendientes", stats.get('citas_pendientes', 0))
        except Exception as e:
            st.error(f"Error al cargar estadísticas generales: {str(e)}")


class AnalisisCargaVeterinaria:
    """Responsabilidad: mostrar carga de trabajo de veterinarios"""
    @staticmethod
    def mostrar():
        try:
            carga = obtener_carga_veterinarios()
            
            if not carga:
                st.info("No hay veterinarios ni citas registradas")
                return
            
            df = pd.DataFrame(carga)
            df = df.rename(columns={'nombre': 'Veterinario', 'num_citas': 'Nº de citas'})
            
            st.subheader("👩‍⚕ Carga de trabajo de los veterinarios")
            st.dataframe(df[["Veterinario", "Nº de citas"]], use_container_width=True)
            
            # Gráfico interactivo de barras
            fig = px.bar(
                df, 
                x="Veterinario", 
                y="Nº de citas", 
                color="Nº de citas",
                color_continuous_scale="Teal", 
                title="Citas por veterinario",
                labels={"Nº de citas": "Número de citas"}
            )
            fig.update_layout(
                xaxis_title="Veterinario", 
                yaxis_title="Número de citas", 
                showlegend=False,
                hovermode="x unified"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        except Exception as e:
            st.error(f"Error al cargar carga de veterinarios: {str(e)}")


class AnalisisByEspecie:
    """Responsabilidad: mostrar distribución de mascotas por especie"""
    @staticmethod
    def mostrar():
        try:
            especiedict = obtener_mascotas_por_especie()
            
            if not especiedict:
                st.info("No hay mascotas registradas.")
                return
            
            labels, values = zip(*especiedict.items())
            
            st.subheader("🐶 Mascotas registradas por especie")
            df = pd.DataFrame({"Especie": labels, "Cantidad": values})
            st.dataframe(df, use_container_width=True)
            
            # Gráfico interactivo de pastel
            fig = px.pie(
                df, 
                names="Especie", 
                values="Cantidad", 
                title="Proporción de mascotas por especie",
                color_discrete_sequence=px.colors.sequential.Tealgrn,
                hole=0  # Cambiar a 0.4 para gráfico de dona
            )
            fig.update_layout(hovermode="closest")
            st.plotly_chart(fig, use_container_width=True)
        
        except Exception as e:
            st.error(f"Error al cargar mascotas por especie: {str(e)}")


class AnalisisProximasCitas:
    """Responsabilidad: mostrar citas próximas por período"""
    @staticmethod
    def mostrar():
        try:
            tabs = st.tabs(["Hoy", "Esta semana", "Este mes"])
            
            getters = [
                ("Hoy", obtener_proximas_citas_hoy),
                ("Semana", obtener_proximas_citas_semana),
                ("Mes", obtener_proximas_citas_mes)
            ]
            
            for i, (titulo, getter) in enumerate(getters):
                with tabs[i]:
                    citas = getter()
                    
                    if not citas:
                        st.info(f"No hay citas para {titulo.lower()}.")
                    else:
                        # Transforma objetos ORM a dict para DataFrame
                        data = []
                        for c in citas:
                            data.append({
                                'ID': c.id,
                                'Fecha': str(c.fecha),
                                'Hora': c.hora,
                                'Mascota': c.mascota.nombre,
                                'Cliente': c.mascota.cliente.nombre,
                                'Veterinario': c.veterinario.nombre,
                                'Estado': c.estado,
                                'Motivo': c.motivo or '-'
                            })
                        
                        df = pd.DataFrame(data)
                        st.dataframe(df, use_container_width=True)
                        st.metric(f"Total de citas {titulo.lower()}", len(citas))
        
        except Exception as e:
            st.error(f"Error al cargar próximas citas: {str(e)}")


class AnalisisVeterinarioTop:
    """Responsabilidad: mostrar el veterinario con más citas"""
    @staticmethod
    def mostrar():
        try:
            top = obtener_veterinario_con_mas_citas()
            
            if not top or top.get("num_citas", 0) == 0:
                st.info("No hay citas registradas para mostrar veterinario destacado.")
                return
            
            st.success(
                f"⭐ Veterinario más solicitado: *{top['nombre']}* con *{top['num_citas']} cita(s)*"
            )
        
        except Exception as e:
            st.error(f"Error al cargar veterinario top: {str(e)}")


class AnalisisEspecieTop:
    """Responsabilidad: mostrar la especie más frecuente"""
    @staticmethod
    def mostrar():
        try:
            especie = obtener_especie_mas_comun()
            
            if especie:
                st.success(f"🏆 Especie de mascota más común: *{especie}*")
            else:
                st.info("No hay datos de especies para mostrar.")
        
        except Exception as e:
            st.error(f"Error al cargar especie top: {str(e)}")


# =========================
# FUNCIÓN PRINCIPAL
# =========================

def main():
    st.title("📊 Panel de Análisis y Estadísticas")
    st.markdown("Resumen de indicadores y tendencias de actividad de la clínica veterinaria")
    st.markdown("---")
    
    # ESTADÍSTICAS GENERALES
    st.subheader("📈 Estadísticas Generales")
    AnalisisGeneral.mostrar()
    
    st.markdown("---")
    
    # DOS COLUMNAS: CARGA VETERINARIA vs MASCOTAS POR ESPECIE
    col_izq, col_der = st.columns(2)
    
    with col_izq:
        AnalisisCargaVeterinaria.mostrar()
        st.markdown("---")
        AnalisisVeterinarioTop.mostrar()
    
    with col_der:
        AnalisisByEspecie.mostrar()
        st.markdown("---")
        AnalisisEspecieTop.mostrar()
    
    st.markdown("---")
    
    # PRÓXIMAS CITAS
    st.subheader("⏳ Próximas citas programadas")
    AnalisisProximasCitas.mostrar()


if __name__ == "__main__":
    main()
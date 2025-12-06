"""
título: módulo de análisis
fecha: 11.11.2025
descripción: implementa estadísticas y reportes de la clínica.
Cubre los requisitos funcionales RF12 (carga de trabajo) y RF16 (próximas citas).
Proporciona dashboards y análisis de datos.
"""

from src.database import session, Cliente, Mascota, Veterinario, Cita
from datetime import date, timedelta
from collections import Counter


def obtener_estadisticas_generales():
    """
    Devuelve estadísticas generales de la clínica
    Return: dict con total_clientes, total_mascotas, total_veterinarios, 
            total_citas, citas_pendientes
    """
    try:
        total_clientes = session.query(Cliente).count()
        total_mascotas = session.query(Mascota).count()
        total_veterinarios = session.query(Veterinario).count()
        total_citas = session.query(Cita).count()
        citas_pendientes = session.query(Cita).filter(Cita.estado == 'Pendiente').count()
        
        return dict(
            total_clientes=total_clientes,
            total_mascotas=total_mascotas,
            total_veterinarios=total_veterinarios,
            total_citas=total_citas,
            citas_pendientes=citas_pendientes
        )
    except Exception as e:
        print(f"Error en obtener_estadisticas_generales: {str(e)}")
        return {
            'total_clientes': 0,
            'total_mascotas': 0,
            'total_veterinarios': 0,
            'total_citas': 0,
            'citas_pendientes': 0
        }


def obtener_total_clientes():
    """Cuenta total de clientes"""
    return obtener_estadisticas_generales()['total_clientes']


def obtener_total_mascotas():
    """Cuenta total de mascotas"""
    return obtener_estadisticas_generales()['total_mascotas']


def obtener_total_citas():
    """Cuenta total de citas"""
    return obtener_estadisticas_generales()['total_citas']


def obtener_citas_pendientes():
    """Cuenta citas con estado 'pendiente'"""
    return obtener_estadisticas_generales()['citas_pendientes']


def obtener_carga_veterinarios():
    """
    Devuelve carga de trabajo de cada veterinario (RF12)
    Return: Lista de dicts con: veterinario_id (int), nombre (str), num_citas (int)
    """
    try:
        veterinarios = session.query(Veterinario).all()
        data = []
        for v in veterinarios:
            num_citas = session.query(Cita).filter(
                Cita.veterinario_id == v.id,
                Cita.estado != "Cancelada"
            ).count()
            data.append(dict(
                veterinario_id=v.id,
                nombre=v.nombre,
                num_citas=num_citas
            ))
        return data
    except Exception as e:
        print(f"Error en obtener_carga_veterinarios: {str(e)}")
        return []


def obtener_veterinario_con_mas_citas():
    """
    Encuentra veterinario con más citas asignadas
    Return: dict con id (int), nombre (str), num_citas (int)
    """
    try:
        lista = obtener_carga_veterinarios()
        if not lista:
            return None
        
        top = max(lista, key=lambda d: d["num_citas"], default=None)
        
        if top and top['num_citas'] > 0:
            return dict(
                id=top['veterinario_id'],
                nombre=top['nombre'],
                num_citas=top['num_citas']
            )
        return None
    except Exception as e:
        print(f"Error en obtener_veterinario_con_mas_citas: {str(e)}")
        return None


def obtener_especie_mas_comun():
    """
    Devuelve la especie de mascota más registrada
    Return: Nombre de la especie (str)
    """
    try:
        especie_stats = obtener_mascotas_por_especie()
        if not especie_stats:
            return None
        return max(especie_stats, key=especie_stats.get)
    except Exception as e:
        print(f"Error en obtener_especie_mas_comun: {str(e)}")
        return None


def obtener_mascotas_por_especie():
    """
    Cuenta mascotas agrupadas por especie
    Return: dict con especie (str): cantidad (int)
    """
    try:
        mascotas = session.query(Mascota).all()
        conteo = Counter([m.especie for m in mascotas if m.especie])
        print(dict(conteo)) # Funciona: {'Perro': 3, 'Pájaro': 1}
        return dict(conteo)
    except Exception as e:
        print(f"Error en obtener_mascotas_por_especie: {str(e)}")
        return {}


def obtener_proximas_citas_hoy():
    """
    Devuelve citas programadas para hoy (RF16)
    Return: Lista de citas de hoy
    """
    try:
        hoy = date.today()
        citas = session.query(Cita).filter(
            Cita.fecha == hoy,
            Cita.estado != "Cancelada"
        ).order_by(Cita.hora).all()
        return citas
    except Exception as e:
        print(f"Error en obtener_proximas_citas_hoy: {str(e)}")
        return []


def obtener_proximas_citas_semana():
    """
    Devuelve citas de la próxima semana (RF16)
    Return: Lista de citas de los próximos 7 días
    """
    try:
        hoy = date.today()
        semana = hoy + timedelta(days=7)
        citas = session.query(Cita).filter(
            Cita.fecha >= hoy,
            Cita.fecha < semana,
            Cita.estado != "Cancelada"
        ).order_by(Cita.fecha, Cita.hora).all()
        return citas
    except Exception as e:
        print(f"Error en obtener_proximas_citas_semana: {str(e)}")
        return []


def obtener_proximas_citas_mes():
    """
    Devuelve citas del próximo mes (RF16)
    Return: Lista de citas de los próximos 30 días
    """
    try:
        hoy = date.today()
        mes = hoy + timedelta(days=30)
        citas = session.query(Cita).filter(
            Cita.fecha >= hoy,
            Cita.fecha < mes,
            Cita.estado != "Cancelada"
        ).order_by(Cita.fecha, Cita.hora).all()
        return citas
    except Exception as e:
        print(f"Error en obtener_proximas_citas_mes: {str(e)}")
        return []

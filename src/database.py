# 10/11 Sqlite3

import sqlite3

# Conectar a la base de datos (la crea si no existe)
conexion = sqlite3.connect('clinica.db')

# Crear un cursor para ejecutar comandos SQL
cursor = conexion.cursor()



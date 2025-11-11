# README PRÁCTICA FINAL CLÍNICA VETERINARIA
Marcos García, Micaela López, Alejandro González
Programación II - UFV - 2025/26
## Outline del proyecto
### Descripción breve
Nuestra plataforma a desarrollar *maneja, desde las páginas de streamlit (front-end), la base de datos de clientes, citas, veterinarios y mascotas de una clínica veterinaria genérica*, con un servidor de python (SQL-back-end). El sistema permitirá tanto consultar como manipular datos. Incluyendo módulos como buscar entidades (clientes, mascotas, veterinarios, citas) a través de distintos criterios, añadir, editar y eliminar registros y visualizar datos.

### Estructura de datos
La base se conforma por cuatro entidades principales:
Clientes
Veterinarios
Mascotas
Citas
Se traducen a las cuatro clases principales de python. Utilizando SQLAlchemy, se pasan los datos a la base.
La tabla de clientes almacena los datos de los clientes
<pre><code>
CLIENTE:
ID_cliente (PK)
Nombre_cliente
DNI_cliente
Tlf_cliente
Correo_electronico_cliente
</code></pre>
La tabla de mascotas almacena los datos de las mascotas
<pre><code>
MASCOTA:
ID_mascota (PK)
Nombre_mascota
Nombre_mascota
Especie_mascota
Raza_mascota
Edad_mascota
Peso_mascota
Sexo_mascota
ID_cliente (FK)
</code></pre>
La tabla de veterinarios almacena los datos de los veterinarios
<pre><code>
VETERINARIO
ID_veterinario (PK)
Nombre_veterinario
DNI_veterinario
Cargo_veterinario
Especialidad_veterinario
Telefono_veterianrio
Correo_electronico_veterinario
</code></pre>
La tabla de citas actúa como tabla expansiva de la relación n:m entre mascota y veterinario.
<pre><code>
CITA:
ID_cita (PK)
ID_mascota (FK)
ID_cliente (FK)
Fecha_cita
Hora_cita
Estado_cita
Diagnostico_cita

</code></pre>


### FUNCIONAMIENTO
Streamlit es el front-end de la aplicación, desde Streamlit el usuario manda peticiones al servidor en Python, el cual procesa la petición (ya sea de consulta o de manipulación de datos) y la valida (ahí va la lógica de validación (formato del query incorrecto, nombres mal escritos…) y, mediante SQLAlchemy, se comunica con la base de datos para obtener o cambiar datos. La base de datos devuelve la petición y esta se transmite a Streamlit.

<pre><code> Streamlit <--> Servidor python <--> BDD </code></pre>

### ESTRUCTURA DEL PROYECTO
<pre><code>
PRACTICA_FINAL/
│
|── pages/ (Módulo front-end, este es el punto de entrada para peticiones y de salida para infomación)
│ ├── 01_clientes.py
│ ├── 02_mascotas.py
│ ├── 03_veterinarios.py
│ ├── 04_citas.py
│ └── 05_analisis.py
│
├── src/ (Módulo de funcionamiento interno, aquí es donde se procesan las peticiones)
│ ├── _init_.py
│ ├── analisis.py
│ ├── citas.py
│ ├── clientes.py
│ ├── database.py
│ ├── mascotas.py
│ ├── utils.py
│ └── veterinarios.py
│
├── tests/ (Módulo de pruebas TDD)
│ ├── _init_.py
│ ├── test_analisis.py
│ ├── test_citas.py
│ ├── test_clientes.py
│ ├── test_database.py
│ ├── test_mascotas.py
│ ├── test_utils.py
│ └── test_veterinarios.py
│
├── venv/ (Entorno virtual)
│
├── .gitignore
├── app.py
├── README.md
└── requirements.txt
</code></pre>

## DESARROLLO DEL PROYECTO
### PRIMERA ENTREGA: ESQUELETO DE LA PRÁCTICA
Para realizar la tarea con entrega el día 11 de noviembre, el equipo se reunió en cuatro ocasiones:
- Primera reunión - Crear la estructura de archivos (6/11/25): El equipo se reune, lee detenidamente el objetivo de la práctica, y se pone de acuerdo para realizar el esqueleto y subirlo a github.
- Segunda  reunión - Investigar el front-end (7/11/25): Se investigó a fondo sobre Streamlit, su uso y se contemplaron distintas formas de utilizarlo en el proyecto.
- Tercera reunión - Investigar el back-end (10/11/25): investigamos el uso de SQLite para entender cómo implementarlo en el proyecto. Además, creamos un entorno virtual para trabajar de forma ordenada y asegurar el correcto funcionamiento del proyecto.
- Cuarta reunión (11/11/25): Definimos las clases y funciones principales según los requisitos del proyecto.
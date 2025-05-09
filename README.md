# 📦 Sistema de Gestión WALDOS

Este proyecto es una aplicación de escritorio desarrollada en Python con Tkinter que permite la gestión de categorías, clientes, empleados, proveedores y unidades. Se conecta a una base de datos MySQL para realizar operaciones CRUD.

---

## 🔧 Requisitos

- Python 3.7 o superior  
- MySQL Server instalado y funcionando  
- Conector MySQL para Python (`mysql-connector-python`)  
- Editor de texto o IDE (recomendado: VS Code)

---

## 🗂️ Pasos para ejecutar el proyecto

### 1. Crear la base de datos

El primer paso es crear la base de datos en tu servidor MySQL. Para ello se proporciona un archivo `.sql` con los comandos necesarios para crear las tablas requeridas para el funcionamiento del sistema.

#### 📥 Ejecutar script .sql desde la terminal de MySQL

1. Abre la terminal o consola de comandos.
2. Ingresa a MySQL con tu usuario y contraseña:
3. Una vez dentro de MySQL, ejecuta el siguiente comando para correr el script (ajusta la ruta según donde esté tu archivo):

```
SOURCE C:/ruta/completa/a/crear_bd_waldos.sql;
```

> 📝 **Nota**: Asegúrate de que el archivo `crear_bd_waldos.sql` contenga la instrucción para crear la base de datos llamada `waldos`, y todas sus tablas: `categorias`, `clientes`, `empleados`, `proveedores`, `unidades`, etc.

---

### 2. Crear entorno virtual en visual studio code

Para mantener las dependencias del proyecto organizadas, es recomendable usar un entorno virtual.

```
python -m venv env23271418
```

---

### 3. Activar entorno virtual

#### Windows:

```bash
env23271418\Scripts\activate
```

#### Linux/MacOS:

```bash
source env23271418/bin/activate
```

---

### 4. Instalar dependencias en caso de no tenerlas

Instala el conector de MySQL para Python:

```bash
pip install mysql-connector-python
```

---

### 5. Ejecutar la aplicación

Una vez configurado todo, puedes ejecutar el archivo principal (en este caso, `PRINCIPAL.py`) que contiene el código del CRUD de WALDOS.

```EN TERMINAL
python Principal.py
```

---

## 🧠 ¿Qué contiene el proyecto?

- Ventana principal con botones para cada módulo: Categorías, Clientes, Empleados, Proveedores y Unidades.
- Interfaces CRUD para cada tabla (crear, leer, actualizar, eliminar).
- Conexión estable a base de datos MySQL.
- Diseño simple pero funcional con `Tkinter` y `ttk`.

---

## 🔐 Conexión a la base de datos

La conexión se realiza con los siguientes parámetros (puedes modificarlos según tu configuración):

```python
self.conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="contraseña",
    database="waldos"
)
```

> ⚠️ **Importante:** Asegúrate de que tu usuario y contraseña sean correctos y que la base de datos `waldos` ya exista.

---

## 📁 Archivos importantes

- `crear_bd_waldos.sql`: Script que contiene la creación de la base de datos y las tablas necesarias.
- `PRINCIPSL.py`: Contiene el código Python con la interfaz y lógica CRUD.

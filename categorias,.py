import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Conexión a la base de datos
conexion = mysql.connector.connect(
    host="localhost",
    user="root",          # ← Cambia esto si tu usuario no es "root"
    password="david1234",          # ← Pon tu contraseña aquí si tienes una
    database="waldos"
)
cursor = conexion.cursor()

# Crear tabla si no existe
cursor.execute("""
CREATE TABLE IF NOT EXISTS categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
)
""")
conexion.commit()

# Funciones CRUD
def guardar():
    if nombre.get():
        sql = "INSERT INTO categorias (nombre) VALUES (%s)"
        cursor.execute(sql, (nombre.get(),))
        conexion.commit()
        mostrar(); limpiar()
    else:
        messagebox.showwarning("Atención", "Debes escribir un nombre.")

def eliminar():
    if id_categoria.get():
        sql = "DELETE FROM categorias WHERE id = %s"
        cursor.execute(sql, (id_categoria.get(),))
        conexion.commit()
        mostrar(); limpiar()

def actualizar():
    if id_categoria.get() and nombre.get():
        sql = "UPDATE categorias SET nombre = %s WHERE id = %s"
        cursor.execute(sql, (nombre.get(), id_categoria.get()))
        conexion.commit()
        mostrar(); limpiar()

def limpiar():
    id_categoria.set("")
    nombre.set("")

def mostrar():
    for i in tabla.get_children(): tabla.delete(i)
    cursor.execute("SELECT id_categoria, nombre FROM categorias")
    for fila in cursor.fetchall():
        tabla.insert("", "end", values=fila)

def seleccionar(e):
    sel = tabla.focus()
    if sel:
        fila = tabla.item(sel)["values"]
        id_categoria.set(fila[0])
        nombre.set(fila[1])

# Interfaz
root = tk.Tk()
root.title("CRUD Categorías")
root.geometry("430x330")

tk.Label(root, text="ID (no editable):").pack()
id_categoria = tk.StringVar()
tk.Entry(root, textvariable=id_categoria, state="readonly", bg="#e6e6e6").pack()

tk.Label(root, text="Nombre:").pack()
nombre = tk.StringVar()
tk.Entry(root, textvariable=nombre, bg="#ccffff").pack()

# Botones
f = tk.Frame(root); f.pack(pady=12)
botones = [
    ("Guardar", guardar, "#b3ffb3"),
    ("Eliminar", eliminar, "#ffb3b3"),
    ("Actualizar", actualizar, "#ffffb3"),
    ("Limpiar", limpiar, "#e6e6e6")
]
for i, (texto, comando, color) in enumerate(botones):
    tk.Button(f, text=texto, command=comando, bg=color, width=10).grid(row=0, column=i, padx=7)

# Tabla
tabla = ttk.Treeview(root, columns=("ID", "Nombre"), show="headings")
tabla.heading("ID", text="ID"); tabla.heading("Nombre", text="Nombre")
tabla.bind("<ButtonRelease-1>", seleccionar)
tabla.pack(fill="both", expand=True, pady=5)

mostrar()
root.mainloop()

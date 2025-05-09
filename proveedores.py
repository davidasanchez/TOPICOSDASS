import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Conexión a la base de datos
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="david1234",
    database="waldos"
)
cursor = conn.cursor()

# Funciones CRUD conectadas a MySQL
def guardar():
    if nombre.get() and direccion.get() and telefono.get() and email.get():
        sql = "INSERT INTO proveedores (nombre, direccion, telefono, email) VALUES (%s, %s, %s, %s)"
        datos = (nombre.get(), direccion.get(), telefono.get(), email.get())
        cursor.execute(sql, datos)
        conn.commit()
        mostrar(); limpiar()
    else:
        messagebox.showwarning("Atención", "Todos los campos son requeridos.")

def eliminar():
    if id_proveedor.get():
        sql = "DELETE FROM proveedores WHERE id_proveedor = %s"
        cursor.execute(sql, (id_proveedor.get(),))
        conn.commit()
        mostrar(); limpiar()

def actualizar():
    if id_proveedor.get() and nombre.get() and direccion.get() and telefono.get() and email.get():
        sql = "UPDATE proveedores SET nombre = %s, direccion = %s, telefono = %s, email = %s WHERE id_proveedor = %s"
        datos = (nombre.get(), direccion.get(), telefono.get(), email.get(), id_proveedor.get())
        cursor.execute(sql, datos)
        conn.commit()
        mostrar(); limpiar()

def limpiar():
    id_proveedor.set("")
    nombre.set("")
    direccion.set("")
    telefono.set("")
    email.set("")

def mostrar():
    for i in tabla.get_children(): tabla.delete(i)
    cursor.execute("SELECT * FROM proveedores")
    for fila in cursor.fetchall():
        tabla.insert("", "end", values=fila)

def seleccionar(e):
    sel = tabla.focus()
    if sel:
        fila = tabla.item(sel)["values"]
        id_proveedor.set(fila[0])
        nombre.set(fila[1])
        direccion.set(fila[2])
        telefono.set(fila[3])
        email.set(fila[4])

# Interfaz
root = tk.Tk()
root.title("CRUD Proveedores (con MySQL)")
root.geometry("600x450")

# Campos de entrada
tk.Label(root, text="ID (no editable):").pack()
id_proveedor = tk.StringVar()
tk.Entry(root, textvariable=id_proveedor, state="readonly", bg="#e6e6e6").pack()

tk.Label(root, text="Nombre:").pack()
nombre = tk.StringVar()
tk.Entry(root, textvariable=nombre, bg="#ccffff").pack()

tk.Label(root, text="Dirección:").pack()
direccion = tk.StringVar()
tk.Entry(root, textvariable=direccion, bg="#ccffff").pack()

tk.Label(root, text="Teléfono:").pack()
telefono = tk.StringVar()
tk.Entry(root, textvariable=telefono, bg="#ccffff").pack()

tk.Label(root, text="Email:").pack()
email = tk.StringVar()
tk.Entry(root, textvariable=email, bg="#ccffff").pack()

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
tabla = ttk.Treeview(root, columns=("ID", "Nombre", "Dirección", "Teléfono", "Email"), show="headings")
for col in ("ID", "Nombre", "Dirección", "Teléfono", "Email"):
    tabla.heading(col, text=col)
tabla.bind("<ButtonRelease-1>", seleccionar)
tabla.pack(fill="both", expand=True, pady=5)

mostrar()
root.mainloop()

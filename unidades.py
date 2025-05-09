import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Conexión a la base de datos MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="david1234",
    database="waldos"
)
cursor = conn.cursor()

# Funciones CRUD
def guardar():
    if nombre.get():
        cursor.execute("INSERT INTO unidades (nombre) VALUES (%s)", (nombre.get(),))
        conn.commit()
        mostrar(); limpiar()
    else:
        messagebox.showwarning("Atención", "Debes escribir un nombre.")

def eliminar():
    if id_unidad.get():
        cursor.execute("DELETE FROM unidades WHERE id = %s", (id_unidad.get(),))
        conn.commit()
        mostrar(); limpiar()

def actualizar():
    if id_unidad.get() and nombre.get():
        cursor.execute("UPDATE unidades SET nombre = %s WHERE id = %s", (nombre.get(), id_unidad.get()))
        conn.commit()
        mostrar(); limpiar()

def limpiar():
    id_unidad.set("")
    nombre.set("")

def mostrar():
    for i in tabla.get_children(): tabla.delete(i)
    cursor.execute("SELECT * FROM unidades")
    for fila in cursor.fetchall():
        tabla.insert("", "end", values=fila)

def seleccionar(e):
    sel = tabla.focus()
    if sel:
        fila = tabla.item(sel)["values"]
        id_unidad.set(fila[0])
        nombre.set(fila[1])

# Interfaz
root = tk.Tk()
root.title("CRUD Unidades (MySQL)")
root.geometry("430x330")

tk.Label(root, text="ID (no editable):").pack()
id_unidad = tk.StringVar()
tk.Entry(root, textvariable=id_unidad, state="readonly", bg="#e6e6e6").pack()

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

import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox

# Conexión a la base de datos
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="david1234",
        database="waldos"
    )

# Lista para guardar registros en memoria (opcional si prefieres obtener directamente desde la base de datos)
clientes = []

# Funciones CRUD
def guardar():
    conexion = conectar()
    cursor = conexion.cursor()
    if nombre.get() and direccion.get() and telefono.get() and email.get():
        cursor.execute(
            "INSERT INTO clientes (nombre, direccion, telefono, email) VALUES (%s, %s, %s, %s)",
            (nombre.get(), direccion.get(), telefono.get(), email.get())
        )
        conexion.commit()
        mostrar()  # Actualiza la tabla
        limpiar()
    else:
        messagebox.showwarning("Atención", "Todos los campos son requeridos.")
    cursor.close()
    conexion.close()

def eliminar():
    conexion = conectar()
    cursor = conexion.cursor()
    if id_cliente.get():
        cursor.execute("DELETE FROM clientes WHERE id_cliente = %s", (id_cliente.get(),))
        conexion.commit()
        mostrar()  # Actualiza la tabla
        limpiar()
    cursor.close()
    conexion.close()

def actualizar():
    conexion = conectar()
    cursor = conexion.cursor()
    if id_cliente.get() and nombre.get() and direccion.get() and telefono.get() and email.get():
        cursor.execute(
            "UPDATE clientes SET nombre = %s, direccion = %s, telefono = %s, email = %s WHERE id_cliente = %s",
            (nombre.get(), direccion.get(), telefono.get(), email.get(), id_cliente.get())
        )
        conexion.commit()
        mostrar()  # Actualiza la tabla
        limpiar()
    cursor.close()
    conexion.close()

def limpiar():
    id_cliente.set("")
    nombre.set("")
    direccion.set("")
    telefono.set("")
    email.set("")

def mostrar():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT id_cliente, nombre, direccion, telefono, email FROM clientes")
    registros = cursor.fetchall()
    for i in tabla.get_children():
        tabla.delete(i)
    for c in registros:
        tabla.insert("", "end", values=(c[0], c[1], c[2], c[3], c[4]))
    cursor.close()
    conexion.close()

def seleccionar(e):
    sel = tabla.focus()
    if sel:
        fila = tabla.item(sel)["values"]
        id_cliente.set(fila[0])
        nombre.set(fila[1])
        direccion.set(fila[2])
        telefono.set(fila[3])
        email.set(fila[4])

# Interfaz
root = tk.Tk()
root.title("CRUD Cliente")
root.geometry("600x450")

# Campos de entrada
tk.Label(root, text="ID (no editable):").pack()
id_cliente = tk.StringVar()
tk.Entry(root, textvariable=id_cliente, state="readonly", bg="#e6e6e6").pack()

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
f = tk.Frame(root)
f.pack(pady=12)
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
tabla.heading("ID", text="ID")
tabla.heading("Nombre", text="Nombre")
tabla.heading("Dirección", text="Dirección")
tabla.heading("Teléfono", text="Teléfono")
tabla.heading("Email", text="Email")
tabla.bind("<ButtonRelease-1>", seleccionar)
tabla.pack(fill="both", expand=True, pady=5)

mostrar()
root.mainloop()

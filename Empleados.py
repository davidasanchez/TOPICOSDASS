import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Función de conexión a MySQL
def conectar():
    return mysql.connector.connect(
        host="localhost",  # Cambia por el nombre de tu host
        user="root",       # Tu usuario de MySQL
        password="david1234",       # Tu contraseña de MySQL
        database="waldos" # Cambia por el nombre de tu base de datos
    )

# Funciones CRUD
def guardar():
    if nombre.get() and cargo.get() and salario.get():
        try:
            salario_val = float(salario.get())
            conexion = conectar()
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO empleados (nombre, cargo, salario) VALUES (%s, %s, %s)", 
                           (nombre.get(), cargo.get(), salario_val))
            conexion.commit()
            conexion.close()
            mostrar()
            limpiar()
        except ValueError:
            messagebox.showwarning("Atención", "El salario debe ser un número.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {e}")
    else:
        messagebox.showwarning("Atención", "Todos los campos son requeridos.")

def eliminar():
    if id_empleado.get():
        try:
            conexion = conectar()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM empleados WHERE id = %s", (id_empleado.get(),))
            conexion.commit()
            conexion.close()
            mostrar()
            limpiar()
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar: {e}")

def actualizar():
    if id_empleado.get() and nombre.get() and cargo.get() and salario.get():
        try:
            salario_val = float(salario.get())
            conexion = conectar()
            cursor = conexion.cursor()
            cursor.execute("UPDATE empleados SET nombre = %s, cargo = %s, salario = %s WHERE id = %s",
                           (nombre.get(), cargo.get(), salario_val, id_empleado.get()))
            conexion.commit()
            conexion.close()
            mostrar()
            limpiar()
        except ValueError:
            messagebox.showwarning("Atención", "El salario debe ser un número.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar: {e}")
    else:
        messagebox.showwarning("Atención", "Todos los campos son requeridos.")

def limpiar():
    id_empleado.set("")
    nombre.set("")
    cargo.set("")
    salario.set("")

def mostrar():
    for i in tabla.get_children(): tabla.delete(i)
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM empleados")
        empleados = cursor.fetchall()
        for e in empleados:
            tabla.insert("", "end", values=(e[0], e[1], e[2], e[3]))
        conexion.close()
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar los datos: {e}")

def seleccionar(e):
    sel = tabla.focus()
    if sel:
        fila = tabla.item(sel)["values"]
        id_empleado.set(fila[0])
        nombre.set(fila[1])
        cargo.set(fila[2])
        salario.set(fila[3])

# Interfaz
root = tk.Tk()
root.title("CRUD Empleados")
root.geometry("500x400")

# Campos de entrada
tk.Label(root, text="ID (no editable):").pack()
id_empleado = tk.StringVar()
tk.Entry(root, textvariable=id_empleado, state="readonly", bg="#e6e6e6").pack()

tk.Label(root, text="Nombre:").pack()
nombre = tk.StringVar()
tk.Entry(root, textvariable=nombre, bg="#ccffff").pack()

tk.Label(root, text="Cargo:").pack()
cargo = tk.StringVar()
tk.Entry(root, textvariable=cargo, bg="#ccffff").pack()

tk.Label(root, text="Salario:").pack()
salario = tk.StringVar()
tk.Entry(root, textvariable=salario, bg="#ccffff").pack()

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
tabla = ttk.Treeview(root, columns=("ID", "Nombre", "Cargo", "Salario"), show="headings")
tabla.heading("ID", text="ID")
tabla.heading("Nombre", text="Nombre")
tabla.heading("Cargo", text="Cargo")
tabla.heading("Salario", text="Salario")
tabla.bind("<ButtonRelease-1>", seleccionar)
tabla.pack(fill="both", expand=True, pady=5)

mostrar()
root.mainloop()

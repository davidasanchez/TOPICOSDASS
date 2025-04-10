import tkinter as tk
from tkinter import ttk, messagebox

# Lista para guardar registros en memoria
empleados = []
contador_id = 1

# Funciones CRUD
def guardar():
    global contador_id
    if nombre.get() and cargo.get() and salario.get():
        try:
            salario_val = float(salario.get())
            empleados.append({"id": contador_id, "nombre": nombre.get(), "cargo": cargo.get(), "salario": salario_val})
            contador_id += 1
            mostrar(); limpiar()
        except ValueError:
            messagebox.showwarning("Atención", "El salario debe ser un número.")
    else:
        messagebox.showwarning("Atención", "Todos los campos son requeridos.")

def eliminar():
    global empleados
    if id_empleado.get():
        empleados = [e for e in empleados if str(e["id"]) != id_empleado.get()]
        mostrar(); limpiar()

def actualizar():
    if id_empleado.get() and nombre.get() and cargo.get() and salario.get():
        try:
            salario_val = float(salario.get())
            for e in empleados:
                if e["id"] == int(id_empleado.get()):
                    e["nombre"] = nombre.get()
                    e["cargo"] = cargo.get()
                    e["salario"] = salario_val
            mostrar(); limpiar()
        except ValueError:
            messagebox.showwarning("Atención", "El salario debe ser un número.")
    else:
        messagebox.showwarning("Atención", "Todos los campos son requeridos.")

def limpiar():
    id_empleado.set("")
    nombre.set("")
    cargo.set("")
    salario.set("")

def mostrar():
    for i in tabla.get_children(): tabla.delete(i)
    for e in empleados:
        tabla.insert("", "end", values=(e["id"], e["nombre"], e["cargo"], e["salario"]))

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

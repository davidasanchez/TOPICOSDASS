import tkinter as tk
from tkinter import ttk, messagebox

# Lista para guardar registros en memoria
proveedores = []
contador_id = 1

# Funciones CRUD
def guardar():
    global contador_id
    if nombre.get() and direccion.get() and telefono.get() and email.get():
        proveedores.append({"id": contador_id, "nombre": nombre.get(), "direccion": direccion.get(), "telefono": telefono.get(), "email": email.get()})
        contador_id += 1
        mostrar(); limpiar()
    else:
        messagebox.showwarning("Atención", "Todos los campos son requeridos.")

def eliminar():
    global proveedores
    if id_proveedor.get():
        proveedores = [p for p in proveedores if str(p["id"]) != id_proveedor.get()]
        mostrar(); limpiar()

def actualizar():
    if id_proveedor.get() and nombre.get() and direccion.get() and telefono.get() and email.get():
        for p in proveedores:
            if p["id"] == int(id_proveedor.get()):
                p["nombre"] = nombre.get()
                p["direccion"] = direccion.get()
                p["telefono"] = telefono.get()
                p["email"] = email.get()
        mostrar(); limpiar()

def limpiar():
    id_proveedor.set("")
    nombre.set("")
    direccion.set("")
    telefono.set("")
    email.set("")

def mostrar():
    for i in tabla.get_children(): tabla.delete(i)
    for p in proveedores:
        tabla.insert("", "end", values=(p["id"], p["nombre"], p["direccion"], p["telefono"], p["email"]))

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
root.title("CRUD Proveedores")
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
tabla.heading("ID", text="ID")
tabla.heading("Nombre", text="Nombre")
tabla.heading("Dirección", text="Dirección")
tabla.heading("Teléfono", text="Teléfono")
tabla.heading("Email", text="Email")
tabla.bind("<ButtonRelease-1>", seleccionar)
tabla.pack(fill="both", expand=True, pady=5)

mostrar()
root.mainloop()

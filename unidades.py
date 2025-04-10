import tkinter as tk
from tkinter import ttk, messagebox

# Lista para guardar registros en memoria
unidades = []
contador_id = 1

# Funciones CRUD
def guardar():
    global contador_id
    if nombre.get():
        unidades.append({"id": contador_id, "nombre": nombre.get()})
        contador_id += 1
        mostrar(); limpiar()
    else:
        messagebox.showwarning("Atención", "Debes escribir un nombre.")

def eliminar():
    global unidades
    if id_unidad.get():
        unidades = [u for u in unidades if str(u["id"]) != id_unidad.get()]
        mostrar(); limpiar()

def actualizar():
    if id_unidad.get() and nombre.get():
        for u in unidades:
            if u["id"] == int(id_unidad.get()):
                u["nombre"] = nombre.get()
        mostrar(); limpiar()

def limpiar():
    id_unidad.set("")
    nombre.set("")

def mostrar():
    for i in tabla.get_children(): tabla.delete(i)
    for u in unidades:
        tabla.insert("", "end", values=(u["id"], u["nombre"]))

def seleccionar(e):
    sel = tabla.focus()
    if sel:
        fila = tabla.item(sel)["values"]
        id_unidad.set(fila[0])
        nombre.set(fila[1])

# Interfaz
root = tk.Tk()
root.title("CRUD Unidades")
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

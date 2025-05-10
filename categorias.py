import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

class CRUDCategorias:
    def __init__(self, root):
        self.root = root
        self.root.title("CRUD Categorías")
        self.root.geometry("500x400")
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.id_categoria = tk.StringVar()
        self.nombre = tk.StringVar()
        
        # Conexión a la base de datos
        self.conexion = None
        self.cursor = None
        self.conectar_db()
        
        # Configurar interfaz
        self.configurar_interfaz()
        self.mostrar()
    
    def conectar_db(self):
        try:
            self.conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="david1234",
                database="waldos"
            )
            self.cursor = self.conexion.cursor()
        except mysql.connector.Error as err:
            messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos:\n{err}")
            self.root.destroy()
    
    def configurar_interfaz(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#f0f0f0', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Campos de entrada
        tk.Label(main_frame, text="ID (no editable):", bg='#f0f0f0').grid(row=0, column=0, sticky="e", pady=5)
        tk.Entry(main_frame, textvariable=self.id_categoria, state="readonly", bg="#e6e6e6").grid(row=0, column=1, pady=5, sticky="ew")
        
        tk.Label(main_frame, text="Nombre:", bg='#f0f0f0').grid(row=1, column=0, sticky="e", pady=5)
        tk.Entry(main_frame, textvariable=self.nombre, bg="#ffffff").grid(row=1, column=1, pady=5, sticky="ew")
        
        # Botones
        btn_frame = tk.Frame(main_frame, bg='#f0f0f0')
        btn_frame.grid(row=2, column=0, columnspan=2, pady=15)
        
        tk.Button(btn_frame, text="Guardar", command=self.guardar, bg="#2ecc71", fg="white", width=10).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Eliminar", command=self.eliminar, bg="#e74c3c", fg="white", width=10).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Actualizar", command=self.actualizar, bg="#3498db", fg="white", width=10).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Limpiar", command=self.limpiar, bg="#f39c12", fg="white", width=10).grid(row=0, column=3, padx=5)
        
        # Tabla
        table_frame = tk.Frame(main_frame, bg='#f0f0f0')
        table_frame.grid(row=3, column=0, columnspan=2, sticky="nsew")
        
        self.tabla = ttk.Treeview(table_frame, columns=("ID", "Nombre"), show="headings")
        self.tabla.heading("ID", text="ID")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.bind("<ButtonRelease-1>", self.seleccionar)
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)
        
        self.tabla.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Configurar expansión
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
    
    def guardar(self):
        if not self.nombre.get():
            messagebox.showwarning("Advertencia", "Debes escribir un nombre")
            return
        
        try:
            sql = "INSERT INTO categorias (nombre) VALUES (%s)"
            self.cursor.execute(sql, (self.nombre.get(),))
            self.conexion.commit()
            self.mostrar()
            self.limpiar()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la categoría:\n{e}")
    
    def eliminar(self):
        if not self.id_categoria.get():
            messagebox.showwarning("Advertencia", "Seleccione una categoría para eliminar")
            return
        
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar esta categoría?"):
            try:
                sql = "DELETE FROM categorias WHERE id_categoria = %s"
                self.cursor.execute(sql, (self.id_categoria.get(),))
                self.conexion.commit()
                self.mostrar()
                self.limpiar()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar la categoría:\n{e}")
    
    def actualizar(self):
        if not self.id_categoria.get() or not self.nombre.get():
            messagebox.showwarning("Advertencia", "Seleccione una categoría y escriba un nombre")
            return
        
        try:
            sql = "UPDATE categorias SET nombre = %s WHERE id_categoria = %s"
            self.cursor.execute(sql, (self.nombre.get(), self.id_categoria.get()))
            self.conexion.commit()
            self.mostrar()
            self.limpiar()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar la categoría:\n{e}")
    
    def limpiar(self):
        self.id_categoria.set("")
        self.nombre.set("")
    
    def mostrar(self):
        try:
            # Limpiar tabla
            for item in self.tabla.get_children():
                self.tabla.delete(item)
            
            # Consultar y mostrar datos
            self.cursor.execute("SELECT id_categoria, nombre FROM categorias")
            for fila in self.cursor.fetchall():
                self.tabla.insert("", "end", values=fila)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las categorías:\n{e}")
    
    def seleccionar(self, event):
        selected = self.tabla.focus()
        if selected:
            values = self.tabla.item(selected, "values")
            self.id_categoria.set(values[0])
            self.nombre.set(values[1])
    
    def __del__(self):
        if self.conexion:
            self.conexion.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = CRUDCategorias(root)
    root.mainloop()
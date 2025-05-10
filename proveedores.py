import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

class CRUDProveedores:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Proveedores")
        self.root.geometry("650x550")
        
        # Variables
        self.id_proveedor = tk.StringVar()
        self.nombre = tk.StringVar()
        self.direccion = tk.StringVar()
        self.telefono = tk.StringVar()
        self.email = tk.StringVar()
        
        # Conexión a DB
        self.conn = self._conectar_db()
        if not self.conn:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            self.root.destroy()
            return
        
        # Interfaz
        self._crear_interfaz()
        self.mostrar_proveedores()
    
    def _conectar_db(self):
        try:
            return mysql.connector.connect(
                host="localhost",
                user="root",
                password="david1234",
                database="waldos"
            )
        except Error as e:
            messagebox.showerror("Error de conexión", f"Error al conectar: {e}")
            return None
    
    def _crear_interfaz(self):
        # Frame principal
        main_frame = tk.Frame(self.root, padx=15, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Formulario
        form_frame = tk.LabelFrame(main_frame, text="Datos del Proveedor", padx=10, pady=10)
        form_frame.pack(fill=tk.X, pady=5)
        
        # Campos
        campos = [
            ("ID:", self.id_proveedor, "readonly"),
            ("Nombre:", self.nombre),
            ("Dirección:", self.direccion),
            ("Teléfono:", self.telefono),
            ("Email:", self.email)
        ]
        
        for i, (texto, var, *estado) in enumerate(campos):
            tk.Label(form_frame, text=texto).grid(row=i, column=0, sticky="e", padx=5, pady=3)
            tk.Entry(form_frame, textvariable=var, state=estado[0] if estado else "normal").grid(row=i, column=1, sticky="ew", padx=5, pady=3)
        
        # Botones
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        botones = [
            ("Guardar", self.guardar_proveedor, "#4CAF50"),
            ("Eliminar", self.eliminar_proveedor, "#F44336"),
            ("Actualizar", self.actualizar_proveedor, "#2196F3"),
            ("Limpiar", self.limpiar_campos, "#FF9800")
        ]
        
        for i, (texto, cmd, color) in enumerate(botones):
            btn = tk.Button(btn_frame, text=texto, command=cmd, 
                          bg=color, fg="white", width=12, padx=5)
            btn.grid(row=0, column=i, padx=5)
            btn_frame.grid_columnconfigure(i, weight=1)
        
        # Tabla
        table_frame = tk.Frame(main_frame)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        self.tabla = ttk.Treeview(table_frame, columns=("ID", "Nombre", "Dirección", "Teléfono", "Email"), 
                                show="headings", height=10)
        
        # Configurar columnas
        columnas = [
            ("ID", 50),
            ("Nombre", 120),
            ("Dirección", 150),
            ("Teléfono", 100),
            ("Email", 150)
        ]
        
        for col, width in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=width, anchor="center")
        
        scroll_y = ttk.Scrollbar(table_frame, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll_y.set)
        
        self.tabla.pack(side="left", fill=tk.BOTH, expand=True)
        scroll_y.pack(side="right", fill=tk.Y)
        
        self.tabla.bind("<ButtonRelease-1>", self.seleccionar_proveedor)
    
    def _ejecutar_consulta(self, sql, params=None):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, params or ())
            self.conn.commit()
            return True
        except Error as e:
            messagebox.showerror("Error", f"Error en la operación:\n{e}")
            return False
        finally:
            cursor.close()
    
    def guardar_proveedor(self):
        if not all([self.nombre.get(), self.direccion.get(), self.telefono.get(), self.email.get()]):
            messagebox.showwarning("Error", "Todos los campos son requeridos")
            return
        
        sql = "INSERT INTO proveedores (nombre, direccion, telefono, email) VALUES (%s, %s, %s, %s)"
        params = (self.nombre.get(), self.direccion.get(), self.telefono.get(), self.email.get())
        
        if self._ejecutar_consulta(sql, params):
            messagebox.showinfo("Éxito", "Proveedor guardado correctamente")
            self.mostrar_proveedores()
            self.limpiar_campos()
    
    def eliminar_proveedor(self):
        if not self.id_proveedor.get():
            messagebox.showwarning("Error", "Seleccione un proveedor")
            return
        
        if messagebox.askyesno("Confirmar", "¿Eliminar este proveedor?"):
            sql = "DELETE FROM proveedores WHERE id_proveedor = %s"
            if self._ejecutar_consulta(sql, (self.id_proveedor.get(),)):
                messagebox.showinfo("Éxito", "Proveedor eliminado correctamente")
                self.mostrar_proveedores()
                self.limpiar_campos()
    
    def actualizar_proveedor(self):
        if not all([self.id_proveedor.get(), self.nombre.get(), self.direccion.get(), self.telefono.get(), self.email.get()]):
            messagebox.showwarning("Error", "Complete todos los campos")
            return
        
        sql = "UPDATE proveedores SET nombre=%s, direccion=%s, telefono=%s, email=%s WHERE id_proveedor=%s"
        params = (self.nombre.get(), self.direccion.get(), self.telefono.get(), self.email.get(), self.id_proveedor.get())
        
        if self._ejecutar_consulta(sql, params):
            messagebox.showinfo("Éxito", "Proveedor actualizado correctamente")
            self.mostrar_proveedores()
            self.limpiar_campos()
    
    def limpiar_campos(self):
        self.id_proveedor.set("")
        self.nombre.set("")
        self.direccion.set("")
        self.telefono.set("")
        self.email.set("")
    
    def mostrar_proveedores(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id_proveedor, nombre, direccion, telefono, email FROM proveedores")
            
            # Limpiar tabla
            for item in self.tabla.get_children():
                self.tabla.delete(item)
            
            # Insertar datos
            for proveedor in cursor.fetchall():
                self.tabla.insert("", tk.END, values=proveedor)
            
            cursor.close()
        except Error as e:
            messagebox.showerror("Error", f"No se pudieron cargar los proveedores:\n{e}")
    
    def seleccionar_proveedor(self, event):
        item = self.tabla.focus()
        if item:
            values = self.tabla.item(item, "values")
            self.id_proveedor.set(values[0])
            self.nombre.set(values[1])
            self.direccion.set(values[2])
            self.telefono.set(values[3])
            self.email.set(values[4])
    
    def __del__(self):
        if hasattr(self, 'conn') and self.conn.is_connected():
            self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = CRUDProveedores(root)
    root.mainloop()
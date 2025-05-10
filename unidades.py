import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

class CRUDUnidades:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Unidades")
        self.root.geometry("500x450")
        
        # Variables
        self.id_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        
        # Conexión a DB
        self.conn = self._conectar_db()
        if not self.conn:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            self.root.destroy()
            return
        
        # Interfaz
        self._crear_interfaz()
        self.mostrar_unidades()
    
    def _conectar_db(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="david1234",
                database="waldos"
            )
            # Verificar si la tabla unidades existe
            cursor = conn.cursor()
            cursor.execute("SHOW TABLES LIKE 'unidades'")
            if not cursor.fetchone():
                # Crear tabla si no existe
                cursor.execute("""
                    CREATE TABLE unidades (
                        id_unidad INT AUTO_INCREMENT PRIMARY KEY,
                        nombre VARCHAR(100) NOT NULL
                    )
                """)
                conn.commit()
            cursor.close()
            return conn
        except Error as e:
            messagebox.showerror("Error de conexión", f"Error al conectar: {e}")
            return None
    
    def _crear_interfaz(self):
        # Frame principal
        main_frame = tk.Frame(self.root, padx=15, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Formulario
        form_frame = tk.LabelFrame(main_frame, text="Datos de la Unidad", padx=10, pady=10)
        form_frame.pack(fill=tk.X, pady=5)
        
        # Campos
        tk.Label(form_frame, text="ID:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        tk.Entry(form_frame, textvariable=self.id_var, state="readonly").grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        
        tk.Label(form_frame, text="Nombre:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        tk.Entry(form_frame, textvariable=self.nombre_var).grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        
        # Botones
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        botones = [
            ("Guardar", self.guardar_unidad, "#4CAF50"),
            ("Eliminar", self.eliminar_unidad, "#F44336"),
            ("Actualizar", self.actualizar_unidad, "#2196F3"),
            ("Limpiar", self.limpiar_campos, "#FF9800")
        ]
        
        for i, (texto, cmd, color) in enumerate(botones):
            btn = tk.Button(btn_frame, text=texto, command=cmd, 
                          bg=color, fg="white", width=12)
            btn.grid(row=0, column=i, padx=5)
            btn_frame.grid_columnconfigure(i, weight=1)
        
        # Tabla
        table_frame = tk.Frame(main_frame)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        self.tabla = ttk.Treeview(table_frame, columns=("ID", "Nombre"), 
                                show="headings", height=10)
        
        # Configurar columnas
        self.tabla.heading("ID", text="ID")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.column("ID", width=80, anchor="center")
        self.tabla.column("Nombre", width=200, anchor="w")
        
        scroll_y = ttk.Scrollbar(table_frame, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll_y.set)
        
        self.tabla.pack(side="left", fill=tk.BOTH, expand=True)
        scroll_y.pack(side="right", fill=tk.Y)
        
        self.tabla.bind("<ButtonRelease-1>", self.seleccionar_unidad)
    
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
    
    def guardar_unidad(self):
        if not self.nombre_var.get():
            messagebox.showwarning("Error", "Debe ingresar un nombre")
            return
        
        sql = "INSERT INTO unidades (nombre) VALUES (%s)"
        if self._ejecutar_consulta(sql, (self.nombre_var.get(),)):
            messagebox.showinfo("Éxito", "Unidad guardada correctamente")
            self.mostrar_unidades()
            self.limpiar_campos()
    
    def eliminar_unidad(self):
        if not self.id_var.get():
            messagebox.showwarning("Error", "Seleccione una unidad para eliminar")
            return
        
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar esta unidad?"):
            sql = "DELETE FROM unidades WHERE id_unidad = %s"
            if self._ejecutar_consulta(sql, (self.id_var.get(),)):
                messagebox.showinfo("Éxito", "Unidad eliminada correctamente")
                self.mostrar_unidades()
                self.limpiar_campos()
    
    def actualizar_unidad(self):
        if not all([self.id_var.get(), self.nombre_var.get()]):
            messagebox.showwarning("Error", "Complete todos los campos")
            return
        
        sql = "UPDATE unidades SET nombre = %s WHERE id_unidad = %s"
        if self._ejecutar_consulta(sql, (self.nombre_var.get(), self.id_var.get())):
            messagebox.showinfo("Éxito", "Unidad actualizada correctamente")
            self.mostrar_unidades()
            self.limpiar_campos()
    
    def limpiar_campos(self):
        self.id_var.set("")
        self.nombre_var.set("")
    
    def mostrar_unidades(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id_unidad, nombre FROM unidades")
            
            # Limpiar tabla
            for item in self.tabla.get_children():
                self.tabla.delete(item)
            
            # Insertar datos
            for unidad in cursor.fetchall():
                self.tabla.insert("", tk.END, values=unidad)
            
            cursor.close()
        except Error as e:
            messagebox.showerror("Error", f"No se pudieron cargar las unidades:\n{e}")
    
    def seleccionar_unidad(self, event):
        item = self.tabla.focus()
        if item:
            values = self.tabla.item(item, "values")
            self.id_var.set(values[0])
            self.nombre_var.set(values[1])
    
    def __del__(self):
        if hasattr(self, 'conn') and self.conn.is_connected():
            self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = CRUDUnidades(root)
    root.mainloop()
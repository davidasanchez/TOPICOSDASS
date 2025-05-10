import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

class CRUDEmpleados:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Empleados")
        self.root.geometry("600x500")
        
        # Variables de control
        self.id_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.cargo_var = tk.StringVar()
        self.salario_var = tk.StringVar()
        
        # Configurar interfaz
        self._crear_interfaz()
        
        # Conectar y cargar datos iniciales
        self.conn = self._conectar_db()
        if self.conn:
            self.mostrar_empleados()
        else:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            self.root.destroy()
    
    def _conectar_db(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="david1234",
                database="waldos"
            )
            return conn
        except Error as e:
            messagebox.showerror("Error de conexión", f"Error al conectar a MySQL: {e}")
            return None
    
    def _crear_interfaz(self):
        # Frame principal
        main_frame = tk.Frame(self.root, padx=15, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Formulario
        form_frame = tk.LabelFrame(main_frame, text="Datos del Empleado", padx=10, pady=10)
        form_frame.pack(fill=tk.X, pady=5)
        
        # Campos del formulario
        campos = [
            ("ID:", self.id_var, "readonly"),
            ("Nombre:", self.nombre_var),
            ("Cargo:", self.cargo_var),
            ("Salario:", self.salario_var)
        ]
        
        for i, (texto, var, *estado) in enumerate(campos):
            tk.Label(form_frame, text=texto).grid(row=i, column=0, sticky="e", padx=5, pady=3)
            tk.Entry(form_frame, textvariable=var, state=estado[0] if estado else "normal", 
                    width=30).grid(row=i, column=1, sticky="ew", padx=5, pady=3)
        
        # Botones
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        botones = [
            ("Guardar", self.guardar_empleado, "#4CAF50"),
            ("Eliminar", self.eliminar_empleado, "#F44336"),
            ("Actualizar", self.actualizar_empleado, "#2196F3"),
            ("Limpiar", self.limpiar_campos, "#FF9800")
        ]
        
        for i, (texto, comando, color) in enumerate(botones):
            btn = tk.Button(btn_frame, text=texto, command=comando, 
                          bg=color, fg="white", width=12, padx=5)
            btn.grid(row=0, column=i, padx=5)
            btn_frame.grid_columnconfigure(i, weight=1)
        
        # Tabla de empleados
        table_frame = tk.Frame(main_frame)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        self.tabla = ttk.Treeview(table_frame, columns=("ID", "Nombre", "Cargo", "Salario"), 
                                show="headings", height=10)
        
        # Configurar columnas
        columnas = [
            ("ID", 50),
            ("Nombre", 150),
            ("Cargo", 120),
            ("Salario", 100)
        ]
        
        for col, width in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=width, anchor="center")
        
        scroll_y = ttk.Scrollbar(table_frame, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll_y.set)
        
        self.tabla.pack(side="left", fill=tk.BOTH, expand=True)
        scroll_y.pack(side="right", fill=tk.Y)
        
        self.tabla.bind("<ButtonRelease-1>", self.seleccionar_empleado)
    
    def _ejecutar_consulta(self, query, params=None):
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params or ())
            self.conn.commit()
            return True
        except Error as e:
            messagebox.showerror("Error en la consulta", f"Error al ejecutar la consulta:\n{e}")
            return False
        finally:
            if 'cursor' in locals():
                cursor.close()
    
    def guardar_empleado(self):
        if not all([self.nombre_var.get(), self.cargo_var.get(), self.salario_var.get()]):
            messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios")
            return
        
        try:
            salario = float(self.salario_var.get())
            query = "INSERT INTO empleados (nombre, cargo, salario) VALUES (%s, %s, %s)"
            if self._ejecutar_consulta(query, (self.nombre_var.get(), self.cargo_var.get(), salario)):
                messagebox.showinfo("Éxito", "Empleado guardado correctamente")
                self.mostrar_empleados()
                self.limpiar_campos()
        except ValueError:
            messagebox.showerror("Error", "El salario debe ser un número válido")
    
    def eliminar_empleado(self):
        if not self.id_var.get():
            messagebox.showwarning("Error", "Seleccione un empleado para eliminar")
            return
        
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este empleado?"):
            query = "DELETE FROM empleados WHERE id_empleado = %s"  # Cambiado a id_empleado
            if self._ejecutar_consulta(query, (self.id_var.get(),)):
                messagebox.showinfo("Éxito", "Empleado eliminado correctamente")
                self.mostrar_empleados()
                self.limpiar_campos()
    
    def actualizar_empleado(self):
        if not all([self.id_var.get(), self.nombre_var.get(), self.cargo_var.get(), self.salario_var.get()]):
            messagebox.showwarning("Error", "Complete todos los campos")
            return
        
        try:
            salario = float(self.salario_var.get())
            query = "UPDATE empleados SET nombre=%s, cargo=%s, salario=%s WHERE id_empleado=%s"  # Cambiado a id_empleado
            if self._ejecutar_consulta(query, (self.nombre_var.get(), self.cargo_var.get(), salario, self.id_var.get())):
                messagebox.showinfo("Éxito", "Empleado actualizado correctamente")
                self.mostrar_empleados()
                self.limpiar_campos()
        except ValueError:
            messagebox.showerror("Error", "El salario debe ser un número válido")
    
    def limpiar_campos(self):
        self.id_var.set("")
        self.nombre_var.set("")
        self.cargo_var.set("")
        self.salario_var.set("")
    
    def mostrar_empleados(self):
        try:
            cursor = self.conn.cursor()
            # Cambiado a id_empleado
            cursor.execute("SELECT id_empleado, nombre, cargo, salario FROM empleados")
            
            # Limpiar tabla
            for item in self.tabla.get_children():
                self.tabla.delete(item)
            
            # Insertar datos
            for empleado in cursor.fetchall():
                self.tabla.insert("", tk.END, values=empleado)
            
            cursor.close()
        except Error as e:
            messagebox.showerror("Error", f"No se pudieron cargar los empleados:\n{e}")
    
    def seleccionar_empleado(self, event):
        item = self.tabla.focus()
        if item:
            values = self.tabla.item(item, "values")
            self.id_var.set(values[0])  # ID (id_empleado)
            self.nombre_var.set(values[1])
            self.cargo_var.set(values[2])
            self.salario_var.set(values[3])
    
    def __del__(self):
        if hasattr(self, 'conn') and self.conn.is_connected():
            self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = CRUDEmpleados(root)
    root.mainloop()
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

class WaldosCRUD:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Waldos")
        self.root.geometry("800x600")
        
        # Conexión a la base de datos
        try:
            self.conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="david1234",
                database="waldos"
            )
            self.cursor = self.conexion.cursor()
        except mysql.connector.Error as e:
            messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos: {str(e)}")
            root.destroy()
            return
            
        # Inicializar variables para todas las tablas
        self.inicializar_variables()
        
        # Pantalla de inicio
        self.mostrar_pantalla_inicio()
    
    def inicializar_variables(self):
        # Categorías
        self.id_categoria = tk.StringVar()
        self.nombre_categoria = tk.StringVar()
        
        # Clientes
        self.id_cliente = tk.StringVar()
        self.nombre_cliente = tk.StringVar()
        self.direccion_cliente = tk.StringVar()
        self.telefono_cliente = tk.StringVar()
        self.email_cliente = tk.StringVar()
        
        # Empleados
        self.id_empleado = tk.StringVar()
        self.nombre_empleado = tk.StringVar()
        self.cargo_empleado = tk.StringVar()
        self.salario_empleado = tk.StringVar()
        
        # Proveedores
        self.id_proveedor = tk.StringVar()
        self.nombre_proveedor = tk.StringVar()
        self.direccion_proveedor = tk.StringVar()
        self.telefono_proveedor = tk.StringVar()
        self.email_proveedor = tk.StringVar()
        
        # Unidades
        self.id_unidad = tk.StringVar()
        self.nombre_unidad = tk.StringVar()
    
    def mostrar_pantalla_inicio(self):
        self.limpiar_pantalla()
        
        # Logo o título
        tk.Label(self.root, text="WALDOS", font=("Arial", 36, "bold"), fg="#2c3e50").pack(pady=50)
        
        # Subtítulo
        tk.Label(self.root, text="Sistema de Gestión Integral", font=("Arial", 14)).pack(pady=10)
        
        # Frame para botones de tablas
        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=30)
        
        # Botones para cada tabla
        tablas = [
            ("Categorías", self.mostrar_categorias),
            ("Clientes", self.mostrar_clientes),
            ("Empleados", self.mostrar_empleados),
            ("Proveedores", self.mostrar_proveedores),
            ("Unidades", self.mostrar_unidades)
        ]
        
        for i, (texto, comando) in enumerate(tablas):
            tk.Button(
                frame_botones, 
                text=texto, 
                command=comando,
                width=15,
                height=2,
                bg="#3498db",
                fg="white",
                font=("Arial", 12)
            ).grid(row=i//3, column=i%3, padx=10, pady=10)
    
    def limpiar_pantalla(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def crear_botones_crud(self, frame):
        botones = [
            ("Guardar", self.guardar, "#2ecc71"),
            ("Eliminar", self.eliminar, "#e74c3c"),
            ("Actualizar", self.actualizar, "#f39c12"),
            ("Limpiar", self.limpiar_campos, "#95a5a6"),
            ("Regresar", self.mostrar_pantalla_inicio, "#34495e")
        ]
        
        for i, (texto, comando, color) in enumerate(botones):
            tk.Button(
                frame, 
                text=texto, 
                command=comando,
                bg=color,
                fg="white",
                width=10
            ).grid(row=0, column=i, padx=5, pady=5)
    
    # ------------------------- Categorías -------------------------
    def mostrar_categorias(self):
        self.limpiar_pantalla()
        self.tabla_actual = "categorias"
        
        tk.Label(self.root, text="Gestión de Categorías", font=("Arial", 18, "bold")).pack(pady=10)
        
        # Frame para controles
        frame_controles = tk.Frame(self.root)
        frame_controles.pack(pady=10)
        
        # Campos
        tk.Label(frame_controles, text="ID:").grid(row=0, column=0, sticky="e")
        entry_id = tk.Entry(frame_controles, textvariable=self.id_categoria, state="readonly", width=30)
        entry_id.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(frame_controles, text="Nombre:").grid(row=1, column=0, sticky="e")
        entry_nombre = tk.Entry(frame_controles, textvariable=self.nombre_categoria, width=30)
        entry_nombre.grid(row=1, column=1, padx=5, pady=5)
        
        # Frame para botones CRUD
        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=10)
        self.crear_botones_crud(frame_botones)
        
        # Tabla
        self.tabla = ttk.Treeview(self.root, columns=("ID", "Nombre"), show="headings")
        self.tabla.heading("ID", text="ID")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.bind("<ButtonRelease-1>", self.seleccionar_registro)
        
        scroll = ttk.Scrollbar(self.root, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll.set)
        
        self.tabla.pack(fill="both", expand=True, padx=10, pady=10)
        scroll.pack(side="right", fill="y")
        
        self.mostrar_registros()
    
    # ------------------------- Clientes -------------------------
    def mostrar_clientes(self):
        self.limpiar_pantalla()
        self.tabla_actual = "clientes"
        
        tk.Label(self.root, text="Gestión de Clientes", font=("Arial", 18, "bold")).pack(pady=10)
        
        # Frame para controles
        frame_controles = tk.Frame(self.root)
        frame_controles.pack(pady=10)
        
        # Definir campos y variables
        campos = [
            ("ID:", self.id_cliente, True),
            ("Nombre:", self.nombre_cliente, False),
            ("Dirección:", self.direccion_cliente, False),
            ("Teléfono:", self.telefono_cliente, False),
            ("Email:", self.email_cliente, False)
        ]
        
        # Crear entradas para cada campo
        for i, (texto, var, readonly) in enumerate(campos):
            tk.Label(frame_controles, text=texto).grid(row=i, column=0, sticky="e")
            entry = tk.Entry(frame_controles, textvariable=var, width=30)
            if readonly:
                entry.config(state="readonly")
            entry.grid(row=i, column=1, padx=5, pady=5)
        
        # Frame para botones CRUD
        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=10)
        self.crear_botones_crud(frame_botones)
        
        # Tabla
        self.tabla = ttk.Treeview(self.root, columns=("ID", "Nombre", "Dirección", "Teléfono", "Email"), show="headings")
        columnas = ["ID", "Nombre", "Dirección", "Teléfono", "Email"]
        for col in columnas:
            self.tabla.heading(col, text=col)
        
        self.tabla.bind("<ButtonRelease-1>", self.seleccionar_registro)
        
        scroll = ttk.Scrollbar(self.root, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll.set)
        
        self.tabla.pack(fill="both", expand=True, padx=10, pady=10)
        scroll.pack(side="right", fill="y")
        
        self.mostrar_registros()
    
    # ------------------------- Empleados -------------------------
    def mostrar_empleados(self):
        self.limpiar_pantalla()
        self.tabla_actual = "empleados"
        
        tk.Label(self.root, text="Gestión de Empleados", font=("Arial", 18, "bold")).pack(pady=10)
        
        # Frame para controles
        frame_controles = tk.Frame(self.root)
        frame_controles.pack(pady=10)
        
        # Definir campos y variables
        campos = [
            ("ID:", self.id_empleado, True),
            ("Nombre:", self.nombre_empleado, False),
            ("Cargo:", self.cargo_empleado, False),
            ("Salario:", self.salario_empleado, False)
        ]
        
        # Crear entradas para cada campo
        for i, (texto, var, readonly) in enumerate(campos):
            tk.Label(frame_controles, text=texto).grid(row=i, column=0, sticky="e")
            entry = tk.Entry(frame_controles, textvariable=var, width=30)
            if readonly:
                entry.config(state="readonly")
            entry.grid(row=i, column=1, padx=5, pady=5)
        
        # Frame para botones CRUD
        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=10)
        self.crear_botones_crud(frame_botones)
        
        # Tabla
        self.tabla = ttk.Treeview(self.root, columns=("ID", "Nombre", "Cargo", "Salario"), show="headings")
        columnas = ["ID", "Nombre", "Cargo", "Salario"]
        for col in columnas:
            self.tabla.heading(col, text=col)
        
        self.tabla.bind("<ButtonRelease-1>", self.seleccionar_registro)
        
        scroll = ttk.Scrollbar(self.root, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll.set)
        
        self.tabla.pack(fill="both", expand=True, padx=10, pady=10)
        scroll.pack(side="right", fill="y")
        
        self.mostrar_registros()
    
    # ------------------------- Proveedores -------------------------
    def mostrar_proveedores(self):
        self.limpiar_pantalla()
        self.tabla_actual = "proveedores"
        
        tk.Label(self.root, text="Gestión de Proveedores", font=("Arial", 18, "bold")).pack(pady=10)
        
        # Frame para controles
        frame_controles = tk.Frame(self.root)
        frame_controles.pack(pady=10)
        
        # Definir campos y variables
        campos = [
            ("ID:", self.id_proveedor, True),
            ("Nombre:", self.nombre_proveedor, False),
            ("Dirección:", self.direccion_proveedor, False),
            ("Teléfono:", self.telefono_proveedor, False),
            ("Email:", self.email_proveedor, False)
        ]
        
        # Crear entradas para cada campo
        for i, (texto, var, readonly) in enumerate(campos):
            tk.Label(frame_controles, text=texto).grid(row=i, column=0, sticky="e")
            entry = tk.Entry(frame_controles, textvariable=var, width=30)
            if readonly:
                entry.config(state="readonly")
            entry.grid(row=i, column=1, padx=5, pady=5)
        
        # Frame para botones CRUD
        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=10)
        self.crear_botones_crud(frame_botones)
        
        # Tabla
        self.tabla = ttk.Treeview(self.root, columns=("ID", "Nombre", "Dirección", "Teléfono", "Email"), show="headings")
        columnas = ["ID", "Nombre", "Dirección", "Teléfono", "Email"]
        for col in columnas:
            self.tabla.heading(col, text=col)
        
        self.tabla.bind("<ButtonRelease-1>", self.seleccionar_registro)
        
        scroll = ttk.Scrollbar(self.root, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll.set)
        
        self.tabla.pack(fill="both", expand=True, padx=10, pady=10)
        scroll.pack(side="right", fill="y")
        
        self.mostrar_registros()
    
    # ------------------------- Unidades -------------------------
    def mostrar_unidades(self):
        self.limpiar_pantalla()
        self.tabla_actual = "unidades"
        
        tk.Label(self.root, text="Gestión de Unidades", font=("Arial", 18, "bold")).pack(pady=10)
        
        # Frame para controles
        frame_controles = tk.Frame(self.root)
        frame_controles.pack(pady=10)
        
        # Campos
        tk.Label(frame_controles, text="ID:").grid(row=0, column=0, sticky="e")
        entry_id = tk.Entry(frame_controles, textvariable=self.id_unidad, state="readonly", width=30)
        entry_id.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(frame_controles, text="Nombre:").grid(row=1, column=0, sticky="e")
        entry_nombre = tk.Entry(frame_controles, textvariable=self.nombre_unidad, width=30)
        entry_nombre.grid(row=1, column=1, padx=5, pady=5)
        
        # Frame para botones CRUD
        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=10)
        self.crear_botones_crud(frame_botones)
        
        # Tabla
        self.tabla = ttk.Treeview(self.root, columns=("ID", "Nombre"), show="headings")
        self.tabla.heading("ID", text="ID")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.bind("<ButtonRelease-1>", self.seleccionar_registro)
        
        scroll = ttk.Scrollbar(self.root, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll.set)
        
        self.tabla.pack(fill="both", expand=True, padx=10, pady=10)
        scroll.pack(side="right", fill="y")
        
        self.mostrar_registros()
    
    # ------------------------- Funciones CRUD genéricas -------------------------
    def guardar(self):
        try:
            if self.tabla_actual == "categorias":
                if not self.nombre_categoria.get():
                    messagebox.showwarning("Advertencia", "El nombre es requerido")
                    return
                
                query = "INSERT INTO categorias (nombre) VALUES (%s)"
                valores = (self.nombre_categoria.get(),)
            
            elif self.tabla_actual == "clientes":
                if not all([self.nombre_cliente.get(), self.direccion_cliente.get(), 
                           self.telefono_cliente.get(), self.email_cliente.get()]):
                    messagebox.showwarning("Advertencia", "Todos los campos son requeridos")
                    return
                
                query = """INSERT INTO clientes (nombre, direccion, telefono, email) 
                           VALUES (%s, %s, %s, %s)"""
                valores = (self.nombre_cliente.get(), self.direccion_cliente.get(),
                          self.telefono_cliente.get(), self.email_cliente.get())
            
            elif self.tabla_actual == "empleados":
                if not all([self.nombre_empleado.get(), self.cargo_empleado.get(), 
                           self.salario_empleado.get()]):
                    messagebox.showwarning("Advertencia", "Todos los campos son requeridos")
                    return
                
                try:
                    salario = float(self.salario_empleado.get())
                except ValueError:
                    messagebox.showwarning("Advertencia", "El salario debe ser un número")
                    return
                
                query = """INSERT INTO empleados (nombre, cargo, salario) 
                           VALUES (%s, %s, %s)"""
                valores = (self.nombre_empleado.get(), self.cargo_empleado.get(), salario)
            
            elif self.tabla_actual == "proveedores":
                if not all([self.nombre_proveedor.get(), self.direccion_proveedor.get(), 
                           self.telefono_proveedor.get(), self.email_proveedor.get()]):
                    messagebox.showwarning("Advertencia", "Todos los campos son requeridos")
                    return
                
                query = """INSERT INTO proveedores (nombre, direccion, telefono, email) 
                           VALUES (%s, %s, %s, %s)"""
                valores = (self.nombre_proveedor.get(), self.direccion_proveedor.get(),
                          self.telefono_proveedor.get(), self.email_proveedor.get())
            
            elif self.tabla_actual == "unidades":
                if not self.nombre_unidad.get():
                    messagebox.showwarning("Advertencia", "El nombre es requerido")
                    return
                
                query = "INSERT INTO unidades (nombre) VALUES (%s)"
                valores = (self.nombre_unidad.get(),)
            
            self.cursor.execute(query, valores)
            self.conexion.commit()
            self.mostrar_registros()
            self.limpiar_campos()
            messagebox.showinfo("Éxito", "Registro guardado correctamente")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {str(e)}")
    
    def eliminar(self):
        try:
            id_var = None
            id_campo = ""
            
            if self.tabla_actual == "categorias":
                id_var = self.id_categoria
                id_campo = "id_categoria"
            elif self.tabla_actual == "clientes":
                id_var = self.id_cliente
                id_campo = "id_cliente"
            elif self.tabla_actual == "empleados":
                id_var = self.id_empleado
                id_campo = "id_empleado"
            elif self.tabla_actual == "proveedores":
                id_var = self.id_proveedor
                id_campo = "id_proveedor"
            elif self.tabla_actual == "unidades":
                id_var = self.id_unidad
                id_campo = "id_unidad"
            
            if not id_var.get():
                messagebox.showwarning("Advertencia", "Seleccione un registro para eliminar")
                return
            
            confirmar = messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este registro?")
            if not confirmar:
                return
            
            query = f"DELETE FROM {self.tabla_actual} WHERE {id_campo} = %s"
            self.cursor.execute(query, (id_var.get(),))
            self.conexion.commit()
            self.mostrar_registros()
            self.limpiar_campos()
            messagebox.showinfo("Éxito", "Registro eliminado correctamente")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar: {str(e)}")
    
    def actualizar(self):
        try:
            if self.tabla_actual == "categorias":
                if not all([self.id_categoria.get(), self.nombre_categoria.get()]):
                    messagebox.showwarning("Advertencia", "Seleccione un registro y complete el nombre")
                    return
                
                query = "UPDATE categorias SET nombre = %s WHERE id_categoria = %s"
                valores = (self.nombre_categoria.get(), self.id_categoria.get())
            
            elif self.tabla_actual == "clientes":
                if not all([self.id_cliente.get(), self.nombre_cliente.get(), 
                           self.direccion_cliente.get(), self.telefono_cliente.get(), 
                           self.email_cliente.get()]):
                    messagebox.showwarning("Advertencia", "Seleccione un registro y complete todos los campos")
                    return
                
                query = """UPDATE clientes SET nombre = %s, direccion = %s, 
                           telefono = %s, email = %s WHERE id_cliente = %s"""
                valores = (self.nombre_cliente.get(), self.direccion_cliente.get(),
                          self.telefono_cliente.get(), self.email_cliente.get(),
                          self.id_cliente.get())
            
            elif self.tabla_actual == "empleados":
                if not all([self.id_empleado.get(), self.nombre_empleado.get(), 
                           self.cargo_empleado.get(), self.salario_empleado.get()]):
                    messagebox.showwarning("Advertencia", "Seleccione un registro y complete todos los campos")
                    return
                
                try:
                    salario = float(self.salario_empleado.get())
                except ValueError:
                    messagebox.showwarning("Advertencia", "El salario debe ser un número")
                    return
                
                query = """UPDATE empleados SET nombre = %s, cargo = %s, 
                           salario = %s WHERE id_empleado = %s"""
                valores = (self.nombre_empleado.get(), self.cargo_empleado.get(),
                          salario, self.id_empleado.get())
            
            elif self.tabla_actual == "proveedores":
                if not all([self.id_proveedor.get(), self.nombre_proveedor.get(), 
                           self.direccion_proveedor.get(), self.telefono_proveedor.get(), 
                           self.email_proveedor.get()]):
                    messagebox.showwarning("Advertencia", "Seleccione un registro y complete todos los campos")
                    return
                
                query = """UPDATE proveedores SET nombre = %s, direccion = %s, 
                           telefono = %s, email = %s WHERE id_proveedor = %s"""
                valores = (self.nombre_proveedor.get(), self.direccion_proveedor.get(),
                          self.telefono_proveedor.get(), self.email_proveedor.get(),
                          self.id_proveedor.get())
            
            elif self.tabla_actual == "unidades":
                if not all([self.id_unidad.get(), self.nombre_unidad.get()]):
                    messagebox.showwarning("Advertencia", "Seleccione un registro y complete el nombre")
                    return
                
                query = "UPDATE unidades SET nombre = %s WHERE id_unidad = %s"
                valores = (self.nombre_unidad.get(), self.id_unidad.get())
            
            self.cursor.execute(query, valores)
            self.conexion.commit()
            self.mostrar_registros()
            self.limpiar_campos()
            messagebox.showinfo("Éxito", "Registro actualizado correctamente")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar: {str(e)}")
    
    def limpiar_campos(self):
        if self.tabla_actual == "categorias":
            self.id_categoria.set("")
            self.nombre_categoria.set("")
        elif self.tabla_actual == "clientes":
            self.id_cliente.set("")
            self.nombre_cliente.set("")
            self.direccion_cliente.set("")
            self.telefono_cliente.set("")
            self.email_cliente.set("")
        elif self.tabla_actual == "empleados":
            self.id_empleado.set("")
            self.nombre_empleado.set("")
            self.cargo_empleado.set("")
            self.salario_empleado.set("")
        elif self.tabla_actual == "proveedores":
            self.id_proveedor.set("")
            self.nombre_proveedor.set("")
            self.direccion_proveedor.set("")
            self.telefono_proveedor.set("")
            self.email_proveedor.set("")
        elif self.tabla_actual == "unidades":
            self.id_unidad.set("")
            self.nombre_unidad.set("")
    
    def mostrar_registros(self):
        try:
            # Limpiar tabla
            for item in self.tabla.get_children():
                self.tabla.delete(item)
            
            # Definir consulta y columnas según la tabla actual
            if self.tabla_actual == "categorias":
                query = "SELECT id_categoria, nombre FROM categorias"
            elif self.tabla_actual == "clientes":
                query = "SELECT id_cliente, nombre, direccion, telefono, email FROM clientes"
            elif self.tabla_actual == "empleados":
                query = "SELECT id_empleado, nombre, cargo, salario FROM empleados"
            elif self.tabla_actual == "proveedores":
                query = "SELECT id_proveedor, nombre, direccion, telefono, email FROM proveedores"
            elif self.tabla_actual == "unidades":
                query = "SELECT id_unidad, nombre FROM unidades"
            
            self.cursor.execute(query)
            registros = self.cursor.fetchall()
            
            # Insertar registros en la tabla
            for registro in registros:
                self.tabla.insert("", "end", values=registro)
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar registros: {str(e)}")
    
    def seleccionar_registro(self, event):
        try:
            item = self.tabla.focus()
            if item:
                valores = self.tabla.item(item, "values")
                
                if self.tabla_actual == "categorias":
                    self.id_categoria.set(valores[0])
                    self.nombre_categoria.set(valores[1])
                elif self.tabla_actual == "clientes":
                    self.id_cliente.set(valores[0])
                    self.nombre_cliente.set(valores[1])
                    self.direccion_cliente.set(valores[2])
                    self.telefono_cliente.set(valores[3])
                    self.email_cliente.set(valores[4])
                elif self.tabla_actual == "empleados":
                    self.id_empleado.set(valores[0])
                    self.nombre_empleado.set(valores[1])
                    self.cargo_empleado.set(valores[2])
                    self.salario_empleado.set(valores[3])
                elif self.tabla_actual == "proveedores":
                    self.id_proveedor.set(valores[0])
                    self.nombre_proveedor.set(valores[1])
                    self.direccion_proveedor.set(valores[2])
                    self.telefono_proveedor.set(valores[3])
                    self.email_proveedor.set(valores[4])
                elif self.tabla_actual == "unidades":
                    self.id_unidad.set(valores[0])
                    self.nombre_unidad.set(valores[1])
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al seleccionar registro: {str(e)}")

# Iniciar aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = WaldosCRUD(root)
    root.mainloop()
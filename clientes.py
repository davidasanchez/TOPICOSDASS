import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox

class CRUDClientes:
    def __init__(self, root):
        self.root = root
        self.root.title("CRUD Clientes")
        self.root.geometry("700x550")
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.id_cliente = tk.StringVar()
        self.nombre = tk.StringVar()
        self.direccion = tk.StringVar()
        self.telefono = tk.StringVar()
        self.email = tk.StringVar()
        
        # Configurar interfaz
        self.configurar_interfaz()
        self.mostrar()
    
    def conectar_db(self):
        try:
            return mysql.connector.connect(
                host="localhost",
                user="root",
                password="david1234",
                database="waldos"
            )
        except mysql.connector.Error as err:
            messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos:\n{err}")
            return None
    
    def configurar_interfaz(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#f0f0f0', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Campos de entrada
        campos = [
            ("ID (no editable):", self.id_cliente, "readonly", "#e6e6e6"),
            ("Nombre:", self.nombre, "normal", "#ffffff"),
            ("Dirección:", self.direccion, "normal", "#ffffff"),
            ("Teléfono:", self.telefono, "normal", "#ffffff"),
            ("Email:", self.email, "normal", "#ffffff")
        ]
        
        for i, (texto, var, estado, color) in enumerate(campos):
            tk.Label(main_frame, text=texto, bg='#f0f0f0').grid(row=i, column=0, sticky="e", pady=5)
            tk.Entry(main_frame, textvariable=var, state=estado, bg=color).grid(row=i, column=1, pady=5, sticky="ew")
        
        # Botones
        btn_frame = tk.Frame(main_frame, bg='#f0f0f0')
        btn_frame.grid(row=5, column=0, columnspan=2, pady=15)
        
        botones = [
            ("Guardar", self.guardar, "#2ecc71"),
            ("Eliminar", self.eliminar, "#e74c3c"),
            ("Actualizar", self.actualizar, "#3498db"),
            ("Limpiar", self.limpiar, "#f39c12")
        ]
        
        for i, (texto, comando, color) in enumerate(botones):
            tk.Button(btn_frame, text=texto, command=comando, 
                     bg=color, fg="white", width=12, font=('Arial', 10)).grid(row=0, column=i, padx=5)
        
        # Tabla con scrollbar
        table_frame = tk.Frame(main_frame, bg='#f0f0f0')
        table_frame.grid(row=6, column=0, columnspan=2, sticky="nsew")
        
        self.tabla = ttk.Treeview(table_frame, columns=("ID", "Nombre", "Dirección", "Teléfono", "Email"), show="headings")
        
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
            self.tabla.column(col, width=width)
        
        self.tabla.bind("<ButtonRelease-1>", self.seleccionar)
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)
        
        self.tabla.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Configurar expansión
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(6, weight=1)
    
    def guardar(self):
        if not all([self.nombre.get(), self.direccion.get(), self.telefono.get(), self.email.get()]):
            messagebox.showwarning("Advertencia", "Todos los campos son requeridos")
            return
        
        conn = self.conectar_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO clientes (nombre, direccion, telefono, email) VALUES (%s, %s, %s, %s)",
                    (self.nombre.get(), self.direccion.get(), self.telefono.get(), self.email.get())
                )
                conn.commit()
                messagebox.showinfo("Éxito", "Cliente guardado correctamente")
                self.mostrar()
                self.limpiar()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"No se pudo guardar el cliente:\n{err}")
            finally:
                cursor.close()
                conn.close()
    
    def eliminar(self):
        if not self.id_cliente.get():
            messagebox.showwarning("Advertencia", "Seleccione un cliente para eliminar")
            return
        
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este cliente?"):
            conn = self.conectar_db()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM clientes WHERE id_cliente = %s", (self.id_cliente.get(),))
                    conn.commit()
                    messagebox.showinfo("Éxito", "Cliente eliminado correctamente")
                    self.mostrar()
                    self.limpiar()
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"No se pudo eliminar el cliente:\n{err}")
                finally:
                    cursor.close()
                    conn.close()
    
    def actualizar(self):
        if not self.id_cliente.get():
            messagebox.showwarning("Advertencia", "Seleccione un cliente para actualizar")
            return
        
        if not all([self.nombre.get(), self.direccion.get(), self.telefono.get(), self.email.get()]):
            messagebox.showwarning("Advertencia", "Todos los campos son requeridos")
            return
        
        conn = self.conectar_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE clientes SET nombre = %s, direccion = %s, telefono = %s, email = %s WHERE id_cliente = %s",
                    (self.nombre.get(), self.direccion.get(), self.telefono.get(), self.email.get(), self.id_cliente.get())
                )
                conn.commit()
                messagebox.showinfo("Éxito", "Cliente actualizado correctamente")
                self.mostrar()
                self.limpiar()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"No se pudo actualizar el cliente:\n{err}")
            finally:
                cursor.close()
                conn.close()
    
    def limpiar(self):
        self.id_cliente.set("")
        self.nombre.set("")
        self.direccion.set("")
        self.telefono.set("")
        self.email.set("")
    
    def mostrar(self):
        conn = self.conectar_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT id_cliente, nombre, direccion, telefono, email FROM clientes")
                
                # Limpiar tabla
                for item in self.tabla.get_children():
                    self.tabla.delete(item)
                
                # Insertar datos
                for cliente in cursor.fetchall():
                    self.tabla.insert("", "end", values=cliente)
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"No se pudieron cargar los clientes:\n{err}")
            finally:
                cursor.close()
                conn.close()
    
    def seleccionar(self, event):
        selected = self.tabla.focus()
        if selected:
            values = self.tabla.item(selected, "values")
            self.id_cliente.set(values[0])
            self.nombre.set(values[1])
            self.direccion.set(values[2])
            self.telefono.set(values[3])
            self.email.set(values[4])

if __name__ == "__main__":
    root = tk.Tk()
    app = CRUDClientes(root)
    root.mainloop()
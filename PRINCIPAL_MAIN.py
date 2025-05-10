import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

class MenuPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Waldo's - Menú Principal")
        self.root.geometry("500x400")
        self.root.configure(bg='#f0f0f0')
        
        # Variables de conexión (consistentes con tus otros scripts)
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'david1234',
            'database': 'waldos'
        }
        
        # Intenta conectar al iniciar
        self.conn = self.conectar_db()
        if not self.conn:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            self.root.destroy()
            return
        
        self.configurar_interfaz()
    
    def conectar_db(self):
        try:
            conn = mysql.connector.connect(**self.db_config)
            return conn
        except Error as e:
            messagebox.showerror("Error de conexión", f"No se pudo conectar a MySQL:\n{e}")
            return None
    
    def configurar_interfaz(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#f0f0f0', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        tk.Label(main_frame, text="Sistema Waldo's", font=('Arial', 20, 'bold'), 
                bg='#f0f0f0', fg='#2c3e50').pack(pady=(0, 20))
        
        # Subtítulo
        tk.Label(main_frame, text="Seleccione el módulo a gestionar:", 
                font=('Arial', 12), bg='#f0f0f0').pack(pady=(0, 15))
        
        # Frame para los botones
        btn_frame = tk.Frame(main_frame, bg='#f0f0f0')
        btn_frame.pack(fill=tk.BOTH, expand=True)
        
        # Botones para cada módulo
        modulos = [
            ("Categorías", self.abrir_categorias, "#3498db"),
            ("Clientes", self.abrir_clientes, "#2ecc71"),
            ("Proveedores", self.abrir_proveedores, "#e74c3c"),
            ("Empleados", self.abrir_empleados, "#9b59b6"),
            ("Unidades", self.abrir_unidades, "#f39c12")
        ]
        
        for i, (texto, comando, color) in enumerate(modulos):
            btn = tk.Button(btn_frame, text=texto, command=comando,
                          bg=color, fg='white', font=('Arial', 12),
                          width=15, height=2, relief=tk.GROOVE, bd=0)
            btn.grid(row=i//2, column=i%2, padx=10, pady=10, sticky="nsew")
            btn_frame.grid_columnconfigure(i%2, weight=1)
        
        btn_frame.grid_rowconfigure(0, weight=1)
        btn_frame.grid_rowconfigure(1, weight=1)
        btn_frame.grid_rowconfigure(2, weight=1)
        
        # Botón de salir
        tk.Button(main_frame, text="Salir", command=self.cerrar_aplicacion,
                 bg='#95a5a6', fg='white', font=('Arial', 12),
                 width=15, height=1).pack(pady=(20, 0))
    
    def abrir_categorias(self):
        from categorias import CRUDCategorias
        self.abrir_ventana(CRUDCategorias, "CRUD Categorías")
    
    def abrir_clientes(self):
        from clientes import CRUDClientes
        self.abrir_ventana(CRUDClientes, "CRUD Clientes")
    
    def abrir_proveedores(self):
        from proveedores import CRUDProveedores
        self.abrir_ventana(CRUDProveedores, "CRUD Proveedores")
    
    def abrir_empleados(self):
        from Empleados import CRUDEmpleados
        self.abrir_ventana(CRUDEmpleados, "CRUD Empleados")
    
    def abrir_unidades(self):
        from unidades import CRUDUnidades
        self.abrir_ventana(CRUDUnidades, "CRUD Unidades")
    
    def abrir_ventana(self, clase, titulo):
        try:
            # Cierra la conexión actual para evitar problemas
            if self.conn and self.conn.is_connected():
                self.conn.close()
            
            # Crea una nueva ventana
            top = tk.Toplevel(self.root)
            top.title(titulo)
            
            # Pasa la configuración de la base de datos
            app = clase(top)
            
            # Maneja el cierre de la ventana secundaria
            top.protocol("WM_DELETE_WINDOW", lambda: self.on_child_close(top))
        except ImportError:
            messagebox.showerror("Error", f"No se pudo importar el módulo requerido")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el módulo:\n{e}")
    
    def on_child_close(self, window):
        window.destroy()
        # Reconecta al cerrar la ventana secundaria
        self.conn = self.conectar_db()
    
    def cerrar_aplicacion(self):
        if self.conn and self.conn.is_connected():
            self.conn.close()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = MenuPrincipal(root)
    root.mainloop()
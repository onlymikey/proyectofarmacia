import tkinter as tk
from tkinter import ttk, messagebox
from Uis.ventaUI import Venta
from Uis.clientesUI import Clientes
from Uis.inventarioUI import Inventario
from Uis.compraUI import Compra
from Uis.empleadosCRUD import Empleados
from Uis.proveedoresUI import SuppliersCRUD
from Uis.loginUI import LoginUI

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Mi Aplicación")
        self.master.geometry("1050x600")

        # Inicialmente no mostrar nada hasta hacer login
        self.tab_control = None

        # Lanzar la interfaz de login
        self.show_login()

    def show_login(self):
        login_window = tk.Toplevel(self.master)
        login_window.title("Login")
        login_ui = LoginUI(login_window, self)

    def init_app(self, profile):
        """ Inicializar las pestañas y el menú según el perfil del usuario """
        self.tab_control = ttk.Notebook(self.master)
        self.tab_control.pack(expand=1, fill="both")

        if profile == "Admin":
            self.add_all_tabs()
            self.create_file_menu()  # Crear menú para Admin
        elif profile == "Gerente":
            self.add_manager_tabs()
            # No se agrega menú para Gerente
        elif profile == "Cajero":
            self.add_cashier_tabs()
            # No se agrega menú para Cajero

    def create_file_menu(self):
        """ Crea el menú "File" para Admin """
        self.menubar = tk.Menu(self.master)
        self.master.config(menu=self.menubar)

        file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=file_menu)

        file_menu.add_command(label="Empleados", command=self.abrir_empleados)
        file_menu.add_command(label="Proveedores", command=self.abrir_proveedores)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.master.quit)

    def abrir_empleados(self):
        ventana_empleados = tk.Toplevel(self.master)
        ventana_empleados.title("Empleados")
        ventana_empleados.geometry("600x300")
        interfaz = Empleados(ventana_empleados)

    def abrir_proveedores(self):
        ventana_proveedores = tk.Toplevel(self.master)
        ventana_proveedores.title("Proveedores")
        ventana_proveedores.geometry("600x300")
        interfaz = SuppliersCRUD(ventana_proveedores)

    def add_all_tabs(self):
        # Crear las pestañas para Admin (todas)
        self.add_venta_tab()
        self.add_clientes_tab()
        self.add_inventario_tab()
        self.add_compra_tab()

    def add_manager_tabs(self):
        # Crear las pestañas solo para Gerente (Clientes, Ventas)
        self.add_venta_tab()
        self.add_clientes_tab()

    def add_cashier_tabs(self):
        # Crear las pestañas solo para Cajero (solo crear/leer Clientes y Ventas)
        self.add_venta_tab()  # Venta con restricciones para Cajero
        self.add_clientes_tab()  # Clientes con restricciones para Cajero

    def add_venta_tab(self):
        self.tab_venta = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_venta, text="Venta")
        self.Venta_interface = Venta(self.tab_venta)

    def add_clientes_tab(self):
        self.tab_clientes = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_clientes, text="Clientes")
        self.clientes_interface = Clientes(self.tab_clientes)

    def add_inventario_tab(self):
        self.tab_inventario = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_inventario, text="Inventario")
        self.inventario_interface = Inventario(self.tab_inventario)

    def add_compra_tab(self):
        self.tab_compra = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_compra, text="Compra")
        self.compra_interface = Compra(self.tab_compra)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

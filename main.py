import tkinter as tk
from tkinter import ttk, messagebox
from Uis.ventaUI import Venta
from Uis.clientesUI import Clientes
from Uis.inventarioUI import Inventario
from Uis.compraUI import Compra
from Uis.empleadosCRUD import Empleados
from Uis.proveedoresUI import SuppliersCRUD

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Mi Aplicación")
        self.master.geometry("800x600")

        # Crear el contenedor para las pestañas
        self.tab_control = ttk.Notebook(self.master)
        self.tab_control.pack(expand=1, fill="both")

        # Crear las pestañas
        self.tab_venta = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_venta, text="Venta")
        self.Venta_interface = Venta(self.tab_venta)

        self.tab_clientes = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_clientes, text="Clientes")
        self.clientes_interface = Clientes(self.tab_clientes)

        self.tab_inventario = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_inventario, text="Inventario")
        self.inventario_interface = Inventario(self.tab_inventario)

        self.tab_compra = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_compra, text="Compra")
        self.compra_interface = Compra(self.tab_compra)

        # Crear el menú
        self.menubar = tk.Menu(self.master)
        self.master.config(menu=self.menubar)

        # Crear el menú "Archivo"
        file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=file_menu)

        # Añadir opciones al menú
        file_menu.add_command(label="Empleados", command=self.abrir_empleados)
        file_menu.add_command(label="Proveedores", command=self.abrir_proveedores)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.master.quit)

    def abrir_empleados(self):
        ventana_empleados = tk.Toplevel(self.master)  # Usa self.master en lugar de self.menubar
        ventana_empleados.title("Empleados")
        ventana_empleados.geometry("600x300")
        interfaz = Empleados(ventana_empleados)        # Pasa ventana_empleados como parent

    def abrir_proveedores(self):
        ventana_proveedores = tk.Toplevel(self.master)  # Usa self.master en lugar de self.menubar
        ventana_proveedores.title("Proveedores")
        ventana_proveedores.geometry("600x300")
        interfaz = SuppliersCRUD(ventana_proveedores)        # Pasa ventana_empleados como parent

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()


import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
from Controllers.supplier_controller import SupplierController

class SuppliersCRUD:
    def __init__(self, parent):
        self.parent = parent
        self.supplier_controller = SupplierController()
        self.create_widgets()

    def create_widgets(self):
        # Frame para los widgets de proveedores
        suppliers_frame = tk.Frame(self.parent)
        suppliers_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Label(suppliers_frame, text="Ingrese IUP del proveedor:").grid(row=0, column=0, padx=10, pady=10)
        self.iup_entry = ttk.Entry(suppliers_frame)
        self.iup_entry.grid(row=0, column=1, padx=10, pady=10)
        ttk.Button(suppliers_frame, text="Buscar", command=self.search_supplier).grid(row=0, column=2, padx=10, pady=10)

        ttk.Label(suppliers_frame, text="IUP:").grid(row=1, column=0, padx=10, pady=10)
        self.iup_display = ttk.Entry(suppliers_frame, state='readonly')
        self.iup_display.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(suppliers_frame, text="Nombre de la empresa:").grid(row=2, column=0, padx=10, pady=10)
        self.company_name_entry = ttk.Entry(suppliers_frame)
        self.company_name_entry.grid(row=2, column=1, padx=10, pady=10)

        ttk.Button(suppliers_frame, text="Nuevo", command=self.new_supplier).grid(row=3, column=0, padx=10, pady=10)
        ttk.Button(suppliers_frame, text="Guardar", command=self.save_supplier).grid(row=3, column=1, padx=10, pady=10)
        ttk.Button(suppliers_frame, text="Actualizar", command=self.update_supplier).grid(row=3, column=2, padx=10, pady=10)
        ttk.Button(suppliers_frame, text="Eliminar", command=self.delete_supplier).grid(row=3, column=3, padx=10, pady=10)

    def search_supplier(self):
        iup = self.iup_entry.get().strip()
        if not iup:
            messagebox.showerror("Error", "Ingrese un IUP para buscar")
            return
        result = self.supplier_controller.get_supplier_by_iup(iup)
        if result['status']:
            self.fill_fields(result['data'])
        else:
            messagebox.showerror("Error", result['message'])

    def fill_fields(self, supplier):
        self.iup_display.config(state='normal')
        self.iup_display.delete(0, tk.END)
        self.iup_display.insert(0, supplier['iup'])  # Asegúrate de que la clave sea correcta
        self.iup_display.config(state='readonly')

        self.company_name_entry.delete(0, tk.END)
        self.company_name_entry.insert(0, supplier['companyName'])  # Asegúrate de que la clave sea correcta

    def new_supplier(self):
        self.clear_fields()
        # Generar un IUP aleatorio de 16 caracteres
        random_iup = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
        self.iup_display.config(state='normal')
        self.iup_display.delete(0, tk.END)
        self.iup_display.insert(0, random_iup)  # Asigna el IUP aleatorio
        self.iup_display.config(state='readonly')

    def clear_fields(self):
        self.iup_display.config(state='normal')
        self.iup_display.delete(0, tk.END)
        self.iup_display.config(state='readonly')
        self.company_name_entry.delete(0, tk.END)

    def save_supplier(self):
        iup = self.iup_display.get().strip()
        company_name = self.company_name_entry.get().strip()
        result = self.supplier_controller.create_supplier(iup, company_name)
        messagebox.showinfo(result['type'], result['message'])
        if result['status']:
            self.clear_fields()

    def update_supplier(self):
        iup = self.iup_display.get().strip()
        company_name = self.company_name_entry.get().strip()
        result = self.supplier_controller.update_supplier(iup, company_name)
        messagebox.showinfo(result['type'], result['message'])
        if result['status']:
            self.clear_fields()

    def delete_supplier(self):
        iup = self.iup_display.get().strip()
        result = self.supplier_controller.delete_supplier(iup)
        messagebox.showinfo(result['type'], result['message'])
        if result['status']:
            self.clear_fields()

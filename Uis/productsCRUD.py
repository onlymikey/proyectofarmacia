import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
from Controllers.product_controller import ProductController

class ProductsCRUD:
    def __init__(self, parent):
        self.parent = parent
        self.product_controller = ProductController()
        self.create_widgets()

    def create_widgets(self):
        # Frame para los widgets de productos
        products_frame = tk.Frame(self.parent)
        products_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Campos para UPC y nombre del producto
        ttk.Label(products_frame, text="Ingrese UPC del producto:").grid(row=0, column=0, padx=10, pady=10)
        self.upc_entry = ttk.Entry(products_frame)
        self.upc_entry.grid(row=0, column=1, padx=10, pady=10)
        ttk.Button(products_frame, text="Buscar", command=self.search_product).grid(row=0, column=2, padx=10, pady=10)

        ttk.Label(products_frame, text="UPC:").grid(row=1, column=0, padx=10, pady=10)
        self.upc_display = ttk.Entry(products_frame, state='readonly')
        self.upc_display.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(products_frame, text="Nombre:").grid(row=2, column=0, padx=10, pady=10)
        self.name_entry = ttk.Entry(products_frame)
        self.name_entry.grid(row=2, column=1, padx=10, pady=10)

        ttk.Label(products_frame, text="Stock:").grid(row=3, column=0, padx=10, pady=10)
        self.stock_entry = ttk.Entry(products_frame)
        self.stock_entry.grid(row=3, column=1, padx=10, pady=10)

        ttk.Label(products_frame, text="Descripción:").grid(row=4, column=0, padx=10, pady=10)
        self.description_entry = ttk.Entry(products_frame)
        self.description_entry.grid(row=4, column=1, padx=10, pady=10)

        ttk.Label(products_frame, text="Precio:").grid(row=5, column=0, padx=10, pady=10)
        self.price_entry = ttk.Entry(products_frame)
        self.price_entry.grid(row=5, column=1, padx=10, pady=10)

        # Botones para operaciones CRUD
        ttk.Button(products_frame, text="Nuevo", command=self.new_product).grid(row=6, column=0, padx=10, pady=10)
        self.save_button = ttk.Button(products_frame, text="Guardar", command=self.save_product)  # Guardar referencia al botón
        self.save_button.grid(row=6, column=1, padx=10, pady=10)
        ttk.Button(products_frame, text="Actualizar", command=self.update_product).grid(row=6, column=2, padx=10, pady=10)
        ttk.Button(products_frame, text="Eliminar", command=self.delete_product).grid(row=6, column=3, padx=10, pady=10)

    def search_product(self):
        upc = self.upc_entry.get().strip()
        if not upc:
            messagebox.showerror("Error", "Ingrese un UPC para buscar")
            return
        result = self.product_controller.get_product_by_upc(upc)
        if result['status']:
            self.fill_fields(result['data'])
            self.save_button.state(['disabled'])
        else:
            messagebox.showerror("Error", result['message'])

    def fill_fields(self, product):
        self.upc_display.config(state='normal')
        self.upc_display.delete(0, tk.END)
        self.upc_display.insert(0, product['upc'])  # Asegúrate de que la clave sea correcta
        self.upc_display.config(state='readonly')

        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, product['name'])  # Asegúrate de que la clave sea correcta

        self.stock_entry.delete(0, tk.END)
        self.stock_entry.insert(0, product['stock'])  # Asegúrate de que la clave sea correcta

        self.description_entry.delete(0, tk.END)
        self.description_entry.insert(0, product['description'])  # Asegúrate de que la clave sea correcta

        self.price_entry.delete(0, tk.END)
        self.price_entry.insert(0, product['price'])  # Asegúrate de que la clave sea correcta

    def new_product(self):
        self.clear_fields()
        self.upc_display.config(state='normal')
        self.upc_display.delete(0, tk.END)

        # Generar un UPC aleatorio de 12 caracteres (números y letras)
        random_upc = ''.join(random.choices(string.digits, k=12))
        self.upc_display.insert(0, random_upc)  # Asigna el UPC generado
        self.upc_display.config(state='readonly')
        self.save_button.state(['!disabled'])

    def clear_fields(self):
        self.upc_display.config(state='normal')
        self.upc_display.delete(0, tk.END)
        self.upc_display.config(state='readonly')
        self.name_entry.delete(0, tk.END)
        self.stock_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)

    def save_product(self):
        upc = self.upc_display.get().strip()
        name = self.name_entry.get().strip()
        stock = int(self.stock_entry.get().strip())
        description = self.description_entry.get().strip()
        price = float(self.price_entry.get().strip())
        
        result = self.product_controller.create_product(upc, name, stock, description, price)
        messagebox.showinfo(result['type'], result['message'])
        if result['status']:
            self.clear_fields()

    def update_product(self):
        upc = self.upc_display.get().strip()
        name = self.name_entry.get().strip()
        stock = int(self.stock_entry.get().strip())
        description = self.description_entry.get().strip()
        price = float(self.price_entry.get().strip())

        result = self.product_controller.update_product(upc, name, stock, description, price)
        messagebox.showinfo(result['type'], result['message'])
        if result['status']:
            self.clear_fields()

        self.save_button.state(['!disabled'])

    def delete_product(self):
        upc = self.upc_display.get().strip()
        result = self.product_controller.delete_product(upc)
        messagebox.showinfo(result['type'], result['message'])
        if result['status']:
            self.clear_fields()

        self.save_button.state(['!disabled'])
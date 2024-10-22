import tkinter as tk
from tkinter import ttk
from Uis.productsCRUD import ProductsCRUD
from Controllers.product_controller import ProductController

class Inventario:
    def __init__(self, parent):
        self.parent = parent
        self.product_controller = ProductController()  # Inicializa el controlador de productos
        self.setup_ui()

    def setup_ui(self):
        # Frame superior (búsqueda y botones)
        frame_superior = tk.Frame(self.parent)
        frame_superior.pack(fill=tk.X, padx=10, pady=5)

        # Campo de búsqueda
        btn_buscar = tk.Button(frame_superior, text="Buscar")
        btn_buscar.grid(row=0, column=0, padx=10, pady=10)
        self.entry_buscar = tk.Entry(frame_superior)
        self.entry_buscar.grid(row=0, column=1, padx=5)

        btn_nuevo = tk.Button(frame_superior, text="CRUD Productos", command=self.nuevo)
        btn_nuevo.grid(row=0, column=3, padx=5)

        btn_actualizar = tk.Button(frame_superior, text="Actualizar", command=self.cargar_productos)
        btn_actualizar.grid(row=0, column=4, padx=5)

        btn_cancelar = tk.Button(frame_superior, text="Cancelar", command=self.cancelar)
        btn_cancelar.grid(row=0, column=5, padx=5)

        btn_editar = tk.Button(frame_superior, text="Editar", command=self.editar)
        btn_editar.grid(row=0, column=6, padx=5)

        btn_eliminar = tk.Button(frame_superior, text="Eliminar", command=self.eliminar)
        btn_eliminar.grid(row=0, column=7, padx=5)

        # Frame para la tabla
        frame_tabla = tk.Frame(self.parent)
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Configuración de la tabla
        cols = ('Seleccionado', 'UPC', 'Nombre', 'Stock', 'Descripción', 'Precio')
        self.tabla = ttk.Treeview(frame_tabla, columns=cols, show='headings')

        for col in cols:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, minwidth=100, width=150)
            self.tabla.column('Seleccionado', width=50)  # Ajustar ancho para la columna de selección

        # Añadir la tabla a la ventana
        self.tabla.pack(fill=tk.BOTH, expand=True)

        # Asociar el evento de clic para alternar el "checkbox"
        self.tabla.bind("<Double-1>", self.alternar_checkbox)

    def cargar_productos(self):
        # Limpiar la tabla antes de cargar nuevos datos
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        # Obtener los productos del controlador
        response = self.product_controller.get_all_products()
        
        if response['status']:
            for product in response['data']:
                self.tabla.insert('', 'end', values=('✖', product['upc'], product['name'], product['stock'], product['description'], product['price']))
        else:
            print("Error:", response['message']) 

    def nuevo(self):
        # Crear una nueva ventana (Toplevel)
        ventana_nueva = tk.Toplevel(self.parent)
        ventana_nueva.title("Gestión de Productos")
        ventana_nueva.geometry("600x400")  # Ajusta el tamaño de la ventana

        # Cargar la interfaz de productos pasando el controlador también
        products_ui = ProductsCRUD(ventana_nueva)

    def salvar(self):
        pass

    def cancelar(self):
        pass

    def editar(self):
        pass

    def eliminar(self):
        pass

    def alternar_checkbox(self, event):
        # Obtener el item seleccionado
        item_id = self.tabla.focus()
        
        # Verificar que hay un item seleccionado
        if item_id:  
            current_value = self.tabla.item(item_id, 'values')[0] 
            
            # Alternar entre '✔' y '✖'
            new_value = '✔' if current_value == '✖' else '✖'
            self.tabla.item(item_id, values=(new_value,) + self.tabla.item(item_id, 'values')[1:])

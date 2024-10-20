import tkinter as tk
from tkinter import ttk

class Compra:
    def __init__(self, parent):
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        # Buscador
        btn_buscar = tk.Button(self.parent, text="Buscar")
        btn_buscar.grid(row=0, column=0, padx=10, pady=10)
        entry_buscar = tk.Entry(self.parent)
        entry_buscar.grid(row=0, column=1, padx=10, pady=10)

        # Folio
        lbl_folio = tk.Label(self.parent, text="Folio:")
        lbl_folio.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        entry_folio = tk.Entry(self.parent)
        entry_folio.grid(row=1, column=1, padx=10, pady=5)

        # Producto
        lbl_producto = tk.Label(self.parent, text="Producto:")
        lbl_producto.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        entry_producto = tk.Entry(self.parent)
        entry_producto.grid(row=2, column=1, padx=10, pady=5)

        # Cantidad
        lbl_cantidad = tk.Label(self.parent, text="Cantidad:")
        lbl_cantidad.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        entry_cantidad = tk.Entry(self.parent)
        entry_cantidad.grid(row=3, column=1, padx=10, pady=5)

        # Crecio compra
        lbl_precio = tk.Label(self.parent, text="Precio de compra:")
        lbl_precio.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        entry_precio = tk.Entry(self.parent)
        entry_precio.grid(row=4, column=1, padx=10, pady=5)

        # Botones Nuevo, Añadir y Eliminar
        btn_nuevo = tk.Button(self.parent, text="Nuevo", command=self.nuevo_producto)
        btn_nuevo.grid(row=2, column=2, padx=10, pady=5)
        btn_anadir = tk.Button(self.parent, text="Añadir", command=self.agregar_producto)
        btn_anadir.grid(row=3, column=2, padx=10, pady=5)
        btn_eliminar = tk.Button(self.parent, text="Eliminar", command=self.eliminar_producto)
        btn_eliminar.grid(row=4, column=2, padx=10, pady=5)

        # tree de productos
        self.tree = ttk.Treeview(self.parent, columns=('Seleccionado',"nombre", "cantidad", "precio"), show="headings")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("cantidad", text="Cantidad")
        self.tree.heading("precio", text="Precio")

        # Simulación de productos en la tree
        productos = [('✖',"Producto 1", "1", "10.00"), 
                     ('✖',"Producto 2", "2", "20.00"), 
                     ('✖',"Producto 3", "3", "30.00")]

        for producto in productos:
            self.tree.insert("", "end", values=producto)

        self.tree.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

        # Asociar el evento de clic para alternar el "checkbox"
        self.tree.bind("<Double-1>", self.alternar_checkbox)

        # Subtotal, Descuento, Total y Puntos
        lbl_subtotal = tk.Label(self.parent, text="Subtotal:")
        lbl_subtotal.grid(row=6, column=2, padx=10, pady=5, sticky="e")
        lbl_subtotal_valor = tk.Label(self.parent, text="XX $")
        lbl_subtotal_valor.grid(row=6, column=3, padx=10, pady=5, sticky="w")

        lbl_total = tk.Label(self.parent, text="Total:")
        lbl_total.grid(row=8, column=2, padx=10, pady=5, sticky="e")
        lbl_total_valor = tk.Label(self.parent, text="XX $")
        lbl_total_valor.grid(row=8, column=3, padx=10, pady=5, sticky="w")

        btn_pagar = tk.Button(self.parent, text="Realizar compra de productos", command=self.compra_productos)
        btn_pagar.grid(row=10, column=3, padx=10, pady=10)


    def compra_productos(self):
        pass

    def nuevo_producto(self):
        pass

    def agregar_producto(self):
        pass

    def eliminar_producto(self):
        pass

    def alternar_checkbox(self, event):
        # Obtener el item seleccionado
        item_id = self.tree.focus()
        
        # Verificar que hay un item seleccionado
        if item_id:  
            current_value = self.tree.item(item_id, 'values')[0] 
            
            # Alternar entre '✔' y '✖'
            new_value = '✔' if current_value == '✖' else '✖'
            self.tree.item(item_id, values=(new_value,) + self.tree.item(item_id, 'values')[1:])
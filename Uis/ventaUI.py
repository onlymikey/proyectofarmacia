import tkinter as tk
from tkinter import ttk

class Venta:
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

        # Cliente
        lbl_cliente = tk.Label(self.parent, text="Cliente:")
        lbl_cliente.grid(row=1, column=2, padx=10, pady=5)
        entry_cliente = tk.Entry(self.parent)
        entry_cliente.grid(row=1, column=3, padx=10, pady=5)

        # Cantidad de puntos
        lbl_puntos = tk.Label(self.parent, text="Cant. puntos:")
        lbl_puntos.grid(row=2, column=2, padx=10, pady=5)
        entry_puntos = tk.Entry(self.parent)
        entry_puntos.grid(row=2, column=3, padx=10, pady=5)

        # Descuento
        lbl_descuento = tk.Label(self.parent, text="% Descuento:")
        lbl_descuento.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        entry_descuento = tk.Entry(self.parent)
        entry_descuento.grid(row=2, column=1, padx=10, pady=5)

        # Producto
        lbl_producto = tk.Label(self.parent, text="Producto:")
        lbl_producto.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        entry_producto = tk.Entry(self.parent)
        entry_producto.grid(row=3, column=1, padx=10, pady=5)

        # Stock
        lbl_stock = tk.Label(self.parent, text="Stock:")
        lbl_stock.grid(row=3, column=2, padx=10, pady=5)
        entry_stock = tk.Entry(self.parent)
        entry_stock.grid(row=3, column=3, padx=10, pady=5)

        # Cantidad
        lbl_cantidad = tk.Label(self.parent, text="Cantidad:")
        lbl_cantidad.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        entry_cantidad = tk.Entry(self.parent)
        entry_cantidad.grid(row=4, column=1, padx=10, pady=5)

        # Botones Añadir y Eliminar
        btn_anadir = tk.Button(self.parent, text="Añadir", command=self.agregar_producto)
        btn_anadir.grid(row=4, column=2, padx=10, pady=5)
        btn_eliminar = tk.Button(self.parent, text="Eliminar", command=self.eliminar_producto)
        btn_eliminar.grid(row=4, column=3, padx=10, pady=5)

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

        lbl_descuento_total = tk.Label(self.parent, text="Descuento:")
        lbl_descuento_total.grid(row=7, column=2, padx=10, pady=5, sticky="e")
        lbl_descuento_valor = tk.Label(self.parent, text="XX%")
        lbl_descuento_valor.grid(row=7, column=3, padx=10, pady=5, sticky="w")

        lbl_total = tk.Label(self.parent, text="Total:")
        lbl_total.grid(row=8, column=2, padx=10, pady=5, sticky="e")
        lbl_total_valor = tk.Label(self.parent, text="XX $")
        lbl_total_valor.grid(row=8, column=3, padx=10, pady=5, sticky="w")

        lbl_puntos_final = tk.Label(self.parent, text="Puntos:")
        lbl_puntos_final.grid(row=9, column=2, padx=10, pady=5, sticky="e")
        lbl_puntos_valor = tk.Label(self.parent, text="XX")
        lbl_puntos_valor.grid(row=9, column=3, padx=10, pady=5, sticky="w")

        # Botones finales
        btn_nuevo = tk.Button(self.parent, text="Nuevo", command=self.nueva_venta)
        btn_nuevo.grid(row=10, column=0, padx=10, pady=10)

        btn_editar = tk.Button(self.parent, text="Editar", command=self.editar_venta)
        btn_editar.grid(row=10, column=1, padx=10, pady=10)

        btn_cancelar = tk.Button(self.parent, text="Cancelar", command=self.cancelar)
        btn_cancelar.grid(row=10, column=2, padx=10, pady=10)

        btn_eliminar_final = tk.Button(self.parent, text="Eliminar", command=self.eliminar_venta)
        btn_eliminar_final.grid(row=10, column=3, padx=10, pady=10)

        btn_pagar = tk.Button(self.parent, text="Pagar", command=self.abrir_ventana_pago)
        btn_pagar.grid(row=10, column=4, padx=10, pady=10)

    def abrir_ventana_pago(self):
        # Crear la ventana de pago
        ventana_pago = tk.Toplevel(self.parent)
        ventana_pago.title("Método de Pago")
        ventana_pago.geometry("300x250")

        # Variables (no usadas en esta etapa, solo visualización)
        metodo_pago = tk.StringVar(value="Efectivo")
        cantidad_recibida = tk.DoubleVar()
        cambio = tk.DoubleVar(value=0.0)

        # Etiquetas y botones en la ventana de pago
        lbl_total = tk.Label(ventana_pago, text="Total a Pagar: XX $")
        lbl_total.pack(pady=10)

        lbl_metodo_pago = tk.Label(ventana_pago, text="Selecciona el método de pago:")
        lbl_metodo_pago.pack(pady=5)

        # Selección del método de pago
        rb_efectivo = tk.Radiobutton(ventana_pago, text="Efectivo", variable=metodo_pago, value="Efectivo")
        rb_tarjeta = tk.Radiobutton(ventana_pago, text="Tarjeta", variable=metodo_pago, value="Tarjeta")
        rb_efectivo.pack()
        rb_tarjeta.pack()

        lbl_cantidad = tk.Label(ventana_pago, text="Cantidad recibida:")
        lbl_cantidad.pack(pady=5)

        entry_cantidad = tk.Entry(ventana_pago)
        entry_cantidad.pack()

        lbl_cambio = tk.Label(ventana_pago, text="Cambio:")
        lbl_cambio.pack()

        lbl_cambio_valor = tk.Label(ventana_pago, text="XX $")
        lbl_cambio_valor.pack()

        btn_aceptar = tk.Button(ventana_pago, text="Aceptar")
        btn_aceptar.pack(pady=10)


    def nueva_venta(self):
        pass

    def cancelar(self):
        pass
    
    def eliminar_venta(self):
        pass

    def editar_venta(self):
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
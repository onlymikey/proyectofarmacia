import tkinter as tk
from tkinter import ttk
import random
import string
from decimal import Decimal
import datetime
from Controllers.sale_controller import SaleController
from Controllers.sales_register_controller import SalesRegisterController
from Controllers.product_controller import ProductController
from Controllers.client_controller import ClientController
from Models.cart_model import Cart
from .loginUI import Session
from Models.cart_model import Cart

class Venta:
    def __init__(self, parent):
        self.parent = parent
        self.sale_controller = SaleController()
        self.sales_register_controller = SalesRegisterController()
        self.product_controller = ProductController()
        self.controller = ClientController()
        self.cart = Cart()
        self.client_data = {}
        self.product_data = self.obtener_productos()  # Productos almacenados como diccionario

        print("Productos obtenidos:", self.product_data)  # Agrega esta línea para depuración

        self.modo_edicion = False  # Indica si estamos en modo edición
        self.setup_ui()
        self.load_clients()

        
    def setup_ui(self):
        # Botón de Nuevo
        btn_nuevo = tk.Button(self.parent, text="Nuevo", command=self.nueva_venta)
        btn_nuevo.grid(row=10, column=0, padx=10, pady=10)

        # Botón de Editar
        self.btn_editar = tk.Button(self.parent, text="Editar", command=self.editar_venta)
        self.btn_editar.grid(row=10, column=1, padx=10, pady=10)
        self.btn_editar.config(state="disabled")  # Deshabilitado inicialmente

        # Botón de Cancelar
        self.btn_cancelar = tk.Button(self.parent, text="Cancelar", command=self.cancelar_accion)
        self.btn_cancelar.grid(row=10, column=2, padx=10, pady=10)
        self.btn_cancelar.config(state="disabled")  # Deshabilitado inicialmente

        # Buscador
        btn_buscar = tk.Button(self.parent, text="Buscar")
        btn_buscar.grid(row=0, column=0, padx=10, pady=10)
        entry_buscar = tk.Entry(self.parent)
        entry_buscar.grid(row=0, column=1, padx=10, pady=10)

        # Folio
        lbl_folio = tk.Label(self.parent, text="Folio:")
        lbl_folio.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_folio = tk.Entry(self.parent, state="readonly")
        self.entry_folio.grid(row=1, column=1, padx=10, pady=5)

        # Cliente
        lbl_cliente = tk.Label(self.parent, text="Cliente:")
        lbl_cliente.grid(row=1, column=2, padx=10, pady=5)
        self.combobox_cliente = ttk.Combobox(self.parent, state="readonly")
        self.combobox_cliente.grid(row=1, column=3, padx=10, pady=5)
        self.combobox_cliente.bind("<<ComboboxSelected>>")

        # Producto (Combobox)
        lbl_producto = tk.Label(self.parent, text="Producto:")
        lbl_producto.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.combobox_producto = ttk.Combobox(
        self.parent, 
        values=[product['name'] for product in self.product_data.values()], 
        state="readonly"
    )
        self.combobox_producto.grid(row=3, column=1, padx=10, pady=5)
        self.combobox_producto.bind("<<ComboboxSelected>>", self.mostrar_stock)

        # Stock (Readonly)
        lbl_stock = tk.Label(self.parent, text="Stock:")
        lbl_stock.grid(row=3, column=2, padx=10, pady=5)
        self.lbl_stock_valor = tk.Label(self.parent, text="0", relief="sunken", width=10)
        self.lbl_stock_valor.grid(row=3, column=3, padx=10, pady=5)

        # Cantidad
        lbl_cantidad = tk.Label(self.parent, text="Cantidad:")
        lbl_cantidad.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.entry_cantidad = tk.Entry(self.parent)
        self.entry_cantidad.grid(row=4, column=1, padx=10, pady=5)

        # Botones Añadir y Eliminar
        btn_anadir = tk.Button(self.parent, text="Añadir", command=self.agregar_producto)
        btn_anadir.grid(row=4, column=2, padx=10, pady=5)
        btn_eliminar = tk.Button(self.parent, text="Eliminar", command=self.eliminar_producto)
        btn_eliminar.grid(row=4, column=3, padx=10, pady=5)

        # Treeview de productos
        self.tree = ttk.Treeview(self.parent, columns=("nombre", "cantidad", "precio"), show="headings")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("cantidad", text="Cantidad")
        self.tree.heading("precio", text="Precio Individual")
        self.tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

        # Subtotal y Total
        lbl_subtotal = tk.Label(self.parent, text="Subtotal:")
        lbl_subtotal.grid(row=6, column=2, padx=10, pady=5, sticky="e")
        self.lbl_subtotal_valor = tk.Label(self.parent, text="0.00 $")
        self.lbl_subtotal_valor.grid(row=6, column=3, padx=10, pady=5, sticky="w")

        lbl_total = tk.Label(self.parent, text="Total (IVA 16%):")
        lbl_total.grid(row=7, column=2, padx=10, pady=5, sticky="e")
        self.lbl_total_valor = tk.Label(self.parent, text="0.00 $")
        self.lbl_total_valor.grid(row=7, column=3, padx=10, pady=5, sticky="w")

        # Botón de Pagar
        self.btn_pagar = tk.Button(self.parent, text="Pagar", command=self.abrir_ventana_pago)
        self.btn_pagar.grid(row=10, column=4, padx=10, pady=10)
        self.btn_pagar.config(state="disabled")  # Deshabilitado hasta que se cree una venta

        # Deshabilitar campos inicialmente
        self.desactivar_campos()

    def load_clients(self):
        """Cargar clientes desde el controlador y llenar el combobox"""
        response = self.controller.get_all_clients()  # Asegúrate de que este método devuelva los clientes
        if response['status']:
            self.client_data = {client['name']: client for client in response['data']}
            self.combobox_cliente['values'] = list(self.client_data.keys())  # Solo los nombres de los clientes
        else:
            tk.messagebox.showerror("Error", "No se pudieron obtener los clientes")

    def generar_folio(self):
        """Generar un folio aleatorio de 12 caracteres alfanuméricos"""
        caracteres = string.digits  # Letras mayúsculas y dígitos
        folio = ''.join(random.choices(caracteres, k=12))  # Folio de 12 caracteres
        return folio

    def nueva_venta(self):
        """Habilitar campos y asignar un folio automáticamente."""
        self.limpiar_campos()
        self.folio = self.generar_folio()  # Asigna un nuevo folio automáticamente
        self.entry_folio.config(state="normal")
        self.entry_folio.insert(0, self.folio)
        self.entry_folio.config(state="readonly")
        self.activar_campos()
        self.modo_edicion = False  # No estamos en modo edición
        self.btn_pagar.config(state="normal")
        self.btn_editar.config(state="normal")
        self.btn_cancelar.config(state="normal")

    def editar_venta(self):
        """Habilitar los campos para edición (excepto folio) si ya existe una venta seleccionada."""
        if self.entry_folio.get():  # Si hay un folio en el campo
            self.activar_campos()
            self.entry_folio.config(state="readonly")  # Folio no debe ser editable
            self.modo_edicion = True

    def cancelar_accion(self):
        """Cancelar la acción de crear o editar, y limpiar todos los campos."""
        self.limpiar_campos()
        self.desactivar_campos()
        self.btn_pagar.config(state="disabled")  # Deshabilitar el botón de Pagar
        self.btn_editar.config(state="disabled")
        self.btn_cancelar.config(state="disabled")
        self.modo_edicion = False  # Salir del modo edición

    def limpiar_campos(self):
        """Limpiar todos los campos de la interfaz."""
        self.entry_folio.delete(0, tk.END)
        self.combobox_cliente.set("")
        self.entry_cantidad.delete(0, tk.END)
        self.combobox_producto.set("")
        self.lbl_stock_valor.config(text="0")
        self.lbl_subtotal_valor.config(text="0.00 $")
        self.lbl_total_valor.config(text="0.00 $")
        self.tree.delete(*self.tree.get_children())  # Eliminar todos los productos de la tabla

    def activar_campos(self):
        """Habilitar los campos para permitir la creación o edición de una venta."""
        self.combobox_cliente.config(state="readonly")
        self.entry_cantidad.config(state="normal")
        self.combobox_producto.config(state="readonly")

    def desactivar_campos(self):
        """Desactivar todos los campos para evitar cambios si no se ha iniciado una nueva venta."""
        self.combobox_cliente.config(state="disabled")
        self.entry_cantidad.config(state="disabled")
        self.combobox_producto.config(state="disabled")
        self.btn_pagar.config(state="disabled")

    def obtener_productos(self):
        """Obtener los productos desde el controlador y almacenarlos en un diccionario"""
        response = self.product_controller.get_all_products()
        if response['status']:
            # Almacenamos los productos en un diccionario con el nombre del producto como clave
            products = {p['name']: p for p in response['data']}
            return products
        else:
            tk.messagebox.showerror("Error", "No se pudieron obtener los productos")
            return {}

    def mostrar_stock(self, event):
        """Mostrar el stock del producto seleccionado en el combobox."""
        producto_seleccionado = self.combobox_producto.get()
        if producto_seleccionado in self.product_data:
            producto = self.product_data[producto_seleccionado]
            self.lbl_stock_valor.config(text=str(producto['stock']))  # Mostramos el stock
        else:
            self.lbl_stock_valor.config(text="0")

    def agregar_producto(self):
        """Agregar producto al carrito"""
        producto_seleccionado = self.combobox_producto.get()
        if producto_seleccionado in self.product_data:
            producto = self.product_data[producto_seleccionado]
            cantidad = int(self.entry_cantidad.get())  # Cantidad ingresada por el usuario
            precio = producto['price']  # Obtenemos el precio directamente del diccionario
            stock_disponible = producto['stock']  # Obtener el stock del producto

            # Validar que la cantidad no sea mayor que el stock disponible
            if cantidad > stock_disponible:
                tk.messagebox.showerror("Error", "La cantidad ingresada supera el stock disponible.")
                return  # No continuar si hay un error

            # Añadir producto al carrito
            self.cart.add_item(producto_seleccionado, cantidad, precio)

            # Insertar en la tabla de la UI
            self.tree.insert("", "end", values=(producto_seleccionado, cantidad, precio))
            
            # Actualizar subtotal y total
            self.actualizar_totales()
        else:
            tk.messagebox.showerror("Error", "Producto no encontrado")

    def eliminar_producto(self):
        """Eliminar el producto seleccionado del carrito"""
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            producto = item['values'][1]
            self.cart.remove_item(producto)
            self.tree.delete(selected_item)
            self.actualizar_totales()

    def actualizar_totales(self):
        """Actualizar el subtotal y el total con IVA."""
        subtotal = self.cart.calculate_subtotal()  # Calcula el subtotal
        
        if not isinstance(subtotal, Decimal):
            subtotal = Decimal(subtotal)

        iva = Decimal(0.16)  # 16% de IVA
        total = subtotal * (Decimal(1) + iva)  # Sumar el IVA al subtotal

        self.lbl_subtotal_valor.config(text=f"{subtotal:.2f} $")  # Muestra el subtotal
        self.lbl_total_valor.config(text=f"{total:.2f} $")  # Muestra el total con IVA

    def abrir_ventana_pago(self):
        """Abrir la ventana para el método de pago"""
        ventana_pago = tk.Toplevel(self.parent)
        ventana_pago.title("Método de Pago")
        ventana_pago.geometry("300x250")

        folio_venta = self.entry_folio.get()

         # Obtener el nombre del cliente seleccionado
        cliente_seleccionado = self.combobox_cliente.get()
        if cliente_seleccionado in self.client_data:
            cliente_id = self.client_data[cliente_seleccionado]['id']  # Asegúrate de que 'id' sea el nombre correcto de la clave
        else:
            tk.messagebox.showerror("Error", "Por favor, selecciona un cliente válido.")
            return

        metodo_pago = tk.StringVar(value="Efectivo")

        lbl_total = tk.Label(ventana_pago, text=f"Total a Pagar: {self.lbl_total_valor.cget('text')}")
        lbl_total.pack(pady=10)

        lbl_metodo_pago = tk.Label(ventana_pago, text="Selecciona el método de pago:")
        lbl_metodo_pago.pack(pady=5)

        rb_efectivo = tk.Radiobutton(ventana_pago, text="Efectivo", variable=metodo_pago, value="Efectivo", command=lambda: actualizar_entry())
        rb_tarjeta = tk.Radiobutton(ventana_pago, text="Tarjeta", variable=metodo_pago, value="Tarjeta", command=lambda: actualizar_entry())
        rb_efectivo.pack()
        rb_tarjeta.pack()

        lbl_cantidad = tk.Label(ventana_pago, text="Cantidad recibida:")
        lbl_cantidad.pack(pady=5)

        entry_cantidad = tk.Entry(ventana_pago)
        entry_cantidad.pack()

        lbl_cambio = tk.Label(ventana_pago, text="Cambio:")
        lbl_cambio.pack()

        lbl_cambio_valor = tk.Label(ventana_pago, text="0.00 $")
        lbl_cambio_valor.pack()

        # Función para actualizar el cambio
        def actualizar_cambio(*args):
            try:
                cantidad_recibida = Decimal(entry_cantidad.get())  # Obtener la cantidad ingresada
                total = Decimal(self.lbl_total_valor.cget('text').replace('$', '').strip())  # Obtener el total a pagar
                cambio = cantidad_recibida - total  # Calcular el cambio
                lbl_cambio_valor.config(text=f"{cambio:.2f} $")  # Mostrar el cambio
            except (ValueError, InvalidOperation):
                lbl_cambio_valor.config(text="0.00 $")  # Resetear el cambio si hay un error

        # Función para actualizar el campo de entrada según el método de pago
        def actualizar_entry():
            if metodo_pago.get() == "Tarjeta":
                total = self.lbl_total_valor.cget('text').replace('$', '').strip()
                entry_cantidad.delete(0, tk.END)  # Limpiar el campo
                entry_cantidad.insert(0, total)  # Asignar el total
                entry_cantidad.config(state='readonly')  # Hacer el campo read-only
                lbl_cambio_valor.config(text="0.00 $")  # Resetear el cambio
            else:
                entry_cantidad.config(state='normal')  # Hacer el campo editable
                entry_cantidad.delete(0, tk.END)  # Limpiar el campo

        # Vínculo del evento de cambio en el Entry
        entry_cantidad.bind("<KeyRelease>", actualizar_cambio)

        def aceptar_pago():
            # Obtener los datos necesarios
            folio = folio_venta
            client_id = cliente_id  
            user_id = Session.current_user_id 
            date = datetime.datetime.now().strftime('%d-%m-%Y')
            total = float(self.lbl_total_valor.cget('text').replace('$', '').strip())

            cart = Cart()

            # Agregar los productos del Treeview al carrito
            for item in self.tree.get_children():  # Itera sobre todos los elementos en el Treeview
                values = self.tree.item(item)['values']  # Obtiene los valores del item
                
                # Agregar cada producto al carrito usando el método add_item
                upc_product = values[0]  # Asumiendo que el UPC del producto está en values[0]
                quantity = values[1]      # La cantidad está en values[1]
                price = values[2]         # El precio está en values[2]
                
                cart.add_item(upc_product, quantity, price)

            # Crear instancias de los controladores
            print(cart)
            sale_controller = SaleController()
            sales_register_controller = SalesRegisterController()

            # Crear la venta
            sale_response = sale_controller.create_sale(folio, client_id, user_id, date, total)

            if sale_response['status']:
                register_response = sales_register_controller.create_sales_register(folio, cart)

                if register_response['status']:
                    tk.messagebox.showinfo("Éxito", "Venta registrada exitosamente.")
                    ventana_pago.destroy()  # Cerrar la ventana de pago
                else:
                    tk.messagebox.showerror("Error", register_response['message'])
            else:
                tk.messagebox.showerror("Error", sale_response['message'])


        btn_aceptar = tk.Button(ventana_pago, text="Aceptar", command= aceptar_pago)
        btn_aceptar.pack(pady=10)


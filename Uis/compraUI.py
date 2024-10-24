import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import random
import string
from Controllers.buy_controller import BuyController
from Controllers.buy_register_controller import BuyRegisterController
from Controllers.product_controller import ProductController
from Controllers.supplier_controller import SupplierController
from Models.cart_model import Cart
from .loginUI import Session


class Compra:
    def __init__(self, parent):
        self.parent = parent
        self.buy_controller = BuyController()
        self.buy_register_controller = BuyRegisterController()
        self.product_controller = ProductController()
        self.supplier_controller = SupplierController()
        self.cart = Cart()
        self.supplier_data = {}
        self.product_data = self.obtener_productos()
        self.setup_ui()
        self.cancelar_accion()

    def setup_ui(self):
        # Buscador
        btn_buscar = tk.Button(self.parent, text="Buscar", command=self.buscar_compra)
        btn_buscar.grid(row=0, column=0, padx=10, pady=10)
        self.entry_buscar = tk.Entry(self.parent)
        self.entry_buscar.grid(row=0, column=1, padx=10, pady=10)

        # Folio
        lbl_folio = tk.Label(self.parent, text="Folio:")
        lbl_folio.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_folio = tk.Entry(self.parent, state="readonly")
        self.entry_folio.grid(row=1, column=1, padx=10, pady=5)

        #proveedores
        lbl_supplier = tk.Label(self.parent, text="Proveedor:")
        lbl_supplier.grid(row=1, column=2, padx=10, pady=5)

        self.combobox_supplier = ttk.Combobox(self.parent, state="readonly")
        self.combobox_supplier.grid(row=1, column=3, padx=10, pady=5)

        # Cargar los nombres de los suppliers en el combobox
        self.combobox_supplier['values'] = [supplier for supplier in self.supplier_data.keys()]

        # Asociar el evento de seleccion del combobox
        self.combobox_supplier.bind("<<ComboboxSelected>>", self.activar_productos)

        # Producto
        # Producto (Combobox)
        lbl_producto = tk.Label(self.parent, text="Producto:")
        lbl_producto.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.combobox_producto = ttk.Combobox(
        self.parent, 
        values=[product['name'] for product in self.product_data.values()], 
        state="readonly"
    )
        self.combobox_producto.grid(row=2, column=1, padx=10, pady=5)
        self.combobox_producto.bind("<<ComboboxSelected>>")

        # Cantidad
        lbl_cantidad = tk.Label(self.parent, text="Cantidad:")
        lbl_cantidad.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.entry_cantidad = tk.Entry(self.parent)
        self.entry_cantidad.grid(row=3, column=1, padx=10, pady=5)

        # Botones Nuevo, Añadir y Eliminar
        self.btn_anadir = tk.Button(self.parent, text="Añadir", command=self.agregar_producto)
        self.btn_anadir.grid(row=4, column=2, padx=10, pady=5)
        self.btn_anadir.config(state="disabled")
        self.btn_eliminar = tk.Button(self.parent, text="Eliminar", command=self.eliminar_producto)
        self.btn_eliminar.grid(row=4, column=3, padx=10, pady=5)
        self.btn_eliminar.config(state="disabled")

        # Botón de Nuevo
        btn_nuevo = tk.Button(self.parent, text="Nuevo", command=self.nueva_compra)
        btn_nuevo.grid(row=10, column=0, padx=10, pady=10)

        # Botón de eliminar venta
        self.btn_eliminar_venta = tk.Button(self.parent, text="Eliminar compra", command = self.eliminar_compra)
        self.btn_eliminar_venta.grid(row=10, column=1, padx=10, pady=10)
        self.btn_eliminar_venta.config(state="disabled")  # Deshabilitado inicialmente

        # Botón de Cancelar
        self.btn_cancelar = tk.Button(self.parent, text="Cancelar", command=self.cancelar_accion)
        self.btn_cancelar.grid(row=10, column=2, padx=10, pady=10)
        self.btn_cancelar.config(state="disabled")  # Deshabilitado inicialmente

        # Treeview de productos
        self.tree = ttk.Treeview(self.parent, columns=("upc_product","nombre", "cantidad", "precio"), show="headings")
        self.tree.heading("upc_product", text="UPC")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("cantidad", text="Cantidad")
        self.tree.heading("precio", text="Precio Individual")
        self.tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

        # Subtotal y Total
        lbl_subtotal = tk.Label(self.parent, text="Subtotal:")
        lbl_subtotal.grid(row=6, column=2, padx=10, pady=5, sticky="e")
        self.lbl_subtotal_valor = tk.Label(self.parent, text="0.00 $")
        self.lbl_subtotal_valor.grid(row=6, column=3, padx=10, pady=5, sticky="w")

        self.lbl_total = tk.Label(self.parent, text="Total (IVA 16%):")
        self.lbl_total.grid(row=7, column=2, padx=10, pady=5, sticky="e")
        self.lbl_total_valor = tk.Label(self.parent, text="0.00 $")
        self.lbl_total_valor.grid(row=7, column=3, padx=10, pady=5, sticky="w")

        self.btn_pagar = tk.Button(self.parent, text="Realizar compra de productos", command=self.realizar_compra)
        self.btn_pagar.grid(row=10, column=3, padx=10, pady=10)
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
        
    def agregar_producto(self):
        """Agregar producto al carrito y actualizar el stock"""
        producto_seleccionado = self.combobox_producto.get()
        if producto_seleccionado in self.product_data:
            self.producto = self.product_data[producto_seleccionado]
            upc_product = self.producto['upc']
            cantidad = int(self.entry_cantidad.get())  # Cantidad ingresada por el usuario
            precio = self.producto['price']  # Obtenemos el precio directamente del diccionario

            # Añadir producto al carrito
            self.cart.add_item(upc_product, cantidad, precio)

            # Insertar en la tabla de la UI
            self.tree.insert("", "end", values=(upc_product, producto_seleccionado, cantidad, precio))

            # Actualizar subtotal y total
            self.actualizar_totales()
        else:
            tk.messagebox.showerror("Error", "Producto no encontrado")

    def actualizar_totales(self):
        subtotal = 0
        # Agregar los productos del Treeview al carrito
        for item in self.tree.get_children():  # Itera sobre todos los elementos en el Treeview
            values = self.tree.item(item)['values']  # Obtiene los valores del item
            cantidad = int(values[2])
            price = float(values[3])
            productos = cantidad * price
            subtotal += productos 

        # Calculamos el IVA
        iva = subtotal * 0.16
        total = subtotal + iva

        self.lbl_subtotal_valor.config(text=f"{subtotal:.2f}")
        self.lbl_total_valor.config(text=f"{total:.2f}")

        # Opcional: Si el carrito está vacío, puedes resetear los valores.
        if not self.tree:
            self.lbl_subtotal_valor.config(text="Subtotal: $0.00")
            self.lbl_subtotal_valor.config(text="Total: $0.00")

    def eliminar_producto(self):
        """Eliminar el producto seleccionado del carrito y actualizar el stock"""
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            upc_product = item['values'][0]  # UPC del producto

            # Eliminar producto del carrito
            self.cart.remove_item(upc_product)

            # Eliminar el producto de la tabla
            self.tree.delete(selected_item)

            # Actualizar subtotal y total
            self.actualizar_totales()

    def load_suppliers(self):
        """Cargar suppliers desde el controlador y llenar el combobox"""
        response = self.supplier_controller.get_all_suppliers()  # Asegúrate de que este método devuelva los proveedores
        if response['status']:
            self.supplier_data = {supplier['companyName']: supplier for supplier in response['data']}
            self.combobox_supplier['values'] = list(self.supplier_data.keys())  # Solo los nombres de los proveedores
        else:
            tk.messagebox.showerror("Error", "No se pudieron obtener los proveedores")

    def nueva_compra(self):
        """Habilitar campos y asignar un folio automáticamente."""
        self.load_suppliers()
        self.product_data = self.obtener_productos()
        self.limpiar_campos()
        self.folio = self.generar_folio()  # Asigna un nuevo folio automáticamente
        self.entry_folio.config(state="normal")
        self.entry_folio.insert(0, self.folio)
        self.entry_folio.config(state="readonly")
        self.activar_campos()
        self.btn_pagar.config(state="normal")
        self.btn_cancelar.config(state="normal")
        self.btn_eliminar.config(state="normal")
        self.btn_anadir.config(state="normal")

    def limpiar_campos(self):
        """Limpiar todos los campos de la interfaz."""
        self.entry_buscar.delete(0, tk.END)
        self.entry_folio.config(state="normal")
        self.entry_folio.delete(0, tk.END)
        self.entry_folio.config(state="readonly")
        self.combobox_supplier.set("")
        self.entry_cantidad.delete(0, tk.END)
        self.combobox_producto.set("")
        self.lbl_subtotal_valor.config(text="0.00 $")
        self.lbl_total_valor.config(text="0.00 $")
        self.tree.delete(*self.tree.get_children()) 

    def activar_campos(self):
        """Habilitar los campos para permitir la creación o edición de una venta."""
        self.combobox_supplier.config(state="readonly")

    def generar_folio(self):
        """Generar un folio aleatorio de 12 caracteres alfanuméricos"""
        caracteres = string.digits  # Letras mayúsculas y dígitos
        folio = ''.join(random.choices(caracteres, k=12))  # Folio de 12 caracteres
        return folio
    
    def cancelar_accion(self):
        """Cancelar la acción de crear o editar, y limpiar todos los campos."""
        self.limpiar_campos()
        self.desactivar_campos()
        self.btn_pagar.config(state="disabled")  # Deshabilitar el botón de Pagar
        self.btn_eliminar_venta.config(state="disabled")
        self.btn_cancelar.config(state="disabled")
        self.btn_eliminar.config(state="disabled")
        self.btn_anadir.config(state="disabled")

    def desactivar_campos(self):
        """Desactivar todos los campos para evitar cambios si no se ha iniciado una nueva venta."""
        self.combobox_supplier.config(state="disabled")
        self.entry_cantidad.config(state="disabled")
        self.combobox_producto.config(state="disabled")
        self.btn_pagar.config(state="disabled")

    def activar_productos(self, event):
        self.combobox_supplier.config(state="disabled")
        self.entry_cantidad.config(state="normal")
        self.combobox_producto.config(state="readonly")

    def realizar_compra(self):
        """Realizar la compra utilizando los controladores."""
        user_id = Session.current_user_id 
        folio = self.entry_folio.get()
        proveedor_seleccionado = self.combobox_supplier.get()
        total = float(self.lbl_total_valor.cget("text").replace("$", "").strip())
        fecha = datetime.datetime.now().strftime('%d-%m-%Y')

        # Obtener el IUP del proveedor seleccionado
        iup_supplier = self.supplier_data[proveedor_seleccionado]['iup']

        # Llamar al controlador para crear la compra
        compra_response = self.buy_controller.create_buy(folio, user_id, iup_supplier, total, fecha)
        if not compra_response['status']:
            tk.messagebox.showerror("Error", compra_response['message'])
            return

        # Agregar el registro de compra
        cart_response = self.buy_register_controller.add_buy_register(folio, self.cart)
        if not cart_response['status']:
            tk.messagebox.showerror("Error", cart_response['message'])
            return

        # Actualizar el stock de los productos comprados
        for producto in self.cart.get_items():  # Accediendo a los productos
            upc = producto.upc_product  # Acceder al atributo upc_product
            cantidad = producto.quantity  # Acceder al atributo quantity

            # Obtener el stock actual del producto
            current_stock_response = self.product_controller.get_product_by_upc(upc)
            if current_stock_response['status']:
                current_stock = current_stock_response['data']['stock']
                new_stock = current_stock + cantidad

                # Llamar al controlador para actualizar el stock
                stock_response = self.product_controller.update_stock(upc, new_stock)
                if not stock_response['status']:
                    tk.messagebox.showerror("Error", stock_response['message'])
                    return

        # Si ambos procesos fueron exitosos, mostrar un mensaje de éxito
        tk.messagebox.showinfo("Éxito", "Compra realizada exitosamente")

        # Limpiar campos después de realizar la compra
        self.cancelar_accion()


    def buscar_compra(self):
        folio = self.entry_buscar.get()  # Obtener el folio de entrada
        result = self.buy_register_controller.get_products_by_folio(folio)  # Obtener productos por folio
        result2 = self.buy_controller.get_buy_by_folio(folio)  # Obtener compra por folio

        if result2['status']:  # Si se encontró la compra
            self.btn_eliminar_venta.config(state="normal")  # Habilitar botón de eliminar
            self.btn_cancelar.config(state="normal")  # Habilitar botón de cancelar

            compra_data = result2['data']

            # Rellenar campos de la compra
            self.entry_folio.config(state='normal')
            self.entry_folio.delete(0, tk.END)
            self.entry_folio.insert(0, folio)  # Mostrar el folio
            self.entry_folio.config(state='readonly')

            self.combobox_supplier.config(state='normal')
            self.combobox_supplier.set(compra_data['iup_supplier']) 
            self.combobox_supplier.config(state='readonly')
            self.combobox_supplier.config(state='disabled')

            # Actualizar total
            self.lbl_total_valor.config(text=f"{compra_data['total']} $")

            if result['status']:  # Si se encontraron productos
                product_data = result['data']

                # Limpiar el treeview y rellenar con productos
                for item in self.tree.get_children():
                    self.tree.delete(item)

                for producto in product_data:
                    # Puedes ajustar esto según la estructura de tu producto
                    entire_product = self.product_controller.get_product_by_upc(producto['upc_product'])
                    self.tree.insert("", "end", values=(
                        producto['upc_product'], entire_product['data']['name'], producto['quantity'], entire_product['data']['price']
                    ))

        else:
            print("Error: Compra no encontrada")

    def eliminar_compra(self):
        folio = self.entry_folio.get()  # Obtener el folio de la compra a eliminar

        # Confirmar la eliminación con el usuario
        confirm = tk.messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de que deseas eliminar la compra con folio {folio}?")
        if not confirm:
            return  # Si el usuario no confirma, salir de la función

        # Obtener los productos de la compra antes de eliminar
        product_data_response = self.buy_register_controller.get_products_by_folio(folio)
        if not product_data_response['status']:
            tk.messagebox.showerror("Error", product_data_response['message'])
            return

        product_data = product_data_response['data']

        # Llamar al controlador para eliminar la compra
        response = self.buy_controller.delete_buy(folio)
        
        if response['status']:  # Si la eliminación fue exitosa
            # Actualizar el stock de los productos eliminados
            for producto in product_data:
                upc = producto['upc_product']
                cantidad = producto['quantity']
                
                # Obtener el stock actual del producto
                current_stock_response = self.product_controller.get_product_by_upc(upc)
                if current_stock_response['status']:
                    current_stock = current_stock_response['data']['stock']
                    new_stock = current_stock - cantidad
                    
                    # Llamar al controlador para actualizar el stock
                    stock_response = self.product_controller.update_stock(upc, new_stock)
                    if not stock_response['status']:
                        tk.messagebox.showerror("Error", stock_response['message'])
                        return

            tk.messagebox.showinfo("Éxito", response['message'])

            # Limpiar los campos de la interfaz
            self.cancelar_accion()

        else:
            tk.messagebox.showerror("Error", response['message']) 
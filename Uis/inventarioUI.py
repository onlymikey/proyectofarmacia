import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from Uis.productsCRUD import ProductsCRUD
from Controllers.product_controller import ProductController

class Inventario:
    def __init__(self, parent):
        self.parent = parent
        self.product_controller = ProductController()  # Inicializa el controlador de productos
        self.editing_mode = False  # Bandera para saber si estamos en modo edición
        self.entries_editing = {}  # Diccionario para almacenar los Entry temporales
        self.setup_ui()

    def setup_ui(self):
        # Frame superior (búsqueda y botones)
        frame_superior = tk.Frame(self.parent)
        frame_superior.pack(fill=tk.X, padx=10, pady=5)

        # Campo de búsqueda
        btn_buscar = tk.Button(frame_superior, text="Buscar", command=self.buscar_producto)
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

        btn_guardar = tk.Button(frame_superior, text="Guardar", command=self.guardar_ediciones)
        btn_guardar.grid(row=0, column=7, padx=5)

        btn_eliminar = tk.Button(frame_superior, text="Eliminar", command=self.eliminar)
        btn_eliminar.grid(row=0, column=8, padx=5)

        # Frame para la tabla
        frame_tabla = tk.Frame(self.parent)
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Configuración de la tabla
        cols = ('Seleccionado', 'UPC', 'Nombre', 'Stock', 'Descripción', 'Precio')
        self.tabla = ttk.Treeview(frame_tabla, columns=cols, show='headings')

        for col in cols:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, minwidth=100, width=150)
            self.tabla.column('Seleccionado', width=50)

        # Añadir la tabla a la ventana
        self.tabla.pack(fill=tk.BOTH, expand=True)

        # Asociar el evento de clic para alternar el "checkbox"
        self.tabla.bind("<Double-1>", self.alternar_checkbox)
        self.cargar_productos()

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
            messagebox.showerror("Error", response['message'])

    def buscar_producto(self):
        query = self.entry_buscar.get()
        if not query:
            messagebox.showwarning("Advertencia", "Ingrese un valor de búsqueda.")
            return
        
        # Buscar por nombre o UPC en el controlador de productos
        response = self.product_controller.get_product_by_name(query) or self.product_controller.get_product_by_upc(query)
        
        if response['status']:
            # Limpiar la tabla antes de mostrar los resultados
            self.tabla.delete(*self.tabla.get_children())
            product = response['data']
            self.tabla.insert('', 'end', values=('✖', product['upc'], product['name'], product['stock'], product['description'], product['price']))
        else:
            messagebox.showinfo("Resultado", "Producto no encontrado.")

    def editar(self):
        # Cambiar al modo edición
        self.editing_mode = True
        self.entries_editing.clear()

        for item_id in self.tabla.get_children():
            item_values = self.tabla.item(item_id, 'values')
            if item_values[0] == '✔':  # Si está seleccionado
                # Crear campos de entrada (Entry) en las celdas editables (Nombre, Descripción, Precio)
                for col_num in [2, 4, 5]:  # Las columnas 2 (Nombre), 4 (Descripción), 5 (Precio)
                    x, y, width, height = self.tabla.bbox(item_id, f'#{col_num+1}')
                    entry = tk.Entry(self.tabla)
                    entry.place(x=x, y=y, width=width, height=height)
                    entry.insert(0, item_values[col_num])
                    entry.focus()

                    # Guardar referencia del Entry y del item
                    self.entries_editing[(item_id, col_num)] = entry

    def guardar_ediciones(self):
        if not self.editing_mode:
            messagebox.showinfo("Info", "No hay ediciones pendientes.")
            return

        cambios_guardados = False

        for (item_id, col_num), entry in self.entries_editing.items():
            new_value = entry.get()
            current_values = list(self.tabla.item(item_id, 'values'))
            current_values[col_num] = new_value

            # Actualizar la tabla con el nuevo valor
            self.tabla.item(item_id, values=tuple(current_values))

            # Actualizar en la base de datos
            upc = current_values[1]  # El UPC es la segunda columna
            name = current_values[2]
            stock = int(current_values[3])  # Convertir stock a entero
            description = current_values[4]
            price = float(current_values[5])  # Convertir precio a float

            response = self.product_controller.update_product(upc, name, stock, description, price)  # Stock permanece igual
            if response['status']:
                cambios_guardados = True
                entry.destroy()  # Desactivar el Entry y volver a la vista de la tabla
            else:
                messagebox.showerror("Error", f"No se pudo actualizar el producto: {response['message']}")

        if cambios_guardados:
            messagebox.showinfo("Éxito", "Los cambios se han guardado correctamente.")

        # Salir del modo edición
        self.editing_mode = False
        self.entries_editing.clear()

    def eliminar(self):
        items_a_eliminar = []
        for item_id in self.tabla.get_children():
            item_values = self.tabla.item(item_id, 'values')
            if item_values[0] == '✔':
                upc = item_values[1]
                items_a_eliminar.append((item_id, upc))

        if not items_a_eliminar:
            messagebox.showwarning("Advertencia", "No hay productos seleccionados para eliminar.")
            return

        respuesta = messagebox.askyesno("Confirmar eliminación", f"¿Seguro que deseas eliminar {len(items_a_eliminar)} producto(s)?")
        if not respuesta:
            return

        for item_id, upc in items_a_eliminar:
            response = self.product_controller.delete_product(upc)
            if response['status']:
                self.tabla.delete(item_id)
            else:
                messagebox.showerror("Error", f"No se pudo eliminar el producto con UPC {upc}: {response['message']}")

    def nuevo(self):
        # Crear una nueva ventana (Toplevel)
        ventana_nueva = tk.Toplevel(self.parent)
        ventana_nueva.title("Gestión de Productos")
        ventana_nueva.geometry("600x400")

        # Llamar a la UI para crear un nuevo producto (CRUD)
        products_ui = ProductsCRUD(ventana_nueva)

    def cancelar(self):
        if not self.editing_mode:
            messagebox.showinfo("Info", "No hay ediciones pendientes para cancelar.")
            return

        for (item_id, col_num), entry in self.entries_editing.items():
            entry.destroy()  # Destruir el Entry
            current_values = list(self.tabla.item(item_id, 'values'))
            self.tabla.item(item_id, values=tuple(current_values))

        self.editing_mode = False
        self.entries_editing.clear()
        messagebox.showinfo("Info", "Las ediciones han sido canceladas.")

    def alternar_checkbox(self, event):
        item_id = self.tabla.focus()
        if item_id:
            current_value = self.tabla.item(item_id, 'values')[0]
            new_value = '✔' if current_value == '✖' else '✖'
            self.tabla.item(item_id, values=(new_value,) + self.tabla.item(item_id, 'values')[1:])
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from Controllers.client_controller import ClientController
from .clientesCRUD import ClientesCRUD

class Clientes:
    def __init__(self, parent):
        self.parent = parent
        self.client_controller = ClientController()  # Inicializar el controlador
        self.setup_ui()  # Llamar al método de configuración de la interfaz
        self.editing_mode = False  # Bandera para saber si estamos en modo edición
        self.entries_editing = {}  # Diccionario para almacenar los Entry temporales

    def setup_ui(self):
        # Frame superior (búsqueda y botones)
        frame_superior = tk.Frame(self.parent)
        frame_superior.pack(fill=tk.X, padx=10, pady=5)

        # Campo de búsqueda
        btn_buscar = tk.Button(frame_superior, text="Buscar")
        btn_buscar.grid(row=0, column=0, padx=10, pady=10)
        self.entry_buscar = tk.Entry(frame_superior)
        self.entry_buscar.grid(row=0, column=1, padx=5)

        # Botones principales
        btn_nuevo = tk.Button(frame_superior, text="CRUD Clientes", command=self.nuevo)
        btn_nuevo.grid(row=0, column=2, padx=5)

        btn_actualizar = tk.Button(frame_superior, text="Actualizar", command=self.cargar_clientes)
        btn_actualizar.grid(row=0, column=3, padx=5)

        btn_cancelar = tk.Button(frame_superior, text="Cancelar", command=self.cancelar)
        btn_cancelar.grid(row=0, column=4, padx=5)

        btn_editar = tk.Button(frame_superior, text="Editar", command=self.editar)
        btn_editar.grid(row=0, column=5, padx=5)

        btn_guardar = tk.Button(frame_superior, text="Guardar", command=self.guardar_ediciones)
        btn_guardar.grid(row=0, column=6, padx=5)

        btn_eliminar = tk.Button(frame_superior, text="Eliminar", command=self.eliminar)
        btn_eliminar.grid(row=0, column=7, padx=5)

        # Frame para la tabla
        frame_tabla = tk.Frame(self.parent)
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Configuración de la tabla
        cols = ('Seleccionado', 'ID', 'Nombre', 'Email', 'Teléfono', 'Puntos')
        self.tabla = ttk.Treeview(frame_tabla, columns=cols, show='headings')

        for col in cols:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, minwidth=100, width=150)
            self.tabla.column('Seleccionado', width=50)  # Ajustar ancho para la columna de selección
            self.tabla.column('ID', width=50)

        # Añadir la tabla a la ventana
        self.tabla.pack(fill=tk.BOTH, expand=True)

        # Asociar el evento de clic para alternar el "checkbox"
        self.tabla.bind("<Double-1>", self.alternar_checkbox)
        self.cargar_clientes()

    def cargar_clientes(self):
        # Limpiar la tabla antes de cargar nuevos datos
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        # Obtener los clientes del controlador
        response = self.client_controller.get_all_clients()

        if response['status']:
            for client in response['data']:
                self.tabla.insert('', 'end', values=('✖', client['id'], client['name'], client['email'], client['phone'], client['points']))
        else:
            print("Error:", response['message'])  # Puedes mostrar un mensaje en la UI si lo prefieres

    def editar(self):
        # Cambiar al modo edición
        self.editing_mode = True
        self.entries_editing.clear()  # Limpiamos los Entry anteriores

        # Recoger los elementos que están seleccionados con '✔'
        for item_id in self.tabla.get_children():
            item_values = self.tabla.item(item_id, 'values')
            if item_values[0] == '✔':  # Si está seleccionado
                # Crear campos de entrada (Entry) en las celdas editables (Nombre, Email, Teléfono)
                for col_num in range(2, 5):  # Las columnas 2 (Nombre), 3 (Email), 4 (Teléfono) son editables
                    x, y, width, height = self.tabla.bbox(item_id, f'#{col_num+1}')
                    entry = tk.Entry(self.tabla)
                    entry.place(x=x, y=y, width=width, height=height)
                    entry.insert(0, item_values[col_num])  # Insertar el valor actual
                    entry.focus()

                    # Guardar referencia del Entry y del item
                    self.entries_editing[(item_id, col_num)] = entry

    def guardar_ediciones(self):
        if not self.editing_mode:
            messagebox.showinfo("Info", "No hay ediciones pendientes.")
            return

        cambios_guardados = False  # Variable para saber si se guardó algún cambio

        # Para cada Entry activo, obtener el nuevo valor y actualizar la tabla y la base de datos
        for (item_id, col_num), entry in self.entries_editing.items():
            new_value = entry.get()
            current_values = list(self.tabla.item(item_id, 'values'))
            current_values[col_num] = new_value

            # Actualizar la tabla con el nuevo valor
            self.tabla.item(item_id, values=tuple(current_values))

            # Actualizar la base de datos con los nuevos datos
            client_id = current_values[1]  # El ID del cliente es la segunda columna
            name = current_values[2]
            email = current_values[3]
            phone = current_values[4]
            points = current_values[5]

            response = self.client_controller.update_client(client_id, name, email, phone, points)
            if response['status']:
                cambios_guardados = True
                entry.destroy()  # Desactivar el Entry y volver a la vista de la tabla
            else:
                messagebox.showerror("Error", f"No se pudo actualizar el cliente: {response['message']}")

        # Si se guardaron cambios, mostramos un mensaje de éxito
        if cambios_guardados:
            messagebox.showinfo("Éxito", "Los cambios se han guardado correctamente.")

        # Salir del modo edición
        self.editing_mode = False
        self.entries_editing.clear()  # Limpiar las entradas después de guardar

    def eliminar(self):
        # Recoger los elementos que están seleccionados con '✔'
        items_a_eliminar = []
        for item_id in self.tabla.get_children():
            item_values = self.tabla.item(item_id, 'values')
            if item_values[0] == '✔':  # Si está seleccionado
                client_id = item_values[1]  # El ID del cliente es la segunda columna
                items_a_eliminar.append((item_id, client_id))

        if not items_a_eliminar:
            messagebox.showwarning("Advertencia", "No hay clientes seleccionados para eliminar.")
            return

        # Confirmar la eliminación
        respuesta = messagebox.askyesno("Confirmar eliminación", f"¿Seguro que deseas eliminar {len(items_a_eliminar)} cliente(s)?")
        if not respuesta:
            return

        # Intentar eliminar de la base de datos
        for item_id, client_id in items_a_eliminar:
            response = self.client_controller.delete_client(client_id)
            if response['status']:
                self.tabla.delete(item_id)  # Eliminar de la tabla si la eliminación en la BD fue exitosa
            else:
                messagebox.showerror("Error", f"No se pudo eliminar el cliente con ID {client_id}: {response['message']}")

    def nuevo(self):
        # Crear una nueva ventana (Toplevel)
        ventana_nueva = tk.Toplevel(self.parent)
        ventana_nueva.title("Gestión de Clientes")
        ventana_nueva.geometry("600x400")  # Ajusta el tamaño de la ventana

        # Cargar la interfaz de clientes pasando el controlador también
        clientes_ui = ClientesCRUD(ventana_nueva, self.client_controller)

    def cancelar(self):
        if not self.editing_mode:
            messagebox.showinfo("Info", "No hay ediciones pendientes para cancelar.")
            return

        # Destruir todos los Entry que están activos y volver a la vista original
        for (item_id, col_num), entry in self.entries_editing.items():
            entry.destroy()  # Destruir el Entry
            current_values = list(self.tabla.item(item_id, 'values'))
            
            # Reiniciar los valores de la tabla a su estado original
            self.tabla.item(item_id, values=tuple(current_values))

        # Salir del modo edición
        self.editing_mode = False
        self.entries_editing.clear()  # Limpiar las entradas editables
        messagebox.showinfo("Info", "Las ediciones han sido canceladas.")

    def alternar_checkbox(self, event):
        # Obtener el item seleccionado
        item_id = self.tabla.focus()
        
        # Verificar que hay un item seleccionado
        if item_id:
            current_value = self.tabla.item(item_id, 'values')[0]
            
            # Alternar entre '✔' y '✖'
            new_value = '✔' if current_value == '✖' else '✖'
            self.tabla.item(item_id, values=(new_value,) + self.tabla.item(item_id, 'values')[1:])

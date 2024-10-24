import tkinter as tk
from tkinter import ttk, messagebox
from Controllers.client_controller import ClientController


class ClientesCRUD:
    def __init__(self, parent, client_controller):
        self.parent = parent
        self.client_controller = client_controller  # Instancia del controlador de clientes
        self.crear_widgets_clients()


    def crear_widgets_clients(self):
        clients_frame = tk.Frame(self.parent)
        clients_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Label(clients_frame, text="Ingrese ID del usuario:").grid(row=0, column=0, padx=10, pady=10)
        self.user_id_entry = ttk.Entry(clients_frame)
        self.user_id_entry.grid(row=0, column=1, padx=10, pady=10)
        ttk.Button(clients_frame, text="Buscar", command=self.buscar_user).grid(row=0, column=2, padx=10, pady=10)

        ttk.Label(clients_frame, text="ID:").grid(row=1, column=0, padx=10, pady=10)
        self.id_entry = ttk.Entry(clients_frame, state='readonly')
        self.id_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(clients_frame, text="Nombre:").grid(row=2, column=0, padx=10, pady=10)
        self.nombre_entry = ttk.Entry(clients_frame)
        self.nombre_entry.grid(row=2, column=1, padx=10, pady=10)

        ttk.Label(clients_frame, text="Telefono:").grid(row=3, column=0, padx=10, pady=10)
        self.telefono_entry = ttk.Entry(clients_frame)
        self.telefono_entry.grid(row=3, column=1, padx=10, pady=10)

        ttk.Label(clients_frame, text="Email:").grid(row=4, column=0, padx=10, pady=10)
        self.email_entry = ttk.Entry(clients_frame)
        self.email_entry.grid(row=4, column=1, padx=10, pady=10)
    
        ttk.Label(clients_frame, text="puntos:").grid(row=5, column=0, padx=10, pady=10)
        self.puntos_entry = ttk.Entry(clients_frame, state = 'disabled')
        self.puntos_entry.grid(row=5, column=1, padx=10, pady=10)

        ttk.Button(clients_frame, text="Nuevo", command=self.nuevo_cliente).grid(row=6, column=0, padx=10, pady=10)
        ttk.Button(clients_frame, text="Guardar", command=self.guardar_cliente).grid(row=6, column=1, padx=10, pady=10)
        ttk.Button(clients_frame, text="Editar", command=self.editar_user).grid(row=6, column=2, padx=10, pady=10)
        ttk.Button(clients_frame, text="Eliminar", command=self.eliminar_cliente).grid(row=6, column=3, padx=10, pady=10)

    # Función para obtener el siguiente ID disponible en la tabla
    def obtener_siguiente_id(self):
        siguiente_id = self.client_controller.get_next_client_id()  # Llamada al método del controlador
        return siguiente_id


    def editar_user(self):
        self.modo_edicion_user = True
        self.user_id_entry.config(state='normal')
        messagebox.showinfo("Modo Edición", "Modo de edición activado. Realice los cambios y presione 'Guardar'.")

    def buscar_user(self):
        user_id = self.user_id_entry.get()  # Obtén el ID del usuario del campo de entrada
        if user_id:
            # Llama al método del controlador para buscar el cliente
            result = self.client_controller.get_client_by_id(int(user_id))
            if result['status']:
                # Llenar los campos con los datos del cliente
                self.limpiar_campos_cliente(result['data'])
            else:
                messagebox.showerror("Error", result['message'])
                self.user_id_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Advertencia", "Por favor ingrese un ID de usuario.")

    def limpiar_campos_cliente(self, user=None):
        if user:  # Si se proporciona un usuario, llenamos los campos
            self.id_entry.config(state='normal')
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, user['id'])  # Asumiendo que 'id' es el atributo del cliente
            self.id_entry.config(state='readonly')
            
            self.nombre_entry.delete(0, tk.END)
            self.nombre_entry.insert(0, user['name'])  # Asumiendo que 'name' es el atributo del cliente

            self.telefono_entry.delete(0, tk.END)
            self.telefono_entry.insert(0, user['phone'])  # Asumiendo que 'phone' es el atributo del cliente

            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, user['email'])  # Asumiendo que 'email' es el atributo del cliente

            self.puntos_entry.config(state='normal')
            self.puntos_entry.delete(0, tk.END)
            self.puntos_entry.insert(0, user['points'])
            self.puntos_entry.config(state='disabled')

        else:  # Si no hay usuario, simplemente limpiamos todos los campos
            self.id_entry.config(state='normal')
            self.id_entry.delete(0, tk.END)
            self.id_entry.config(state='readonly')

            self.nombre_entry.delete(0, tk.END)
            self.telefono_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)

            self.puntos_entry.config(state='normal')
            self.puntos_entry.delete(0, tk.END)
            self.puntos_entry.config(state='disabled')


    def nuevo_cliente(self):
        self.limpiar_campos_cliente()  # Limpiar todos los campos de entrada
        siguiente_id = self.client_controller.get_next_client_id()  # Obtener el siguiente ID de cliente
        self.id_entry.config(state='normal')  # Permitir modificar el campo de ID temporalmente
        self.id_entry.delete(0, tk.END)  # Limpiar el campo de ID
        self.id_entry.insert(0, siguiente_id)  # Colocar el siguiente ID en el campo de ID
        self.id_entry.config(state='readonly')  # Marcar el campo de ID como readonly


    def guardar_cliente(self):
        """Guarda un nuevo cliente o actualiza uno existente."""
        client_id_act = self.user_id_entry.get()
        client_id = self.id_entry.get()  # Obtiene el ID del cliente
        name = self.nombre_entry.get()
        phone = self.telefono_entry.get()
        email = self.email_entry.get()
        points = self.puntos_entry.get()


        if client_id_act and client_id_act.isdigit():  # Comprobamos si hay un ID válido
            # Si el campo ID tiene un valor, estamos actualizando un cliente existente
            resultado = self.client_controller.update_client(int(client_id), name, email, phone, points)
        else:
            # Si no hay ID, estamos creando un nuevo cliente
            resultado = self.client_controller.create_client(name, email, phone)

        if resultado['status']:
            messagebox.showinfo("Éxito", resultado['message'])
            self.limpiar_campos_cliente()
        else:
            messagebox.showerror("Error", resultado['message'])


    def eliminar_cliente(self):
        """Elimina un cliente por ID ingresado."""
        client_id = self.id_entry.get()
        if not client_id:
            messagebox.showerror("Error", "Debes seleccionar un cliente para eliminar.")
            return

        confirm = messagebox.askyesno("Confirmación", "¿Estás seguro de que deseas eliminar este cliente?")
        if confirm:
            resultado = self.client_controller.delete_client(int(client_id))
            if resultado['status']:
                messagebox.showinfo("Éxito", resultado['message'])
                self.limpiar_campos_cliente()
            else:
                messagebox.showerror("Error", resultado['message'])
                
    def limpiar_campos_user(self):
        self.id_entry.config(state='normal')
        self.id_entry.delete(0, tk.END)
        self.id_entry.config(state='readonly')

        self.user_id_entry.delete(0, tk.END)
        self.nombre_entry.delete(0, tk.END)
        self.telefono_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)

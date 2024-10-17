import tkinter as tk
from tkinter import ttk, messagebox
from Controllers.user_controller import UserController  # Importar el controlador

class Empleados:

    def __init__(self, parent):
        self.parent = parent
        self.user_controller = UserController()  # Crear una instancia del controlador
        self.crear_widgets_users()

    def crear_widgets_users(self):
        users_frame = tk.Frame(self.parent)
        users_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Label(users_frame, text="Ingrese ID del usuario:").grid(row=0, column=0, padx=10, pady=10)
        self.user_id_entry = ttk.Entry(users_frame)
        self.user_id_entry.grid(row=0, column=1, padx=10, pady=10)
        ttk.Button(users_frame, text="Buscar", command=self.buscar_user).grid(row=0, column=2, padx=10, pady=10)

        ttk.Label(users_frame, text="ID:").grid(row=1, column=0, padx=10, pady=10)
        self.id_entry = ttk.Entry(users_frame, state='readonly')
        self.id_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(users_frame, text="Nombre:").grid(row=2, column=0, padx=10, pady=10)
        self.nombre_entry = ttk.Entry(users_frame)
        self.nombre_entry.grid(row=2, column=1, padx=10, pady=10)

        ttk.Label(users_frame, text="Username:").grid(row=3, column=0, padx=10, pady=10)
        self.username_entry = ttk.Entry(users_frame)
        self.username_entry.grid(row=3, column=1, padx=10, pady=10)

        ttk.Label(users_frame, text="Password:").grid(row=4, column=0, padx=10, pady=10)
        self.password_entry = ttk.Entry(users_frame, show="*")
        self.password_entry.grid(row=4, column=1, padx=10, pady=10)

        ttk.Label(users_frame, text="Perfil:").grid(row=2, column=2, padx=10, pady=10)
        self.perfil_entry = ttk.Combobox(users_frame, values=["Admin", "Gerente", "Cajero"], state='readonly')
        self.perfil_entry.grid(row=2, column=3, padx=10, pady=10)

        ttk.Button(users_frame, text="Nuevo", command=self.nuevo_user).grid(row=5, column=0, padx=10, pady=10)
        ttk.Button(users_frame, text="Guardar", command=self.guardar_user).grid(row=5, column=1, padx=10, pady=10)
        ttk.Button(users_frame, text="Editar", command=self.editar_user).grid(row=5, column=2, padx=10, pady=10)
        ttk.Button(users_frame, text="Eliminar", command=self.eliminar_user).grid(row=5, column=3, padx=10, pady=10)

    # Función para obtener el siguiente ID disponible en la tabla
    def get_next_user_id(self) -> int:
        """Obtiene el siguiente id de usuario"""
        next_user_id = self.user_service.get_next_user_id()
        return next_user_id


    def editar_user(self):
        self.modo_edicion_user = True
        self.user_id_entry.config(state='normal')
        messagebox.showinfo("Modo Edición", "Modo de edición activado. Realice los cambios y presione 'Guardar'.")

    def buscar_user(self):
        user_id = self.user_id_entry.get()
        if user_id.isdigit():
            result = self.user_controller.get_user_by_id(int(user_id))
            print(result)
            if result['status']:
                self.llenar_campos_user(result['data'])
            else:
                messagebox.showerror("Error", result['message'])
        else:
            messagebox.showerror("Error", "El ID del usuario debe ser un número válido.")
        


    def llenar_campos_user(self, user):
        self.id_entry.config(state='normal')
        self.id_entry.delete(0, tk.END)
        self.id_entry.insert(0, user.get('id', ''))  # Asumimos que el campo devuelto es 'user_id'
        self.id_entry.config(state='readonly')

        self.nombre_entry.delete(0, tk.END)
        self.nombre_entry.insert(0, user.get('name', ''))

        self.username_entry.delete(0, tk.END)
        self.username_entry.insert(0, user.get('username', ''))

        self.password_entry.delete(0, tk.END) 
        self.password_entry.insert(0, user.get('password', ''))
        self.perfil_entry.set(user.get('profile', ''))  # Asumimos que el campo es 'profile'


    def nuevo_user(self):
        self.limpiar_campos_user()  # Limpia todos los campos
        siguiente_id = self.user_controller.get_next_user_id()  # Obtén el siguiente ID
        self.id_entry.config(state='normal')
        self.id_entry.insert(0, siguiente_id)  # Coloca el siguiente ID en el campo
        self.id_entry.config(state='readonly')  # Lo marcas como readonly para evitar ediciones


    def guardar_user(self):
        name = self.nombre_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()  # Recuerda, no deberías manejar contraseñas en texto plano.
        profile = self.perfil_entry.get()

        if not name or not username or not password or not profile:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        user_id = self.user_id_entry.get()
        if user_id:  # Si hay un ID, actualizamos
            result = self.user_controller.update_user(int(user_id), name, username, password, profile)
        else:  # Si no hay ID, creamos un nuevo usuario
            result = self.user_controller.create_user(name, username, password, profile)

        if result['status']:
            messagebox.showinfo("Éxito", result['message'])
            self.limpiar_campos_user()
        else:
            messagebox.showerror("Error", result['message'])


    def eliminar_user(self):
        user_id = self.id_entry.get()
        if not user_id:
            messagebox.showerror("Error", "Seleccione un usuario para eliminar.")
            return

        result = self.user_controller.delete_user(int(user_id))
        if result['status']:
            messagebox.showinfo("Éxito", result['message'])
            self.limpiar_campos_user()
        else:
            messagebox.showerror("Error", result['message'])


    def limpiar_campos_user(self):
        self.id_entry.config(state='normal')
        self.id_entry.delete(0, tk.END)
        self.id_entry.config(state='readonly')

        self.nombre_entry.delete(0, tk.END)
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.perfil_entry.set('') 

import tkinter as tk
from tkinter import ttk, messagebox

class Empleados:
    def __init__(self, parent):
        self.parent = parent
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
        self.perfil_entry = ttk.Combobox(users_frame, values=["Admin", "Secretario", "Mecanico"], state='readonly')
        self.perfil_entry.grid(row=2, column=3, padx=10, pady=10)

        ttk.Button(users_frame, text="Nuevo", command=self.nuevo_user).grid(row=5, column=0, padx=10, pady=10)
        ttk.Button(users_frame, text="Guardar", command=self.guardar_user).grid(row=5, column=1, padx=10, pady=10)
        ttk.Button(users_frame, text="Editar", command=self.editar_user).grid(row=5, column=2, padx=10, pady=10)
        ttk.Button(users_frame, text="Eliminar", command=self.eliminar_user).grid(row=5, column=3, padx=10, pady=10)

    # Función para obtener el siguiente ID disponible en la tabla
    def obtener_siguiente_id(self):
        pass

    def editar_user(self):
        self.modo_edicion_user = True
        self.user_id_entry.config(state='normal')
        messagebox.showinfo("Modo Edición", "Modo de edición activado. Realice los cambios y presione 'Guardar'.")

    def buscar_user(self):
        pass

    def llenar_campos_user(self, user):
        pass

    def nuevo_user(self):
        self.limpiar_campos_user()

    def guardar_user(self):
        pass

    def eliminar_user(self):
        pass

    def limpiar_campos_user(self):
        self.id_entry.config(state='normal')
        self.id_entry.delete(0, tk.END)
        self.id_entry.config(state='readonly')

        self.nombre_entry.delete(0, tk.END)
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.perfil_entry.set('') 

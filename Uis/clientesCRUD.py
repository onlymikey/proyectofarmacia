import tkinter as tk
from tkinter import ttk, messagebox

class ClientesCRUD:
    def __init__(self, parent):
        self.parent = parent
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
        self.email_entry = ttk.Entry(clients_frame, show="*")
        self.email_entry.grid(row=4, column=1, padx=10, pady=10)

        ttk.Button(clients_frame, text="Nuevo", command=self.nuevo_user).grid(row=5, column=0, padx=10, pady=10)
        ttk.Button(clients_frame, text="Guardar", command=self.guardar_user).grid(row=5, column=1, padx=10, pady=10)
        ttk.Button(clients_frame, text="Editar", command=self.editar_user).grid(row=5, column=2, padx=10, pady=10)
        ttk.Button(clients_frame, text="Eliminar", command=self.eliminar_user).grid(row=5, column=3, padx=10, pady=10)

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
        self.telefono_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)

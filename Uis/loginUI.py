import tkinter as tk
from tkinter import messagebox

from Controllers.user_controller import UserController

class Session:
    """Clase para almacenar información de sesión del usuario."""
    current_user_id = None
    current_username = None

class LoginUI:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.user_controller = UserController()

        # Crear interfaz de login
        self.frame = tk.Frame(self.master)
        self.frame.pack(pady=50)

        tk.Label(self.frame, text="Username:").grid(row=0, column=0, padx=10, pady=10)
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.grid(row=0, column=1)

        tk.Label(self.frame, text="Password:").grid(row=1, column=0, padx=10, pady=10)
        self.password_entry = tk.Entry(self.frame, show='*')
        self.password_entry.grid(row=1, column=1)

        tk.Button(self.frame, text="Login", command=self.login).grid(row=2, columnspan=2, pady=20)

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        result = self.user_controller.verify_user(username, password)

        if result['status']:
            user = result['data']
            Session.current_user_id = user['id']
            messagebox.showinfo("Login Exitoso", f"Bienvenido {user['name']} ({user['profile']})")
            self.master.destroy()  # Cierra la ventana de login

            # Llamar a la función de la app principal pasando el perfil
            self.app.init_app(user['profile'])

        else:
            messagebox.showerror("Error de Login", result['message'])

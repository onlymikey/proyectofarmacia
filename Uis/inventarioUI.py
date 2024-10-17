import tkinter as tk
from tkinter import ttk

class Inventario:
    def __init__(self, parent):
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        # Frame superior (búsqueda y botones)
        frame_superior = tk.Frame(self.parent)
        frame_superior.pack(fill=tk.X, padx=10, pady=5)

        # Campo de búsqueda
        btn_buscar = tk.Button(frame_superior, text="Buscar")
        btn_buscar.grid(row=0, column=0, padx=10, pady=10)
        self.entry_buscar = tk.Entry(frame_superior)
        self.entry_buscar.grid(row=0, column=1, padx=5)

        btn_salvar = tk.Button(frame_superior, text="Salvar", command=self.salvar)
        btn_salvar.grid(row=0, column=3, padx=5)

        btn_cancelar = tk.Button(frame_superior, text="Cancelar", command=self.cancelar)
        btn_cancelar.grid(row=0, column=4, padx=5)

        btn_editar = tk.Button(frame_superior, text="Editar", command=self.editar)
        btn_editar.grid(row=0, column=5, padx=5)

        btn_eliminar = tk.Button(frame_superior, text="Eliminar", command=self.eliminar)
        btn_eliminar.grid(row=0, column=6, padx=5)

        # Frame para la tabla
        frame_tabla = tk.Frame(self.parent)
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Configuración de la tabla
        cols = ('Seleccionado', 'Folio', 'Nombre', 'Stock', 'Precio')
        self.tabla = ttk.Treeview(frame_tabla, columns=cols, show='headings')

        for col in cols:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, minwidth=100, width=150)
            self.tabla.column('Seleccionado', width=50)  # Ajustar ancho para la columna de selección
            self.tabla.column('Folio', width=50)

        # Datos de ejemplo para la tabla con checkboxes simulados
        datos = [
            ('✖', 1, 'Producto 1', '99', 'xxx'),
            ('✖', 2, 'Producto 2', '99', 'xxx'),
            ('✖', 3, 'Producto 3', '99', 'xxx'),
            ('✖', 4, 'Producto 4', '99', 'xxx'),
        ]

        for dato in datos:
            self.tabla.insert("", "end", values=dato)

        # Añadir la tabla a la ventana
        self.tabla.pack(fill=tk.BOTH, expand=True)

        # Asociar el evento de clic para alternar el "checkbox"
        self.tabla.bind("<Double-1>", self.alternar_checkbox)

    def salvar(self):
        pass

    def cancelar(self):
        pass
    def editar(self):
        pass

    def eliminar(self):
        pass

    def alternar_checkbox(self, event):
        # Obtener el item seleccionado
        item_id = self.tabla.focus()
        
        # Verificar que hay un item seleccionado
        if item_id:  
            current_value = self.tabla.item(item_id, 'values')[0] 
            
            # Alternar entre '✔' y '✖'
            new_value = '✔' if current_value == '✖' else '✖'
            self.tabla.item(item_id, values=(new_value,) + self.tabla.item(item_id, 'values')[1:])


# Sofía Veldman Paniego
# Mohamed Boulman Mokhlis
# Juan del Junco Sampol

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Importa el módulo ttk para usar Combobox
from GestorBaseDatos import *
from Compra import compra

class InterfazCentroBuceo(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Centro de Buceo")
        self.geometry("370x260")

        # Crear una instancia de GestorBasesDatos
        self.gestor = GestorBasesDatos()
        self.paises_disponibles = self.gestor.obtener_paises_Buceo()

        # Variables de entrada
        self.var_equipo = tk.StringVar()
        self.var_pais = tk.StringVar(value="ESPAÑA")
        self.var_talla = tk.StringVar()
        self.var_cantidad = tk.IntVar()
        self.var_precio_compra = tk.DoubleVar()

        # Lista de productos
        productos = [
            "Traje (Neopreno)",
            "Chaleco (BCD)",
            "Regulador",
            "Tanque",
            "Máscara",
            "Aletas",
            "Cinturón",
            "Ordenador",
            "Manómetro",
            "Cuchillo",
            "Silbato"
        ]

        # Lista de tallas
        tallas = ['XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL']

        # Etiquetas y campos de entrada
        tk.Label(self, text="Equipo de Buceo:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        ttk.Combobox(self, textvariable=self.var_equipo, values=productos).grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        tk.Label(self, text="País:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        ttk.Combobox(self, textvariable=self.var_pais, values=self.paises_disponibles).grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        tk.Label(self, text="Talla:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        ttk.Combobox(self, textvariable=self.var_talla, values=tallas).grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        self.var_talla.set("XXS")# "XXS" como valor inicial

        tk.Label(self, text="Cantidad:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        tk.Entry(self, textvariable=self.var_cantidad, validate="key", validatecommand=(self.register(self.Validacion), "%P")).grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        tk.Label(self, text="Precio de Compra:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        tk.Entry(self, textvariable=self.var_precio_compra, validate="key", validatecommand=(self.register(self.Validacion_precio), "%P")).grid(row=4, column=1, padx=10, pady=5, sticky="ew")

        self.var_equipo.set("Traje (Neopreno)")  # "Traje de Buceo (Neopreno)" como valor inicial

        # Botones
        tk.Button(self, text="Agregar", command=self.agregar_compra_Buceo, width=8).grid(row=5, column=0, columnspan=1, pady=(10, 5))
        tk.Button(self, text="Limpiar", command=self.limpiar_campos, width=8).grid(row=5, column=1, columnspan=1, pady=(10, 5), padx=(5, 0))
        tk.Button(self, text="Salir", command=self.salir, width=8).grid(row=5, column=2, columnspan=1, pady=(10, 5), padx=(5, 0))

    def agregar_compra_Buceo(self):
        equipo = self.var_equipo.get()
        pais = self.var_pais.get()
        talla = self.var_talla.get()
        cantidad = self.var_cantidad.get()
        precio_compra = self.var_precio_compra.get()

        # método de GestorBasesDatos para agregar la compra
        self.gestor.agregar_compra_Buceo(compra(equipo, pais, talla, cantidad, precio_compra))
        messagebox.showinfo("Alta compra Buceo", f"Actualizado el equipo {equipo}...")

    def limpiar_campos(self):
        # Limpiar todos los campos de entrada
        self.var_equipo.set("")
        self.var_pais.set("ESPAÑA")
        self.var_talla.set("XXS")
        self.var_cantidad.set("")
        self.var_precio_compra.set("")

    def salir(self):
        self.destroy()

    def Validacion(self, Valor_nuevo):
        try:
            if Valor_nuevo:
                int(Valor_nuevo)
            return True
        except ValueError:
            return False

    def Validacion_precio(self, Valor_nuevo):
        try:
            if Valor_nuevo:
                float(Valor_nuevo)
            return True
        except ValueError:
            return False

if __name__ == "__main__":

    app = InterfazCentroBuceo()
    app.mainloop()

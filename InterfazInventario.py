# Sofía Veldman Paniego
# Mohamed Boulman Mokhlis
# Juan del Junco Sampol

import tkinter as tk
from tkinter import ttk, messagebox
from GestorBaseDatos import *

class Inventario(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Inventario")
        self.geometry("450x450")  
        self.pais_var, self.talla_var, self.actividad_var = tk.StringVar(), tk.StringVar(), tk.StringVar()
        self.gestor = GestorBasesDatos()
        self.configurar_interfaz()

    def configurar_interfaz(self):
        tk.Label(self, text="País:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        tk.Label(self, text="Talla:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        tk.Label(self, text="Actividad:").grid(row=2, column=0, padx=10, pady=10, sticky="w")

        # Inicializa el Combobox de países
        paises = sorted(list(set(self.gestor.obtener_paises_Buceo() + self.gestor.obtener_paises_Esqui())))
        self.pais_combobox = ttk.Combobox(self, textvariable=self.pais_var, values=paises, state="readonly")
        self.pais_combobox.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
         
        self.pais_var.set('ESPAÑA')#'ESPAÑA' como el país por defecto

        # Lista de tallas
        tallas = ['XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL']
        ttk.Combobox(self, textvariable=self.talla_var, values=tallas).grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.talla_var.set('M') #'M' como la talla por defecto

        # Lista de actividades
        actividades = ["BUCEO", "ESQUI"]
        ttk.Combobox(self, textvariable=self.actividad_var, values=actividades).grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        self.actividad_var.set('BUCEO') # 'BUCEO' como la actividad por defecto

        ttk.Button(self, text="Consultar", command=self.realizar_consulta).grid(row=3, column=0, columnspan=2, pady=10)

        # Los resultados nos lo devuelve en las columnas del Treeview
        self.resultados_treeview = ttk.Treeview(self, columns=("Equipo", "Cantidad Disponible"))
        self.resultados_treeview.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.resultados_treeview.yview)
        scrollbar.grid(row=4, column=2, sticky="ns")
        self.resultados_treeview.configure(yscrollcommand=scrollbar.set)

        # Ajusta la alineación de las columnas
        self.resultados_treeview.heading("#1", text="Equipo")
        self.resultados_treeview.heading("#2", text="Cantidad Disponible")

        self.resultados_treeview.column("#0", anchor="w")
        # Oculta la columna de identificación
        self.resultados_treeview.column("#0", width=0, stretch=tk.NO)

        # Cambia el texto de la etiqueta del Treeview
        self.resultados_treeview.heading("#0", text="Cantidad Disponible")

    def realizar_consulta(self):
        pais, talla, actividad = self.pais_var.get(), self.talla_var.get(), self.actividad_var.get()
        resultados = self.gestor.consultar_cantidad_disponible(pais, talla, actividad)

        # Limpiamos la tabla antes de agregar nuevos resultados
        for item in self.resultados_treeview.get_children():
            self.resultados_treeview.delete(item)

        # Si no se encuentran resultados, mostramos un mensaje de advertencia
        if not resultados:
            messagebox.showwarning("Advertencia", "No se encontraron resultados para la consulta.")
            return

        # Insertamos los resultados en la tabla
        for equipo, cantidad in resultados.items():
            self.resultados_treeview.insert("", "end", values=(equipo, cantidad))

if __name__ == "__main__":
    app = Inventario()
    app.mainloop()

"""Alta (compra) y baja de material en los centros de buceo y de esquí."""

import tkinter as tk
from tkinter import messagebox

from ..config import BUCEO, EQUIPOS, TALLAS
from ..gestor import GestorBasesDatos
from ..modelos import Compra
from .comun import campo, combo


class VentanaCompra(tk.Toplevel):
    def __init__(self, master, gestor: GestorBasesDatos, actividad: str, baja: bool = False):
        super().__init__(master)
        self.gestor = gestor
        self.actividad = actividad
        self.baja = baja
        centro = "Centro de buceo" if actividad == BUCEO else "Centro de esquí"
        self.title(f"{centro} · {'baja' if baja else 'alta'} de material")
        self.resizable(False, False)

        self.equipo = campo(self, 0, "Equipo:", combo(self, EQUIPOS[actividad]))
        paises = gestor.paises(actividad)
        self.pais = campo(self, 1, "País:", combo(self, paises, ancho=30,
                                                   inicial="ESPAÑA" if "ESPAÑA" in paises else None))
        self.talla = campo(self, 2, "Talla:", combo(self, TALLAS, inicial="M"))
        self.cantidad = campo(self, 3, "Cantidad:", tk.Entry(self))
        if not baja:
            self.precio = campo(self, 4, "Precio de compra (€/u.):", tk.Entry(self))
        botones = tk.Frame(self)
        botones.grid(row=5, column=0, columnspan=2, pady=10)
        tk.Button(botones, text="Dar de baja" if baja else "Agregar", width=10,
                  command=self.registrar).pack(side=tk.LEFT, padx=5)
        tk.Button(botones, text="Limpiar", width=10, command=self.limpiar).pack(side=tk.LEFT, padx=5)
        tk.Button(botones, text="Salir", width=10, command=self.destroy).pack(side=tk.LEFT, padx=5)

    def registrar(self):
        try:
            cantidad = int(self.cantidad.get())
            if cantidad <= 0:
                raise ValueError
            precio = 0.0 if self.baja else float(self.precio.get().replace(",", "."))
            if precio < 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Revisa los datos",
                                   "La cantidad debe ser un entero positivo y el precio un número.",
                                   parent=self)
            return
        compra = Compra(self.actividad, self.equipo.get(), self.pais.get(), self.talla.get(),
                        -cantidad if self.baja else cantidad, precio)
        try:
            self.gestor.registrar_compra(compra)
        except ValueError as error:
            messagebox.showerror("No se ha podido registrar", str(error), parent=self)
            return
        stock = self.gestor.stock(self.actividad, compra.pais, compra.talla)[compra.equipo]
        messagebox.showinfo("Hecho", f"{compra.equipo} talla {compra.talla} en {compra.pais}: "
                                     f"ahora hay {stock} unidades.", parent=self)

    def limpiar(self):
        self.cantidad.delete(0, tk.END)
        if not self.baja:
            self.precio.delete(0, tk.END)

"""Consulta del stock por país, talla y actividad."""

import tkinter as tk
from tkinter import messagebox, ttk

from ..config import ACTIVIDADES, TALLAS
from ..gestor import GestorBasesDatos
from .comun import campo, combo


class VentanaInventario(tk.Toplevel):
    def __init__(self, master, gestor: GestorBasesDatos):
        super().__init__(master)
        self.gestor = gestor
        self.title("Inventario")

        self.actividad = campo(self, 0, "Actividad:", combo(self, ACTIVIDADES))
        self.pais = campo(self, 1, "País:", combo(self, [], ancho=30))
        self.talla = campo(self, 2, "Talla:", combo(self, TALLAS, inicial="M"))
        self.actividad.bind("<<ComboboxSelected>>", lambda _e: self._cargar_paises())
        self._cargar_paises()
        ttk.Button(self, text="Consultar", command=self.consultar).grid(row=3, column=0, columnspan=2, pady=8)

        self.tabla = ttk.Treeview(self, columns=("equipo", "cantidad"), show="headings", height=11)
        self.tabla.heading("equipo", text="Equipo")
        self.tabla.heading("cantidad", text="Unidades disponibles")
        self.tabla.column("cantidad", anchor="e", width=140)
        self.tabla.grid(row=4, column=0, columnspan=2, padx=10, pady=(0, 10))

    def _cargar_paises(self):
        paises = self.gestor.paises(self.actividad.get())
        self.pais.config(values=paises)
        self.pais.set("ESPAÑA" if "ESPAÑA" in paises else (paises[0] if paises else ""))

    def consultar(self):
        self.tabla.delete(*self.tabla.get_children())
        stock = self.gestor.stock(self.actividad.get(), self.pais.get(), self.talla.get())
        if not stock:
            messagebox.showinfo("Inventario", "No hay inventario para esa combinación.", parent=self)
        for equipo, unidades in stock.items():
            self.tabla.insert("", tk.END, values=(equipo, unidades))

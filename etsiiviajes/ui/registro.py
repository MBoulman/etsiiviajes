"""Menú «Registro y consultas»: usuarios, especies, puntos, inventario y compras."""

import tkinter as tk

from ..config import BUCEO, ESQUI
from ..gestor import GestorBasesDatos
from .comun import FUENTE_NEGRITA, poner_icono
from .compras import VentanaCompra
from .fauna_flora import VentanaAltaEspecie, VentanaConsultaEspecie
from .inventario import VentanaInventario
from .puntos import VentanaPuntosEsqui, VentanaPuntosInmersion
from .usuarios import VentanaUsuarios


class VentanaRegistro(tk.Toplevel):
    def __init__(self, master, gestor: GestorBasesDatos):
        super().__init__(master)
        self.title("Registro y consultas")
        self.geometry("700x480")
        self.resizable(False, False)
        self.configure(bg="white")
        poner_icono(self, "registro")
        tk.Label(self, bg="grey").place(x=10, y=40, width=680, height=410)

        g = gestor
        self._seccion("USUARIOS", 30, 45, 75, [
            ("BUCEADORES", lambda: VentanaUsuarios(self, g, BUCEO)),
            ("ESQUIADORES", lambda: VentanaUsuarios(self, g, ESQUI))], en_fila=True)
        self._seccion("FAUNA Y FLORA", 30, 157, 75, [
            ("ALTA", lambda: VentanaAltaEspecie(self, g)),
            ("CONSULTA", lambda: VentanaConsultaEspecie(self, g))], en_fila=True)
        self._seccion("PUNTOS", 30, 280, 115, [
            ("ALTA Y CONSULTA PUNTOS DE INMERSIÓN", lambda: VentanaPuntosInmersion(self, g)),
            ("ALTA Y CONSULTA PUNTOS DE ESQUÍ", lambda: VentanaPuntosEsqui(self, g))])
        self._seccion("INVENTARIO", 355, 45, 75, [
            ("INVENTARIO", lambda: VentanaInventario(self, g))])
        self._seccion("COMPRAS", 355, 157, 237, [
            ("ALTA PRODUCTO CENTRO BUCEO", lambda: VentanaCompra(self, g, BUCEO)),
            ("BAJA PRODUCTO CENTRO BUCEO", lambda: VentanaCompra(self, g, BUCEO, baja=True)),
            ("ALTA PRODUCTO CENTRO ESQUÍ", lambda: VentanaCompra(self, g, ESQUI)),
            ("BAJA PRODUCTO CENTRO ESQUÍ", lambda: VentanaCompra(self, g, ESQUI, baja=True))])

    def _seccion(self, titulo, x, y, alto, botones, en_fila=False):
        """Recuadro blanco con un título amarillo y sus botones negros."""
        tk.Label(self, text=titulo, font=FUENTE_NEGRITA, bg="grey", fg="yellow").place(
            x=x + 157, y=y, anchor="n")
        marco = tk.Frame(self, bg="white", highlightthickness=2, highlightbackground="white")
        marco.place(x=x, y=y + 25, width=315, height=alto)
        for texto, accion in botones:
            boton = tk.Button(marco, text=texto, command=accion, bg="black", fg="white",
                              font=FUENTE_NEGRITA)
            if en_fila:
                boton.pack(side=tk.LEFT, expand=True, pady=15)
            else:
                boton.pack(pady=(12, 0))

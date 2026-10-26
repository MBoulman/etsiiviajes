"""Ventana de inicio: menú, calendario, reservas y carrusel de especies."""

import random
import tkinter as tk

from tkcalendar import Calendar

from ..gestor import GestorBasesDatos
from .agenda import VentanaAgenda
from .ayuda import VentanaAyuda
from .comun import foto_tk, poner_icono
from .devolucion import VentanaDevolucion
from .estadisticas import VentanaEstadisticas
from .mapa import VentanaMapa
from .registro import VentanaRegistro
from .reserva import VentanaReserva

ANCHO, ALTO = 1130, 630
FOTOS_CARRUSEL = 5
SEGUNDOS_CARRUSEL = 5


class VentanaPrincipal(tk.Tk):
    def __init__(self, gestor: GestorBasesDatos):
        super().__init__()
        self.gestor = gestor
        self.title("ETSIIVIAJES")
        self.geometry(f"{ANCHO}x{ALTO}")
        self.resizable(False, False)
        poner_icono(self, "global")
        self.protocol("WM_DELETE_WINDOW", self.salir)

        self._crear_menu()
        self._crear_textos()
        self._crear_calendario()
        self._crear_carrusel()

    def _crear_menu(self):
        marco = tk.Frame(self, bg="#23BEBE")
        marco.place(x=10, y=10)
        botones = [("Registro y Consultas", lambda: VentanaRegistro(self, self.gestor)),
                   ("Mapa", lambda: VentanaMapa(self, self.gestor)),
                   ("Estadísticas", lambda: VentanaEstadisticas(self, self.gestor)),
                   ("Ayuda", lambda: VentanaAyuda(self))]
        for texto, accion in botones:
            tk.Button(marco, text=texto, font=("Calibri", 12), command=accion).pack(
                fill=tk.X, padx=10, pady=5)

    def _crear_textos(self):
        tk.Label(self, text="BIENVENIDO A LA INMERSIÓN", font=("Calibri", 35, "bold")).place(x=200, y=100)
        tk.Label(self, text="EN EL AGUA Y EN LA NIEVE", font=("Calibri", 12)).place(x=630, y=160)
        cita = ("«El agua, testigo inmaculado de la crónica de la Tierra, guarda en sus\n"
                "profundidades los misterios de la creación y el poder de transformar\n"
                "los destinos de nuestro planeta.»")
        tk.Label(self, text=cita, font=("Calibri", 15), justify="left").place(x=200, y=200)
        tk.Label(self, text="Jacques-Yves Cousteau", font=("Calibri", 12)).place(x=630, y=290)

    def _crear_calendario(self):
        marco = tk.Frame(self)
        marco.place(x=ANCHO - 290, y=10)
        Calendar(marco, selectmode="day", locale="es_ES", date_pattern="dd/mm/yyyy").pack(padx=10, pady=5)
        tk.Button(marco, text="Agenda", font=("Calibri", 14),
                  command=lambda: VentanaAgenda(self, self.gestor)).pack(pady=5)
        botones = tk.Frame(marco)
        botones.pack(pady=5)
        tk.Button(botones, text="Reservar", font=("Calibri", 14),
                  command=lambda: VentanaReserva(self, self.gestor)).pack(side=tk.LEFT, padx=15)
        tk.Button(botones, text="Devolver", font=("Calibri", 14),
                  command=lambda: VentanaDevolucion(self, self.gestor)).pack(side=tk.LEFT, padx=15)

    def _crear_carrusel(self):
        self.especies = [e for e in self.gestor.listar_especies() if e.foto]
        marco = tk.Frame(self)
        marco.place(x=10, y=ALTO - 215, width=ANCHO - 20, height=210)
        self.fotos, self.nombres, self._imagenes = [], [], []
        for i in range(FOTOS_CARRUSEL):
            marco.columnconfigure(i, weight=1)
            foto = tk.Label(marco)
            foto.grid(row=0, column=i, pady=(5, 0))
            nombre = tk.Label(marco, font=("Calibri", 10))
            nombre.grid(row=1, column=i)
            self.fotos.append(foto)
            self.nombres.append(nombre)
        self._cambiar_fotos()

    def _cambiar_fotos(self):
        if not self.especies:
            return
        elegidas = random.sample(self.especies, min(FOTOS_CARRUSEL, len(self.especies)))
        self._imagenes = [foto_tk(e.foto, (180, 170), master=self) for e in elegidas]
        for etiqueta, nombre, especie, imagen in zip(self.fotos, self.nombres, elegidas, self._imagenes):
            etiqueta.config(image=imagen)
            nombre.config(text=especie.nombre)
        self.after(SEGUNDOS_CARRUSEL * 1000, self._cambiar_fotos)

    def salir(self):
        self.gestor.cerrar()
        self.destroy()

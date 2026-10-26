"""Agenda de cursos y competiciones, guardada en la base de datos."""

import tkinter as tk
from datetime import date
from tkinter import messagebox

from tkcalendar import Calendar

from ..gestor import GestorBasesDatos
from .comun import combo, texto_solo_lectura

HORAS = ("10:00", "12:00", "16:00", "17:00", "18:00")
EVENTOS = ("CURSO INICIAL DE ESQUI", "CURSO INTERMEDIO DE ESQUI", "CURSO AVANZADO DE ESQUI",
           "CURSO BASICO DE BUCEO", "CURSO INTERMEDIO DE BUCEO", "CURSO AVANZADO DE BUCEO",
           "CURSO FAUNA Y FLORA", "COMPETICIÓN ESQUÍ <18", "COMPETICIÓN ESQUÍ 18-30",
           "COMPETICIÓN ESQUÍ 30-45")


class VentanaAgenda(tk.Toplevel):
    def __init__(self, master, gestor: GestorBasesDatos):
        super().__init__(master)
        self.gestor = gestor
        self.title("Agenda de eventos")
        self.calendario = Calendar(self, selectmode="day", locale="es_ES", date_pattern="dd/mm/yyyy")
        self.calendario.pack(padx=10, pady=10)
        self.calendario.bind("<<CalendarSelected>>", lambda _e: self.mostrar_dia())
        self.hora = combo(self, HORAS)
        self.hora.pack(pady=3)
        self.evento = combo(self, EVENTOS, ancho=30)
        self.evento.pack(pady=3)
        botones = tk.Frame(self)
        botones.pack(pady=5)
        tk.Button(botones, text="Registrar evento", command=self.registrar).pack(side=tk.LEFT, padx=4)
        tk.Button(botones, text="Eventos de hoy", command=self.hoy).pack(side=tk.LEFT, padx=4)
        self.lista = tk.Text(self, width=42, height=6, state="disabled")
        self.lista.pack(padx=10, pady=(0, 10))
        self.mostrar_dia()

    def _dia(self) -> date:
        return self.calendario.selection_get() or date.today()

    def registrar(self):
        dia = self._dia()
        self.gestor.agregar_evento(dia.isoformat(), self.hora.get(), self.evento.get())
        messagebox.showinfo("Evento registrado", f"{self.evento.get()} el {dia:%d/%m/%Y} a las "
                            f"{self.hora.get()}.", parent=self)
        self.mostrar_dia()

    def hoy(self):
        self.calendario.selection_set(date.today())
        self.calendario.see(date.today())
        self.mostrar_dia()

    def mostrar_dia(self):
        dia = self._dia()
        eventos = self.gestor.eventos_del_dia(dia.isoformat())
        lineas = [f"{hora} · {nombre}" for hora, nombre in eventos] or ["Sin eventos."]
        texto_solo_lectura(self.lista, f"{dia:%d/%m/%Y}\n" + "\n".join(lineas))

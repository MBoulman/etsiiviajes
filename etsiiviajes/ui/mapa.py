"""Ventana del mapa: vídeo de fondo y botones para generar y abrir el mapa Folium."""

import tkinter as tk
from tkinter import messagebox

from PIL import Image, ImageTk

from ..config import VIDEO_MAPA
from ..gestor import GestorBasesDatos
from ..mapa import RUTA_MAPA, generar_mapa
from ..utils import abrir_archivo

try:
    import cv2
except ImportError:  # el vídeo es decorativo: sin OpenCV la ventana funciona igual
    cv2 = None

ANCHO, ALTO, ANCHO_VIDEO = 1130, 630, 800


class VentanaMapa(tk.Toplevel):
    def __init__(self, master, gestor: GestorBasesDatos):
        super().__init__(master)
        self.gestor = gestor
        self.title("Mapa")
        self.resizable(False, False)
        self.lienzo = tk.Canvas(self, width=ANCHO, height=ALTO, bg="white", highlightthickness=0)
        self.lienzo.pack()
        tk.Button(self, text="Abrir mapa", font=("Arial", 12), command=self.abrir).place(
            relx=0.5, rely=0.45, anchor="n")
        tk.Button(self, text="Actualizar mapa", font=("Arial", 12), command=self.actualizar).place(
            relx=0.5, rely=0.55, anchor="n")
        self.video = cv2.VideoCapture(str(VIDEO_MAPA)) if cv2 and VIDEO_MAPA.exists() else None
        self.protocol("WM_DELETE_WINDOW", self.cerrar)
        self._siguiente_fotograma()

    def _siguiente_fotograma(self):
        if self.video is None or not self.video.isOpened():
            return
        ok, fotograma = self.video.read()
        if not ok:  # fin del vídeo: vuelve al principio
            self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ok, fotograma = self.video.read()
        if ok:
            alto = int(fotograma.shape[0] * ANCHO_VIDEO / fotograma.shape[1])
            fotograma = cv2.cvtColor(cv2.resize(fotograma, (ANCHO_VIDEO, alto)), cv2.COLOR_BGR2RGB)
            self._imagen = ImageTk.PhotoImage(Image.fromarray(fotograma), master=self)
            self.lienzo.delete("video")
            self.lienzo.create_image((ANCHO - ANCHO_VIDEO) // 2, (ALTO - alto) // 2, anchor="nw",
                                     image=self._imagen, tags="video")
            self.lienzo.tag_lower("video")
        self.after(40, self._siguiente_fotograma)

    def actualizar(self):
        self.config(cursor="watch")
        self.update_idletasks()
        try:
            ruta = generar_mapa(self.gestor)
        finally:
            self.config(cursor="")
        if messagebox.askyesno("Mapa actualizado", "El mapa se ha generado con los puntos actuales. "
                               "¿Abrirlo ahora?", parent=self):
            abrir_archivo(ruta)

    def abrir(self):
        if not RUTA_MAPA.exists():
            self.actualizar()
        else:
            abrir_archivo(RUTA_MAPA)

    def cerrar(self):
        if self.video is not None:
            self.video.release()
        self.destroy()

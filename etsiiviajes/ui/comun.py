"""Utilidades de interfaz compartidas por todas las ventanas."""

import sys
import tkinter as tk
from io import BytesIO
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from PIL import Image, ImageTk

from ..config import ICONOS

FUENTE = ("Calibri", 11)
FUENTE_NEGRITA = ("Helvetica", 10, "bold")


def poner_icono(ventana: tk.Misc, nombre: str) -> None:
    """Pone ``assets/iconos/<nombre>.ico`` como icono de la ventana, en cualquier sistema."""
    ruta = ICONOS / f"{nombre}.ico"
    if not ruta.exists():
        return
    try:
        if sys.platform.startswith("win"):
            ventana.iconbitmap(str(ruta))
        else:
            imagen = ImageTk.PhotoImage(Image.open(ruta), master=ventana)
            ventana.iconphoto(False, imagen)
            ventana._icono = imagen  # evita que el recolector de basura la borre
    except (tk.TclError, OSError):
        pass


def foto_tk(datos, tamano: tuple[int, int], master=None) -> ImageTk.PhotoImage:
    """Convierte una ruta o unos bytes de imagen en un ``PhotoImage`` del tamaño dado."""
    origen = BytesIO(datos) if isinstance(datos, (bytes, bytearray)) else datos
    with Image.open(origen) as img:
        img = img.convert("RGB")
        img.thumbnail(tamano, Image.LANCZOS)
        return ImageTk.PhotoImage(img, master=master)


def mostrar_imagen(master: tk.Misc, titulo: str, datos, tamano=(350, 350)) -> None:
    """Abre una ventana con una imagen; se cierra al hacer clic sobre ella."""
    ventana = tk.Toplevel(master)
    ventana.title(titulo)
    imagen = foto_tk(datos, tamano, master=ventana)
    etiqueta = tk.Label(ventana, image=imagen, cursor="hand2")
    etiqueta.image = imagen
    etiqueta.pack()
    etiqueta.bind("<Button-1>", lambda _e: ventana.destroy())


def mostrar_figura(master: tk.Misc, figura, titulo: str) -> None:
    """Muestra una figura de matplotlib en una ventana propia con barra de herramientas."""
    ventana = tk.Toplevel(master)
    ventana.title(titulo)
    lienzo = FigureCanvasTkAgg(figura, master=ventana)
    NavigationToolbar2Tk(lienzo, ventana).update()
    lienzo.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    lienzo.draw()


def campo(marco: tk.Misc, fila: int, texto: str, widget: tk.Widget, columna: int = 0) -> tk.Widget:
    """Coloca una etiqueta y su widget en una fila de un ``grid``."""
    tk.Label(marco, text=texto).grid(row=fila, column=columna, padx=5, pady=4, sticky="w")
    widget.grid(row=fila, column=columna + 1, padx=5, pady=4, sticky="we")
    return widget


def combo(marco: tk.Misc, valores, inicial=None, ancho: int = 22) -> ttk.Combobox:
    """Desplegable de solo lectura: el usuario no puede escribir valores fuera de la lista."""
    c = ttk.Combobox(marco, values=list(valores), state="readonly", width=ancho)
    if inicial is not None:
        c.set(inicial)
    elif valores:
        c.current(0)
    return c


def texto_solo_lectura(widget: tk.Text, contenido: str) -> None:
    widget.config(state="normal")
    widget.delete("1.0", tk.END)
    widget.insert(tk.END, contenido)
    widget.config(state="disabled")

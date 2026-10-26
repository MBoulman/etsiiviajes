"""Alta y consulta de especies de fauna y flora."""

import tkinter as tk
from tkinter import filedialog, messagebox

from ..config import AGUAS
from ..gestor import GestorBasesDatos
from ..modelos import Especie
from ..utils import imagen_a_bytes
from .comun import combo, mostrar_imagen, poner_icono, texto_solo_lectura


class VentanaAltaEspecie(tk.Toplevel):
    def __init__(self, master, gestor: GestorBasesDatos):
        super().__init__(master)
        self.gestor = gestor
        self.foto: bytes | None = None
        self.title("Alta fauna y flora")
        poner_icono(self, "fauna_flora")

        tk.Label(self, text="Nombre:").grid(row=0, column=0, padx=8, pady=4, sticky="w")
        self.nombre = tk.Entry(self, width=25)
        self.nombre.grid(row=0, column=1, padx=8, pady=4)
        tk.Label(self, text="Tipo:").grid(row=1, column=0, padx=8, pady=4, sticky="w")
        self.tipo = combo(self, ("FAUNA", "FLORA"))
        self.tipo.grid(row=1, column=1, padx=8, pady=4)

        tk.Label(self, text="Vista en:", font=("Calibri", 11, "bold")).grid(
            row=2, column=0, padx=8, pady=(10, 2), sticky="w")
        self.aguas = {}
        for fila, (clave, nombre) in enumerate(AGUAS.items(), start=3):
            variable = tk.BooleanVar(value=False)
            tk.Checkbutton(self, text=nombre, variable=variable).grid(
                row=fila, column=0, columnspan=2, padx=20, sticky="w")
            self.aguas[clave] = variable

        fila = 3 + len(AGUAS)
        tk.Label(self, text="Foto:").grid(row=fila, column=0, padx=8, pady=8, sticky="w")
        self.etiqueta_foto = tk.Label(self, text="(sin foto)", fg="grey")
        self.etiqueta_foto.grid(row=fila, column=1, sticky="w")
        tk.Button(self, text="Examinar", command=self.examinar).grid(row=fila, column=1, sticky="e")
        botones = tk.Frame(self)
        botones.grid(row=fila + 1, column=0, columnspan=2, pady=10)
        tk.Button(botones, text="Agregar", command=self.agregar, width=9).pack(side=tk.LEFT, padx=5)
        tk.Button(botones, text="Limpiar", command=self.limpiar, width=9).pack(side=tk.LEFT, padx=5)

    def examinar(self):
        ruta = filedialog.askopenfilename(parent=self, title="Seleccionar foto",
                                          filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.gif")])
        if ruta:
            try:
                self.foto = imagen_a_bytes(ruta, lado_max=400)
                self.etiqueta_foto.config(text="foto cargada", fg="green")
            except OSError:
                messagebox.showerror("Foto", "No se ha podido abrir la imagen.", parent=self)

    def agregar(self):
        nombre = self.nombre.get().strip()
        if not nombre:
            messagebox.showwarning("Alta", "Escribe el nombre de la especie.", parent=self)
            return
        aguas = {clave: var.get() for clave, var in self.aguas.items()}
        if not any(aguas.values()):
            messagebox.showwarning("Alta", "Marca al menos unas aguas.", parent=self)
            return
        especie = Especie(nombre=nombre.upper(), tipo=self.tipo.get(), aguas=aguas, foto=self.foto)
        if self.gestor.agregar_especie(especie):
            messagebox.showinfo("Alta", f"{especie.nombre} se ha añadido.", parent=self)
            self.limpiar()
        else:
            messagebox.showerror("Alta", f"{especie.nombre} ya estaba registrada.", parent=self)

    def limpiar(self):
        self.nombre.delete(0, tk.END)
        self.tipo.current(0)
        for variable in self.aguas.values():
            variable.set(False)
        self.foto = None
        self.etiqueta_foto.config(text="(sin foto)", fg="grey")


class VentanaConsultaEspecie(tk.Toplevel):
    def __init__(self, master, gestor: GestorBasesDatos):
        super().__init__(master)
        self.gestor = gestor
        self.title("Consulta fauna y flora")
        poner_icono(self, "fauna_flora")

        tk.Label(self, text="Nombre:").grid(row=0, column=0, padx=10, pady=8, sticky="w")
        self.nombre = tk.Entry(self, width=25)
        self.nombre.grid(row=0, column=1, columnspan=2, padx=10, sticky="w")

        self.modo = tk.StringVar(value="nombre")
        tk.Radiobutton(self, text="Buscar por nombre", variable=self.modo, value="nombre",
                       command=self._actualizar).grid(row=1, column=0, columnspan=2, sticky="w", padx=10)
        tk.Radiobutton(self, text="Buscar por aguas", variable=self.modo, value="aguas",
                       command=self._actualizar).grid(row=2, column=0, columnspan=2, sticky="w", padx=10)
        self.etiqueta_aguas = tk.Label(self, text="Aguas:")
        self.etiqueta_aguas.grid(row=3, column=0, padx=10, sticky="w")
        self.aguas = combo(self, AGUAS.values())
        self.aguas.grid(row=3, column=1, columnspan=2, padx=10, pady=4, sticky="w")

        botones = tk.Frame(self)
        botones.grid(row=4, column=0, columnspan=3, pady=8)
        for texto, accion in (("Buscar", self.buscar), ("Imagen", self.ver_imagen),
                              ("Limpiar", self.limpiar), ("Eliminar", self.eliminar)):
            tk.Button(botones, text=texto, command=accion, width=8).pack(side=tk.LEFT, padx=4)

        tk.Label(self, text="Resultados:").grid(row=5, column=0, padx=10, sticky="w")
        self.resultado = tk.Text(self, height=9, width=42, state="disabled")
        self.resultado.grid(row=6, column=0, columnspan=3, padx=10, pady=(0, 10))
        self._actualizar()

    def _actualizar(self):
        visible = self.modo.get() == "aguas"
        for widget in (self.etiqueta_aguas, self.aguas):
            if visible:
                widget.grid()
            else:
                widget.grid_remove()

    def _especie(self):
        nombre = self.nombre.get().strip()
        if not nombre:
            messagebox.showwarning("Consulta", "Escribe el nombre de la especie.", parent=self)
            return None
        especie = self.gestor.obtener_especie(nombre)
        if especie is None:
            texto_solo_lectura(self.resultado, f"No hay ninguna especie llamada «{nombre.upper()}».")
        return especie

    def buscar(self):
        especie = self._especie()
        if especie is None:
            return
        if self.modo.get() == "nombre":
            vistas = [AGUAS[c] for c, vista in especie.aguas.items() if vista]
            texto = f"TIPO: {especie.tipo}\nAGUAS:\n  " + "\n  ".join(vistas or ["(ninguna)"])
        else:
            nombre_aguas = self.aguas.get()
            clave = next(c for c, n in AGUAS.items() if n == nombre_aguas)
            presente = "SÍ" if especie.aguas[clave] else "NO"
            texto = f"¿{especie.nombre.title()} en {nombre_aguas}? {presente}"
        texto_solo_lectura(self.resultado, texto)

    def ver_imagen(self):
        especie = self._especie()
        if especie is None:
            return
        if especie.foto:
            mostrar_imagen(self, especie.nombre, especie.foto, (300, 300))
        else:
            messagebox.showinfo("Imagen", f"{especie.nombre} no tiene foto.", parent=self)

    def limpiar(self):
        self.nombre.delete(0, tk.END)
        texto_solo_lectura(self.resultado, "")

    def eliminar(self):
        nombre = self.nombre.get().strip().upper()
        if not nombre or not messagebox.askyesno("Eliminar", f"¿Borrar {nombre}?", parent=self):
            return
        if self.gestor.borrar_especie(nombre):
            messagebox.showinfo("Eliminar", f"{nombre} se ha borrado.", parent=self)
            self.limpiar()
        else:
            messagebox.showinfo("Eliminar", f"No hay ninguna especie llamada {nombre}.", parent=self)

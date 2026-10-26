"""Alta, consulta y baja de puntos de inmersión y de esquí."""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from ..config import AGUAS
from ..gestor import GestorBasesDatos
from ..modelos import PuntoEsqui, PuntoInmersion
from ..utils import imagen_a_bytes
from .comun import combo, mostrar_imagen


class _VentanaPuntos(tk.Toplevel):
    """Parte común: formulario de alta arriba, búsqueda y borrado abajo."""

    titulo = ""
    texto_foto = "Foto:"

    def __init__(self, master, gestor: GestorBasesDatos):
        super().__init__(master)
        self.gestor = gestor
        self.foto: bytes | None = None
        self.title(self.titulo)
        self.resizable(False, False)
        self.entradas: dict[str, tk.Widget] = {}
        fila = 0
        for clave, texto, widget in self.campos():
            tk.Label(self, text=texto).grid(row=fila, column=0, padx=8, pady=3, sticky="w")
            widget.grid(row=fila, column=1, padx=8, pady=3, sticky="we")
            self.entradas[clave] = widget
            fila += 1
        tk.Label(self, text=self.texto_foto).grid(row=fila, column=0, padx=8, pady=3, sticky="w")
        self.etiqueta_foto = tk.Label(self, text="(sin imagen)", fg="grey")
        self.etiqueta_foto.grid(row=fila, column=1, sticky="w", padx=8)
        tk.Button(self, text="Seleccionar", command=self.seleccionar_foto).grid(row=fila, column=2, padx=8)
        fila += 1
        tk.Button(self, text="Agregar", command=self.agregar, width=9).grid(row=fila, column=1, pady=8)
        tk.Button(self, text="Limpiar", command=self.limpiar, width=9).grid(row=fila, column=2, pady=8)
        fila += 1
        tk.Frame(self, height=2, bg="grey").grid(row=fila, column=0, columnspan=3, sticky="we", pady=6)
        fila += 1
        tk.Label(self, text="Nombre:").grid(row=fila, column=0, padx=8, sticky="w")
        self.nombre_buscar = tk.Entry(self)
        self.nombre_buscar.grid(row=fila, column=1, padx=8, sticky="we")
        fila += 1
        botones = tk.Frame(self)
        botones.grid(row=fila, column=0, columnspan=3, pady=8)
        tk.Button(botones, text="Mostrar", command=self.mostrar, width=9).pack(side=tk.LEFT, padx=5)
        tk.Button(botones, text="Imagen", command=self.ver_imagen, width=9).pack(side=tk.LEFT, padx=5)
        tk.Button(botones, text="Eliminar", command=self.eliminar, width=9).pack(side=tk.LEFT, padx=5)

    # Lo implementa cada subclase
    def campos(self):
        raise NotImplementedError

    def crear_punto(self, valores: dict):
        raise NotImplementedError

    def describir(self, punto) -> str:
        raise NotImplementedError

    def seleccionar_foto(self):
        ruta = filedialog.askopenfilename(parent=self, title="Seleccionar imagen",
                                          filetypes=[("Imágenes", "*.png *.jpg *.jpeg")])
        if ruta:
            try:
                self.foto = imagen_a_bytes(ruta)
                self.etiqueta_foto.config(text="imagen cargada", fg="green")
            except OSError:
                messagebox.showerror("Imagen", "No se ha podido abrir la imagen.", parent=self)

    def _valores(self) -> dict:
        valores = {}
        for clave, widget in self.entradas.items():
            valores[clave] = widget.get().strip()
        if not valores["nombre"] or not valores["pais"]:
            raise ValueError("El nombre y el país son obligatorios.")
        try:
            valores["latitud"] = float(valores["latitud"].replace(",", "."))
            valores["longitud"] = float(valores["longitud"].replace(",", "."))
        except ValueError:
            raise ValueError("La latitud y la longitud deben ser números.") from None
        if not (-90 <= valores["latitud"] <= 90 and -180 <= valores["longitud"] <= 180):
            raise ValueError("Latitud entre -90 y 90, longitud entre -180 y 180.")
        return valores

    def agregar(self):
        try:
            punto = self.crear_punto(self._valores())
        except ValueError as error:
            messagebox.showwarning("Revisa los datos", str(error), parent=self)
            return
        if self.guardar(punto):
            messagebox.showinfo("Alta", f"{punto.nombre} se ha añadido. Actualiza el mapa para verlo.",
                                parent=self)
            self.limpiar()
        else:
            messagebox.showerror("Alta", f"Ya existe un punto llamado {punto.nombre}.", parent=self)

    def limpiar(self):
        for widget in self.entradas.values():
            if not isinstance(widget, ttk.Combobox):
                widget.delete(0, tk.END)
        self.foto = None
        self.etiqueta_foto.config(text="(sin imagen)", fg="grey")

    def _buscar(self):
        nombre = self.nombre_buscar.get().strip()
        if not nombre:
            messagebox.showwarning("Buscar", "Escribe el nombre del punto.", parent=self)
            return None
        punto = self.obtener(nombre)
        if punto is None:
            messagebox.showinfo("Buscar", f"No hay ningún punto llamado {nombre}.", parent=self)
        return punto

    def mostrar(self):
        punto = self._buscar()
        if punto:
            messagebox.showinfo(punto.nombre, self.describir(punto), parent=self)

    def ver_imagen(self):
        punto = self._buscar()
        if punto is None:
            return
        imagen = getattr(punto, "foto", None) or getattr(punto, "mapa_pistas", None)
        if imagen:
            mostrar_imagen(self, punto.nombre, imagen, (500, 400))
        else:
            messagebox.showinfo("Imagen", f"{punto.nombre} no tiene imagen.", parent=self)

    def eliminar(self):
        nombre = self.nombre_buscar.get().strip()
        if not nombre or not messagebox.askyesno("Eliminar", f"¿Eliminar el punto {nombre}?", parent=self):
            return
        if self.borrar(nombre):
            messagebox.showinfo("Eliminar", f"{nombre} se ha eliminado.", parent=self)
            self.nombre_buscar.delete(0, tk.END)
        else:
            messagebox.showinfo("Eliminar", f"No hay ningún punto llamado {nombre}.", parent=self)


class VentanaPuntosInmersion(_VentanaPuntos):
    titulo = "Puntos de inmersión"

    def campos(self):
        return [("nombre", "Nombre:", tk.Entry(self)), ("pais", "País:", tk.Entry(self)),
                ("latitud", "Latitud:", tk.Entry(self)), ("longitud", "Longitud:", tk.Entry(self)),
                ("aguas", "Aguas:", combo(self, AGUAS.values())),
                ("profundidad", "Profundidad (m):", tk.Entry(self))]

    def crear_punto(self, v):
        try:
            profundidad = float(v["profundidad"].replace(",", "."))
        except ValueError:
            raise ValueError("La profundidad debe ser un número.") from None
        return PuntoInmersion(v["nombre"], v["pais"].upper(), v["latitud"], v["longitud"],
                              v["aguas"], profundidad, self.foto)

    def describir(self, p):
        return (f"País: {p.pais}\nLatitud: {p.latitud}\nLongitud: {p.longitud}\n"
                f"Aguas: {p.aguas}\nProfundidad: {p.profundidad:g} m")

    def guardar(self, punto):
        return self.gestor.agregar_punto_inmersion(punto)

    def obtener(self, nombre):
        return self.gestor.obtener_punto_inmersion(nombre)

    def borrar(self, nombre):
        return self.gestor.borrar_punto_inmersion(nombre)


class VentanaPuntosEsqui(_VentanaPuntos):
    titulo = "Puntos de esquí"
    texto_foto = "Mapa de pistas:"

    def campos(self):
        return [("nombre", "Nombre:", tk.Entry(self)), ("pais", "País:", tk.Entry(self)),
                ("latitud", "Latitud:", tk.Entry(self)), ("longitud", "Longitud:", tk.Entry(self)),
                ("km", "Km de pistas:", tk.Entry(self))]

    def crear_punto(self, v):
        try:
            km = float(v["km"].replace(",", "."))
        except ValueError:
            raise ValueError("Los km de pistas deben ser un número.") from None
        return PuntoEsqui(v["nombre"], v["pais"].upper(), v["latitud"], v["longitud"], km, self.foto)

    def describir(self, p):
        return (f"País: {p.pais}\nLatitud: {p.latitud}\nLongitud: {p.longitud}\n"
                f"Km de pistas: {p.km_pistas:g}")

    def guardar(self, punto):
        return self.gestor.agregar_punto_esqui(punto)

    def obtener(self, nombre):
        return self.gestor.obtener_punto_esqui(nombre)

    def borrar(self, nombre):
        return self.gestor.borrar_punto_esqui(nombre)

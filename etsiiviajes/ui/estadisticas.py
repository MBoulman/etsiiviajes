"""Ventana de estadísticas: clientes, ventas (con modelo de regresión) y especies."""

import tkinter as tk
from tkinter import messagebox

from .. import estadisticas as est
from ..config import AGUAS, BUCEO, ESQUI, TALLAS
from ..gestor import GestorBasesDatos
from .comun import combo, mostrar_figura, poner_icono, texto_solo_lectura


class VentanaEstadisticas(tk.Toplevel):
    def __init__(self, master, gestor: GestorBasesDatos):
        super().__init__(master)
        self.gestor = gestor
        self.title("Estadísticas")
        poner_icono(self, "estadisticas")
        for col in range(2):
            self.columnconfigure(col, weight=1)
        self._panel_clientes(0, 0, "BUCEADORES", BUCEO)
        self._panel_clientes(0, 1, "ESQUIADORES", ESQUI)
        self._panel_ventas(1, 0)
        self._panel_especies(1, 1)

    def _marco(self, fila, col, titulo):
        marco = tk.LabelFrame(self, text=titulo, font=("Arial", 11, "bold"), padx=10, pady=6)
        marco.grid(row=fila, column=col, padx=12, pady=8, sticky="nsew")
        salida = tk.Text(marco, height=6, width=48, state="disabled")
        return marco, salida

    def _intentar(self, salida, funcion):
        """Ejecuta un análisis y muestra el error en el cuadro si no hay datos suficientes."""
        try:
            funcion()
        except (ValueError, KeyError) as error:
            texto_solo_lectura(salida, f"No se puede calcular: {error}")

    # ------------------------------------------------------------- clientes

    def _panel_clientes(self, fila, col, titulo, actividad):
        marco, salida = self._marco(fila, col, titulo)
        nombre = titulo.title()

        def datos():
            df = est.datos_clientes(self.gestor, actividad)
            if df.empty:
                raise ValueError("no hay clientes registrados")
            return df

        def edades():
            texto_solo_lectura(salida, est.resumen_edad(datos()))

        def nacionalidades():
            df = datos()
            texto_solo_lectura(salida, df["nacionalidad"].value_counts().to_string())
            mostrar_figura(self, est.grafico_nacionalidades(df, nombre), "Nacionalidades")

        def niveles():
            df = datos()
            texto_solo_lectura(salida, df["nivel"].value_counts().to_string())
            mostrar_figura(self, est.grafico_niveles(df, nombre), "Niveles")

        def grupos():
            df, figuras = est.clusters(datos(), nombre)
            resumen = df.groupby("grupo")[["edad", "altura", "peso"]].mean().round(1)
            resumen.insert(0, "clientes", df["grupo"].value_counts().sort_index())
            texto_solo_lectura(salida, "Medias por grupo (K-means):\n" + resumen.to_string())
            for figura in figuras:
                mostrar_figura(self, figura, "Grupos")

        botones = tk.Frame(marco)
        botones.pack()
        for i, (texto, accion) in enumerate((("Edad media y cuartiles", edades),
                                             ("Nacionalidades", nacionalidades),
                                             ("Niveles", niveles), ("Grupos (clúster)", grupos))):
            tk.Button(botones, text=texto, width=20,
                      command=lambda a=accion: self._intentar(salida, a)).grid(
                row=i // 2, column=i % 2, padx=3, pady=2)
        salida.pack(pady=6)

    # --------------------------------------------------------------- ventas

    def _panel_ventas(self, fila, col):
        marco, salida = self._marco(fila, col, "VENTAS")

        def gasto():
            texto_solo_lectura(salida, est.gasto_medio(est.datos_ventas(self.gestor)))

        def grafico(funcion, titulo):
            def mostrar():
                df = est.datos_ventas(self.gestor)
                if df.empty:
                    raise ValueError("no hay ventas")
                mostrar_figura(self, funcion(df), titulo)
            return mostrar

        botones = tk.Frame(marco)
        botones.pack()
        acciones = (("Gasto medio", gasto),
                    ("Gasto por país", grafico(est.grafico_gasto_por_pais, "Gasto por país")),
                    ("Ventas por actividad", grafico(est.grafico_ventas_por_actividad, "Actividad")),
                    ("Reservas por talla", grafico(est.grafico_tallas, "Tallas")))
        for i, (texto, accion) in enumerate(acciones):
            tk.Button(botones, text=texto, width=20,
                      command=lambda a=accion: self._intentar(salida, a)).grid(
                row=i // 2, column=i % 2, padx=3, pady=2)

        pred = tk.Frame(marco)
        pred.pack(pady=(6, 0))
        tk.Label(pred, text="Predicción del importe:").grid(row=0, column=0, columnspan=3, sticky="w")
        actividad = combo(pred, (BUCEO, ESQUI), ancho=8)
        actividad.grid(row=1, column=0, padx=2)
        talla = combo(pred, TALLAS, inicial="M", ancho=5)
        talla.grid(row=1, column=1, padx=2)
        pais = combo(pred, self.gestor.paises(actividad.get()), ancho=22)
        pais.grid(row=1, column=2, padx=2)
        actividad.bind("<<ComboboxSelected>>", lambda _e: (
            pais.config(values=self.gestor.paises(actividad.get())), pais.current(0)))

        def predecir():
            modelo = est.ModeloPrecio(est.datos_ventas(self.gestor))
            valor = modelo.predecir(talla.get(), pais.get(), actividad.get())
            texto_solo_lectura(salida, (
                f"Importe previsto: {max(valor, 0):.2f} €\n"
                f"Regresión lineal entrenada con {modelo.n} ventas.\n"
                f"R² en el conjunto de prueba: {modelo.r2:.2f}\n"
                "(El precio depende sobre todo de la fecha, así que un R² bajo es lo esperado.)"))

        tk.Button(pred, text="Predecir", command=lambda: self._intentar(salida, predecir)).grid(
            row=2, column=0, columnspan=3, pady=3)
        salida.pack(pady=6)

    # -------------------------------------------------------------- especies

    def _panel_especies(self, fila, col):
        marco, salida = self._marco(fila, col, "FAUNA Y FLORA")

        def por_aguas():
            conteo, figura = est.grafico_especies_por_aguas(self.gestor)
            texto_solo_lectura(salida, "\n".join(f"{k}: {v}" for k, v in conteo.items()))
            mostrar_figura(self, figura, "Especies por aguas")

        tk.Button(marco, text="Especies por aguas", width=20,
                  command=lambda: self._intentar(salida, por_aguas)).pack(pady=2)
        aguas = combo(marco, AGUAS.values(), ancho=25)
        aguas.pack(pady=2)

        def consultar():
            clave = next(c for c, n in AGUAS.items() if n == aguas.get())
            fauna, flora = est.especies_de_aguas(self.gestor, clave)
            if not fauna and not flora:
                messagebox.showinfo("Especies", "No hay especies registradas en esas aguas.", parent=self)
            texto_solo_lectura(salida, f"FAUNA ({len(fauna)}): {', '.join(fauna)}\n\n"
                                       f"FLORA ({len(flora)}): {', '.join(flora)}")

        tk.Button(marco, text="Especies de estas aguas", width=20,
                  command=lambda: self._intentar(salida, consultar)).pack(pady=2)
        salida.config(wrap="word")
        salida.pack(pady=6)

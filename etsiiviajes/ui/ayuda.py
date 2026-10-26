"""Ventana de ayuda con secciones desplegables."""

import tkinter as tk

SECCIONES = {
    "REGISTRO Y CONSULTAS": (
        "Usuarios: los botones BUCEADORES y ESQUIADORES abren una ventana con el alta de "
        "clientes a la izquierda (se comprueba la letra del DNI/NIE, el email y que peso y altura "
        "sean números) y, a la derecha, la búsqueda y el borrado por DNI.\n\n"
        "Fauna y flora: ALTA registra una especie nueva, las aguas en las que se ha visto y su "
        "foto. CONSULTA busca una especie por nombre (tipo y aguas) o comprueba si se ha visto en "
        "unas aguas concretas; también enseña su foto y permite borrarla.\n\n"
        "Puntos: altas, consultas y bajas de puntos de inmersión y de esquí. Después de añadir "
        "un punto, pulsa «Actualizar mapa» en la ventana del mapa para que aparezca.\n\n"
        "Inventario y compras: el stock se lleva por país, actividad y talla. Las compras suman "
        "unidades y su coste; las bajas restan unidades y no dejan el stock en negativo."),
    "RESERVAS Y DEVOLUCIONES": (
        "RESERVAR (debajo del calendario) pide la actividad, el país del centro, la talla, el "
        "número de personas, la fecha y el DNI de un cliente ya registrado. El precio por persona "
        "depende de la fecha y se fija al calcularlo: es el mismo que se guarda y el que aparece "
        "en la factura. La reserva solo se registra si hay stock de todo el equipo; entonces se "
        "resta del inventario en la misma operación.\n\n"
        "Tras reservar se puede imprimir la factura (base imponible, IVA y total) y un PDF con la "
        "fauna y flora de las aguas del país.\n\n"
        "DEVOLVER muestra las reservas de un DNI y devuelve al inventario la última reserva "
        "pendiente. Una reserva ya devuelta no se puede devolver otra vez."),
    "MAPA": (
        "«Actualizar mapa» genera un mapa interactivo con todos los puntos de la base de datos y "
        "«Abrir mapa» lo abre en el navegador. Los marcadores morados son puntos de buceo y los "
        "verdes, estaciones de esquí; el selector de capas de la esquina permite filtrarlos. Al "
        "pulsar un marcador se ven sus datos y su foto."),
    "ESTADÍSTICAS": (
        "Buceadores y esquiadores: edad media y cuartiles, nacionalidades, niveles y una "
        "segmentación en grupos con K-means (altura, peso, edad y nacionalidad).\n\n"
        "Ventas: gasto medio, gasto por país, facturación por actividad y reservas por talla. La "
        "predicción del importe usa una regresión lineal y muestra su R² para que se vea la "
        "calidad del modelo.\n\n"
        "Fauna y flora: número de especies por aguas y lista de especies de unas aguas."),
    "AGENDA": (
        "Registra cursos y competiciones en un día y una hora. Los eventos se guardan en la base "
        "de datos y se ven al seleccionar el día en el calendario."),
    "ACERCA DE": (
        "ETSIIVIAJES es el trabajo final de Programación en Python (ETSII-UPM, curso 2023-24), "
        "revisado en 2026. Autores: Sofía Veldman Paniego, Juan del Junco Sampol y Mohamed "
        "Boulman Mokhlis.\n\nMás proyectos en www.mboulman.com y mboulman.es"),
}


class Seccion(tk.Frame):
    """Título que muestra u oculta su texto al pulsarlo."""

    def __init__(self, master, titulo: str, contenido: str):
        super().__init__(master)
        self.boton = tk.Button(self, text="+", width=2, relief=tk.FLAT, command=self.alternar)
        self.boton.grid(row=0, column=0, padx=(5, 0))
        cabecera = tk.Label(self, text=titulo, font=("Calibri", 12, "bold"), cursor="hand2")
        cabecera.grid(row=0, column=1, sticky="w")
        cabecera.bind("<Button-1>", lambda _e: self.alternar())
        self.texto = tk.Label(self, text=contenido, wraplength=980, justify="left")
        self.abierta = False

    def alternar(self):
        self.abierta = not self.abierta
        self.boton.config(text="−" if self.abierta else "+")
        if self.abierta:
            self.texto.grid(row=1, column=1, sticky="w", padx=(20, 10), pady=(0, 10))
        else:
            self.texto.grid_remove()


class VentanaAyuda(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Ayuda")
        self.geometry("1100x600")
        for titulo, contenido in SECCIONES.items():
            Seccion(self, titulo, contenido).pack(fill=tk.X, padx=30, pady=8)

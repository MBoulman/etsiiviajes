"""Consulta de reservas por DNI y devolución del material."""

import tkinter as tk
from tkinter import messagebox

from ..gestor import GestorBasesDatos
from ..utils import de_iso
from .comun import texto_solo_lectura


class VentanaDevolucion(tk.Toplevel):
    def __init__(self, master, gestor: GestorBasesDatos):
        super().__init__(master)
        self.gestor = gestor
        self.title("Devolución por DNI")

        fila = tk.Frame(self)
        fila.pack(padx=10, pady=10)
        tk.Label(fila, text="DNI:").pack(side=tk.LEFT)
        self.dni = tk.Entry(fila, width=20)
        self.dni.pack(side=tk.LEFT, padx=5)
        for texto, accion in (("Ver reservas", self.ver), ("Devolver", self.devolver),
                              ("Limpiar", self.limpiar)):
            tk.Button(fila, text=texto, command=accion).pack(side=tk.LEFT, padx=3)
        self.resultado = tk.Text(self, width=62, height=16, state="disabled", font=("Courier", 10))
        self.resultado.pack(padx=10, pady=(0, 10))

    def ver(self):
        dni = self.dni.get().strip()
        ventas = self.gestor.ventas_por_dni(dni)
        if not ventas:
            texto_solo_lectura(self.resultado, f"No hay reservas para el DNI {dni}.")
            return
        lineas = [f"RESERVAS DE {ventas[0].nombre} ({dni.upper()})", ""]
        for v in ventas:
            estado = "DEVUELTA" if v.devuelto else "PENDIENTE"
            lineas += [f"Nº {v.id} · {estado}",
                       f"  {v.actividad} en {v.pais}, talla {v.talla}, {v.cantidad} persona(s)",
                       f"  Actividad: {de_iso(v.fecha_actividad)} · Reserva: {de_iso(v.fecha_venta)}",
                       f"  Pagado: {v.precio_total:.2f} €", ""]
        texto_solo_lectura(self.resultado, "\n".join(lineas))

    def devolver(self):
        dni = self.dni.get().strip()
        pendiente = self.gestor.ultima_reserva_pendiente(dni) if dni else None
        if pendiente is None:
            messagebox.showinfo("Devolución", f"El DNI «{dni}» no tiene reservas pendientes de "
                                "devolver.", parent=self)
            return
        if not messagebox.askyesno(
                "Devolución", f"¿Registrar la devolución de la reserva nº {pendiente.id} "
                f"({pendiente.cantidad} equipo(s) de {pendiente.actividad.lower()}, "
                f"talla {pendiente.talla}, {pendiente.pais})?", parent=self):
            return
        venta = self.gestor.procesar_devolucion(dni)
        messagebox.showinfo("Devolución", f"Reserva nº {venta.id} devuelta: el material vuelve "
                            f"al inventario de {venta.pais}.", parent=self)
        self.ver()

    def limpiar(self):
        self.dni.delete(0, tk.END)
        texto_solo_lectura(self.resultado, "")

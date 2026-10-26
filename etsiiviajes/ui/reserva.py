"""Reserva de equipo: comprueba stock, guarda la venta y genera factura e informe."""

import tkinter as tk
from datetime import date
from tkinter import messagebox

from tkcalendar import DateEntry

from ..config import ACTIVIDADES, BUCEO, FOTO_BUCEO, FOTO_ESQUI, TALLAS
from ..documentos import (aguas_de_pais, calcular_precio, generar_factura,
                          generar_informe_especies)
from ..gestor import GestorBasesDatos, StockInsuficiente
from ..modelos import Alquiler, Venta
from ..utils import abrir_archivo, de_iso
from .comun import campo, combo, foto_tk


class VentanaReserva(tk.Toplevel):
    def __init__(self, master, gestor: GestorBasesDatos):
        super().__init__(master)
        self.gestor = gestor
        self.precio_unitario: float | None = None
        self.venta: Venta | None = None
        self.title("Reserva")
        self.resizable(False, False)

        f = tk.Frame(self)
        f.grid(row=0, column=0, padx=10, pady=10, sticky="n")
        self.actividad = campo(f, 0, "Actividad:", combo(f, ACTIVIDADES))
        self.pais = campo(f, 1, "País:", combo(f, [], ancho=30))
        self.talla = campo(f, 2, "Talla:", combo(f, TALLAS, inicial="M"))
        self.cantidad = campo(f, 3, "Personas:", tk.Spinbox(f, from_=1, to=20, width=5))
        self.fecha = campo(f, 4, "Fecha de actividad:", DateEntry(
            f, date_pattern="dd/mm/yyyy", locale="es_ES", mindate=date.today()))
        self.dni = campo(f, 5, "DNI del cliente:", tk.Entry(f))
        tk.Button(f, text="Buscar cliente", command=self.buscar_cliente).grid(row=5, column=2, padx=5)
        self.nombre = campo(f, 6, "Nombre:", tk.Entry(f, state="readonly"))
        self.email = campo(f, 7, "Email:", tk.Entry(f, state="readonly"))
        self.precio = campo(f, 8, "Precio por persona:", tk.Entry(f, state="readonly"))

        for widget in (self.actividad, self.pais, self.talla):
            widget.bind("<<ComboboxSelected>>", lambda _e: self._datos_cambiados())
        self.actividad.bind("<<ComboboxSelected>>", lambda _e: self._cargar_paises(), add="+")
        self.fecha.bind("<<DateEntrySelected>>", lambda _e: self._datos_cambiados())
        self._cargar_paises()

        b = tk.Frame(f)
        b.grid(row=9, column=0, columnspan=3, pady=10)
        tk.Button(b, text="Precio estimado", width=16, command=self.estimar_precio).grid(row=0, column=0, padx=4, pady=3)
        tk.Button(b, text="Registrar reserva", width=16, command=self.registrar).grid(row=0, column=1, padx=4, pady=3)
        self.boton_factura = tk.Button(b, text="Imprimir factura", width=16, state="disabled",
                                       command=self.factura)
        self.boton_factura.grid(row=1, column=0, padx=4, pady=3)
        self.boton_informe = tk.Button(b, text="Información país", width=16, state="disabled",
                                       command=self.informe)
        self.boton_informe.grid(row=1, column=1, padx=4, pady=3)
        tk.Button(b, text="Nueva reserva", width=16, command=self.limpiar).grid(row=2, column=0, columnspan=2, pady=3)

        fotos = tk.Frame(self)
        fotos.grid(row=0, column=1, padx=10, pady=10)
        self._fotos = []
        for ruta in (FOTO_BUCEO, FOTO_ESQUI):
            if ruta.exists():
                imagen = foto_tk(ruta, (300, 230), master=self)
                self._fotos.append(imagen)
                tk.Label(fotos, image=imagen).pack(pady=4)

    # ---------------------------------------------------------------- acciones

    def _cargar_paises(self):
        paises = self.gestor.paises(self.actividad.get())
        self.pais.config(values=paises)
        self.pais.set("ESPAÑA" if "ESPAÑA" in paises else (paises[0] if paises else ""))

    def _datos_cambiados(self):
        """Si cambia la fecha o el producto, el precio hay que volver a calcularlo."""
        self.precio_unitario = None
        self._escribir(self.precio, "")

    @staticmethod
    def _escribir(entrada: tk.Entry, texto: str):
        entrada.config(state="normal")
        entrada.delete(0, tk.END)
        entrada.insert(0, texto)
        entrada.config(state="readonly")

    def buscar_cliente(self):
        dni = self.dni.get().strip()
        cliente = self.gestor.obtener_usuario(self.actividad.get(), dni) if dni else None
        if cliente is None:
            self._escribir(self.nombre, "")
            self._escribir(self.email, "")
            tipo = "buceador" if self.actividad.get() == BUCEO else "esquiador"
            messagebox.showwarning(
                "Cliente no encontrado",
                f"No hay ningún {tipo} con el DNI «{dni}». Regístralo antes en "
                "Registro y consultas.", parent=self)
            return None
        self._escribir(self.nombre, cliente.nombre_completo)
        self._escribir(self.email, cliente.email)
        return cliente

    def estimar_precio(self):
        self.precio_unitario = calcular_precio(self.fecha.get_date())
        self._escribir(self.precio, f"{self.precio_unitario:.2f} €")

    def registrar(self):
        cliente = self.buscar_cliente()
        if cliente is None:
            return
        try:
            cantidad = int(self.cantidad.get())
            if cantidad <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Revisa los datos", "El número de personas debe ser un entero "
                                   "positivo.", parent=self)
            return
        if self.precio_unitario is None:
            self.estimar_precio()
        alquiler = Alquiler(
            dni=cliente.dni, nombre=cliente.nombre_completo, email=cliente.email,
            actividad=self.actividad.get(), pais=self.pais.get(), talla=self.talla.get(),
            cantidad=cantidad, fecha_actividad=self.fecha.get_date().isoformat(),
            precio_unitario=self.precio_unitario)
        resumen = (f"Cliente: {alquiler.nombre} ({alquiler.dni})\n"
                   f"Actividad: {alquiler.actividad} en {alquiler.pais}\n"
                   f"Fecha: {de_iso(alquiler.fecha_actividad)}\n"
                   f"Talla {alquiler.talla} · {cantidad} persona(s) × {alquiler.precio_unitario:.2f} €\n"
                   f"Total: {alquiler.precio_total:.2f} € (IVA incluido)")
        if not messagebox.askyesno("Confirmar reserva", resumen, parent=self):
            return
        try:
            self.venta = self.gestor.registrar_reserva(alquiler)
        except StockInsuficiente as error:
            messagebox.showerror("Sin stock", str(error), parent=self)
            return
        self.boton_factura.config(state="normal")
        self.boton_informe.config(state="normal")
        messagebox.showinfo("Reserva registrada",
                            f"Reserva nº {self.venta.id} registrada. Total: "
                            f"{self.venta.precio_total:.2f} €.", parent=self)

    def factura(self):
        if self.venta:
            abrir_archivo(generar_factura(self.venta))

    def informe(self):
        if not self.venta:
            return
        puntos = self.gestor.puntos_inmersion(self.venta.pais)
        especies = self.gestor.especies_en_aguas(aguas_de_pais(puntos))
        if not especies:
            messagebox.showinfo("Información país", "No hay puntos de inmersión registrados en "
                                f"{self.venta.pais.title()}.", parent=self)
            return
        abrir_archivo(generar_informe_especies(self.venta.nombre, self.venta.pais, especies))

    def limpiar(self):
        self.venta = None
        self.boton_factura.config(state="disabled")
        self.boton_informe.config(state="disabled")
        self.dni.delete(0, tk.END)
        for entrada in (self.nombre, self.email):
            self._escribir(entrada, "")
        self._datos_cambiados()

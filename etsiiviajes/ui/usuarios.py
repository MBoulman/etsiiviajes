"""Alta, consulta y baja de buceadores y esquiadores (una sola ventana para ambos)."""

import tkinter as tk
from datetime import date
from tkinter import filedialog, messagebox, ttk

from tkcalendar import DateEntry

from ..config import BUCEO, NIVELES, TIPOS_CLUB
from ..gestor import GestorBasesDatos
from ..modelos import Buzo, Esquiador
from ..utils import de_iso, imagen_a_bytes, validar_documento, validar_email
from .comun import campo, combo, foto_tk, poner_icono

TEXTOS = {
    BUCEO: {"titulo": "Buzos", "nivel": "Tipo de buzo:", "icono": "buzo", "clase": Buzo},
    "ESQUI": {"titulo": "Esquiadores", "nivel": "Tipo de esquiador:", "icono": "esquiador",
              "clase": Esquiador},
}


class VentanaUsuarios(tk.Toplevel):
    def __init__(self, master, gestor: GestorBasesDatos, actividad: str):
        super().__init__(master)
        self.gestor = gestor
        self.actividad = actividad
        self.textos = TEXTOS[actividad]
        self.foto: bytes | None = None
        self.title(self.textos["titulo"])
        poner_icono(self, self.textos["icono"])

        izquierda = tk.Frame(self)
        izquierda.grid(row=0, column=0, padx=10, pady=10, sticky="n")
        ttk.Separator(self, orient="vertical").grid(row=0, column=1, sticky="ns", pady=10)
        derecha = tk.Frame(self)
        derecha.grid(row=0, column=2, padx=10, pady=10, sticky="n")
        self._formulario(izquierda)
        self._consulta(derecha)

    # ---------------------------------------------------------------- alta

    def _formulario(self, marco):
        self.entradas = {}
        etiquetas = [("dni", "DNI / pasaporte:"), ("nombre", "Nombre:"), ("apellidos", "Apellidos:")]
        for fila, (clave, texto) in enumerate(etiquetas):
            self.entradas[clave] = campo(marco, fila, texto, tk.Entry(marco))
        self.fecha = campo(marco, 3, "Fecha de nacimiento:", DateEntry(
            marco, date_pattern="dd/mm/yyyy", locale="es_ES", year=1990, maxdate=date.today()))
        etiquetas = [("nacionalidad", "Nacionalidad:"), ("peso", "Peso (kg):"),
                     ("altura", "Altura (cm):"), ("telefono", "Teléfono:"),
                     ("email", "Correo electrónico:"), ("direccion", "Dirección:")]
        for fila, (clave, texto) in enumerate(etiquetas, start=4):
            self.entradas[clave] = campo(marco, fila, texto, tk.Entry(marco))
        self.club = campo(marco, 10, "Tipo de club:", combo(marco, TIPOS_CLUB))
        self.nivel = campo(marco, 11, self.textos["nivel"], combo(marco, NIVELES[self.actividad]))
        self.enfermedad = campo(marco, 12, "Enfermedad:", combo(marco, ("NO", "SI")))
        tk.Label(marco, text="Foto:").grid(row=13, column=0, padx=5, pady=4, sticky="w")
        tk.Button(marco, text="Cargar foto", command=self.cargar_foto).grid(
            row=13, column=1, padx=5, sticky="w")
        self.miniatura = tk.Label(marco)
        self.miniatura.grid(row=13, column=2, padx=5)

        botones = tk.Frame(marco)
        botones.grid(row=14, column=0, columnspan=3, pady=10)
        for texto, accion in (("Guardar", self.guardar), ("Limpiar", self.limpiar),
                              ("Salir", self.destroy)):
            tk.Button(botones, text=texto, command=accion, width=9).pack(side=tk.LEFT, padx=5)

    def cargar_foto(self):
        ruta = filedialog.askopenfilename(
            parent=self, title="Seleccionar foto",
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg"), ("Todos los archivos", "*.*")])
        if not ruta:
            return
        try:
            self.foto = imagen_a_bytes(ruta, lado_max=400)
        except OSError:
            messagebox.showerror("Foto", "No se ha podido abrir la imagen.", parent=self)
            return
        imagen = foto_tk(self.foto, (80, 80), master=self)
        self.miniatura.config(image=imagen)
        self.miniatura.image = imagen

    def _leer_formulario(self):
        """Devuelve el usuario del formulario o lanza ValueError con el primer error."""
        datos = {clave: e.get().strip() for clave, e in self.entradas.items()}
        if not validar_documento(datos["dni"]):
            raise ValueError("El DNI/NIE no es válido (revisa la letra) o el pasaporte "
                             "no tiene entre 6 y 12 letras y números.")
        if not datos["nombre"]:
            raise ValueError("El nombre es obligatorio.")
        for clave, minimo, maximo in (("peso", 20, 250), ("altura", 100, 250)):
            try:
                valor = int(datos[clave])
            except ValueError:
                raise ValueError(f"El campo {clave} debe ser un número entero.") from None
            if not minimo <= valor <= maximo:
                raise ValueError(f"El campo {clave} debe estar entre {minimo} y {maximo}.")
            datos[clave] = valor
        if datos["email"] and not validar_email(datos["email"]):
            raise ValueError("El correo electrónico no es válido.")
        return self.textos["clase"](
            dni=datos["dni"].upper(), nombre=datos["nombre"].upper(),
            apellidos=datos["apellidos"].upper(),
            fecha_nacimiento=self.fecha.get_date().isoformat(),
            nacionalidad=datos["nacionalidad"].upper(), peso=datos["peso"],
            altura=datos["altura"], telefono=datos["telefono"], email=datos["email"],
            direccion=datos["direccion"], tipo_club=self.club.get(), nivel=self.nivel.get(),
            enfermedad=self.enfermedad.get(), foto=self.foto)

    def guardar(self):
        try:
            usuario = self._leer_formulario()
        except ValueError as error:
            messagebox.showwarning("Revisa los datos", str(error), parent=self)
            return
        if self.gestor.guardar_usuario(usuario):
            messagebox.showinfo("Guardado", f"{usuario.nombre_completo} se ha registrado.",
                                parent=self)
            self.limpiar()
        else:
            messagebox.showerror("Ya existe", f"Ya hay un cliente con el DNI {usuario.dni}.",
                                 parent=self)

    def limpiar(self):
        for entrada in self.entradas.values():
            entrada.delete(0, tk.END)
        for desplegable in (self.club, self.nivel, self.enfermedad):
            desplegable.current(0)
        self.foto = None
        self.miniatura.config(image="")

    # ------------------------------------------------------------- consulta

    def _consulta(self, marco):
        tk.Label(marco, text="Buscar por DNI:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.dni_buscar = tk.Entry(marco)
        self.dni_buscar.grid(row=0, column=1, padx=5)
        tk.Button(marco, text="Buscar", command=self.buscar).grid(row=0, column=2, padx=5)

        self.tabla = ttk.Treeview(marco, columns=("valor",), height=14)
        self.tabla.heading("#0", text="Dato")
        self.tabla.heading("valor", text=f"Información del {self.textos['titulo'][:-1].lower()}")
        self.tabla.column("#0", width=150)
        self.tabla.column("valor", width=220)
        self.tabla.grid(row=1, column=0, columnspan=3, pady=5)
        self.foto_resultado = tk.Label(marco)
        self.foto_resultado.grid(row=2, column=0, columnspan=3)

        tk.Label(marco, text="Borrar por DNI:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.dni_borrar = tk.Entry(marco)
        self.dni_borrar.grid(row=3, column=1, padx=5)
        tk.Button(marco, text="Borrar", command=self.borrar).grid(row=3, column=2, padx=5)

    def buscar(self):
        dni = self.dni_buscar.get().strip()
        if not dni:
            messagebox.showwarning("Buscar", "Escribe un DNI.", parent=self)
            return
        u = self.gestor.obtener_usuario(self.actividad, dni)
        self.tabla.delete(*self.tabla.get_children())
        self.foto_resultado.config(image="")
        if u is None:
            messagebox.showinfo("Buscar", f"No hay ningún cliente con el DNI {dni}.", parent=self)
            return
        filas = [("DNI", u.dni), ("Nombre", u.nombre), ("Apellidos", u.apellidos),
                 ("Fecha de nacimiento", de_iso(u.fecha_nacimiento)),
                 ("Nacionalidad", u.nacionalidad), ("Peso", f"{u.peso} kg"),
                 ("Altura", f"{u.altura} cm"), ("Teléfono", u.telefono), ("Email", u.email),
                 ("Dirección", u.direccion), ("Tipo de club", u.tipo_club),
                 ("Nivel", u.nivel), ("Enfermedad", u.enfermedad)]
        for dato, valor in filas:
            # values debe ser una tupla: con una cadena, Tk la parte por los espacios
            self.tabla.insert("", tk.END, text=dato, values=(valor,))
        if u.foto:
            imagen = foto_tk(u.foto, (120, 120), master=self)
            self.foto_resultado.config(image=imagen)
            self.foto_resultado.image = imagen

    def borrar(self):
        dni = self.dni_borrar.get().strip()
        if not dni:
            messagebox.showwarning("Borrar", "Escribe un DNI.", parent=self)
            return
        if not messagebox.askyesno("Confirmar", f"¿Borrar al cliente con DNI {dni}?", parent=self):
            return
        if self.gestor.borrar_usuario(self.actividad, dni):
            messagebox.showinfo("Borrado", f"Cliente {dni} borrado.", parent=self)
            self.dni_borrar.delete(0, tk.END)
            self.tabla.delete(*self.tabla.get_children())
        else:
            messagebox.showinfo("Borrar", f"No hay ningún cliente con el DNI {dni}.", parent=self)

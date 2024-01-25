# Sofía Veldman Paniego
# Mohamed Boulman Mokhlis
# Juan del Junco Sampol

from GestorBaseDatos import *
from Esquiador import *
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os
from tkcalendar import DateEntry
from tkinter import font
from Esquiador import*
from tkinter import ttk
import base64
import io
ENFERMEDADES_OPC = ["SÍ", "NO"]
class InterfazEsquiador(tk.Tk):
    def __init__(self, gestor):
        super().__init__()
        self.title("Esquiadores")

        # Obtenemos la ruta de la carpeta actual del script
        script_folder = os.path.dirname(os.path.abspath(__file__))

        # Construimosla ruta completa del icono en la carpeta "icono"
        icon_folder = os.path.join(script_folder, "Iconos")
        icon_path = os.path.join(icon_folder, "Esquiador.ico")

        # Verificamos si el archivo de icono existe antes de intentar establecerlo
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)
        else:
            print(f"No se encontró el archivo de icono en la ruta: {icon_path}")

        self.gestor = gestor

        # Creamos dos marcos
        self.frame_izquierdo = tk.Frame(self)
        self.frame_derecho = tk.Frame(self)

        # Configuramos ambos marcos
        self.configurar_marco_izquierdo()
        self.configurar_marco_derecho()

        # Agregamos línea vertical entre que divide los marcos izquierdo y derecho
        self.canvas_line = tk.Canvas(self, width=2, height=500, bg="black")
        self.canvas_line.grid(row=0, column=1, rowspan=15)

        # Posicionamoa marcos en la ventana principal
        self.frame_izquierdo.grid(row=0, column=0, padx=10, pady=10)
        self.frame_derecho.grid(row=0, column=2, padx=10, pady=10)

    def configurar_marco_izquierdo(self):
        # Widgets en el marco izquierdo
        self.label_dni = tk.Label(self.frame_izquierdo, text="DNI:")
        self.entry_dni = tk.Entry(self.frame_izquierdo)

        self.label_nombre = tk.Label(self.frame_izquierdo, text="Nombre:")
        self.entry_nombre = tk.Entry(self.frame_izquierdo)

        self.label_apellidos = tk.Label(self.frame_izquierdo, text="Apellidos:")
        self.entry_apellidos = tk.Entry(self.frame_izquierdo)

        self.label_fecha_nacimiento = tk.Label(self.frame_izquierdo, text="Fecha de Nacimiento:")
        self.date_picker = DateEntry(self.frame_izquierdo, date_pattern="dd/mm/yyyy")

        self.label_nacionalidad = tk.Label(self.frame_izquierdo, text="Nacionalidad:")
        self.entry_nacionalidad = tk.Entry(self.frame_izquierdo)

        self.label_peso = tk.Label(self.frame_izquierdo, text="Peso (kg):")
        self.entry_peso = tk.Entry(self.frame_izquierdo)

        self.label_altura = tk.Label(self.frame_izquierdo, text="Altura(Cm):")
        self.entry_altura = tk.Entry(self.frame_izquierdo)

        self.label_tel = tk.Label(self.frame_izquierdo, text="Teléfono:")
        self.entry_tel = tk.Entry(self.frame_izquierdo)

        self.label_email = tk.Label(self.frame_izquierdo, text="Correo Electrónico:")
        self.entry_email = tk.Entry(self.frame_izquierdo)

        self.label_direccion = tk.Label(self.frame_izquierdo, text="Dirección:")
        self.entry_direccion = tk.Entry(self.frame_izquierdo)

        self.label_tipo_club = tk.Label(self.frame_izquierdo, text="Tipo de Club:")
        self.combo_tipo_club = ttk.Combobox(self.frame_izquierdo, values=["AMATEUR", "PROFESIONAL"])
        self.combo_tipo_club.set("AMATEUR")  

        self.label_foto = tk.Label(self.frame_izquierdo, text="Foto:")
        self.btn_cargar_foto = tk.Button(self.frame_izquierdo, text="Cargar Foto", command=self.cargar_foto)
        self.foto_path = None
        self.foto_label = tk.Label(self.frame_izquierdo)

        self.label_tipo_esquiador = tk.Label(self.frame_izquierdo, text="Tipo de Esquiador:")
        self.combo_tipo_esquiador = ttk.Combobox(self.frame_izquierdo, values=["ALPINO", "FONDO", "TRAVESÍA", "FREESTYLE", "FREERIDE"])
        self.combo_tipo_esquiador.set("ALPINO")  
        self.label_enfermedad = tk.Label(self.frame_izquierdo, text="Enfermedad:")
        self.combo_enfermedad = ttk.Combobox(self.frame_izquierdo, values=ENFERMEDADES_OPC)
        self.combo_enfermedad.set(ENFERMEDADES_OPC[1])
        self.btn_guardar = tk.Button(self.frame_izquierdo, text="Guardar", command=self.guardar_esquiador, font="bold")
        self.btn_limpiar = tk.Button(self.frame_izquierdo, text="Limpiar", command=self.limpiar_campos, font="bold")
        self.btn_salir = tk.Button(self.frame_izquierdo, text="Salir", command=self.destroy, font="bold")

        self.btn_guardar.grid(row=14, column=0, padx=5, pady=5, sticky='w', ipadx=10)
        self.btn_limpiar.grid(row=14, column=1, padx=5, pady=5, sticky='w', ipadx=10)
        self.btn_salir.grid(row=14, column=2, padx=5, pady=5, sticky='w', ipadx=10)


        # Posicionamos widgets en el marco izquierdo
        self.label_dni.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.entry_dni.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        self.label_nombre.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.entry_nombre.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.label_apellidos.grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.entry_apellidos.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.label_fecha_nacimiento.grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.date_picker.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        self.label_nacionalidad.grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.entry_nacionalidad.grid(row=4, column=1, padx=5, pady=5, sticky='w')
        self.label_peso.grid(row=5, column=0, padx=5, pady=5, sticky='w')
        self.entry_peso.grid(row=5, column=1, padx=5, pady=5, sticky='w')
        self.label_altura.grid(row=6, column=0, padx=5, pady=5, sticky='w')
        self.entry_altura.grid(row=6, column=1, padx=5, pady=5, sticky='w')
        self.label_tel.grid(row=7, column=0, padx=5, pady=5, sticky='w')
        self.entry_tel.grid(row=7, column=1, padx=5, pady=5, sticky='w')
        self.label_email.grid(row=8, column=0, padx=5, pady=5, sticky='w')
        self.entry_email.grid(row=8, column=1, padx=5, pady=5, sticky='w')
        self.label_direccion.grid(row=9, column=0, padx=5, pady=5, sticky='w')
        self.entry_direccion.grid(row=9, column=1, padx=5, pady=5, sticky='w')
        self.label_tipo_club.grid(row=10, column=0, padx=5, pady=5, sticky='w')
        self.combo_tipo_club.grid(row=10, column=1, padx=5, pady=5, sticky='w')
        self.label_foto.grid(row=11, column=0, padx=5, pady=5, sticky='w')
        self.btn_cargar_foto.grid(row=11, column=1, padx=5, pady=5, sticky='w')
        self.foto_label.grid(row=11, column=2, padx=5, pady=5, sticky='w')
        self.label_tipo_esquiador.grid(row=12, column=0, padx=5, pady=5, sticky='w')
        self.combo_tipo_esquiador.grid(row=12, column=1, padx=5, pady=5, sticky='w')
        self.label_enfermedad.grid(row=13, column=0, padx=5, pady=5, sticky='w')
        self.combo_enfermedad.grid(row=13, column=1, padx=5, pady=5, sticky='w')
        self.btn_guardar.grid(row=14, column=0, padx=5, pady=5, sticky='w')
        self.btn_limpiar.grid(row=14, column=1, padx=5, pady=5, sticky='w')
        self.btn_salir.grid(row=14, column=2, padx=5, pady=5, sticky='w')


    def configurar_marco_derecho(self):
        # Widgets en el marco derecho
        self.label_buscar_dni = tk.Label(self.frame_derecho, text="Buscar por DNI:")
        self.entry_buscar_dni = tk.Entry(self.frame_derecho)
        self.btn_buscar_esquiador = tk.Button(self.frame_derecho, text="Buscar", command=self.buscar_esquiador)
        self.label_resultado_busqueda = tk.Label(self.frame_derecho, text="Resultado de la búsqueda:")
        self.label_borrar_dni = tk.Label(self.frame_derecho, text="Borrar por DNI:")
        self.entry_borrar_dni = tk.Entry(self.frame_derecho)
        self.btn_borrar_esquiador = tk.Button(self.frame_derecho, text="Borrar", command=self.borrar_esquiador_por_dni)


        # Creamos Treeview para mostrar los resultados de la búsqueda en una tabla de dos columnas
        self.treeview_resultado = ttk.Treeview(self.frame_derecho)
        self.treeview_resultado['columns'] = ('Valor',)
        self.treeview_resultado.heading('#0', text='Datos')
        self.treeview_resultado.heading('Valor', text='Información Esquiador')

        # Posicionamos widgets en el marco derecho
        self.label_buscar_dni.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.entry_buscar_dni.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        self.btn_buscar_esquiador.grid(row=0, column=2, padx=5, pady=5, sticky='w')
        self.label_resultado_busqueda.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.treeview_resultado.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky='w', rowspan=10)
        self.label_borrar_dni.grid(row=12, column=0, padx=5, pady=5, sticky='w')
        self.entry_borrar_dni.grid(row=12, column=1, padx=5, pady=5, sticky='w')
        self.btn_borrar_esquiador.grid(row=12, column=2, padx=5, pady=5, sticky='w')

    def mostrar_resultado_busqueda(self, esquiador):
        # Limpiamos la tabla antes de mostrar nuevos resultados
        for item in self.treeview_resultado.get_children():
            self.treeview_resultado.delete(item)

        # Insertamos datos del esquiador en la tabla
        self.treeview_resultado.insert('', 'end', text='DNI', values=(esquiador.dni))
        self.treeview_resultado.insert('', 'end', text='Nombre', values=(esquiador.nombre))
        self.treeview_resultado.insert('', 'end', text='Nombre', values=(esquiador.apellidos))
        self.treeview_resultado.insert('', 'end', text='Fecha de Nacimiento', values=(esquiador.fecha_nacimiento))
        self.treeview_resultado.insert('', 'end', text='Nacionalidad', values=(esquiador.nacionalidad))
        self.treeview_resultado.insert('', 'end', text='Peso', values=(f"{esquiador.peso} kg"))
        self.treeview_resultado.insert('', 'end', text='Altura', values=(f"{esquiador.altura} cm"))
        self.treeview_resultado.insert('', 'end', text='Teléfono', values=(esquiador.tel))
        self.treeview_resultado.insert('', 'end', text='Email', values=(esquiador.email))
        self.treeview_resultado.insert('', 'end', text='Dirección', values=(esquiador.direccion))
        self.treeview_resultado.insert('', 'end', text='Tipo de Club', values=(esquiador.tipo_club))
        self.treeview_resultado.insert('', 'end', text='Tipo de Esquiador', values=(esquiador.tipo_esquiador))
        self.treeview_resultado.insert('', 'end', text='Enfermedad', values=(esquiador.enfermedad))


    def cargar_foto(self):
        file_path = filedialog.askopenfilename(title="Seleccionar Foto", filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.foto_path = file_path
            self.mostrar_foto()

    def mostrar_foto(self):
        if self.foto_path:
            imagen = Image.open(self.foto_path)
            imagen = imagen.resize((100, 100), resample=Image.BICUBIC)

            foto = ImageTk.PhotoImage(imagen)
            self.foto_label.config(image=foto)
            self.foto_label.image = foto

    def guardar_esquiador(self):
        dni = self.entry_dni.get()
        nombre = self.entry_nombre.get()
        apellidos = self.entry_apellidos.get()
        fecha_nacimiento = self.date_picker.get()
        nacionalidad = self.entry_nacionalidad.get()
        peso = int(self.entry_peso.get())
        altura = int(self.entry_altura.get())
        tel = int(self.entry_tel.get())
        email = self.entry_email.get()
        direccion = self.entry_direccion.get()
        tipo_club = self.combo_tipo_club.get()
        tipo_esquiador = self.combo_tipo_esquiador.get()
        enfermedad = self.combo_enfermedad.get()

        esquiador = Esquiador(dni=dni, nombre=nombre, apellidos=apellidos, fecha_nacimiento=fecha_nacimiento,
                    nacionalidad=nacionalidad, peso=peso, altura=altura, tel=tel, email=email,
                    direccion=direccion, tipo_club=tipo_club, tipo_esquiador=tipo_esquiador, enfermedad=enfermedad,
                    foto=self.foto_path)

        self.gestor.guardar_esquiador(esquiador)

        messagebox.showinfo("Éxito", "Esquiador guardado correctamente.")

        # Limpiamos campos después de guardar el esquiador
        self.limpiar_campos()

    def limpiar_campos(self):
        self.entry_dni.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)
        self.entry_apellidos.delete(0, tk.END)
        self.date_picker.delete(0, tk.END)
        self.entry_nacionalidad.delete(0, tk.END)
        self.entry_peso.delete(0, tk.END)
        self.entry_altura.delete(0, tk.END)
        self.entry_tel.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_direccion.delete(0, tk.END)
        self.combo_tipo_club.set("AMATEUR")
        self.combo_tipo_esquiador.set("ALPINO")
        self.combo_enfermedad.set(ENFERMEDADES_OPC[1])
        self.foto_label.config(image=None)

    def buscar_esquiador(self):
        dni_buscar = self.entry_buscar_dni.get()
        if dni_buscar:
            esquiador_encontrado = self.gestor.mostrar_esquiador_por_dni(dni_buscar)
            if esquiador_encontrado:
                self.mostrar_resultado_busqueda(esquiador_encontrado)
            else:
                messagebox.showinfo("Búsqueda", f"No se encontró ningún esquiador con el DNI {dni_buscar}.")
        else:
            messagebox.showwarning("Advertencia", "Ingrese un DNI para buscar.")

    def borrar_esquiador_por_dni(self):
        dni_borrar = self.entry_borrar_dni.get()
        if dni_borrar:
            confirmacion = messagebox.askyesno("Confirmación", f"¿Estás seguro de que quieres borrar el esquiador con DNI {dni_borrar}?")
            if confirmacion:
                esquiador_borrado = self.gestor.borrar_esquiador_por_dni(dni_borrar)
                if esquiador_borrado:
                    messagebox.showinfo("Éxito", f"Esquiador con DNI {dni_borrar} borrado correctamente.")
                    # Limpiar campos después de borrar el esquiador
                    self.limpiar_campos()
                    self.limpiar_resultado_busqueda()

        else:
            messagebox.showwarning("Advertencia", "Ingrese un DNI para borrar.")

    def limpiar_resultado_busqueda(self):
        # Limpiamos la tabla de resultados
        for item in self.treeview_resultado.get_children():
            self.treeview_resultado.delete(item)



if __name__ == "__main__":
    gestor = GestorBasesDatos()
    app = InterfazEsquiador(gestor)
    app.mainloop()

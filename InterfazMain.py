
# Sofía Veldman Paniego
# Mohamed Boulman Mokhlis
# Juan del Junco Sampol

import tkinter as tk
from tkcalendar import Calendar
from datetime import datetime
from PIL import Image, ImageTk
import os
import random
import math
import subprocess
from Agenda import*

class ElementosReserva(tk.Canvas):
    def __init__(self,master, **kwargs):
        tk.Canvas.__init__(self,master, **kwargs)
        self.crear_botones()

    def abrir_ayuda(self):
        subprocess.Popen(["python", "InterfazAyuda.py"])

    def abrir_estadistica(self):
        subprocess.Popen(["python", "Interfaz_Estadistica.py"])

    def abrir_registro(self):
        subprocess.Popen(["python", "InterfazRegistroyConsultas.py"])

    def abrir_mapa(self):
        subprocess.Popen(["python", "Interfaz_mapa.py"])

    def crear_botones(self):
        btn1 = tk.Button(self, text="Registro y Consultas", font=('calibri', 12),command=self.abrir_registro)
        btn2 = tk.Button(self, text="Mapa", font=('calibri', 12),command=self.abrir_mapa)
        btn3 = tk.Button(self, text="Estadísticas", font=('calibri', 12),command=self.abrir_estadistica)
        btn4 = tk.Button(self, text="Ayuda", font=('calibri', 12),command=self.abrir_ayuda)

        btn1.pack(fill=tk.X, padx=10, pady=5)
        btn2.pack(fill=tk.X, padx=10, pady=5)
        btn3.pack(fill=tk.X, padx=10, pady=5)
        btn4.pack(fill=tk.X, padx=10, pady=5)

class InterfazReserva:

    def __init__(self, ventana):


        self.ventana = ventana
        self.ventana.title("")
        self.carpeta_imagenes = "C:\\Users\\Mohamed\\Desktop\\Trabajo Python\\Código\\Bases_datos\\Bases_datos\\Fotos FF"
        ancho_ventana = 1130
        alto_ventana = 630
        self.ventana.minsize(ancho_ventana, alto_ventana)
        self.ventana.maxsize(ancho_ventana, alto_ventana)

        ruta_icono = "C:\\Users\\Mohamed\\Desktop\\Trabajo Python\\Código\\Bases_datos\\Iconos\\Global.ico"
        self.ventana.iconbitmap(ruta_icono)

        frame_calendario = tk.Frame(self.ventana)
        frame_calendario.pack(pady=10, padx=10, anchor="ne")
        fecha_actual = datetime.now()
        year, month, day = fecha_actual.year, fecha_actual.month, fecha_actual.day
        

        calendario = Calendar(frame_calendario, selectmode="day", year=fecha_actual.year, month=fecha_actual.month, day=fecha_actual.day)
        calendario.pack(padx=10, pady=10)

        btn_Agenda = tk.Button(frame_calendario, text="Agenda", command=self.Agenda, font=('calibri', 15))
        btn_Agenda.pack(pady=10)

        self.lbl_fecha = tk.Label(frame_calendario, text="", font=('calibri', 12))
        self.lbl_fecha.pack(pady=10)

        contenedor_botones = tk.Frame(self.ventana, bg='#23BEBE')
        contenedor_botones.place(x=10, y=10)

        elementos_reserva = ElementosReserva(contenedor_botones)
        elementos_reserva.pack(pady=10)

        lbl_bienvenido = tk.Label(text="BIENVENIDO A LA INMERSIÓN", font=('calibri', 35, 'bold'))
        lbl_bienvenido.place(x=200, y=100)

        lbl_en_el_agua_y_nieve = tk.Label(text="EN EL AGUA Y EN LA NIEVE", font=('calibri', 12))
        lbl_en_el_agua_y_nieve.place(x=630, y=150)

        lbl_Frase1 = tk.Label(text="''El agua, testigo inmaculado de la crónica de la Tierra, guarda en sus", font=('calibri', 15))
        lbl_Frase1.place(x=200, y=200)
        lbl_Frase2 = tk.Label(text="  profundidades los misterios de la creación y el poder de transformar ", font=('calibri', 15))
        lbl_Frase2.place(x=200, y=235)
        lbl_Frase3 = tk.Label(text="  los destinos de nuestro planeta.''", font=('calibri', 15))
        lbl_Frase3.place(x=200, y=265)

        lbl_autor = tk.Label(text="Jacques-Yves Cousteau", font=('calibri', 12))
        lbl_autor.place(x=630, y=270)



        self.img_files = [f for f in os.listdir(self.carpeta_imagenes) if f.endswith((".jpg", ".png"))]
        imagenes_seleccionadas = random.sample(self.img_files, min(5, len(self.img_files)))

        self.imagenes = []

        for i, img_file in enumerate(imagenes_seleccionadas):
            ruta_imagen = os.path.join(self.carpeta_imagenes, img_file)
            imagen_original = Image.open(ruta_imagen)

            if imagen_original.width > imagen_original.height:
                try:
                    orientacion = next(valor for etiqueta, valor in imagen_original._getexif().items() if etiqueta == 274)
                    if orientacion == 3:
                        imagen_original = imagen_original.rotate(180, expand=True)
                    elif orientacion == 6:
                        imagen_original = imagen_original.rotate(270, expand=True)
                    elif orientacion == 8:
                        imagen_original = imagen_original.rotate(90, expand=True)
                except (AttributeError, StopIteration):
                    pass

            imagen_redimensionada = imagen_original.resize((200, 200))
            imagen = ImageTk.PhotoImage(imagen_redimensionada)
            self.imagenes.append(imagen)

        contenedor_imagenes = tk.Frame(self.ventana)
        contenedor_imagenes.pack(expand=True, fill=tk.BOTH)

        self.etiquetas_imagen = []
        self.etiquetas_nombres = []

        for i, imagen in enumerate(self.imagenes):
            etiqueta_imagen = tk.Label(contenedor_imagenes, image=imagen)
            etiqueta_imagen.image = imagen
            etiqueta_imagen.grid(row=0, column=i, padx=10, pady=(5, 0))  
            self.etiquetas_imagen.append(etiqueta_imagen)

            nombre_archivo_sin_extension = os.path.splitext(imagenes_seleccionadas[i])[0]
            etiqueta_nombre = tk.Label(contenedor_imagenes, text=nombre_archivo_sin_extension, font=('calibri', 10))
            etiqueta_nombre.grid(row=1, column=i, padx=10, pady=(0, 5))  
            self.etiquetas_nombres.append(etiqueta_nombre)


        btn_reservar = tk.Button(frame_calendario, text="Reservar", command=self.reservar, font=('calibri', 15))
        btn_devolver = tk.Button(frame_calendario, text="Devolver", command=self.devolver, font=('calibri', 15))

        btn_reservar.pack(side=tk.LEFT, padx=(40, 0), pady=(0, 20))
        btn_devolver.pack(side=tk.LEFT, padx=(40, 0), pady=(0, 20))

        self.ventana.after(5000, self.cambiar_imagen)

    def Agenda(self):

        subprocess.Popen(["python", "Agenda.py"])


    def cambiar_imagen(self):
        
        nuevas_imagenes_seleccionadas = random.sample(self.img_files, min(5, len(self.img_files)))

        for i, img_file in enumerate(nuevas_imagenes_seleccionadas):
            ruta_imagen = os.path.join(self.carpeta_imagenes, img_file)
            imagen_original = Image.open(ruta_imagen)

            if imagen_original.width > imagen_original.height:
                try:
                    orientacion = next(valor for etiqueta, valor in imagen_original._getexif().items() if etiqueta == 274)
                    if orientacion == 3:
                        imagen_original = imagen_original.rotate(180, expand=True)
                    elif orientacion == 6:
                        imagen_original = imagen_original.rotate(270, expand=True)
                    elif orientacion == 8:
                        imagen_original = imagen_original.rotate(90, expand=True)
                except (AttributeError, StopIteration):
                    pass

            imagen_redimensionada = imagen_original.resize((200, 200))
            imagen = ImageTk.PhotoImage(imagen_redimensionada)
            self.imagenes[i] = imagen

            self.etiquetas_imagen[i].config(image=imagen)
            self.etiquetas_imagen[i].image = imagen

            nombre_archivo_sin_extension = os.path.splitext(img_file)[0]
            self.etiquetas_nombres[i].config(text=nombre_archivo_sin_extension)

        self.ventana.after(5000, self.cambiar_imagen)

    def reservar(self):
        subprocess.Popen(["python", "Boton_Reserva.py"])

    def devolver(self):
        subprocess.Popen(["python", "Boton_Devolver.py"])

if __name__ == "__main__":
    ventana = tk.Tk()
    app = InterfazReserva(ventana)
    ventana.mainloop()

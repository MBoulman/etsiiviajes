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

class ElementosReserva(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        tk.Canvas.__init__(self, master, **kwargs)
        self.dibujar_relojes()
        self.actualizar_horas()

    def dibujar_relojes(self):
        # Dibujar primer reloj con hora local
        self.create_oval(10, 10, 150, 150, width=2, outline='black', fill='#e0e0e0')
        for i in range(1, 13):
            angulo = math.radians(90 - i * 30)
            x = 80 + 60 * math.cos(angulo)
            y = 80 - 60 * math.sin(angulo)
            self.create_text(x, y, text=str(i), font=('calibri', 10, 'bold'))
        
        self.mano_horas = self.create_line(80, 80, 80, 35, width=4, fill='blue')
        self.mano_minutos = self.create_line(80, 80, 80, 30, width=2, fill='green')
        self.mano_segundos = self.create_line(80, 80, 80, 25, width=1, fill='red')

        # Dibujar segundo reloj con hora local + 4 horas
        self.create_oval(180, 10, 320, 150, width=2, outline='black', fill='#e0e0e0')
        for i in range(1, 13):
            angulo = math.radians(90 - i * 30)
            x = 250 + 60 * math.cos(angulo)
            y = 80 - 60 * math.sin(angulo)
            self.create_text(x, y, text=str(i), font=('calibri', 10, 'bold'))

        self.mano_horas_male = self.create_line(250, 80, 250, 75, width=4, fill='purple')
        self.mano_minutos_male = self.create_line(250, 80, 250, 70, width=2, fill='orange')
        self.mano_segundos_male = self.create_line(250, 80, 250, 65, width=1, fill='pink')

    def actualizar_horas(self):
        ahora = datetime.now()
        hora, minuto, segundo = ahora.hour, ahora.minute, ahora.second

        # Actualizar manecillas del primer reloj (hora local)
        angulo_horas = math.radians(90 - (hora % 12 + minuto / 60) * 30)
        angulo_minutos = math.radians(90 - minuto * 6)
        angulo_segundos = math.radians(90 - segundo * 6)

        self.coords(self.mano_horas, 80, 80, 80 + 25 * math.cos(angulo_horas), 80 - 25 * math.sin(angulo_horas))
        self.coords(self.mano_minutos, 80, 80, 80 + 35 * math.cos(angulo_minutos), 80 - 35 * math.sin(angulo_minutos))
        self.coords(self.mano_segundos, 80, 80, 80 + 45 * math.cos(angulo_segundos), 80 - 45 * math.sin(angulo_segundos))

        # Actualizar manecillas del segundo reloj (hora local + 4 horas)
        offset_horas = 4
        hora_male = (hora + offset_horas) % 12
        angulo_horas_male = math.radians(90 - (hora_male + minuto / 60) * 30)
        angulo_minutos_male = math.radians(90 - (minuto) * 6)
        angulo_segundos_male = math.radians(90 - (segundo) * 6)

        self.coords(self.mano_horas_male, 250, 80, 250 + 25 * math.cos(angulo_horas_male), 80 - 25 * math.sin(angulo_horas_male))
        self.coords(self.mano_minutos_male, 250, 80, 250 + 35 * math.cos(angulo_minutos_male), 80 - 35 * math.sin(angulo_minutos_male))
        self.coords(self.mano_segundos_male, 250, 80, 250 + 45 * math.cos(angulo_segundos_male), 80 - 45 * math.sin(angulo_segundos_male))

        self.after(1000, self.actualizar_horas)

class InterfazReserva:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Reservas y devoluciones")
        self.ventana.configure(bg="white")  
        self.carpeta_imagenes = "C:/Users/Mohamed/Desktop/Trabajo Python/Código/Bases_datos/Bases_datos/Fotos FF"
        ancho_ventana = 1130
        alto_ventana = 690

        frame_calendario = tk.Frame(self.ventana, bg="white") 
        frame_calendario.pack(pady=10, padx=10, anchor="ne")

        # Reducir el tamaño del Calendar
        cal = Calendar(frame_calendario, selectmode="day", year=2023, month=1, day=1, width=10, bg="white")  # Fondo blanco
        cal.pack(padx=10, pady=10)

        btn_obtener_fecha = tk.Button(frame_calendario, text="Obtener Fecha", command=self.obtener_fecha, font=('calibri', 12), bg="white")  # Fondo blanco
        btn_obtener_fecha.pack(pady=10)

        self.lbl_fecha = tk.Label(frame_calendario, text="", font=('calibri', 12), bg="white")  # Fondo blanco
        self.lbl_fecha.pack(pady=10)

        reloj_actual = ElementosReserva(ventana, width=150, height=150, bg="white")  # Fondo blanco
        reloj_actual.place(x=10, y=100)

        reloj_male = ElementosReserva(ventana, width=150, height=150, bg="white")  # Fondo blanco
        reloj_male.place(x=10, y=255)

        lbl_bienvenido = tk.Label(text="BIENVENIDO A LA INMERSIÓN", font=('calibri', 35, 'bold'), bg="white")  # Fondo blanco
        lbl_bienvenido.place(x=200, y=110)

        lbl_en_el_agua_y_nieve = tk.Label(text="EN EL AGUA Y EN LA NIEVE", font=('calibri', 12), bg="white")  # Fondo blanco
        lbl_en_el_agua_y_nieve.place(x=630, y=160)

        lbl_Frase1 = tk.Label(text="''El agua, testigo inmaculado de la crónica de la Tierra, guarda en sus", font=('calibri', 15), bg="white")  # Fondo blanco
        lbl_Frase1.place(x=200, y=200)
        lbl_Frase2 = tk.Label(text="  profundidades los misterios de la creación y el poder de transformar ", font=('calibri', 15), bg="white")  # Fondo blanco
        lbl_Frase2.place(x=200, y=235)
        lbl_Frase3 = tk.Label(text="  los destinos de nuestro planeta.''", font=('calibri', 15), bg="white")  # Fondo blanco
        lbl_Frase3.place(x=200, y=265)

        lbl_autor = tk.Label(text="Jacques-Yves Cousteau", font=('calibri', 12), bg="white")  # Fondo blanco
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
        contenedor_imagenes.configure(bg='white')
        contenedor_imagenes.pack(expand=True, fill=tk.BOTH)


        self.etiquetas_imagen = []
        self.etiquetas_nombres = []

        for i, imagen in enumerate(self.imagenes):
            etiqueta_imagen = tk.Label(contenedor_imagenes, image=imagen, bg="white")
            etiqueta_imagen.image = imagen
            etiqueta_imagen.grid(row=0, column=i, padx=10, pady=(30, 2))  
            self.etiquetas_imagen.append(etiqueta_imagen)

            nombre_archivo_sin_extension = os.path.splitext(imagenes_seleccionadas[i])[0]
            etiqueta_nombre = tk.Label(contenedor_imagenes, text=nombre_archivo_sin_extension, font=('calibri', 10), bg="white")
            etiqueta_nombre.grid(row=1, column=i, padx=10, pady=(10, 20)) 
            self.etiquetas_nombres.append(etiqueta_nombre)


        btn_reservar = tk.Button(frame_calendario, text="Reservar", command=self.reservar, font=('calibri', 15))
        btn_devolver = tk.Button(frame_calendario, text="Devolver", command=self.devolver, font=('calibri', 15))

        btn_reservar.pack(side=tk.LEFT, padx=(40, 0), pady=(0, 20))
        btn_devolver.pack(side=tk.LEFT, padx=(40, 0), pady=(0, 20))

        self.ventana.after(5000, self.cambiar_imagen)

    def obtener_fecha(self):
        fecha_seleccionada = cal.get_date()
        self.lbl_fecha.config(text=f"Fecha seleccionada: {fecha_seleccionada}")


    def cambiar_imagen(self):
        # Utiliza self.carpeta_imagenes en lugar de carpeta_imagenes
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
        pass

    def devolver(self):
        pass

if __name__ == "__main__":
    ventana = tk.Tk()
    app = InterfazReserva(ventana)
    ventana.mainloop()

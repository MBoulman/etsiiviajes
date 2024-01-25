# Sofía Veldman Paniego
# Mohamed Boulman Mokhlis
# Juan del Junco Sampol

import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import webbrowser
import subprocess
import time
class Mapa:
    def __init__(self, parent_frame, video_path, mapa_path):
        self.parent_frame = parent_frame
        self.frame = ttk.Frame(self.parent_frame)
        self.frame.pack(expand=True, fill="both")

        self.parent_frame.grid_rowconfigure(0, weight=1)
        self.parent_frame.grid_columnconfigure(0, weight=1)

        self.video_path = video_path
        self.mapa_path = mapa_path

        self.cap = cv2.VideoCapture(self.video_path)
        self.video_width = int(self.cap.get(3))
        self.video_height = int(self.cap.get(4))

        self.scaled_width = 800
        self.scaled_height = int(self.video_height * (self.scaled_width / self.video_width))

        self.canvas = tk.Canvas(self.frame, width=1130, height=630, bg="white")
        self.canvas.pack()

        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12), padding=10)
        style.configure("Toolbutton", font=("Arial", 12), padding=10, relief="flat", background="#d9d9d9")

        self.btn_abrir_mapa = ttk.Button(self.frame, text="Abrir Mapa", command=self.abrir_mapa, style="Toolbutton")
        self.btn_abrir_mapa.place(relx=0.5, rely=0.5, anchor='n')

        self.btn_ejecutar_mapamundi = ttk.Button(
        self.frame, text="Ejecutar MapaMundi", command=self.iniciar_carga, style="Toolbutton")
        self.btn_ejecutar_mapamundi.place(relx=0.5, rely=0.65, anchor='n')

        self.frame.after(100, self.reproducir_infinitamente)

    def abrir_mapa(self):
        webbrowser.open("file://" + self.mapa_path)

    def iniciar_carga(self):
        self.panel_carga = tk.Toplevel(self.frame)
        self.panel_carga.title("Actualizando...")

        # Barra de progreso
        self.barra_progreso = ttk.Progressbar(self.panel_carga, length=300, mode="determinate")
        self.barra_progreso.pack(padx=20, pady=20)

        screen_width = self.panel_carga.winfo_screenwidth()
        screen_height = self.panel_carga.winfo_screenheight()
        window_width = self.panel_carga.winfo_reqwidth()
        window_height = self.panel_carga.winfo_reqheight()
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        #La posición de la ventana
        self.panel_carga.geometry(f"+{x_position}+{y_position}")

        # Simulación de carga
        self.simular_carga(0)

    def simular_carga(self, paso):
        # Actualización la barra de progreso
        progreso_actual = (paso / 20) * 100
        self.barra_progreso["value"] = progreso_actual

        # Verificación si la simulación ha terminado
        if paso < 15:
            
            self.panel_carga.after(1000, lambda: self.simular_carga(paso + 1))
        else:
            self.panel_carga.destroy()
            ruta_script = r"C:\\Users\\Mohamed\\Desktop\Trabajo Python\\Código\\Bases_datos\\MapaMundi.py"
            subprocess.run(["python", "-m", "MapaMundi"])


    def reproducir_infinitamente(self):
        if self.cap.get(cv2.CAP_PROP_POS_FRAMES) == self.cap.get(cv2.CAP_PROP_FRAME_COUNT):
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        ret, frame = self.cap.read()

        if ret:
            frame = cv2.resize(frame, (self.scaled_width, self.scaled_height))
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img_tk = ImageTk.PhotoImage(Image.fromarray(frame_rgb))

            self.canvas.delete("all")

            x_position = (1130 - self.scaled_width) // 2
            y_position = (630 - self.scaled_height) // 2

            self.canvas.create_image(x_position, y_position, anchor=tk.NW, image=img_tk)
            self.canvas.img_tk = img_tk

        self.frame.after(100, self.reproducir_infinitamente)



# Inicio de la ventana principal
ventana_mapa = tk.Tk()
ventana_mapa.title("Mapa")

# Rutas 
video_path = "C:\\Users\\Mohamed\\Desktop\\Trabajo Python\\Código\\Bases_datos\\mapa-3d.mp4"
mapa_path = "C:\\Users\\Mohamed\\Desktop\\Trabajo Python\\Código\\Bases_datos\\mapa.html"
app = Mapa(ventana_mapa, video_path, mapa_path)

#Bucle
ventana_mapa.mainloop()
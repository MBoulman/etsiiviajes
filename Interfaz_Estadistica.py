# Sofía Veldman Paniego
# Mohamed Boulman Mokhlis
# Juan del Junco Sampol


import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os
from tkcalendar import DateEntry
from tkinter import font
from tkinter import ttk
import base64
import io
from EstadisticaBuzos import *
from EstadisticaEsqui import *
from EstadisticaVentas import *
from Estadisticaflorayfauna import *
from GestorBaseDatos import*
gestor=GestorBasesDatos()

class InterfazEstadistica(tk.Tk):
    def __init__(self, gestor):
        super().__init__()
        self.title("Estadisticas")        
        ruta_icono = "C:\\Users\\Mohamed\\Desktop\\Trabajo Python\\Código\\Bases_datos\\Iconos\\Estadisticas.ico"
        self.iconbitmap(ruta_icono)
        self.gestor = gestor
        self.option_add('TLabel', {'font': ('Arial', 20)})
        self.configure_window_size() 

       
        self.frames = [[tk.Frame(self) for _ in range(2)] for _ in range(2)]

        self.configure_frames()

    def configure_window_size(self):
        self.geometry("1130x619")

    def configure_frames(self):

############Marco 1

        self.frames[0][0].grid(row=0, column=0, padx=100, pady=(10,40))
        label = tk.Label(self.frames[0][0], text=f"BUZOS", font=("Arial", 12, "bold"))
        label.pack()

        def on_click_boton1():
            self.result_display_1.delete("1.0", tk.END)
            resultado=round(media_edad(),2)
            self.result_display_1.insert(tk.END, resultado)

        def on_click_boton2():
            self.result_display_1.delete("1.0", tk.END)
            resultado=cuartiles()
            self.result_display_1.insert(tk.END, resultado)

        def on_click_boton3():
            self.result_display_1.delete("1.0", tk.END)
            resultado=max_nacionalidad()
            self.result_display_1.insert(tk.END, resultado)

        def on_click_boton4():
            self.result_display_1.delete("1.0", tk.END)
            resultado=nivel_buzo()
            self.result_display_1.insert(tk.END, resultado)

        def on_click_boton5():
            self.result_display_1.delete("1.0", tk.END)
            resultado=cluster()
            self.result_display_1.insert(tk.END, resultado)


        button1 = tk.Button(self.frames[0][0], text=f"Media Edad",command=on_click_boton1)
        button1.pack()

        button2 = tk.Button(self.frames[0][0], text=f"Cuartiles",command=on_click_boton2)
        button2.pack()

        button3 = tk.Button(self.frames[0][0], text=f"Nacionalidades",command=on_click_boton3)
        button3.pack()

        button4 = tk.Button(self.frames[0][0], text=f"Nivel buzo",command=on_click_boton4)
        button4.pack()

        button5 = tk.Button(self.frames[0][0], text=f"Grupos Cluster",command=on_click_boton5)
        button5.pack()

        self.result_display_1 = tk.Text(self.frames[0][0], height=5, width=40)
        self.result_display_1.pack(pady=10)

#############Marco 2

        self.frames[0][1].grid(row=0, column=1, padx=(0,50), pady=(10,40))
        label = tk.Label(self.frames[0][1], text=f"ESQUIADORES", font=("Arial", 12, "bold"))
        label.pack()

        def on_click_boton6():
            self.result_display_2.delete("1.0", tk.END)
            resultado=round(media_edad_esqui(),2)
            self.result_display_2.insert(tk.END, resultado)

        def on_click_boton7():
            self.result_display_2.delete("1.0", tk.END)
            resultado=cuartiles_esqui()
            self.result_display_2.insert(tk.END, resultado)

        def on_click_boton8():
            self.result_display_2.delete("1.0", tk.END)
            resultado=max_nacionalidad_esqui()
            self.result_display_2.insert(tk.END, resultado)

        def on_click_boton9():
            self.result_display_2.delete("1.0", tk.END)
            resultado=nivel_esqui()
            self.result_display_2.insert(tk.END, resultado)

        def on_click_boton10():
            self.result_display_2.delete("1.0", tk.END)
            resultado=cluster_esqui()
            self.result_display_2.insert(tk.END, resultado)

        button6 = tk.Button(self.frames[0][1], text=f"Media Edad",command=on_click_boton6)
        button6.pack()

        button7 = tk.Button(self.frames[0][1], text=f"Cuartiles",command=on_click_boton7)
        button7.pack()

        button8 = tk.Button(self.frames[0][1], text=f"Nacionalidades",command=on_click_boton8)
        button8.pack()

        button9 = tk.Button(self.frames[0][1], text=f"Nivel esqui",command=on_click_boton9)
        button9.pack()

        button10 = tk.Button(self.frames[0][1], text=f"Grupos Cluster",command=on_click_boton10)
        button10.pack()

        self.result_display_2 = tk.Text(self.frames[0][1], height=5, width=40)
        self.result_display_2.pack(pady=10)


###########Marco 3

        self.frames[1][0].grid(row=1, column=0, padx=100, pady=(0,30))
        label = tk.Label(self.frames[1][0], text=f"VENTAS", font=("Arial", 12, "bold"))
        label.grid(row=0, column=0, padx=10, pady=10)

        def on_click_boton11():
            self.result_display_3.delete("1.0", tk.END)
            resultado=round(media_gasto(),2)
            self.result_display_3.insert(tk.END, resultado)

        def on_click_boton12():
            self.result_display_3.delete("1.0", tk.END)
            resultado=round(media_por_pais(),2)
            self.result_display_3.insert(tk.END, resultado)

        def on_click_boton13():
            self.result_display_3.delete("1.0", tk.END)
            resultado=ventas_por_actividad()
            self.result_display_3.insert(tk.END, resultado)

        def on_click_boton14():
            self.result_display_3.delete("1.0", tk.END)
            resultado=tallas_mas_vendidas()
            self.result_display_3.insert(tk.END, resultado)

        def on_click_boton15():
            talla=self.talla_seleccionada.get()
            pais=self.Pais_seleccionado.get()
            actividad=self.actividad_seleccionada.get()
            resultado = round(abs(predict_precio(talla, pais, actividad)), 2)

            self.result_display_3.delete("1.0", tk.END)
            self.result_display_3.insert(tk.END, resultado)


        button11 = tk.Button(self.frames[1][0], text=f"Gasto Medio",command=on_click_boton11)
        button11.grid(row=1, column=0, padx=10, pady=(5, 0),sticky="ew")

        button12 = tk.Button(self.frames[1][0], text=f"Media/Pais",command=on_click_boton12)
        button12.grid(row=1, column=1, padx=10, pady=(5, 0),sticky="ew")

        button13 = tk.Button(self.frames[1][0], text=f" Ventas/Actividad",command=on_click_boton13)
        button13.grid(row=2, column=0, padx=10, pady=(5, 0),sticky="ew")


        button14 = tk.Button(self.frames[1][0], text=f"Tallas",command=on_click_boton14)
        button14.grid(row=2, column=1, padx=10, pady=(5, 0),sticky="ew")

        # label_talla = tk.Label(self.frames[1][0], text="Talla:")
        # label_talla.grid(row=3, column=0, padx=10, pady=(3, 0))
        opciones_talla = ["XXS", "XS", "S", "M", "L", "XL"]

        # Variable para almacenar la talla seleccionada
        self.talla_seleccionada = tk.StringVar()

        # ComboBox para seleccionar la talla
        combo_talla = ttk.Combobox(self.frames[1][0], textvariable=self.talla_seleccionada, values=opciones_talla)
        combo_talla.grid(row=3, column=1, padx=10, pady=(3, 0))
        combo_talla.set("Selecciona una talla")
        # Etiqueta
        label_talla = tk.Label(self.frames[1][0], text="Talla:")
        label_talla.grid(row=3, column=0, padx=10, pady=(3, 0))

        # Configuración adicional (si es necesario)
        combo_talla.config(state="readonly")  # Para hacer el ComboBox de solo lectura

        label_pais = tk.Label(self.frames[1][0], text="País:")
        label_pais.grid(row=4, column=0, padx=10, pady=(3, 0))

        # Lista de opciones para el ComboBox
        opciones_actividad = ["ESQUIAR", "BUCEO"]

        # Variable para almacenar la opción seleccionada
        self.actividad_seleccionada = tk.StringVar()

        # ComboBox para seleccionar la actividad
        combo_actividad = ttk.Combobox(self.frames[1][0], textvariable=self.actividad_seleccionada, values=opciones_actividad)
        combo_actividad.grid(row=5, column=1, padx=10, pady=(3, 0))
        combo_actividad.set("Selecciona una actividad")
        # Etiqueta
        label_actividad = tk.Label(self.frames[1][0], text="Actividad:")
        label_actividad.grid(row=5, column=0, padx=10, pady=(3, 0))

        # Configuración adicional (si es necesario)
        combo_actividad.config(state="readonly")  # Para hacer el ComboBox de solo lectura


        # self.entry_talla = tk.Entry(self.frames[1][0])
        # self.entry_talla.grid(row=3, column=1, padx=10, pady=(3, 0))

        self.Pais_seleccionado = tk.StringVar()

        paises_unicos = self.gestor.PaisesVenta()
        self.combobox_paises = ttk.Combobox(self.frames[1][0], textvariable=self.Pais_seleccionado, values=paises_unicos)

        self.combobox_paises.set("Selecciona un país")  # Texto predeterminado en el Combobox
        self.combobox_paises.grid(row=4, column=1, padx=10, pady=(5, 0))

        # self.entry_actividad = tk.Entry(self.frames[1][0])
        # self.entry_actividad.grid(row=5, column=1, padx=10, pady=(5, 0))

        button15 = tk.Button(self.frames[1][0], text=f"Predecir precio",command=on_click_boton15)
        button15.grid(row=6, column=0, columnspan=2, padx=10, pady=(5, 0),sticky="ew")

        self.result_display_3 = tk.Text(self.frames[1][0], height=5, width=40)
        self.result_display_3.grid(row=9, column=0, columnspan=2, padx=10, pady=10,sticky="nsew")

########Marco 4

        self.frames[1][1].grid(row=1, column=1, padx=(0,50), pady=(0,30))
        label = tk.Label(self.frames[1][1], text=f"FLORA Y FAUNA", font=("Arial", 12, "bold"))
        label.pack()

        def on_click_boton16():
            self.result_display_4.delete("1.0", tk.END)
            resultado=variedad_por_oceano()
            self.result_display_4.insert(tk.END, resultado)

        def on_click_boton17():
            self.result_display_4.delete("1.0", tk.END)
            oceano = self.entry_oceano.get().upper()
            resultado=flora_oceano(oceano)
            self.result_display_4.insert(tk.END, resultado)


        button16 = tk.Button(self.frames[1][1], text=f"Variedad/Oceano",command=on_click_boton16)
        button16.pack()

        self.entry_oceano = tk.Entry(self.frames[1][1])
        self.entry_oceano.pack()

        button17 = tk.Button(self.frames[1][1], text=f"Consultar Oceano",command=on_click_boton17)
        button17.pack()



        self.result_display_4 = tk.Text(self.frames[1][1], height=5, width=40)
        self.result_display_4.pack(pady=10)


if __name__ == "__main__":
    gestor=GestorBasesDatos()
    app = InterfazEstadistica(gestor)
    app.mainloop()

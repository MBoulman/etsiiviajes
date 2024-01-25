# Sofía Veldman Paniego
# Mohamed Boulman Mokhlis
# Juan del Junco Sampol

import tkinter as tk
from PIL import Image, ImageTk
from GestorBaseDatos import *
from fauna_y_flora import*
from tkinter import filedialog
import tkinter as tk
from io import BytesIO
import base64
from tkinter import filedialog, messagebox

class Interfaz_Fauna_y_Flora_Alta(tk.Tk):
    def __init__(self):
        super().__init__()
        self.gestor = GestorBasesDatos()  
        self.title("Alta Fauna y Flora")
        
        
        self.geometry("400x400")
        self.font = ("Helvetica", 12)

        self.label_nombre = tk.Label(self, text="Nombre:")
        self.label_tipo = tk.Label(self, text="Tipo:")
        self.label_atlantico = tk.Label(self, text="Atlántico:")
        self.label_pacifico = tk.Label(self, text="Pacífico:")
        self.label_indico = tk.Label(self, text="Índico:")
        self.label_mediterraneo = tk.Label(self, text="Mediterráneo:")
        self.label_caribe = tk.Label(self, text="Caribe:")
        self.label_mar_rojo = tk.Label(self, text="Mar Rojo:")
        self.label_indo_pacifico = tk.Label(self, text="Indo-Pacífico:")
        self.label_foto = tk.Label(self, text="Foto:")


        self.entry_nombre = tk.Entry(self, font=self.font)
        self.entry_tipo = tk.StringVar(self)
        self.entry_tipo.set("FLORA")  
        self.entry_tipo_menu = tk.OptionMenu(self, self.entry_tipo, "FLORA", "FAUNA")
        self.entry_atlantico = tk.StringVar(self)
        self.entry_atlantico.set("NO")  
        self.entry_pacifico = tk.StringVar(self)
        self.entry_pacifico.set("NO") 
        self.entry_indico = tk.StringVar(self)
        self.entry_indico.set("NO")  
        self.entry_mediterraneo = tk.StringVar(self)
        self.entry_mediterraneo.set("NO")  
        self.entry_caribe = tk.StringVar(self)
        self.entry_caribe.set("NO") 
        self.entry_mar_rojo = tk.StringVar(self)
        self.entry_mar_rojo.set("NO") 
        self.entry_indo_pacifico = tk.StringVar(self)
        self.entry_indo_pacifico.set("NO") 

        self.button_agregar = tk.Button(self, text="Agregar", command=self.agregar_fauna_flora, font=self.font)
        self.button_borrar = tk.Button(self, text="Borrar", command=self.borrar_campos, font=self.font)
        self.button_examinar = tk.Button(self, text="Examinar", command=self.examinar_foto, font=self.font)

        # Posicionamiento de widgets en la interfaz
        self.label_nombre.grid(row=0, column=0)
        self.label_tipo.grid(row=1, column=0)
        self.label_atlantico.grid(row=2, column=0)
        self.label_pacifico.grid(row=3, column=0)
        self.label_indico.grid(row=4, column=0)
        self.label_mediterraneo.grid(row=5, column=0)
        self.label_caribe.grid(row=6, column=0)
        self.label_mar_rojo.grid(row=7, column=0)
        self.label_indo_pacifico.grid(row=8, column=0)
        self.label_foto.grid(row=9, column=0)

        self.entry_nombre.grid(row=0, column=1)
        self.entry_tipo_menu.grid(row=1, column=1)
        tk.Label(self, text="").grid(row=2, column=1)  # Espacio en blanco
        tk.OptionMenu(self, self.entry_atlantico, "SI", "NO").grid(row=2, column=1)
        tk.OptionMenu(self, self.entry_pacifico, "SI", "NO").grid(row=3, column=1)
        tk.OptionMenu(self, self.entry_indico, "SI", "NO").grid(row=4, column=1)
        tk.OptionMenu(self, self.entry_mediterraneo, "SI", "NO").grid(row=5, column=1)
        tk.OptionMenu(self, self.entry_caribe, "SI", "NO").grid(row=6, column=1)
        tk.OptionMenu(self, self.entry_mar_rojo, "SI", "NO").grid(row=7, column=1)
        tk.OptionMenu(self, self.entry_indo_pacifico, "SI", "NO").grid(row=8, column=1)

        self.button_examinar.grid(row=9, column=1, pady=10)
        self.button_agregar.grid(row=10, column=0, padx=(100, 0), pady=10)
        self.button_borrar.grid(row=10, column=1, padx=(0,0), pady=10)

        self.foto_path = None

    def examinar_foto(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Seleccionar archivo", filetypes=(("Archivos de imagen", "*.png;*.jpg;*.jpeg;*.gif"), ("Todos los archivos", "*.*")))
        if filename:
            self.foto_path = filename

    def agregar_fauna_flora(self):
        nombre = self.entry_nombre.get()
        tipo = self.entry_tipo.get()
        atlantico = self.entry_atlantico.get()
        pacifico = self.entry_pacifico.get()
        indico = self.entry_indico.get()
        mediterraneo = self.entry_mediterraneo.get()
        caribe = self.entry_caribe.get()
        mar_rojo = self.entry_mar_rojo.get()
        indo_pacifico = self.entry_indo_pacifico.get()

        fauna_flora = fauna_y_flora(nombre.upper(), tipo, atlantico, pacifico, indico, mediterraneo, caribe, mar_rojo, indo_pacifico, foto=self.foto_path)
        self.gestor.agregar_fauna_y_flora(fauna_flora)
        messagebox.showinfo("Éxito", "Fauna/Flora agregado correctamente.")
        self.borrar_campos()

    def borrar_campos(self):
        # Borramos los campos y restablece opciones predeterminadas
        self.entry_nombre.delete(0, tk.END)
        self.entry_tipo.set("FLORA")
        self.entry_atlantico.set("NO")
        self.entry_pacifico.set("NO")
        self.entry_indico.set("NO")
        self.entry_mediterraneo.set("NO")
        self.entry_caribe.set("NO")
        self.entry_mar_rojo.set("NO")
        self.entry_indo_pacifico.set("NO")
        self.foto_path = None


if __name__ == "__main__":
    
    root = Interfaz_Fauna_y_Flora_Alta()
    root.mainloop()


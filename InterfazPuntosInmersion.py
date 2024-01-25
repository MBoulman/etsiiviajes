# Sofía Veldman Paniego
# Mohamed Boulman Mokhlis
# Juan del Junco Sampol

import tkinter as tk
from tkinter import filedialog, messagebox
from GestorBaseDatos import *
from Punto_de_inmersion import *
from PIL import Image, ImageTk
from io import BytesIO
import base64
from PIL import Image, ImageTk
from tkinter import ttk
gestor= GestorBasesDatos()
class InterfazPuntosInmersion(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Puntos de Inmersión")
        self.geometry("300x350")  
        self.label_nombre_agregar = tk.Label(self, text="Nombre:")
        self.entry_nombre_agregar = tk.Entry(self)
        self.label_pais = tk.Label(self, text="País:")
        self.entry_pais = tk.Entry(self)
        self.label_latitud = tk.Label(self, text="Latitud:")
        self.entry_latitud = tk.Entry(self)
        self.label_longitud = tk.Label(self, text="Longitud:")
        self.entry_longitud = tk.Entry(self)

        #lista de aguas
        opciones_aguas = ["Mar Mediterráneo", "Océano Atlántico", "Mar Rojo", "Océano Índico", "Indo-Pacífico", "Océano Pacífico", "Mar Caribe"]

        self.label_aguas = tk.Label(self, text="Aguas:")
        self.combo_aguas = ttk.Combobox(self, values=opciones_aguas)
        self.combo_aguas.set("Mar Mediterráneo")  #Mediterraneo como valor inicial
        self.label_profundidad = tk.Label(self, text="Profundidad:")
        self.entry_profundidad = tk.Entry(self)
        self.label_foto = tk.Label(self, text="Foto:")
        self.entry_foto = tk.Entry(self, state="readonly")

        #botones
        self.btn_seleccionar_foto = tk.Button(self, text="Seleccionar", command=self.seleccionar_foto)
        self.btn_agregar = tk.Button(self, text="Agregar", command=self.agregar_punto)
        self.btn_limpiar_agregar = tk.Button(self, text="Limpiar", command=self.limpiar_campos_agregar)

        # Posición de los widgets de agregar
        self.label_nombre_agregar.grid(row=0, column=0)
        self.entry_nombre_agregar.grid(row=0, column=1)
        self.label_pais.grid(row=1, column=0)
        self.entry_pais.grid(row=1, column=1)
        self.label_latitud.grid(row=2, column=0)
        self.entry_latitud.grid(row=2, column=1)
        self.label_longitud.grid(row=3, column=0)
        self.entry_longitud.grid(row=3, column=1)
        self.label_aguas.grid(row=4, column=0)
        self.combo_aguas.grid(row=4, column=1)
        self.label_profundidad.grid(row=5, column=0)
        self.entry_profundidad.grid(row=5, column=1)
        self.label_foto.grid(row=6, column=0)
        self.entry_foto.grid(row=6, column=1)
        self.btn_seleccionar_foto.grid(row=6, column=2)
        self.btn_agregar.grid(row=7, column=1, pady=10)
        self.btn_limpiar_agregar.grid(row=7, column=2, pady=10)


        # Campos de buscar/borrar
        self.label_nombre_buscar_borrar = tk.Label(self, text="Nombre:")
        self.entry_nombre_buscar_borrar = tk.Entry(self)

        self.btn_mostrar = tk.Button(self, text="Mostrar", command=self.mostrar_punto)
        self.btn_borrar = tk.Button(self, text="Eliminar", command=self.borrar_punto)

        # Posicion widgets de buscar/borrar
        self.label_nombre_buscar_borrar.grid(row=8, column=0)
        self.entry_nombre_buscar_borrar.grid(row=8, column=1)

        self.btn_mostrar.grid(row=11, column=1)
        self.btn_borrar.grid(row=11, column=2)

    def seleccionar_foto(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Seleccionar", filetypes=[("Archivos de Imagen", "*.png;*.jpg;*.jpeg")])
        self.entry_foto.config(state="normal")
        self.entry_foto.delete(0, tk.END)
        self.entry_foto.insert(0, filename)
        self.entry_foto.config(state="readonly")

    def agregar_punto(self):
        try:
            nombre = self.entry_nombre_agregar.get()
            pais = self.entry_pais.get()
            latitud = float(self.entry_latitud.get())
            longitud = float(self.entry_longitud.get())
            aguas = self.combo_aguas.get()  
            profundidad = float(self.entry_profundidad.get())
            foto = self.entry_foto.get()

            punto = Punto_de_inmersion(nombre, pais, latitud, longitud, aguas, profundidad, foto)

            gestor.agregar_punto_inmersion(punto)

            self.limpiar_campos_agregar()

            messagebox.showinfo("Éxito", "Punto de inmersión agregado correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar el punto de inmersión:\n{str(e)}")

    def mostrar_punto(self):
        try:
            nombre = self.entry_nombre_buscar_borrar.get()
            punto = gestor.mostrar_punto_inmersion_por_nombre(nombre)

            if punto:
                info_punto = (
                    f"NOMBRE           : {punto[0]}                   \n"
                    f"PAÍS             : {punto[1]}                   \n"
                    f"LATITUD          : {punto[2]}                   \n"
                    f"LONGITUD         : {punto[3]}                   \n"
                    f"AGUAS            : {punto[4]}                   \n"
                    f"PROFUNDIDAD  : {punto[5]} m                 \n"
                )

                # # Mostrar la imagen en un cuadro de imagen
                # img_data = punto[6]

                # try:
                #     img = Image.open(BytesIO(img_data))
                #     img.thumbnail((150, 150))  # Ajustar tamaño de la imagen
                #     img_tk = ImageTk.PhotoImage(img)
                #     image_label = tk.Label(self, image=img_tk)
                #     image_label.image = img_tk
                #     info_punto += "Foto:"
                #     image_label.grid(row=10, column=1, columnspan=2, pady=10)
                # except Exception as img_error:
                #     print(f"Error al mostrar la imagen: {str(img_error)}")

                messagebox.showinfo("Información del Punto de Inmersión", info_punto)
            else:
                messagebox.showinfo("Punto de Inmersión no encontrado", "El punto de inmersión no se encontró.")
        except Exception as e:
            messagebox.showerror("Error", f"Debe introducir todos los campos.\n{str(e)}")



    def borrar_punto(self):
            try:
                nombre = self.entry_nombre_buscar_borrar.get()

                # Preguntar al usuario si realmente desea eliminar el punto
                confirmacion = messagebox.askyesno("Confirmar eliminación", f"¿Estás seguro de que deseas eliminar el punto {nombre}?")

                if confirmacion:
                    gestor.borrar_punto_inmersion_por_nombre(nombre)
                    self.limpiar_campos_agregar()

                    messagebox.showinfo("Éxito", "Punto de inmersión eliminado correctamente")
                else:
                    messagebox.showinfo("Cancelado", "La eliminación del punto de inmersión fue cancelada.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar el punto de inmersión:\n{str(e)}")
                
    def limpiar_campos_agregar(self):
        self.entry_nombre_agregar.delete(0, tk.END)
        self.entry_pais.delete(0, tk.END)
        self.entry_latitud.delete(0, tk.END)
        self.entry_longitud.delete(0, tk.END)
        self.combo_aguas.set("Mar Mediterráneo")
        self.entry_profundidad.delete(0, tk.END)
        self.entry_foto.config(state="normal")
        self.entry_foto.delete(0, tk.END)
        self.entry_foto.config(state="readonly")
        self.entry_nombre_buscar_borrar.delete(0, tk.END)

if __name__ == "__main__":
    gestor= GestorBasesDatos()
    app = InterfazPuntosInmersion()
    app.mainloop()

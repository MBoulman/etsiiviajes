# Sofía Veldman Paniego
# Mohamed Boulman Mokhlis
# Juan del Junco Sampol

import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from io import BytesIO
from GestorBaseDatos import GestorBasesDatos
from fauna_y_flora import fauna_y_flora
from tkinter import messagebox
import os

gestor=GestorBasesDatos()
class Interfaz_Fauna_y_Flora(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Interfaz de Búsqueda")

        # Variables para almacenar el tipo de búsqueda y encabezado elegido
        self.tipo_busqueda = tk.StringVar(value="fauna_flora")  
        self.encabezado_elegido = tk.StringVar(value="ATLANTICO")  

        # Creamos widgets
        self.label_nombre = tk.Label(self, text="NOMBRE:")
        self.entry_nombre = tk.Entry(self)

        self.radio_fauna_flora = tk.Radiobutton(
            self, text="BUSCAR POR NOMBRE", variable=self.tipo_busqueda,
            value="fauna_flora", command=self.actualizar_campos,
            justify=tk.LEFT, anchor="w", padx=10
        )
        self.radio_por_aguas = tk.Radiobutton(
            self, text="BUSCAR POR AGUAS", variable=self.tipo_busqueda,
            value="por_aguas", command=self.actualizar_campos,
            justify=tk.LEFT, anchor="w", padx=8)

        # Menú desplegable para seleccionar el encabezado
        self.label_encabezado = tk.Label(self, text="AGUAS:")
        self.menu_encabezado = tk.OptionMenu(self, self.encabezado_elegido,
                                             *['ATLANTICO', 'PACIFICO', 'INDICO', 'MEDITERRANEO', 'CARIBE', 'MAR_ROJO',
                                               'INDO_PACIFICO'])
        self.menu_encabezado.grid_remove()  # Inicialmente oculto

        self.resultados_label = tk.Label(self, text="RESULTADOS:")
        self.resultados_label.grid(row=5, column=0, columnspan=1, pady=10)

        # Agregamos un widget Text con barra de desplazamiento horizontal
        self.resultados_text = tk.Text(self, height=8, width=40, wrap="none", state="disabled")
        self.resultados_text.grid(row=6, column=0, columnspan=3, pady=10)

        self.scrollbar_horizontal = tk.Scrollbar(self, orient="horizontal", command=self.resultados_text.xview)
        self.scrollbar_horizontal.grid(row=7, column=0, columnspan=3, sticky="ew")
        self.resultados_text.configure(xscrollcommand=self.scrollbar_horizontal.set)

        self.button_buscar = tk.Button(self, text="Buscar", command=self.realizar_busqueda)
        self.button_borrar = tk.Button(self, text="Limpiar", command=self.borrar_resultados)
        self.button_borrar_fauna = tk.Button(self, text="Eliminar", command=self.eliminar_fauna_y_flora)
        self.button_ver_imagen = tk.Button(self, text="Imagen", command=lambda: self.ver_imagen(self.entry_nombre.get()))



        # Posicionamos widgets
        self.label_nombre.grid(row=0, column=0, padx=10, pady=10)
        self.entry_nombre.grid(row=0, column=1, padx=10, pady=10)
        self.radio_fauna_flora.grid(row=1, column=0, columnspan=2, pady=5)
        self.radio_por_aguas.grid(row=2, column=0, columnspan=2, pady=5)

        # Posicionamos menú desplegable para el encabezado
        self.label_encabezado.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
        self.menu_encabezado.grid(row=3, column=1, padx=10, pady=10, sticky=tk.W)

        self.button_buscar.grid(row=4, column=0, padx=(10, 5))
        self.button_borrar.grid(row=4, column=1, padx=5)
        self.button_borrar_fauna.grid(row=4, column=2, padx=(5, 10))
        self.button_ver_imagen.grid(row=5, column=1, padx=5)
        self.actualizar_campos()



    def actualizar_campos(self):
        # Ocultar o mostrar el menú desplegable según el tipo de búsqueda seleccionado
        if self.tipo_busqueda.get() == "fauna_flora":
            self.label_encabezado.grid_remove()
            self.menu_encabezado.grid_remove()
        elif self.tipo_busqueda.get() == "por_aguas":
            self.label_encabezado.grid()
            self.menu_encabezado.grid()


    def realizar_busqueda(self):
        nombre = self.entry_nombre.get()

        if self.tipo_busqueda.get() == "fauna_flora":
            resultado = gestor.buscar_fauna_y_flora_por_nombre(nombre.upper())
            self.mostrar_resultados(resultado)

        elif self.tipo_busqueda.get() == "por_aguas":
            encabezado_elegido = self.encabezado_elegido.get()
            resultado = gestor.buscar_por_nombre_y_aguas(nombre.upper(),encabezado_elegido.upper())
            self.mostrar_resultados(resultado)

    def borrar_resultados(self):
        self.resultados_text.config(state="normal")
        self.resultados_text.delete(1.0, tk.END)
        self.resultados_text.config(state="disabled")
        self.entry_nombre.delete(0, tk.END)

    def eliminar_fauna_y_flora(self):
        

        nombre = self.entry_nombre.get()
        confirmacion = messagebox.askyesno("Confirmación", f"¿Estás seguro que deseas borrar {nombre}?")

        if confirmacion:
            # Metodo para borrar fauna y flora por nombre en el gestor de bases de datos
            gestor.borrar_fauna_y_flora_por_nombre(nombre.upper())

            # Limpia la entrada después de borrar
            self.entry_nombre.delete(0, tk.END)

    
            print(f"Fauna y flora {nombre} borrada correctamente")

    def mostrar_resultados(self, resultado):
        if resultado:
            if self.tipo_busqueda.get() == "por_aguas":  # Resultado de buscar_fauna_y_flora_por_nombre y por aguas
                respuesta=resultado
                resultados_texto = f"Presencia: {respuesta}\n"

            elif self.tipo_busqueda.get() == "fauna_flora":  # Resultado de fauna_flora por nombre
                tipo, encabezados_con_si= resultado
                resultados_texto = f"TIPO : {tipo}\nAGUAS:"
                resultados_texto += "\n      "
                resultados_texto += "\n      ".join(str(item) for item in encabezados_con_si)
            else:
                raise ValueError("El resultado no tiene la estructura esperada.")


            self.resultados_text.config(state="normal")
            self.resultados_text.delete(1.0, tk.END)
            self.resultados_text.insert(tk.END, resultados_texto)
            self.resultados_text.config(state="disabled")

    def ver_imagen(self, nombre):
        #Busca la imagen en la carpeta por nombre
        carpeta_imagenes = 'C:\\Users\\Mohamed\\Desktop\\Trabajo Python\\Código\\Bases_datos\\Bases_datos\\Fotos FF'

        # Construye la ruta de la imagen
        ruta_imagen = os.path.join(carpeta_imagenes, f'{nombre}.jpg')

        # Verfica si el archivo existe
        if os.path.exists(ruta_imagen):

            # Creamos la nueva ventana para mostrar la imagen
            ventana_imagen = tk.Toplevel(self)
            
            # Configura el título de la ventana con el nombre correspondiente
            ventana_imagen.title(nombre.upper())

            # Carga la imagen desde el archivo
            imagen_original = Image.open(ruta_imagen)

            # Redimensiona la imagen a 250x250
            imagen_redimensionada = imagen_original.resize((250, 250), Image.ANTIALIAS)

            # Convversión de la imagen redimensionada para que pueda ser mostrada
            imagen_tk = ImageTk.PhotoImage(imagen_redimensionada)

            # Creación del widget Label para mostrar la imagen
            etiqueta_imagen = tk.Label(ventana_imagen)
            etiqueta_imagen.image = imagen_tk  
            etiqueta_imagen.configure(image=imagen_tk)

            # Posiciona el widget Label en la ventana
            etiqueta_imagen.pack()

            # Cierra la ventana cuando se hace clic en la imagen
            etiqueta_imagen.bind("<Button-1>", lambda event: ventana_imagen.destroy())

            # Bucle principal de la ventana
            ventana_imagen.mainloop()
        else:
            # Muestra un mensaje si el archivo no se encuentra
            messagebox.showinfo("Error", f"La imagen para '{nombre}' no se encontró en la carpeta de imágenes.")


if __name__ == "__main__":
    gestor = GestorBasesDatos() 
    app = Interfaz_Fauna_y_Flora()
    app.mainloop()

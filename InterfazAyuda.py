# Sofía Veldman Paniego
# Mohamed Boulman Mokhlis
# Juan del Junco Sampol


import tkinter as tk




class Texto(tk.Frame):
    def __init__(self, master=None, titulo="", contenido="",imagen=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.titulo = titulo
        self.contenido = contenido
        self.expandido = False

        self.crear_widgets()


    def crear_widgets(self):
        self.boton_toggle = tk.Button(self, text="+", command=self.toggle_expansion, relief=tk.FLAT, width=2)
        self.boton_toggle.grid(row=0, column=0, sticky="w", padx=(5, 0))
        self.boton_toggle.bind("<Button-1>", self.toggle_expansion)

        self.etiqueta_titulo = tk.Label(self, text=self.titulo, font=('calibri', 12, 'bold'), cursor="hand2")
        self.etiqueta_titulo.grid(row=0, column=1, sticky="w")
        self.etiqueta_titulo.bind("<Button-1>", self.toggle_expansion)

        self.etiqueta_contenido = tk.Label(self, text=self.contenido, wraplength=1000,justify='left')
        self.etiqueta_contenido.grid(row=1, column=1, sticky="w", padx=(20, 10), pady=(0, 10))
        self.etiqueta_contenido.grid_remove()




    def toggle_expansion(self, event=None):
        self.expandido = not self.expandido
        self.actualizar_texto_boton()
        if self.expandido:
            self.etiqueta_contenido.grid()
        else:
            self.etiqueta_contenido.grid_remove()


    def actualizar_texto_boton(self):
        self.boton_toggle["text"] = "-" if self.expandido else "+"

    def actualizar_contenido(self):
        texto_formateado = self.format_text(self.contenido)
        self.etiqueta_contenido.config(text=texto_formateado)

    def format_text(self, text):
        words = text.split()
        formatted_text = ''

        for word in words:
            if word.isupper():
                formatted_text += f'<b>{word}</b> '
            else:
                formatted_text += word + ' '

        return formatted_text

class Ayuda(tk.Tk):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.title("Ayuda")
        self.geometry("1130x619")

        marco1 = Texto(self, titulo="REGISTRO Y CONSULTAS", contenido="Pulsando el botón de REGISTRO Y CONSULTAS se pueden observar seis zonas claramente diferenciadas. En el área de usuario, pulsándose los botones BUCEADORES y ESQUIADORES, se podrá" 
                                 " DAR DE ALTA un nuevo usuario, buceador o esquiador. Se abrirá un desplegable en el cual se solicitarán todos los datos personales correspondientes al nuevo cliente, y cuyo registro ha de confirmarse pulsando en GUARDAR. Existe también la funcionalidad de limpiar los campos, con el botón inferior LIMPIAR. En la zona derecha del desplegable podrán consultarse los datos de "
                                 "usuarios ya previamente dados de alta. La búsqueda ha de hacerse introduciendo DNI de la persona. Bajo la búsqueda por DNI hay a disposición la opción de 'Borrar por DNI' donde, introduciendo el DNI por pantalla, permite borrar los datos de ese cliente del sistema. \n\n"
                                 "Pasando a la zona de Fauna y Flora, podrán darse de ALTA nuevas especies encontradas. Pulsando sobre ALTA, se abrirá una interface, en la cual el usuario deberá indicar el nombre de la especie avistada (incluyendo si se trata de fauna o flora) e indicar el lugar de avistamiento (seleccionando el mar/océano correspondiente). El botón examinar permite agregar una fotografía del animal/planta avistado. El botón borrar permite eliminar los datos hasta entonces introducidos. \n\n"
                                 " Por otro, pulsando sobre CONSULTA, se ofrece la posibilidad de hacer una busqueda de especies tanto por fauna/flora, como por aguas. Para el primero, seleccionando BUSCAR FAUNA Y FLORA, se ha de introducir el nombre de la especie buscada. Pulsando buscar, se mostrarán los datos de salida en la pantalla de resultados. Igual que para el resto de desplegables, se podrán tanto ELIMINAR datos, así como hacer una limpieza de los campos rellenos en ese momento. Si por el contrario se selecciona BUSCAR POR AGUAS, el usuario ha de seleccionar el mar/océano en el que quiere realizar la búsqueda, así como el nombre de la especie buscada. Los resultados se mostrarán del mismo modo que en el caso anterior.\n\n "
                                 
                                 "Para las zonas de PUNTOS DE INMERSIÓN Y ESQUÍ, a través de los distintos botones se podrán tanto CONSULTAR PUNTOS de inmersión y esquí, así como dar de alta nuevos puntos. En la zona inferiro del desplegable, Introduciendo el nombre del punto solicitado, se odrá tanto consultar (MOSTRAR) como eliminar su información (ELIMINAR). Para dar de alta un nuevo punto, se utilizarán los campos país, nombre, latitud, longitud, aguas, profundidad, así como una fotografía de este (botón SELECCIONAR). Será fundamental confirmar la alta del nuevo punto pulsando AGREGAR. Igual que en las anteriores situaciones, podrá hacerse una limpieza de todos los campos (LIMPIAR)  \n\n"
                                 "En el area de CONSULTAS "
                                 "Para las COMPRAS, existe la opción de dar de ALTA y de BAJA artículos, ya sea por la entrada de nuevo stock, así como materiales defectuosos o cualquier otra necesidad relacionada.\n\n"
                                 "En el INVENTARIO se podrá consultar el stock disponible. Se abrirá una ventana en la que se debe seleccionar el pais en el que se desea hacer la consulta de inventario, la talla, y la actividad (esquí o buceo). Se recuerda que los inventarios y las reservas, así como la variación de equipo disponible, es gestionado a nivel particular para cada centro. Esto evita posibles desajustes, y facilia el estudio de los centros y puntos más exitosos entre el público, las zonas de mayor demanda, de modo que se agilicen y amplíen stocks en esos centros, etc.")
        marco1.pack(fill=tk.X, padx=30, pady=10)

        marco2 = Texto(self, titulo="RESERVA", contenido="El botón de RESERVAS permite la gestión de reservas y devoluciones del equipo, tanto de esquí como de buceo. Los datos de la nueva reserva se añaden directamente a la base correspondiente. A su vez, al realizarse la devolución del material, el programa actualiza automaticamente el stock de equipos, así como los datos del cliente.\n\n"
                                                           "Los botones de RESERVA Y DEVOLUCION están disponibles en la zona derecha de la pantalla, bajo el calendario. Este último permite obtener al usuario la/s fecha/s deseadas para llevar a cabo su actividad.  Cabe destacar que, la contabilización y descuento de material se hace en función de la localización geográfica del centro. Es decir, los inventarios son particulares para cada cento de actividades, lo que facilita la gestión de compras, traspaso entre centros y dirección en general. Esta segmentación de inventarios será por pais.")
        marco2.pack(fill=tk.X, padx=30, pady=10)

        marco3 = Texto(self, titulo="MAPAMUNDI", contenido="Si se pulsa en MAPAMUNDI se presentan varias opciones ABRIR MAPA y EJECUTAR MAPA. La ejecución del mapa será fundamental para actualizar los puntos dados de alta previamente. Es decir, si se desea añadir un nuevo punto de inmersión o esquí, será FUNDAMENTAL pulsar el botón de EJECUTAR antes de abrir el mapa para su consulta, Se seleccionará ABRIR MAPA para poder consultar los numerosos puntos de esquí y buceo disponibles repartidos por el planeta.\n En la esquina superior derecha, sobre el icono de mapa, se podrá filtrar por preferencias los puntos de esqui o buceo. Las localizaciones moradas corresponden a zonas de interés para buceadores, mientras que las verdes están indicadas para actividades de esquí.")
        marco3.pack(fill=tk.X, padx=30, pady=10)

        marco4 = Texto(self, titulo="ESTADISTICAS", contenido="Con el botón de ESTADISTICAS se abrirá una interface con amplias opciones. Este apartado se presenta como una importante fuente de información sobre el funcionamiento de la agencia y el tratamiento estadístico de los datos, presentandose como una fuente única de información para posibles camapañas de marketing o decisiones estratégicas para la empresa.\n\n"
                                                              "Para la categoría BUZOS se podrá consultar la EDAD MEDIA, MEDIANA Y CUARTILES, todo datos de gran interés a nivel estadístico y basicos para llevar a cabo cualquier otro trabajo de investigación con los datos. Se presentará un gráfico con la distribución de las NACIONALIDADES de los usuarios, así como de sus NIVELES. Por útlimo, a nivel más avanzado, se divide el "
                                                              "conjunto de buceadores con un análisis Clúster, con el objetivo de segmentar el público objetivo, y dirigir mejor posibles campañas, promociones...   Las mismas funcionalidades están disponibles para la categoría ESQUIADORES.\n\n Para el apartado de VENTAS, hay disponbiles interesantes análisis, como el GASTO MEDIO actual de los clientes, la MEDIA DE VENTAS POR PAIS, las "
                                                              "VENTAS POR ACTIVIDAD, así como el número de ventas por TALLA. Todos estos botones, al ser pulsados, mostrarán por pantalla tanto los datos solicitados como los gráficos correspondientes. Por último, con la PREDICCION DE PRECIO, introduciendo la talla, el pais y la actividad que practica, el programa predice el gasto para ese consumidor. Esto permite al empresario seleccionar"
                                                              "el público objetivo más interesante, y al que más conviene dirigir campañas de marketing.\n\n"
                                                              "Para la FLORA Y FAUNA se podrá consultar la VARIEDAD de especies en cada OCEANO. Se podrá también introducir por pantalla el nombre del océano a consultar, lo que generará un gráfico que muestra las distintas especies encontradas en esa localización.\n\n")
        marco4.pack(fill=tk.X, padx=30, pady=10)



if __name__ == "__main__":
    ayuda = Ayuda()
    ayuda.mainloop()



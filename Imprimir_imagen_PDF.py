# Sofía Veldman Paniego
# Mohamed Boulman Mokhlis
# Juan del Junco Sampol

from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
import subprocess
from GestorBaseDatos import *

class BuscadorInformacion:
    def __init__(self,pais):
        self.pais=None 
        self.gestor = GestorBasesDatos()
        self.tipo_aguas_a_buscar = None
        self.lista_fauna_flora = []

    def buscar_puntos_por_pais(self, pais):
        resultados = self.gestor.buscar_puntos_por_pais(pais.upper())
        if resultados:
            for fila in resultados:
                self.definir_tipo_aguas(fila[1])
        else:
            print("No se encontraron resultados.")
        return resultados

    def definir_tipo_aguas(self, tipo_aguas):
        tipos_aguas = {
            'Mar Mediterraneo': 'mediterraneo',
            'Oceano Atlántico': 'atlantico',
            'Mar Rojo': 'mar_rojo',
            'Indico': 'indico',
            'Indo-Pacífico': 'indo_pacifico',
            'Pacifico': 'pacifico',
            'Mar Caribe': 'caribe'
        }
        self.tipo_aguas_a_buscar = tipos_aguas.get(tipo_aguas, None)

    def buscar_fauna_flora(self):
        if self.tipo_aguas_a_buscar is not None:
            resultados_fauna_flora = self.gestor.buscar_fauna_flora_por_H20(self.tipo_aguas_a_buscar)
            if resultados_fauna_flora:
                self.lista_fauna_flora = [fila[0] for fila in resultados_fauna_flora]
                for nombre_fauna_flora in self.lista_fauna_flora:
                    print(f"Nombre de Fauna/Flora: {nombre_fauna_flora}")
            else:
                print("No se encontraron resultados de fauna/flora para el tipo de aguas especificado.")
        else:
            print("Primero debes buscar puntos por país para definir el tipo de aguas.")
        return self.lista_fauna_flora

    def agregar_imagenes_a_pdf(self, carpeta, nombres_imagenes, nombre_pdf, titulo, mensaje_parte1, mensaje_parte2):
        # Obtener la lista de archivos en la carpeta
        lista_archivos = os.listdir(carpeta)

        # Filtrar las imágenes por nombres
        imagenes_encontradas = [os.path.join(carpeta, archivo) for archivo in lista_archivos if any(nombre in archivo for nombre in nombres_imagenes)]

        # Verificar si se encontraron imágenes
        if not imagenes_encontradas:
            print("No se encontraron imágenes para incluir en el PDF.")
            return

        # Crear un nuevo PDF
        pdf_path = nombre_pdf + ".pdf"
        c = canvas.Canvas(pdf_path, pagesize=letter)

        # Coordenadas para el título en la parte superior del PDF
        x_pos_titulo = letter[0] / 2
        y_pos_titulo = letter[1] - 30

        # Coordenadas para el mensaje parte 1 debajo del título
        x_pos_mensaje1 = x_pos_titulo
        y_pos_mensaje1 = y_pos_titulo - 50

        # Agregar el título en la parte superior del PDF
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(x_pos_titulo, y_pos_titulo, titulo)

        # Agregar el mensaje parte 1 debajo del título en la primera página
        c.setFont("Helvetica", 12)
        c.drawCentredString(x_pos_mensaje1, y_pos_mensaje1, mensaje_parte1)

        # Coordenadas para el mensaje parte 2 debajo del mensaje parte 1
        x_pos_mensaje2 = x_pos_titulo
        y_pos_mensaje2 = y_pos_mensaje1 - 20

        # Agregar el mensaje parte 2 debajo del mensaje parte 1 en la primera página
        c.drawCentredString(x_pos_mensaje2, y_pos_mensaje2, mensaje_parte2)

        # Coordenadas iniciales para la primera imagen
        x_pos_inicial = 50
        y_pos_inicial = y_pos_mensaje2 - 120

        # Contador de imágenes encontradas
        total_imagenes = len(imagenes_encontradas)
        imagenes_incluidas = 0

        # Después de agregar el título y mensajes, ahora agregamos las imágenes con nombres
        imagenes_por_pagina = 20
        for i, ruta_imagen in enumerate(imagenes_encontradas[:imagenes_por_pagina]):
            # Calcular las coordenadas para la imagen y el texto
            x_pos = x_pos_inicial + (i % 4) * 120  # Espaciado horizontal entre imágenes, 4 imágenes por fila
            y_pos = y_pos_inicial - (i // 4) * 130  # Espaciado vertical entre filas

            # Agregar la imagen al PDF
            imagen = Image.open(ruta_imagen)
            width, height = imagen.size
            imagen_width = 100
            imagen_height = 100
            c.drawInlineImage(ruta_imagen, x_pos, y_pos, width=imagen_width, height=imagen_height)

            # Agregar el nombre de la imagen (sin extensión) debajo de la foto
            c.setFont("Helvetica", 10)
            c.drawString(x_pos, y_pos - 20, f"{os.path.splitext(os.path.basename(ruta_imagen))[0]}")

        

        # Guardar y cerrar el PDF
        c.save()

        print(f"PDF creado con el nombre: {pdf_path}")

        # Abrir el PDF automáticamente
        self.abrir_pdf(pdf_path)

    def abrir_pdf(self, pdf_path):
        try:
            # Utilizar el comando adecuado para abrir archivos en Windows
            subprocess.run(["start", "", pdf_path], shell=True)
        except Exception as e:
            print(f"No se pudo abrir el PDF. Error: {e}")


# cliente='Mohamed'
# pais_a_buscar = "España".upper()
# info = BuscadorInformacion(pais_a_buscar)

# # Utiliza el método buscar_puntos_por_pais para obtener los resultados
# resultados_puntos_agua = info.buscar_puntos_por_pais(pais_a_buscar)

# # Si hay resultados, utiliza la instancia de BuscadorInformacion para buscar fauna/flora
# if resultados_puntos_agua:
#     # El método buscar_fauna_flora se llama en la instancia de BuscadorInformacion
#     fauna_flora_encontrada = info.buscar_fauna_flora()

#     carpeta_imagenes = "C:\\Users\\Mohamed\\Desktop\\Trabajo Python\\Código\\Bases_datos\\Bases_datos\\Fotos FF"
#     nombre_pdf = "Información cliente"
#     titulo_pdf = "La fauna/flora más vista"
#     mensaje_parte1_pdf = f"Estimado {cliente}: El equipo de buceadores le adjunta la fauna y flora más vistas en las aguas de {pais_a_buscar}."
#     mensaje_parte2_pdf = f"Para cualquier duda, pongase en contacto con nosotros: info@etsiiviajes.example. Disfrute su aventura."

#     # Crea y abre un PDF con las imágenes
#     Salida = info.agregar_imagenes_a_pdf(carpeta_imagenes, fauna_flora_encontrada, nombre_pdf, titulo_pdf, mensaje_parte1_pdf, mensaje_parte2_pdf)
# else:
#     print("No se encontraron resultados de puntos de agua.")

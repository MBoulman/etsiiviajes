# Sofía Veldman Paniego
# Mohamed Boulman Mokhlis
# Juan del Junco Sampol


import tkinter as tk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image, ImageTk
import subprocess

class GeneradorFactura:
    def __init__(self):
        self.numero_factura = 0

    def generar_factura(self, nombre, dni, cantidad, actividad, total_pagar):
        self.numero_factura += 1
        nombre_archivo = f"factura_{self.numero_factura}_2024.pdf"

        # Creamos el documento PDF
        pdf = canvas.Canvas(nombre_archivo, pagesize=letter)

        # fuente de la cabecera
        pdf.setFont("Helvetica-Bold", 16)

        # Encabezado
        pdf.drawString(50, 750, "Factura")
        pdf.drawString(50, 730, f"Número: {self.numero_factura}/2024")



        pdf.setFont("Helvetica", 12)
        # Información del cliente
        pdf.drawString(50, 700, f"Nombre: {nombre}")
        pdf.drawString(50, 680, f"DNI: {dni}")

        # Tabla
        pdf.drawString(50, 650, "Nombre")
        pdf.drawString(150, 650, "DNI")
        pdf.drawString(250, 650, "Cantidad")
        pdf.drawString(350, 650, "Actividad")
        pdf.drawString(470, 650, "Subtotal sin IVA")
        pdf.drawString(400, 570, "IVA        :")
        pdf.drawString(470, 560, "____________")
        pdf.drawString(400, 540, "Total a pagar:")

        pdf.drawString(50, 630, "-" * 550)  # Línea separadora

        pdf.drawString(50, 610, nombre)
        pdf.drawString(150, 610, dni)
        pdf.drawString(250, 610, str(cantidad))
        pdf.drawString(350, 610, actividad)
        pdf.drawString(485, 610, f"{total_pagar/(1.21):.2f} €")
        pdf.drawString(485, 570, f"{total_pagar*0.21:.2f} €")
        pdf.drawString(485, 540, f"{total_pagar:.2f} €")

        # Se guarda el pdf y se despues utilizamos al interprete de ordenes para abrirlo
        pdf.save()

        print(f"Factura generada: {nombre_archivo}")
        subprocess.Popen(["start", "", nombre_archivo], shell=True)


# generador = GeneradorFactura()
# generador.generar_factura("CLIENTE", "00000000T", 2, "BUCEO", 150.0)

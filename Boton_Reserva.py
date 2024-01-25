# Sofía Veldman Paniego
# Mohamed Boulman Mokhlis
# Juan del Junco Sampol

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from GestorBaseDatos import *
import random
from datetime import datetime
from Compra import Alquiler
from ttkthemes import ThemedStyle
from Imprimir_imagen_PDF import*
from Factura import*
class Reserva:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("RESERVA")
        self.ventana.geometry("650x540")
        self.ventana.resizable(False, False)
        self.Valor_registro=0
        self.Valor_registro1=0
        self.nombre_label = tk.Label(self.ventana, text="Nombre:")
        self.nombre_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")  
        self.nombre_entry = tk.Entry(self.ventana)
        self.nombre_entry.grid(row=5, column=1, padx=10, pady=10)

        self.actividad_label = tk.Label(self.ventana, text="Actividad:")
        self.actividad_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")  

        self.actividad_options = ["BUCEO", "ESQUIAR"]
        self.actividad_var = tk.StringVar()
        self.actividad_var.set(self.actividad_options[0])

        self.actividad_menu = tk.OptionMenu(self.ventana, self.actividad_var, *self.actividad_options)
        self.actividad_menu.grid(row=0, column=1, padx=10, pady=10)

        self.pais_label = tk.Label(self.ventana, text="País:")
        self.pais_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")  

        # Instancia de la base de datos para extraer paises
        self.gestor = GestorBasesDatos()

        self.paises = sorted(list(set(self.gestor.obtener_paises_Buceo() + self.gestor.obtener_paises_Esqui())))

        self.pais_var = tk.StringVar()
        self.pais_combobox = ttk.Combobox(self.ventana, textvariable=self.pais_var, values=self.paises, state="readonly")
        self.pais_combobox.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.pais_var.set('ESPAÑA')  # Establecemos España como país por defecto

        self.talla_label = tk.Label(self.ventana, text="Talla:")
        self.talla_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")  

        # Lista de tallas disponibles
        self.tallas = ["XXS", "XS", "S", "M", "L", "XL", "XXL"]

        self.talla_var = tk.StringVar()
        self.talla_combobox = ttk.Combobox(self.ventana, textvariable=self.talla_var, values=self.tallas, state="readonly")
        self.talla_combobox.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        self.talla_var.set('M')  # Establecemos Talla 'M' por defecto

        self.cantidad_label = tk.Label(self.ventana, text="Cantidad:")
        self.cantidad_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")  

        self.cantidad_entry = tk.Entry(self.ventana)
        self.cantidad_entry.grid(row=3, column=1, padx=10, pady=10)

        self.fecha_actividad_label = tk.Label(self.ventana, text="Fecha de actividad:")
        self.fecha_actividad_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")  

        self.fecha_actividad_entry = DateEntry(self.ventana, date_pattern='dd/mm/yyyy')
        self.fecha_actividad_entry.grid(row=4, column=1, padx=10, pady=10)

        self.dni_label = tk.Label(self.ventana, text="DNI:")
        self.dni_label.grid(row=6, column=0, padx=10, pady=10, sticky="w")  

        self.dni_entry = tk.Entry(self.ventana)
        self.dni_entry.grid(row=6, column=1, padx=10, pady=10)

        self.email_label = tk.Label(self.ventana, text="Email:")
        self.email_label.grid(row=7, column=0, padx=10, pady=10, sticky="w")  
        self.email_entry = tk.Entry(self.ventana)
        self.email_entry.grid(row=7, column=1, padx=10, pady=10)

        self.precio_label = tk.Label(self.ventana, text="Precio Estimado:")
        self.precio_label.grid(row=8, column=0, padx=10, pady=10, sticky="w") 
        self.precio_entry = tk.Entry(self.ventana, state="readonly")
        self.precio_entry.grid(row=8, column=1, padx=10, pady=10)

        # Botón para actualizar el precio estimado

        self.actualizar_precio_button = tk.Button(self.ventana, text="Precio estimado", command=self.actualizar_precio)
        self.actualizar_precio_button.grid(row=9, column=0, columnspan=1, pady=10)

        self.registrar_button = tk.Button(self.ventana, text="Registrar Reserva", command=self.registrar_reserva)
        self.registrar_button.grid(row=10, column=0, columnspan=1, pady=10)

        self.detalles_button = tk.Button(self.ventana, text="Mostrar Detalles", command=self.mostrar_detalles)
        self.detalles_button.grid(row=11, column=0, columnspan=1, pady=10)

        self.informacion_pais_button = tk.Button(self.ventana, text="Información Pais", command=lambda: self.obtener_informacion_pais(self.Valor_registro))
        self.informacion_pais_button.grid(row=9, column=1, columnspan=1, pady=10)

        self.imprimir_factura_button = tk.Button(self.ventana, text="Imprimir factura", command=lambda: self.imprimir_factura(self.Valor_registro))
        self.imprimir_factura_button.grid(row=10, column=1, columnspan=1, pady=10)

        self.limpiar_campos_button = tk.Button(self.ventana, text="Limpiar campos", command=self.limpiar_campos)
        self.limpiar_campos_button.grid(row=11, column=1, columnspan=1, pady=10)

        self.imagen1 = Image.open("C:\\Users\\Mohamed\\Desktop\\Trabajo Python\\Código\\Bases_datos\\Bases_datos\\Fotos Reserva\\Buceo.jpg")
        self.imagen1 = self.imagen1.resize((300, 230), Image.ANTIALIAS)
        self.imagen1 = ImageTk.PhotoImage(self.imagen1)
        self.label_imagen1 = tk.Label(self.ventana, image=self.imagen1)
        self.label_imagen1.grid(row=0, column=2, rowspan=6, padx=10, pady=2)

        self.imagen2 = Image.open("C:\\Users\\Mohamed\\Desktop\\Trabajo Python\\Código\\Bases_datos\\Bases_datos\\Fotos Reserva\\Esqui.jpg")
        self.imagen2 = self.imagen2.resize((300, 230), Image.ANTIALIAS)
        self.imagen2 = ImageTk.PhotoImage(self.imagen2)
        self.label_imagen2 = tk.Label(self.ventana, image=self.imagen2)
        self.label_imagen2.grid(row=6, column=2, rowspan=6, padx=10, pady=10)



    def calcular_precio(self, actividad, fecha_actividad):
        fecha_actividad = datetime.strptime(fecha_actividad, "%d/%m/%Y")
        fecha_referencia = datetime.strptime("15-01", "%d-%m").replace(year=datetime.now().year)
        dias_entre_fechas = (fecha_actividad - fecha_referencia).days
        
        precio_estimado = 120 - (dias_entre_fechas / 5)
        # Se añade variablidad al precio
        precio_aleatorio = random.uniform(precio_estimado - 10, precio_estimado + 10)
        return max(40, precio_aleatorio)  # Establecemos 40 euros como precio minimo
    def registrar_reserva(self):
        nombre = self.nombre_entry.get()
        actividad = self.actividad_var.get()
        pais = self.pais_var.get()
        talla = self.talla_var.get()
        cantidad = self.cantidad_entry.get()
        if cantidad:
            try:
                cantidad = float(cantidad)
            except ValueError:
                messagebox.showerror("Error", "La cantidad debe ser un número válido.")
                return
        else:
            messagebox.showerror("Error", "Por favor, ingresa una cantidad.")
            return
        fecha_actividad = self.fecha_actividad_entry.get()
        dni = self.dni_entry.get()
        email = self.email_entry.get()

        precio_estimado = self.calcular_precio(actividad, fecha_actividad)

        confirmacion = messagebox.askyesno(
            "Confirmar Registro",
            f"¿Deseas registrar la reserva?\n\nNombre: {nombre}\nActividad: {actividad}\nPaís: {pais}\nTalla: {talla}\nCantidad: {cantidad}\nFecha de actividad: {fecha_actividad}\nPrecio Estimado: {precio_estimado:.2f} euros\nDNI: {dni}\nEmail: {email}",
            icon="question" 
        )

        precio_total = precio_estimado * float(cantidad)

        if confirmacion:
            nuevo_alquiler = Alquiler(nombre, actividad, pais, talla, cantidad, fecha_actividad, precio_estimado, dni, email)
            self.gestor.insertar_venta_cliente(nuevo_alquiler.dni, nuevo_alquiler.nombre, nuevo_alquiler.email, nuevo_alquiler.actividad, nuevo_alquiler.talla, nuevo_alquiler.pais, nuevo_alquiler.cantidad, nuevo_alquiler.fecha_actividad, precio_total)
            self.gestor.restar_alquiler(nuevo_alquiler)
            self.Valor_registro = 1
            # self.resultado_label.config(text=f"Reserva registrada con éxito. Total a pagar: {precio_total:.2f} € .")
        else:
            self.resultado_label.config(text="Registro cancelado.")

    def mostrar_detalles(self):
        try:
            nombre = self.nombre_entry.get().upper()
            actividad = self.actividad_var.get()
            pais = self.pais_var.get()
            talla = self.talla_var.get()
            cantidad = self.cantidad_entry.get()
            fecha_actividad = self.fecha_actividad_entry.get()
            dni = self.dni_entry.get()
            email = self.email_entry.get()
            precio_estimado = self.precio_entry.get()

            detalles = f"Nombre: {nombre}\nActividad: {actividad}\nPaís: {pais}\nTalla: {talla}\nCantidad: {cantidad}\nFecha de actividad: {fecha_actividad}\nPrecio Estimado: {precio_estimado}\nDNI: {dni}\nEmail: {email}"
            messagebox.showinfo("Detalles del Alquiler", detalles, icon="info")  
        except Exception as e:
            messagebox.showwarning("Error", f"Error al mostrar detalles: {e}", icon="warning")  

    def actualizar_precio(self):
        fecha_actividad = self.fecha_actividad_entry.get()
        actividad = self.actividad_var.get()
        precio_estimado = self.calcular_precio(actividad, fecha_actividad)
        self.precio_entry.config(state="normal")
        self.precio_entry.delete(0, tk.END)
        self.precio_entry.insert(0, f"{precio_estimado:.2f} € ")
        self.precio_entry.config(state="readonly")


    def obtener_informacion_pais(self,Valor_registro):

        if Valor_registro==1:
        
            cliente = self.nombre_entry.get().upper()
            pais_a_buscar = pais = self.pais_var.get().upper()
            info = BuscadorInformacion(pais_a_buscar)

            resultados_puntos_agua = info.buscar_puntos_por_pais(pais_a_buscar)

            if resultados_puntos_agua:
                # El método buscar_fauna_flora llama a la instancia de BuscadorInformacion
                fauna_flora_encontrada = info.buscar_fauna_flora()

                carpeta_imagenes = "C:\\Users\\Mohamed\\Desktop\\Trabajo Python\\Código\\Bases_datos\\Bases_datos\\Fotos FF"
                nombre_pdf = "Información cliente"
                titulo_pdf = "La fauna/flora más vista"
                mensaje_parte1_pdf = f"Estimado {cliente}: El equipo de buceadores le adjunta la fauna y flora más vistas en las aguas de {pais_a_buscar}."
                mensaje_parte2_pdf = f"Para cualquier duda, pongase en contacto con nosotros: info@etsiiviajes.example. Disfrute su aventura."

                # Creamos el pdf
                PDFSalida = info.agregar_imagenes_a_pdf(carpeta_imagenes, fauna_flora_encontrada, nombre_pdf, titulo_pdf, mensaje_parte1_pdf, mensaje_parte2_pdf)
        else:
                
            messagebox.showwarning("Error", f"DEBERÍA REGISTRAR LA RESERVA PRIMERO", icon="warning")  



    def imprimir_factura(self,Valor_registro):
        
        if Valor_registro==1:

            cliente = self.nombre_entry.get().upper()
            DNI= self.dni_entry.get()
            Cantidad=self.cantidad_entry.get()
            Actividad=self.actividad_var.get()
            fecha_Actividad = self.fecha_actividad_entry.get()
            Precio=self.calcular_precio(Actividad, fecha_Actividad)
            generador = GeneradorFactura()
            generador.generar_factura(cliente, DNI, Cantidad, Actividad, Precio)

        else:
                
            messagebox.showwarning("Error", f"DEBERÍA REGISTRAR LA RESERVA PRIMERO", icon="warning") 

    def limpiar_campos(self):
        self.nombre_entry.delete(0, tk.END)
        self.actividad_var.set(self.actividad_options[0])
        self.pais_var.set('ESPAÑA')
        self.talla_var.set('M')
        self.cantidad_entry.delete(0, tk.END)
        self.fecha_actividad_entry.delete(0, tk.END)
        self.dni_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.precio_entry.config(state="normal")
        self.precio_entry.delete(0, tk.END)
        self.precio_entry.config(state="readonly")

    def Ejecucion(self):
        # Bucle de la ventana
        self.ventana.mainloop()


Reserva = Reserva()
Reserva.Ejecucion()


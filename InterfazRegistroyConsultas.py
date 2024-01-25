# Sofía Veldman Paniego
# Mohamed Boulman Mokhlis
# Juan del Junco Sampol

from tkinter import font
from tkinter import *
from Interfaz_Buzo import *
from Interfaz_Esquiador import *
from Interfaz_Fauna_y_Flora_Alta import *
from Interfaz_Fauna_y_Flora_Consulta import *
from InterfazPuntosInmersion import *
from InterfazPuntosEsqui import *
from InterfazInventario import *
from InterfazCentroBuceo import *
from InterfazCentroEsqui import *
from InterfazCentroBuceoBaja import*
from InterfazCentroEsquiBaja import*
import subprocess
gestor = GestorBasesDatos()
class InterfazBase:
    def __init__(self, ventana, titulo, bg_color):
        self.ventana = ventana
        self.titulo = titulo
        self.bg_color = bg_color
        # La ventana principal
        self.ventana.title(self.titulo)
        self.ventana.geometry("400x640")
        self.ventana.configure(bg=self.bg_color)

        # Crear una fuente más gruesa
        self.fuente_gruesa = font.Font(family="Helvetica", size=10, weight="bold")

    def registro_consultas(self):
        lbl = Label(self.ventana, bg="grey")
        lbl.place(x=10, y=40, width=680, height=410)

        ########################################################################### USUARIOS
        def usuario_buceadores():
            InterfazBuzo(gestor)

        def usuario_esquiadores():
            InterfazEsquiador(gestor)

        titulo = Label(self.ventana, text="USUARIOS", font=self.fuente_gruesa, bg="gray", fg="yellow")
        titulo.place(x=150, y=45)

        marco = Label(self.ventana, bg="white")
        marco.place(x=30, y=70, width=315, height=75)

        fondo = Label(self.ventana, bg="white")
        fondo.place(x=32.5, y=72.5, width=310, height=70)

        boton = Button(self.ventana, text="BUCEADORES", command=usuario_buceadores, bg="black", fg="white",
                       font=self.fuente_gruesa)
        boton.place(x=52.5, y=92.5)

        boton = Button(self.ventana, text="ESQUIADORES", command=usuario_esquiadores, bg="black", fg="white",
                       font=self.fuente_gruesa)
        boton.place(x=212.5, y=92.5)

        ########################################################################### FAUNA Y FLORA
        def fauna_y_flora_alta():
            Interfaz_Fauna_y_Flora_Alta()

        def fauna_y_flora_consulta():
            
            subprocess.Popen(["python", "Interfaz_Fauna_y_Flora_Consulta.py"])
        titulo = Label(self.ventana, text="FAUNA Y FLORA", font=self.fuente_gruesa, bg="gray", fg="yellow")
        titulo.place(x=135, y=157.5)

        marco = Label(self.ventana, bg="white")
        marco.place(x=30, y=185, width=315, height=75)

        fondo = Label(self.ventana, bg="white")
        fondo.place(x=32.5, y=187.5, width=310, height=70)

        boton = Button(self.ventana, text="ALTA", command=fauna_y_flora_alta, bg="black", fg="white",
                       font=self.fuente_gruesa)
        boton.place(x=82.5, y=207.5)

        boton = Button(self.ventana, text="CONSULTA", command=fauna_y_flora_consulta, bg="black", fg="white",
                       font=self.fuente_gruesa)
        boton.place(x=220, y=207.5)

        ########################################################################### PUNTOS

        def punto_inmersion_alta():
            InterfazPuntosInmersion()
        def punto_esqui_alta():
            InterfazPuntosEsqui()

        titulo = Label(self.ventana, text="PUNTOS", font=self.fuente_gruesa, bg="gray", fg="yellow")
        titulo.place(x=160, y=280)

        marco = Label(self.ventana, bg="white")
        marco.place(x=30, y=307.5, width=315, height=115)

        fondo = Label(self.ventana, bg="white")
        fondo.place(x=32.5, y=310, width=310, height=110)

        boton = Button(self.ventana, text="ALTA Y CONSULTA PUNTOS DE INMERSIÓN", command=punto_inmersion_alta,
                       bg="black", fg="white", font=self.fuente_gruesa)
        boton.place(x=40, y=330)

        boton = Button(self.ventana, text="ALTA Y CONSULTA PUNTOS DE ESQUÍ", command=punto_esqui_alta, bg="black",
                       fg="white", font=self.fuente_gruesa)
        boton.place(x=55, y=370)

        ########################################################################### INVENTARIO
        def inventario_consulta():
            subprocess.Popen(["python", "InterfazInventario.py"])
        titulo = Label(self.ventana, text="INVENTARIO", font=self.fuente_gruesa, bg="gray", fg="yellow")
        titulo.place(x=150 + 325, y=45)

        marco = Label(self.ventana, bg="white")
        marco.place(x=30 + 325, y=70, width=315, height=75)

        fondo = Label(self.ventana, bg="white")
        fondo.place(x=32.5 + 325, y=72.5, width=310, height=70)

        boton = Button(self.ventana, text="INVENTARIO", command=inventario_consulta, bg="black", fg="white",
                       font=self.fuente_gruesa)
        boton.place(x=150.5 + 325, y=92.5)

        ########################################################################### COMPRAS
        def compra_alta_buceo():
            #InterfazCentroBuceo(gestor)
            subprocess.Popen(["python", "InterfazCentroBuceo.py"])

        def compra_baja_buceo():
            subprocess.Popen(["python", "InterfazCentroBuceoBaja.py"])
            

        def compra_alta_esqui():
            subprocess.Popen(["python", "InterfazCentroEsqui.py"])            


        def compra_baja_esqui():
            subprocess.Popen(["python", "InterfazCentroEsquiBaja.py"])




        titulo = Label(self.ventana, text="COMPRAS", font=self.fuente_gruesa,bg="gray", fg="yellow")
        titulo.place(x=157.5 + 325, y=157.5)

        marco = Label(self.ventana, bg="white")
        marco.place(x=30 + 325, y=185, width=315, height=237.5)  #Cambiamos tamaño marco

        fondo = Label(self.ventana, bg="white")
        fondo.place(x=32.5 + 325, y=187.5, width=310, height=225) #Cambiamos tamaño fondo

        boton = Button(self.ventana, text="ALTA PRODUCTO CENTRO BUCEO", command=compra_alta_buceo, bg="black", fg="white", font=self.fuente_gruesa)
        boton.place(x=85 + 325, y=207.5)

        boton = Button(self.ventana, text="BAJA PRODUCTO CENTRO BUCEO", command= compra_baja_buceo, bg="black", fg="white", font=self.fuente_gruesa)
        boton.place(x=85 + 325, y=257.5)

        boton_opcion_3 = Button(self.ventana, text="ALTA PRODUCTO CENTRO ESQUI", command=compra_alta_esqui, bg="black", fg="white", font=self.fuente_gruesa)
        boton_opcion_3.place(x=85 + 325, y=307.5) #añadimos un boton

        boton_opcion_4 = Button(self.ventana, text="BAJA PRODUCTO CENTRO ESQUI", command=compra_baja_esqui, bg="black", fg="white", font=self.fuente_gruesa)
        boton_opcion_4.place(x=85 + 325, y=357.5) #añadimos otro botón

        ########################################################################### CENTROS


# Crear la ventana principal
ventana = Tk()
ventana.title("Registro y consultas")
ancho_ventana = 700
alto_ventana = 480
ventana.geometry(f"{ancho_ventana}x{alto_ventana}")
ventana.minsize(ancho_ventana, alto_ventana)
ventana.maxsize(ancho_ventana, alto_ventana)
# Configurar el fondo de la ventana
ventana.configure(bg="white")

#Fuentes más gruesas para los titulos
fuente_gruesa = font.Font(family="Helvetica", size=10, weight="bold")
fuente_titulo = font.Font(family="Helvetica", size=30, weight="bold")

# Bucle de la ventana
interfaz = InterfazBase(ventana, "Registro y consultas", "white")
interfaz.registro_consultas()
ventana.mainloop()

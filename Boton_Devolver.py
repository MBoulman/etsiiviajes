# Sofía Veldman Paniego
# Mohamed Boulman Mokhlis
# Juan del Junco Sampol

import tkinter as tk
from tkinter import messagebox

from GestorBaseDatos import *

# Instancia para la base de datos
gestor = GestorBasesDatos()

def obtener_dni():
    dni = entry_dni.get()
    resultados = gestor.consultar_ventas_por_dni(dni)

    if resultados:
        # Ventana para mostrar los resultados
        ventana_resultados = tk.Toplevel(ventana)
        ventana_resultados.title(f"Resultados para el DNI {dni}")

        # Cuadro de texto para mostrar los resultados.
        cuadro_texto = tk.Text(ventana_resultados, wrap=tk.WORD, height=15, width=45)
        cuadro_texto.pack(expand=True, fill=tk.BOTH)

        # Agregar resultados al cuadro de texto
        cuadro_texto.insert(tk.END, f"ULTIMA RESERVA DEL {dni}:\n\n")
        cuadro_texto.insert(tk.END, f"\n\n")

        ancho_columna = max(len(str(resultado[0])) for resultado in resultados) + 4

        for resultado in resultados:
            cuadro_texto.insert(tk.END, f"DNI                : {resultado[0]:<{ancho_columna}}\n")
            cuadro_texto.insert(tk.END, f"NOMBRE             : {resultado[1]:<{ancho_columna}}\n")
            cuadro_texto.insert(tk.END, f"EMAIL              : {resultado[2]:<{ancho_columna}}\n")
            cuadro_texto.insert(tk.END, f"ACTIVIDAD          : {resultado[3]:<{ancho_columna}}\n")
            cuadro_texto.insert(tk.END, f"TALLA              : {resultado[4]:<{ancho_columna}}\n")
            cuadro_texto.insert(tk.END, f"PAÍS ACTIVIDAD     : {resultado[5]:<{ancho_columna}}\n")
            cuadro_texto.insert(tk.END, f"CANTIDAD RESERVADA : {resultado[6]:<{ancho_columna}}\n")
            cuadro_texto.insert(tk.END, f"FECHA ACTIVIDAD    : {resultado[7]:<{ancho_columna}}\n")
            cuadro_texto.insert(tk.END, f"FECHA VENTA        : {resultado[8]:<{ancho_columna}}\n")
            cuadro_texto.insert(tk.END, f"PRECIO PAGADO (€)  : {resultado[9]:>10.2f}\n\n")

        cuadro_texto.config(state=tk.DISABLED)
    else:
        messagebox.showinfo("Resultados", f"No hay ventas para el DNI {dni}")

def limpiar_campo():
    entry_dni.delete(0, tk.END)

def devolver(dni):
    gestor.procesar_devolucion(dni)
    messagebox.showinfo("Devolución realizada con éxito", "Devolución realizada con éxito", icon=tk.messagebox.INFO)

# Ventana principal
ventana = tk.Tk()
ventana.title("Devolución por DNI")


marco_entrada = tk.Frame(ventana)
marco_entrada.pack(pady=10)

label_instruccion = tk.Label(marco_entrada, text="Introduzca DNI:")
label_instruccion.pack(side=tk.TOP, pady=5)  

entry_dni = tk.Entry(marco_entrada, width=20)  
entry_dni.pack(side=tk.LEFT, padx=5) 

marco_botones = tk.Frame(ventana)
marco_botones.pack()

# Boton que busca el DNI en la tabla
boton_obtener_dni = tk.Button(marco_botones, text="Última reserva", command=obtener_dni)
boton_obtener_dni.pack(side=tk.LEFT, padx=5) 

# Botón que ejcuta la devolución
boton_devolver = tk.Button(marco_botones, text="Devolver", command=lambda: devolver(entry_dni.get()))
boton_devolver.pack(side=tk.LEFT, padx=5) 
# Boton que limpia los campos
boton_limpiar = tk.Button(marco_botones, text="Limpiar", command=limpiar_campo)
boton_limpiar.pack(side=tk.LEFT, padx=5)  


ventana.geometry("400x150")  

# Iniciamos el bucle principal de la interfaz
ventana.mainloop()

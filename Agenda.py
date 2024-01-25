
# Sofía Veldman Paniego
# Mohamed Boulman Mokhlis
# Juan del Junco Sampol



import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from tkcalendar import Calendar
from datetime import datetime

class Agenda:
    def __init__(self, ventana_agenda):
        self.ventana_agenda = ventana_agenda
        self.ventana_agenda.title("AGENDA DE EVENTOS")
        self.ventana_agenda.geometry("400x450") 

        fecha_actual = datetime.now()
        año_actual = fecha_actual.year
        mes_actual = fecha_actual.month
        dia_actual = fecha_actual.day

        self.calendario = Calendar(ventana_agenda, selectmode="day", year=año_actual, month=mes_actual, day=dia_actual)
        self.calendario.pack(pady=20)


        self.horas_disponibles = ["10:00", "12:00", "16:00", "17:00", "18:00"]
        self.combobox_horas = ttk.Combobox(ventana_agenda, values=self.horas_disponibles, state="readonly")
        self.combobox_horas.set("Seleccione la Hora")
        self.combobox_horas.pack(pady=10)

        nombres_evento = ["CURSO INICIAL DE ESQUI","CURSO INTERMEDIO DE ESQUI","CURSO AVANZADO DE ESQUI","CURSO BASICO DE BUCEO","CURSO INTERMEDIO DE BUCEO","CURSO AVANZADO DE BUCEO","CURSO FAUNA FLORA","COMP ESQUÍ <18","COMP ESQUÍ >18 Y <30","COMP ESQUÍ >30 Y <45",]
        self.combobox_nombres = ttk.Combobox(ventana_agenda, values=nombres_evento, state="readonly")
        self.combobox_nombres.set("Seleccione el Nombre")
        self.combobox_nombres.pack(pady=10)

        self.boton_registrar_evento = tk.Button(ventana_agenda, text="Registrar Evento", command=self.registrar_evento)
        self.boton_registrar_evento.pack(pady=10)

        self.boton_eventos_hoy = tk.Button(ventana_agenda, text="Eventos de Hoy", command=self.mostrar_eventos_hoy)
        self.boton_eventos_hoy.pack(pady=10)

        self.etiqueta_evento = tk.Label(ventana_agenda, text="")
        self.etiqueta_evento.pack(pady=5)

        # EVentos para enseñar el día de la presentación
        self.eventos = {
            "25-01-2024": ["10:00 - CURSO AVANZADO DE BUCEO", "18:00 PM - CURSO INTERMEDIO DE BUCEO"],
            "25-01-2024": ["12:00 - CURSO FAUNA FLORA", "17:00 - CURSO BÁSICO DE BUCEO"],}

    def registrar_evento(self):
        # selecionamos la fecha
        fecha_seleccionada = self.calendario.get_date()
        fecha_seleccionada_str = datetime.strptime(fecha_seleccionada, "%m/%d/%y").strftime("%d-%m-%y")

        hora_seleccionada = self.combobox_horas.get()
        nombre_evento = self.combobox_nombres.get()

        if hora_seleccionada != "Seleccione la Hora" and nombre_evento != "Seleccione el Nombre":
            # Agregamos el evento a la lista
            if fecha_seleccionada_str not in self.eventos:
                self.eventos[fecha_seleccionada_str] = []

            self.eventos[fecha_seleccionada_str].append(f"{hora_seleccionada} - {nombre_evento}")

            mensaje = f"Evento: {nombre_evento} a las {hora_seleccionada}\nFecha: {fecha_seleccionada_str}"
            self.etiqueta_evento.config(text=mensaje)
            messagebox.showinfo("Evento Registrado", f"Evento '{nombre_evento}' registrado el {fecha_seleccionada_str} a las {hora_seleccionada}.")
        elif hora_seleccionada == "Seleccione la Hora":
            messagebox.showwarning("Error", "Por favor, selecciona una hora.")
        else:
            messagebox.showwarning("Error", "Por favor, selecciona un nombre de evento.")

    def mostrar_eventos_hoy(self):
        fecha_hoy = datetime.now().strftime("%d-%m-%y")
        eventos_hoy = self.eventos.get(fecha_hoy, [])
        if eventos_hoy:
            mensaje = f"Eventos de Hoy ({fecha_hoy}):\n"
            mensaje += "\n".join(eventos_hoy)
            messagebox.showinfo("Eventos de Hoy", mensaje)
        else:
            messagebox.showinfo("Eventos de Hoy", "No hay eventos programados para hoy.")

if __name__ == "__main__":
    ventana_agenda = tk.Tk()
    app = Agenda(ventana_agenda)
    ventana_agenda.mainloop()

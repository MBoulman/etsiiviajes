# Sofía Veldman Paniego
# Mohamed Boulman Mokhlis
# Juan del Junco Sampol
from GestorBaseDatos import*

class Punto_de_inmersion(GestorBasesDatos):
    def __init__(self, nombre, pais, latitud, longitud, aguas, profundidad, foto=None):
        super().__init__()  #inicializador de la clase base
        self.Nombre = nombre
        self.Pais = pais
        self.Latitud = latitud
        self.Longitud = longitud
        self.Aguas = aguas
        self.Profundidad = profundidad
        self.Foto = foto

    def __str__(self):
        return f"Punto de Inmersión: {self.Nombre}, País: {self.Pais}, Latitud: {self.Latitud}, Longitud: {self.Longitud}, Aguas: {self.Aguas}, Profundidad: {self.Profundidad}m"

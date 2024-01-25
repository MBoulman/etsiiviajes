# Sofía Veldman Paniego
# Mohamed Boulman Mokhlis
# Juan del Junco Sampol

from GestorBaseDatos import*

class Punto_de_esqui(GestorBasesDatos):
    def __init__(self, nombre, pais, latitud, longitud, km_pistas, mapa_pistas = None):
        super().__init__()  # inicializador de la clase base
        self.nombre = nombre
        self.pais = pais
        self.latitud = latitud
        self.longitud = longitud
        self.km_pistas = km_pistas
        self.mapa_pistas = mapa_pistas

    def __str__(self):
        return (f"Punto de esqui: {self.nombre}, País: {self.pais}, Latitud: {self.latitud}, Longitud: {self.longitud}, Km de pistas: {self.km_pistas}")
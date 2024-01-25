# Sofía Veldman Paniego
# Mohamed Boulman Mokhlis
# Juan del Junco Sampol

class compra:
    def __init__(self, equipo, pais, talla, cantidad, precio_compra):
        self.equipo = equipo
        self.pais = pais
        self.talla = talla
        self.cantidad = cantidad
        self.precio_compra = precio_compra

class Alquiler:
    def __init__(self, nombre, actividad, pais, talla, cantidad, fecha_actividad, precio, dni, email):
        self.nombre = nombre
        self.actividad = actividad
        self.pais = pais
        self.talla = talla
        self.cantidad = cantidad
        self.fecha_actividad = fecha_actividad
        self.precio = precio
        self.dni = dni
        self.email = email

class devolver:
    def __init__(self, dni, actividad, pais):
        self.dni=dni
        self.actividad = actividad
        self.pais = pais
class baja:
    def __init__(self, equipo, pais, talla, cantidad):
        self.equipo = equipo
        self.pais = pais
        self.talla = talla
        self.cantidad = cantidad

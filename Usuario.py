# Sofía Veldman Paniego
# Mohamed Boulman Mokhlis
# Juan del Junco Sampol

class Usuario():
    def __init__(self, dni, nombre, apellidos, fecha_nacimiento, nacionalidad,
                 peso, altura, tel, email, direccion, tipo_club=None, foto=None):
        super().__init__() 
        self.dni = dni
        self.nombre = nombre
        self.apellidos = apellidos
        self.fecha_nacimiento = fecha_nacimiento
        self.nacionalidad = nacionalidad
        self.peso = peso
        self.altura = altura
        self.tel = tel
        self.email = email
        self.direccion = direccion
        self.tipo_club = tipo_club  # Nuevo atributo para el tipo de club
        self.foto = foto  # La foto puede ser None si no se proporciona
    
    def asignar_tipo_club(self, tipo):
        self.tipo_club = tipo

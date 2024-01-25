# Sofía Veldman Paniego
# Mohamed Boulman Mokhlis
# Juan del Junco Sampol

from Usuario import *

class Buzo(Usuario):

    def __init__(self, dni, nombre, apellidos, fecha_nacimiento, nacionalidad,
                 peso, altura, tel, email, direccion, tipo_club=None, tipo_buzo=None,
                 enfermedad=None, foto=None):
        """Constructor de la clase Buzo."""
        super().__init__(dni, nombre, apellidos, fecha_nacimiento, nacionalidad,
                         peso, altura, tel, email, direccion, tipo_club, foto)
        self._tipo_buzo = tipo_buzo
        self._enfermedad = enfermedad
    
    @property
    def tipo_buzo(self):

        return self._tipo_buzo
    
    @property
    def enfermedad(self):
        
        return self._enfermedad

    def get_tipo_buzo(self):

        return self.tipo_buzo

    def get_enfermedad(self):
        
        return self.enfermedad

    def get_nombre(self):

        return self.nombre

    def get_apellidos(self):

        return self.apellidos



# Sofía Veldman Paniego
# Mohamed Boulman Mokhlis
# Juan del Junco Sampol
from Usuario import *

class Esquiador(Usuario):
    def __init__(self, dni, nombre, apellidos, fecha_nacimiento, nacionalidad,
                 peso, altura, tel, email, direccion, tipo_club=None, tipo_esquiador=None,
                 enfermedad=None, foto=None):
        super().__init__(dni, nombre, apellidos, fecha_nacimiento, nacionalidad,
                         peso, altura, tel, email, direccion, tipo_club, foto)
        self._tipo_esquiador = tipo_esquiador
        self._enfermedad = enfermedad
    
    @property
    def tipo_esquiador(self):
        return self._tipo_esquiador
    
    @property
    def enfermedad(self):
        return self._enfermedad
    
    def comprobar_enfermedad(self):
        return self.enfermedad
    

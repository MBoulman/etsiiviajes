"""Clases de datos de la aplicación."""

from dataclasses import dataclass, field

from .config import BUCEO, ESQUI


@dataclass
class Usuario:
    """Datos comunes a buceadores y esquiadores."""

    dni: str
    nombre: str
    apellidos: str
    fecha_nacimiento: str          # aaaa-mm-dd
    nacionalidad: str
    peso: int                      # kg
    altura: int                    # cm
    telefono: str
    email: str
    direccion: str
    tipo_club: str = "AMATEUR"
    nivel: str = ""
    enfermedad: str = "NO"
    foto: bytes | None = field(default=None, repr=False)

    actividad = ""  # la definen las subclases

    @property
    def nombre_completo(self) -> str:
        return f"{self.nombre} {self.apellidos}".strip()


@dataclass
class Buzo(Usuario):
    actividad = BUCEO


@dataclass
class Esquiador(Usuario):
    actividad = ESQUI


@dataclass
class Compra:
    """Entrada (cantidad > 0) o baja (cantidad < 0) de material en un centro."""

    actividad: str
    equipo: str
    pais: str
    talla: str
    cantidad: int
    precio_unitario: float = 0.0


@dataclass
class Alquiler:
    """Reserva de un equipo completo de buceo o esquí."""

    dni: str
    nombre: str
    email: str
    actividad: str
    pais: str
    talla: str
    cantidad: int
    fecha_actividad: str           # aaaa-mm-dd
    precio_unitario: float

    @property
    def precio_total(self) -> float:
        return round(self.precio_unitario * self.cantidad, 2)


@dataclass
class Venta(Alquiler):
    id: int = 0
    fecha_venta: str = ""
    devuelto: bool = False


@dataclass
class PuntoInmersion:
    nombre: str
    pais: str
    latitud: float
    longitud: float
    aguas: str
    profundidad: float
    foto: bytes | None = field(default=None, repr=False)


@dataclass
class PuntoEsqui:
    nombre: str
    pais: str
    latitud: float
    longitud: float
    km_pistas: float
    mapa_pistas: bytes | None = field(default=None, repr=False)


@dataclass
class Especie:
    """Especie de fauna o flora y las aguas en las que se ha visto."""

    nombre: str
    tipo: str                      # FAUNA o FLORA
    aguas: dict[str, bool]         # clave de config.AGUAS -> visto sí/no
    foto: bytes | None = field(default=None, repr=False)

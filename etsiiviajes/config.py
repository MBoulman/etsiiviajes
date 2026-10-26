"""Rutas y constantes compartidas por toda la aplicación."""

from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DATOS = RAIZ / "datos"
ASSETS = RAIZ / "assets"
ICONOS = ASSETS / "iconos"
SALIDA = RAIZ / "salida"  # facturas, PDF y mapa generados (no se suben a Git)

CATALOGO_DB = DATOS / "catalogo.db"      # datos de referencia, versionados
BASE_DATOS = DATOS / "etsiiviajes.db"    # datos de trabajo, se generan al arrancar

VIDEO_MAPA = ASSETS / "mapa-3d.mp4"
FOTO_BUCEO = ASSETS / "reserva" / "buceo.jpg"
FOTO_ESQUI = ASSETS / "reserva" / "esqui.jpg"

BUCEO = "BUCEO"
ESQUI = "ESQUI"
ACTIVIDADES = (BUCEO, ESQUI)

TALLAS = ("XXS", "XS", "S", "M", "L", "XL", "XXL")

EQUIPOS = {
    BUCEO: (
        "Traje (Neopreno)", "Chaleco (BCD)", "Regulador", "Tanque", "Máscara",
        "Aletas", "Cinturón", "Ordenador", "Manómetro", "Cuchillo", "Silbato",
    ),
    ESQUI: (
        "Bastones", "Botas de esqui", "Tablas de snowboard", "Botas de snowboard",
        "Cascos", "Chaquetas", "Pantalones",
    ),
}

# Columna de la tabla fauna_y_flora -> nombre que se muestra al usuario
AGUAS = {
    "atlantico": "Océano Atlántico",
    "pacifico": "Océano Pacífico",
    "indico": "Océano Índico",
    "mediterraneo": "Mar Mediterráneo",
    "caribe": "Mar Caribe",
    "mar_rojo": "Mar Rojo",
    "indo_pacifico": "Indo-Pacífico",
}

TIPOS_CLUB = ("AMATEUR", "PROFESIONAL")
NIVELES = {
    BUCEO: ("AFICIONADO", "RECREATIVO", "CIENTÍFICO", "MILITAR", "POLICIAL"),
    ESQUI: ("ALPINO", "FONDO", "TRAVESÍA", "FREESTYLE", "FREERIDE"),
}

IVA = 0.21
EMAIL_CONTACTO = "info@etsiiviajes.example"

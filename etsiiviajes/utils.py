"""Funciones auxiliares sin dependencia de la interfaz ni de la base de datos."""

import os
import re
import subprocess
import sys
import webbrowser
from datetime import date, datetime
from io import BytesIO
from pathlib import Path

from PIL import Image

LETRAS_DNI = "TRWAGMYFPDXBNJZSQVHLCKE"
_PATRON_DNI = re.compile(r"^[XYZ]?\d{7,8}[A-Z]$")
_PATRON_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[A-Za-z]{2,}$")


def validar_dni(dni: str) -> bool:
    """Comprueba el formato y la letra de control de un DNI o NIE español."""
    dni = dni.strip().upper()
    if not _PATRON_DNI.match(dni):
        return False
    numero = dni[:-1].replace("X", "0").replace("Y", "1").replace("Z", "2")
    return LETRAS_DNI[int(numero) % 23] == dni[-1]


def validar_documento(documento: str) -> bool:
    """Acepta un DNI/NIE válido o un pasaporte (6-12 letras y números)."""
    documento = documento.strip().upper()
    if _PATRON_DNI.match(documento):  # tiene forma de DNI/NIE: la letra debe cuadrar
        return validar_dni(documento)
    return bool(re.fullmatch(r"[A-Z0-9]{6,12}", documento)) and not documento.isdigit()


def validar_email(email: str) -> bool:
    return bool(_PATRON_EMAIL.match(email.strip()))


def a_iso(fecha_ddmmaaaa: str) -> str:
    """'25/01/2024' -> '2024-01-25'."""
    return datetime.strptime(fecha_ddmmaaaa, "%d/%m/%Y").date().isoformat()


def de_iso(fecha_iso: str) -> str:
    """'2024-01-25' -> '25/01/2024'."""
    return date.fromisoformat(fecha_iso[:10]).strftime("%d/%m/%Y")


def edad(fecha_nacimiento: date, hoy: date | None = None) -> int:
    hoy = hoy or date.today()
    return hoy.year - fecha_nacimiento.year - (
        (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day)
    )


def imagen_a_bytes(origen, lado_max: int = 800, calidad: int = 80) -> bytes:
    """Lee una imagen (ruta o bytes), la reduce y la devuelve como JPEG."""
    if isinstance(origen, (bytes, bytearray)):
        origen = BytesIO(origen)
    with Image.open(origen) as img:
        img = img.convert("RGB")
        img.thumbnail((lado_max, lado_max))
        salida = BytesIO()
        img.save(salida, format="JPEG", quality=calidad, optimize=True)
        return salida.getvalue()


def abrir_archivo(ruta) -> None:
    """Abre un archivo con el programa predeterminado del sistema."""
    ruta = Path(ruta).resolve()
    if sys.platform.startswith("win"):
        os.startfile(ruta)  # type: ignore[attr-defined]
    elif sys.platform == "darwin":
        subprocess.Popen(["open", str(ruta)])
    else:
        webbrowser.open(ruta.as_uri())

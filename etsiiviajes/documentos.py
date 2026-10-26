"""Precios, facturas y el PDF informativo que se entrega al cliente."""

import random
from datetime import date
from io import BytesIO
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from .config import AGUAS, EMAIL_CONTACTO, IVA, SALIDA
from .modelos import Especie, Venta
from .utils import de_iso

PRECIO_BASE = 120.0
PRECIO_MINIMO = 40.0


def calcular_precio(fecha_actividad: date, rng: random.Random | None = None) -> float:
    """Precio por persona: baja 1 € cada 5 días desde el 15 de enero, ±10 € y mínimo 40 €."""
    rng = rng or random.Random()
    dias = (fecha_actividad - date(fecha_actividad.year, 1, 15)).days
    precio = PRECIO_BASE - dias / 5 + rng.uniform(-10, 10)
    return round(max(PRECIO_MINIMO, precio), 2)


def desglose_iva(total: float) -> tuple[float, float]:
    """Separa un precio con IVA incluido en (base imponible, cuota de IVA)."""
    base = round(total / (1 + IVA), 2)
    return base, round(total - base, 2)


def generar_factura(venta: Venta, carpeta: Path = SALIDA) -> Path:
    """Crea ``factura_<n>_<año>.pdf``. El número de factura es el de la venta."""
    carpeta.mkdir(parents=True, exist_ok=True)
    anio = venta.fecha_venta[:4]
    ruta = carpeta / f"factura_{venta.id}_{anio}.pdf"
    base, cuota_iva = desglose_iva(venta.precio_total)

    pdf = canvas.Canvas(str(ruta), pagesize=A4)
    _, alto = A4
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, alto - 60, "ETSIIVIAJES · Factura")
    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, alto - 85, f"Número: {venta.id}/{anio}")
    pdf.drawString(50, alto - 100, f"Fecha: {de_iso(venta.fecha_venta)}")
    pdf.drawString(50, alto - 130, f"Cliente: {venta.nombre}")
    pdf.drawString(50, alto - 145, f"DNI: {venta.dni}")

    y = alto - 190
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(50, y, "Concepto")
    for x, texto in ((330, "Personas"), (430, "Precio/u."), (545, "Importe")):
        pdf.drawRightString(x, y, texto)
    pdf.line(50, y - 5, 545, y - 5)
    pdf.setFont("Helvetica", 11)
    y -= 22
    pdf.drawString(50, y, f"Alquiler de equipo de {venta.actividad.lower()}, talla {venta.talla}")
    pdf.drawRightString(330, y, str(venta.cantidad))
    pdf.drawRightString(430, y, f"{venta.precio_unitario:.2f} €")
    pdf.drawRightString(545, y, f"{venta.precio_total:.2f} €")
    pdf.setFont("Helvetica", 9)
    pdf.drawString(50, y - 13, f"Centro de {venta.pais.title()} · {de_iso(venta.fecha_actividad)}")
    pdf.setFont("Helvetica", 11)

    y -= 50
    for etiqueta, importe in (("Base imponible", base), (f"IVA ({IVA:.0%})", cuota_iva)):
        pdf.drawString(350, y, etiqueta)
        pdf.drawRightString(545, y, f"{importe:.2f} €")
        y -= 18
    pdf.line(350, y + 8, 545, y + 8)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(350, y - 6, "Total")
    pdf.drawRightString(545, y - 6, f"{venta.precio_total:.2f} €")
    pdf.save()
    return ruta


def aguas_de_pais(puntos) -> list[str]:
    """Claves de ``config.AGUAS`` en las que hay algún punto de inmersión."""
    por_nombre = {v: k for k, v in AGUAS.items()}
    return sorted({por_nombre[p.aguas] for p in puntos if p.aguas in por_nombre})


def generar_informe_especies(cliente: str, pais: str, especies: list[Especie],
                             carpeta: Path = SALIDA) -> Path:
    """PDF con foto y nombre de las especies de las aguas del país (4 por fila)."""
    carpeta.mkdir(parents=True, exist_ok=True)
    ruta = carpeta / f"especies_{pais.lower().replace(' ', '_')}.pdf"
    pdf = canvas.Canvas(str(ruta), pagesize=A4)
    ancho, alto = A4

    def cabecera():
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawCentredString(ancho / 2, alto - 50, f"Fauna y flora de las aguas de {pais.title()}")
        pdf.setFont("Helvetica", 11)
        pdf.drawCentredString(ancho / 2, alto - 75,
                              f"Estimado/a {cliente}: estas son las especies que puede encontrar.")
        pdf.drawCentredString(ancho / 2, alto - 92,
                              f"Para cualquier duda escríbanos a {EMAIL_CONTACTO}. ¡Disfrute su aventura!")

    cabecera()
    lado, margen_x, hueco = 100, 60, 125
    y = alto - 230
    for i, especie in enumerate(especies):
        columna = i % 4
        if columna == 0 and i > 0:
            y -= 140
            if y < 60:
                pdf.showPage()
                cabecera()
                y = alto - 230
        x = margen_x + columna * hueco
        if especie.foto:
            pdf.drawImage(ImageReader(BytesIO(especie.foto)), x, y, lado, lado,
                          preserveAspectRatio=True, anchor="c")
        pdf.setFont("Helvetica", 9)
        pdf.drawCentredString(x + lado / 2, y - 14, especie.nombre.capitalize())
    pdf.save()
    return ruta

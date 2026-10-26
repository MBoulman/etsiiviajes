"""Mapa mundial interactivo (Folium) con los puntos de buceo y de esquí."""

import base64
import html
from pathlib import Path

import folium

from .config import SALIDA
from .gestor import GestorBasesDatos
from .utils import imagen_a_bytes

RUTA_MAPA = SALIDA / "mapa.html"
MAPAS_BASE = {"Callejero": "World_Street_Map", "Satélite": "World_Imagery"}


def _popup(titulo: str, lineas: list[str], foto: bytes | None) -> folium.Popup:
    contenido = f"<b>{html.escape(titulo)}</b><br>" + "<br>".join(html.escape(l) for l in lineas)
    if foto:
        miniatura = base64.b64encode(imagen_a_bytes(foto, lado_max=300, calidad=70)).decode()
        contenido += (f"<br><img src='data:image/jpeg;base64,{miniatura}' "
                      "style='width:180px;height:auto;margin-top:4px'>")
    return folium.Popup(contenido, max_width=220)


def generar_mapa(gestor: GestorBasesDatos, ruta: Path = RUTA_MAPA) -> Path:
    """Crea el HTML del mapa con una capa por actividad y un selector de capas."""
    mapa = folium.Map(location=[20, 0], zoom_start=2, tiles=None)
    # Mapas base de Esri: funcionan sin clave y también al abrir el HTML como archivo
    # local (los servidores de OpenStreetMap bloquean las peticiones sin «Referer»).
    for nombre, servicio in MAPAS_BASE.items():
        folium.TileLayer(
            tiles=f"https://server.arcgisonline.com/ArcGIS/rest/services/{servicio}/MapServer/tile/{{z}}/{{y}}/{{x}}",
            attr="Tiles &copy; Esri", name=nombre, max_zoom=18,
        ).add_to(mapa)
    buceo = folium.FeatureGroup(name="Puntos de buceo")
    esqui = folium.FeatureGroup(name="Puntos de esquí")

    for p in gestor.puntos_inmersion():
        folium.Marker(
            [p.latitud, p.longitud], tooltip=p.nombre,
            popup=_popup(p.nombre, [p.pais.title(), p.aguas, f"Profundidad: {p.profundidad:g} m"],
                         p.foto),
            icon=folium.Icon(color="purple", icon="tint"),
        ).add_to(buceo)

    for p in gestor.puntos_esqui():
        folium.Marker(
            [p.latitud, p.longitud], tooltip=p.nombre,
            popup=_popup(p.nombre, [p.pais.title(), f"{p.km_pistas:g} km de pistas"],
                         p.mapa_pistas),
            icon=folium.Icon(color="lightgreen", icon="flag"),
        ).add_to(esqui)

    buceo.add_to(mapa)
    esqui.add_to(mapa)
    folium.LayerControl(collapsed=False).add_to(mapa)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    mapa.save(str(ruta))
    return ruta

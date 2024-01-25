# Sofía Veldman Paniego
# Mohamed Boulman Mokhlis
# Juan del Junco Sampol


import base64
import folium
from sqlalchemy import create_engine, Column, String, Float, BLOB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import webbrowser
import os
from sqlalchemy.orm import declarative_base
Base = declarative_base()

class PuntoInmersion(Base):
    __tablename__ = 'Puntos_inmersion'

    Nombre = Column(String, primary_key=True)
    Latitud = Column(Float)
    Longitud = Column(Float)
    Foto = Column(BLOB)


class PuntoEsqui(Base):
    __tablename__ = 'Puntos_esqui'
    
    Nombre = Column(String, primary_key=True)
    Latitud = Column(Float)
    Longitud = Column(Float)
    mapa_pistas = Column(BLOB)


class Mapamundi:
    def __init__(self):
        self.mapa = folium.Map(location=[0, 0], zoom_start=1.5)
        self.mostrar_buceo = True
        self.mostrar_esqui = True
        self.puntos_buceo = folium.FeatureGroup(name='Puntos de Buceo')
        self.puntos_esqui = folium.FeatureGroup(name='Puntos de Esquí')

    def agregar_punto_buceo(self, nombre, latitud, longitud, foto=None):
        popup_content = f"<b>{nombre}</b>"
        if foto:
            encoded_image = base64.b64encode(foto).decode('utf-8')
            popup_content += f"<br><img src='data:image/png;base64,{encoded_image}' alt='Foto' style='width:150px;height:150px;'>"
        punto = folium.Marker(
            [latitud, longitud],
            popup=folium.Popup(popup_content, max_width=200),
            icon=folium.Icon(color='purple', shadow=False)
        )
        punto.add_to(self.puntos_buceo)

    def agregar_punto_esqui(self, nombre, latitud, longitud, foto=None):
        popup_content = f"<b>{nombre}</b>"
        if foto:
            encoded_image = base64.b64encode(foto).decode('utf-8')
            popup_content += f"<br><img src='data:image/png;base64,{encoded_image}' alt='Foto' style='width:150px;height=150px;'>"
        punto = folium.Marker(
            [latitud, longitud],
            popup=folium.Popup(popup_content, max_width=200),
            icon=folium.Icon(color='lightgreen', shadow=False)
        )
        punto.add_to(self.puntos_esqui)

    def agregar_controles_capas(self):
        folium.LayerControl().add_to(self.mapa)

    def agregar_checkbox(self, nombre, estado_inicial, capa):
        checkbox = folium.map.CustomPane(nombre, z_index=10)
        checkbox.add_to(self.mapa)


    def obtener_puntos_inmersion(self):
        # LA RUTA DE LA BASE DE DATOS
        script_directory = os.path.dirname(os.path.realpath(__file__))
        db_path = os.path.join(script_directory, 'Bases_datos', 'Puntos_inmersion.sqlite')
        engine = create_engine(f'sqlite:///{db_path}')

        Session = sessionmaker(bind=engine)
        session = Session()

        puntos = session.query(PuntoInmersion).all()

        session.close()
        return puntos
    
    def obtener_puntos_esqui(self):
        # LA RUTA DE LA BASE DE DATOS
        script_directory = os.path.dirname(os.path.realpath(__file__))
        db_path = os.path.join(script_directory, 'Bases_datos', 'Puntos_esqui.db')
        engine = create_engine(f'sqlite:///{db_path}')

        Session = sessionmaker(bind=engine)
        session = Session()

        puntos = session.query(PuntoEsqui).all()

        session.close()
        return puntos

    def mostrar_mapa(self):
        # LIMPIAMOS EL MAPA
        self.mapa = folium.Map(location=[0, 0], zoom_start=1.5)  

        puntos_inmersion = self.obtener_puntos_inmersion()
        puntos_esqui = self.obtener_puntos_esqui()

        if not puntos_inmersion and not puntos_esqui:
            print("No se encontraron puntos en la base de datos.")
            return

        # AGREGAMOS CHECKBOX Y CAPAS
        self.agregar_checkbox("Mostrar Buceo", self.mostrar_buceo, "Puntos de Buceo")
        self.agregar_checkbox("Mostrar Esquí", self.mostrar_esqui, "Puntos de Esquí")

        # AGREGAMOS LOS PUNTOS INMERSIÓN
        if puntos_inmersion and self.mostrar_buceo:
            for punto in puntos_inmersion:
                self.agregar_punto_buceo(punto.Nombre, punto.Latitud, punto.Longitud, foto=punto.Foto)

        # AGREGAMOS LOS PUNTOS ESQUI
        if puntos_esqui and self.mostrar_esqui:
            for punto in puntos_esqui:
                self.agregar_punto_esqui(punto.Nombre, punto.Latitud, punto.Longitud, foto=punto.mapa_pistas)

        # AGREGAMOS CAPAS
        self.mapa.add_child(self.puntos_buceo)
        self.mapa.add_child(self.puntos_esqui)

        # AGREGAMOS CONTROLES DE CAPAS
        self.agregar_controles_capas()

        # Crear un script JavaScript para controlar la visibilidad de las capas
        script = """
            function toggleLayer(checkbox, layerName) {
                var layer = map.layerControl._layers[layerName].layer;
                if (checkbox.checked) {
                    map.addLayer(layer);
                } else {
                    map.removeLayer(layer);
                }
            }
        """
        # PASAMOS A  HTML
        folium.Html(script).add_to(self.mapa)

        self.mapa.save('mapa.html')
        webbrowser.open('mapa.html')
        print("Mapa generado. Abre el archivo 'mapa.html' en tu navegador para ver los puntos.")

if __name__ == "__main__":
    mapa_mundi = Mapamundi()
    mapa_mundi.mostrar_mapa()

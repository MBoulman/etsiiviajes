# Sofía Veldman Paniego
# Mohamed Boulman Mokhlis
# Juan del Junco Sampol

import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from datetime import datetime
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random
from GestorBaseDatos import*


gestor = GestorBasesDatos()  
fauna_flora = gestor.Extracion_datos_fauna_flora()
fauna_flora_sin=gestor.Extracion_datos_fauna_flor_sin()


def variedad_por_oceano():
    regiones = ['ATLANTICO', 'PACIFICO', 'INDICO', 'MEDITERRANEO', 'CARIBE','MAR ROJO','INDO-PACIFICO']
    conteo_por_region = {region: sum(especie[region] for especie in fauna_flora) for region in regiones}
    print("Conteo de especies por región:", conteo_por_region)
    return conteo_por_region
def flora_oceano(region_a_consultar):
    regiones_sin = ['ATLANTICO', 'PACIFICO', 'INDICO', 'MEDITERRANEO', 'CARIBE','MAR ROJO','INDO-PACIFICO']
    
    especies_en_region_sin = [especie.get('Fauna') for especie in fauna_flora_sin if especie.get(region_a_consultar) == 1]

    if not especies_en_region_sin:
        print(f"No hay especies de fauna en el {region_a_consultar}")
        return

    print(f"Especies en el {region_a_consultar}")

    # Grafico pastel
    labels = list(set(especies_en_region_sin))
    sizes = [especies_en_region_sin.count(label) for label in labels]

    # Generar colores aleatorios
    num_colors = len(labels)
    colors = ['#%06x' % random.randint(0, 0xFFFFFF) for _ in range(num_colors)]

    # Ajustar al tamaño de la figura
    fig, ax = plt.subplots(figsize=(10, 10))

    wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140, textprops=dict(color="w", fontsize=6))

    # Los nombres dentro del disco
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    kw = dict(arrowprops=dict(arrowstyle="-"),
              bbox=bbox_props, zorder=0, va="center")

    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = "angle,angleA=0,angleB={}".format(ang)
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax.annotate(labels[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                    horizontalalignment=horizontalalignment, **kw, fontsize=6)

    plt.axis('equal')  
    plt.title(f'DISTRIBUCIÓN DE LA REGIÓN {region_a_consultar}')
    plt.tight_layout() 
    plt.show()


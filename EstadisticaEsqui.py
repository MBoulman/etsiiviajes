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
datos_esquiadores_extraidos = gestor.ExtraccionEsquiadores()

df=pd.DataFrame(datos_esquiadores_extraidos)


#Convertimos formato fecha para sacar la edad real
hoy = datetime.today()
df['fecha_nacimiento'] = pd.to_datetime(df['fecha_nacimiento'], format='%d/%m/%Y')
df['edad'] = hoy.year - df['fecha_nacimiento'].dt.year



##Primero ANALISIS GENERAL
#Media de edad
def media_edad_esqui():
    media_edad =df['edad'].mean()
    print("La media de edad de los buzos es:", media_edad)
    return media_edad
#Cuartiles
def cuartiles_esqui():
    cuartiles_edad = df['edad'].quantile([0.25, 0.5, 0.75])
    print("Primer cuartil (25%):", cuartiles_edad[0.25])
    print("Mediana (Segundo cuartil - 50%):", cuartiles_edad[0.5])
    print("Tercer cuartil (75%):", cuartiles_edad[0.75])
    return cuartiles_edad
#NACIONALIDADES
def max_nacionalidad_esqui():
    max=df['Pais'].value_counts()
    print('TOTAL POR NACIONALIDAD: ',max)

    colores = ['#%06x' % random.randint(0, 0xFFFFFF) for _ in range(len(df['Pais'].value_counts()))]
    max.plot(kind='bar', figsize=(8, 6), color=colores)
    plt.title('NÚMERO DE ESQUIADORES POR PAÍS')
    plt.xlabel('PAÍSES')
    plt.ylabel('CANTIDAD DE ESQUIADORES')
    plt.xticks(rotation=45)
    plt.show()

    return max
#NIVELES DE BUCEO
def nivel_esqui():
    nivel=df['tipo_esquiador'].value_counts()
    print('Para cada nivel tenemos: ',nivel)

    nivel.plot(kind='pie', figsize=(7, 7), autopct='%1.1f%%', startangle=90, colors=['orange','gold', 'red', 'blue', 'green'])
    plt.title('DISTRIBUCIÓN DE NIVELES DE ESQUIADORES')
    plt.axis('equal')  # Hace que el gráfico de pastel se vea como un círculo
    plt.show()

    return nivel

def cluster_esqui():
    data=df[['Altura','Peso','edad','Pais']]

    #Pasamos a factor la columna de datos Pais (no numerica)
    column_transf=ColumnTransformer([('encoder', OneHotEncoder(), [3])], remainder='passthrough')
    data_encoded=column_transf.fit_transform(data)


    #Normalizamos los datos
    scaled = StandardScaler(with_mean=False)
    data_scaled = scaled.fit_transform(data_encoded)
    #Cluster metodo kmeans(hacemos 3 grupos)
    kmeans=KMeans(n_clusters=3,n_init=25)
    kmeans.fit(data_scaled)

    df['Cluster']=kmeans.labels_ #Le ponemos etiquetas a cada observacion del dataframe

    plt.scatter(df['Altura'], df['Peso'], c=df['Cluster'], cmap='viridis', marker='o')
    plt.title('CLUSTERS DE ESQUIADORES POR ALTURA Y PESO')
    plt.xlabel('ALTURA')
    plt.ylabel('PESO')
    plt.show()

    # Boxplot de 'edad' por cluster

    df.boxplot(column='edad', by='Cluster', figsize=(10, 6))
    plt.title('BOXPLOT DE ALTURA POR CLUSTER')
    plt.xlabel('CLUSTE')
    plt.ylabel('EDAD')
    plt.suptitle('')  # Para eliminar el título predeterminado generado por boxplot
    plt.show()

    #3D

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')

    # Gráfico tridimensional de 'Altura', 'Peso' y 'Edad' por cluster
    for cluster in df['Cluster'].unique():
        cluster_data = df[df['Cluster'] == cluster]
        ax.scatter(cluster_data['Altura'], cluster_data['Peso'], cluster_data['edad'], label=f'Cluster {cluster}')

    ax.set_title('VISUALIZACIÓN EN 3D DE CLUSTERS')
    ax.set_xlabel('ALTURA')
    ax.set_ylabel('PESO')
    ax.set_zlabel('EDAD')
    ax.legend()
    plt.show()

#max_nacionalidad()
#media_edad()
#cuartiles()
#nivel_buzo()
#cluster()

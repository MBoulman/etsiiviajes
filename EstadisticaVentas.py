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
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import random
import matplotlib
from GestorBaseDatos import*

gestor = GestorBasesDatos()
datos_ventas_extraidos = gestor.ExtraccionVentas()
df=pd.DataFrame(datos_ventas_extraidos)

def media_gasto():
    media=df['Precio'].mean()
    print('La media del gasto de los clientes en € es: ',float(media))

    return media

def media_por_pais():
    media=df.groupby('Pais')['Precio'].mean()
    print('La media de gasto por nacionalidades es: ',media)

    colores = []
    for i in range(len(media)):
        colores.append('#%06x' % random.randint(0, 0xFFFFFF))

    #Grafico de media por pais
    media.plot(kind='bar', figsize=(10, 6),color=colores)
    plt.title('MEDIA DE GASTO POR NACIONALIDAD')
    plt.xlabel('PAISES')
    plt.ylabel('PRECIO')
    plt.xticks(rotation=45)
    plt.show()


    return media

def ventas_por_actividad():
    media=df.groupby('Actividad')['Precio'].sum()
    print('La media de ventas por actividad es: ',media)

    colores = []
    for i in range(len(media)):
        colores.append('#%06x' % random.randint(0, 0xFFFFFF))

    # Grafico de ventas por actividad
    media.plot(kind='bar', figsize=(10, 6),color=colores)
    plt.title('VENTAS POR ACTIVIDAD')
    plt.xlabel('ACTIVIDADES')
    plt.ylabel('TOTAL DE VENTAS')
    plt.xticks(rotation=45)
    plt.show()

    #Me premitirá ver que actividad es mas rentable/ produce mayores ventas
    return media

def tallas_mas_vendidas():
    tallas=df['Talla'].value_counts()

    colores = ['#%06x' % random.randint(0, 0xFFFFFF) for _ in range(len(tallas.index))]

    # Crear gráfico de barras para visualizar las tallas más vendidas con colores aleatorios
    tallas.plot(kind='bar', figsize=(8, 6), color=colores)
    plt.title('CANTIDAD DE VENTAS POR TALLA')
    plt.xlabel('TALLAS')
    plt.ylabel('CANTIDAD')
    plt.xticks(rotation=45)
    plt.show()

    return tallas

#Haremos un analisis con regresión lineal para poder hacer una prediccion
#de los poribles intereses del usuario

def predict_precio(talla,pais,actividad):
    #Vamos a precedir cuanto se gastan de media los usuarios en funcion de:
    X = pd.get_dummies(df[['Talla', 'Pais', 'Actividad']])
    y = df['Precio']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    #Como corresponde, debemos dividir la base de datos en train y test, para corroborar la ejectividad del modelo (R^2)
    regression_model = LinearRegression()
    regression_model.fit(X_train, y_train)

    y_pred = regression_model.predict(X_test)
    #Hacemos predicciones con el grupo test para hacer la validación cruzada
    mse = mean_squared_error(y_test, y_pred) #Error acumulado
    r2 = r2_score(y_test, y_pred) #Como de bien explica el modelo
    #print(f"Error cuadrático medio (MSE): {mse}")
    #print(f"Coeficiente de determinación (R2): {r2}")

    #Vamos a predecir con la nueva observación
    #print('Introudzca por pantalla los siguientes datos:\n')
   # talla=input('Cual es la talla: ')
    #pais=input('Cual es el pais (primera letra en mayuscula): ')
    #actividad=input('Cual es la actividad (ESQUI o BUCEO): ')
    nuevo={'Talla':talla,'Pais':pais,'Actividad':actividad}
    nuevo_df=pd.DataFrame([nuevo])

    nuevo_numerico = pd.get_dummies(nuevo_df)

    X_train_columns = X_train.columns
    for column in X_train_columns:
        if column not in nuevo_numerico.columns:
            nuevo_numerico[column] = 0
    #Reordenamos las clumnas
    nuevo_numerico = nuevo_numerico[X_train_columns]

    precio_predicho = regression_model.predict(nuevo_numerico)
    print(f"El precio predicho para la nueva instancia es: {precio_predicho[0]}")
    return precio_predicho[0]


#media_gasto()
#media_por_pais()

#predict_precio()





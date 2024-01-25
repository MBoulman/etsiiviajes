# Sofía Veldman Paniego
# Mohamed Boulman Mokhlis
# Juan del Junco Sampol

import sqlite3
import os
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
#from EnviarCorreo import*
from Compra import*
from Buzo import*
from Esquiador import*
from fauna_y_flora import*
from io import BytesIO
import base64
from PIL import Image, ImageTk
from Compra import Alquiler

class GestorBasesDatos:
    def __init__(self):
        self.base_datos_folder = "Bases_datos"  # Carpeta para las bases de datos
        self._crear_carpeta_base_datos()  # Verificamos y creamos la carpeta si no existe

        self.buzos_db = os.path.join(self.base_datos_folder, "buzos.db")
        self.esquiadores_db = os.path.join(self.base_datos_folder, "esquiadores.db")
        self.club_db = os.path.join(self.base_datos_folder, "club.db")
        self.Puntos_inmersion_db = os.path.join(self.base_datos_folder, "Puntos_inmersion.SQLITE")        
        self.Centro_Buceo_db = os.path.join(self.base_datos_folder, "Centro_Buceo.SQLITE")
        self.Puntos_Esqui_db = os.path.join(self.base_datos_folder, "Puntos_Esqui.db")        
        self.Centro_Esqui_db = os.path.join(self.base_datos_folder, "Centro_Esqui.SQLITE")
        self.Ventas_por_cliente_db = os.path.join(self.base_datos_folder, "Ventas_por_cliente.db") 
        self.fauna_y_flora_db = os.path.join(self.base_datos_folder, "fauna_y_flora.db")

        # Comprueba si las bases de datos existen, si no, las crea
        self._crear_base_datos(self.buzos_db)
        self._crear_base_datos(self.esquiadores_db)
        self._crear_base_datos(self.club_db)
        self._crear_base_datos(self.Puntos_inmersion_db)
        self._crear_base_datos(self.Centro_Buceo_db)
        self._crear_base_datos(self.Puntos_Esqui_db)
        self._crear_base_datos(self.Centro_Esqui_db)
        self._crear_base_datos(self.Ventas_por_cliente_db)
        self._crear_base_datos(self.fauna_y_flora_db)



        # creamos las conexiones con las bases de datos
        self.buzos_conn = sqlite3.connect(self.buzos_db)
        self.buzos_cursor = self.buzos_conn.cursor()

        self.esquiadores_conn = sqlite3.connect(self.esquiadores_db)
        self.esquiadores_cursor = self.esquiadores_conn.cursor()

        self.club_conn = sqlite3.connect(self.club_db)
        self.club_cursor = self.club_conn.cursor()

        self.Puntos_inmersion_conn = sqlite3.connect(self.Puntos_inmersion_db)
        self.Puntos_inmersion_cursor = self.Puntos_inmersion_conn.cursor()
        self.Centro_Buceo_conn = sqlite3.connect(self.Centro_Buceo_db)
        self.Centro_Buceo_cursor = self.Centro_Buceo_conn.cursor()

        self.Puntos_Esqui_conn = sqlite3.connect(self.Puntos_Esqui_db)
        self.Puntos_Esqui_cursor = self.Puntos_Esqui_conn.cursor()
        self.Centro_Esqui_conn = sqlite3.connect(self.Centro_Esqui_db)
        self.Centro_Esqui_cursor = self.Centro_Esqui_conn.cursor()

        self.Ventas_por_cliente_conn = sqlite3.connect(self.Ventas_por_cliente_db)
        self.Ventas_por_cliente_cursor = self.Ventas_por_cliente_conn.cursor()


        self.fauna_y_flora_conn = sqlite3.connect(self.fauna_y_flora_db)
        self.fauna_y_flora_cursor = self.fauna_y_flora_conn.cursor()
       
        # Creamos las tbalas
        self._crear_tabla_buzos()
        self._crear_tabla_esquiadores()
        self._crear_tabla_puntos_inmersion()
        self._crear_tabla_Centro_Buceo()
        self._crear_tabla_puntos_Esqui()
        self._crear_tabla_Centro_Esqui()
        self._crear_tabla_Ventas_por_cliente()
        self._crear_tabla_fauna_y_flora()

    def _crear_carpeta_base_datos(self):
        if not os.path.exists(self.base_datos_folder):
            os.makedirs(self.base_datos_folder)
            print(f"Carpeta '{self.base_datos_folder}' creada correctamente.")
        else:
            print(f"Carpeta '{self.base_datos_folder}' ya existe.")

    def _crear_base_datos(self, db_path):
        if not os.path.exists(db_path):
            open(db_path, 'a').close()  # Crea un archivo vacío si no existe
            print(f"Base de datos '{db_path}' creada correctamente.")
        else:
            print(f"Base de datos '{db_path}' ya existe.")

#-----------------------------------------------------------------------------------
#Buzos
        
    def _crear_tabla_buzos(self):
        self.buzos_cursor.execute('''
            CREATE TABLE IF NOT EXISTS buzos (
                dni TEXT PRIMARY KEY,
                nombre TEXT,
                apellidos TEXT, 
                fecha_nacimiento DATE,
                nacionalidad TEXT,
                peso INT,
                altura INT,
                tel INT, 
                email TEXT,
                direccion TEXT,
                tipo_club TEXT,
                tipo_buzo TEXT,
                enfermedad TEXT,
                foto BLOB
            )
        ''')
        self.buzos_conn.commit()
        
    def guardar_buzo(self, buzo):
        # Verifica si el DNI existe
        self.buzos_cursor.execute('SELECT dni FROM buzos WHERE dni = ?', (buzo.dni,))
        existente = self.buzos_cursor.fetchone()

        if existente:
            print("El DNI ya existe en la base de datos. No se puede agregar este buzo.")
        else:
            self.buzos_cursor.execute('''
                INSERT INTO buzos (dni, nombre, apellidos, fecha_nacimiento, nacionalidad,
                                    peso, altura, tel, email, direccion, tipo_club,
                                    tipo_buzo, enfermedad, foto)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (buzo.dni, buzo.nombre, buzo.apellidos, buzo.fecha_nacimiento, buzo.nacionalidad,
                  buzo.peso, buzo.altura, buzo.tel, buzo.email, buzo.direccion, buzo.tipo_club,
                  buzo.tipo_buzo, buzo.enfermedad, buzo.foto))
            self.buzos_conn.commit()

    def mostrar_buzo_por_dni(self, dni):
        
            self.buzos_cursor.execute('SELECT * FROM buzos WHERE dni = ?', (dni,))
            buzo_dato = self.buzos_cursor.fetchone()

            if buzo_dato:
                # Construimos el objeto buzo recuperado de la BD
                buzo = Buzo(*buzo_dato)
                return buzo

    def borrar_buzo_por_dni(self, dni):
            self.buzos_cursor.execute('SELECT * FROM buzos WHERE dni = ?', (dni,))
            buzo = self.buzos_cursor.fetchone()

            if buzo:
                self.buzos_cursor.execute('DELETE FROM buzos WHERE dni = ?', (dni,))
                self.buzos_conn.commit()
                print("Buzo borrado correctamente")
            else:
                print("Buzo no encontrado")
#-----------------------------------------------------------------------------------
#Esquiadores
        
    def _crear_tabla_esquiadores(self):
        self.esquiadores_cursor.execute('''
            CREATE TABLE IF NOT EXISTS esquiadores (
                dni TEXT PRIMARY KEY,
                nombre TEXT,
                apellidos TEXT, 
                fecha_nacimiento DATE,
                nacionalidad TEXT,
                peso INT,
                altura INT,
                tel INT, 
                email TEXT,
                direccion TEXT,
                tipo_club TEXT,
                tipo_esquiador TEXT,
                enfermedad TEXT,
                foto BLOB
            )
        ''')
        self.esquiadores_conn.commit()
        
    def guardar_esquiador(self, esquiador):
        # Verifica si existe el DNI
        self.esquiadores_cursor.execute('SELECT dni FROM esquiadores WHERE dni = ?', (esquiador.dni,))
        existente = self.esquiadores_cursor.fetchone()

        if existente:
            print("El DNI ya existe en la base de datos. No se puede agregar este esquiador.")
        else:
            self.esquiadores_cursor.execute('''
                INSERT INTO esquiadores (dni, nombre, apellidos, fecha_nacimiento, nacionalidad,
                                    peso, altura, tel, email, direccion, tipo_club,
                                    tipo_esquiador, enfermedad, foto)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (esquiador.dni, esquiador.nombre, esquiador.apellidos, esquiador.fecha_nacimiento, esquiador.nacionalidad,
                  esquiador.peso, esquiador.altura, esquiador.tel, esquiador.email, esquiador.direccion, esquiador.tipo_club,
                  esquiador.tipo_esquiador, esquiador.enfermedad, esquiador.foto))
            self.esquiadores_conn.commit()

    def mostrar_esquiador_por_dni(self, dni):
        self.esquiadores_cursor.execute('SELECT * FROM esquiadores WHERE dni = ?', (dni,))
        esquiador_dato = self.esquiadores_cursor.fetchone()

        if esquiador_dato:
            # Construye el objeto Esquiador con los datos recuperados de la BD
            esquiador = Esquiador(*esquiador_dato)
            return esquiador

    def borrar_esquiador_por_dni(self, dni):
    
            self.esquiadores_cursor.execute('SELECT * FROM esquiadores WHERE dni = ?', (dni,))
            esquiador = self.esquiadores_cursor.fetchone()
            if esquiador:
                self.esquiadores_cursor.execute('DELETE FROM esquiadores WHERE dni = ?', (dni,))
                self.esquiadores_conn.commit()
#-----------------------------------------------------------------------------------
#Puntos de inmersion

    def _crear_tabla_puntos_inmersion(self):
        self.Puntos_inmersion_cursor.execute('''
            CREATE TABLE IF NOT EXISTS Puntos_inmersion (
                Nombre TEXT PRIMARY KEY,
                Pais TEXT,
                Latitud REAL,
                Longitud REAL,
                Aguas TEXT,
                Profundidad REAL,
                Foto BLOB
            )
        ''')
        self.Puntos_inmersion_conn.commit()

    def agregar_punto_inmersion(self, punto):
        # Verificar si el punto ya existe en la base de datos (usando el nombre como clave primaria)
        self.Puntos_inmersion_cursor.execute('SELECT Nombre FROM Puntos_inmersion WHERE Nombre = ?', (punto.Nombre,))
        existente = self.Puntos_inmersion_cursor.fetchone()

        if existente:
            print("El punto de inmersión ya existe en la base de datos. No se puede agregar.")
        else:
            self.Puntos_inmersion_cursor.execute('''
                INSERT INTO Puntos_inmersion (Nombre, Pais, Latitud, Longitud, Aguas, Profundidad, Foto)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (punto.Nombre, punto.Pais, punto.Latitud, punto.Longitud, punto.Aguas, punto.Profundidad, punto.Foto))
            self.Puntos_inmersion_conn.commit()




    def mostrar_punto_inmersion_por_nombre(self, nombre):
        try:
            self.Puntos_inmersion_cursor.execute('SELECT Nombre, Pais, Latitud, Longitud, Aguas, Profundidad FROM Puntos_inmersion WHERE Nombre = ?', (nombre,))
            punto = self.Puntos_inmersion_cursor.fetchone()

            if punto:
                return punto
            else:
                print(f"No se encontró el punto de inmersión con el nombre '{nombre}'.")
                return None
        except Exception as e:
            print(f"Error al buscar el punto de inmersión: {e}")
            return None



    def borrar_punto_inmersion_por_nombre(self,Nombre):
      
        self.Puntos_inmersion_cursor.execute('DELETE FROM Puntos_inmersion WHERE Nombre = ?', (Nombre,))
        self.Puntos_inmersion_conn.commit()


    def buscar_puntos_por_pais(self, pais):
        # Consulta para recuperar Nombre y Aguas para el país dado
        consulta = '''
            SELECT Nombre, Aguas
            FROM Puntos_inmersion
            WHERE Pais = ?
        '''

        # Introducimos try-excepte para manejar errores
        try:
            # Consulta con el país proporcionado
            self.Puntos_inmersion_cursor.execute(consulta, (pais,))

            #  resultados
            resultados = self.Puntos_inmersion_cursor.fetchall()

            # Devolver los resultados
            return resultados
        except Exception as e:
            # Errores(puedes querer registrar o imprimir el error)
            print(f"Error durante la búsqueda: {e}")
            return None
#---------------------------------------------------------------------------------------
#Puntos de Esqui

    def _crear_tabla_puntos_Esqui(self):
        self.Puntos_Esqui_cursor.execute('''
            CREATE TABLE IF NOT EXISTS Puntos_Esqui (
                Nombre TEXT PRIMARY KEY,
                Pais TEXT,
                Latitud REAL,
                Longitud REAL,
                Km_pistas Real,
                Mapa_pistas BLOB
            )
        ''')
        self.Puntos_Esqui_conn.commit()


    def agregar_punto_Esqui(self, punto):
        # verifica Si el punto existe en la base de datos (usando el nombre como clave primaria)
        self.Puntos_Esqui_cursor.execute('SELECT Nombre FROM Puntos_Esqui WHERE Nombre = ?', (punto.nombre,))
        existente = self.Puntos_Esqui_cursor.fetchone()

        if existente:
            print("El punto de Esqui ya existe en la base de datos. No se puede agregar.")
        else:
            self.Puntos_Esqui_cursor.execute('''
                INSERT INTO Puntos_Esqui (Nombre, Pais, Latitud, Longitud, Km_pistas, Mapa_pistas)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (punto.nombre, punto.pais, punto.latitud, punto.longitud, punto.km_pistas, punto.mapa_pistas))
            self.Puntos_Esqui_conn.commit()


    def mostrar_punto_esqui_por_nombre(self,Nombre):
        try:
            self.Puntos_Esqui_cursor.execute('SELECT * FROM Puntos_Esqui WHERE Nombre = ?', (Nombre,))
            punto = self.Puntos_Esqui_cursor.fetchone()

            if punto:
                return punto
            else:
                    print(f"No se encontró el punto de Esqui  con el nombre '{nombre}'.")
                    return None
        except Exception as e:
            print(f"Error al buscar el punto de Esqui: {e}")


    def borrar_punto_inmersion_por_nombre(self,Nombre):
      
        self.Puntos_inmersion_cursor.execute('DELETE FROM Puntos_inmersion WHERE Nombre = ?', (Nombre,))
        self.Puntos_inmersion_conn.commit()


    def borrar_punto_esqui_por_nombre(self,Nombre):

        self.Puntos_Esqui_cursor.execute('DELETE FROM Puntos_Esqui WHERE Nombre = ?', (Nombre,))
        self.Puntos_Esqui_conn.commit()
#-------------------------------------------------------------------------------------
#Centro de buceo
    def _crear_tabla_Centro_Buceo(self):
        self.Centro_Buceo_cursor.execute('''
            CREATE TABLE IF NOT EXISTS Centro_Buceo (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Equipo_de_Buceo TEXT,
                Pais TEXT,
                XXS INTEGER,
                XS INTEGER,
                S INTEGER,
                M INTEGER,
                L INTEGER,
                XL INTEGER,
                XXL INTEGER,
                Precio_Compra REAL
            )
        ''')
        self.Centro_Buceo_conn.commit()

    def agregar_compra_Buceo(self, compra):
        # Lista de nombres permitidos
        nombres_permitidos = [
            "Traje (Neopreno)",
            "Chaleco (BCD)",
            "Regulador",
            "Tanque",
            "Máscara",
            "Aletas",
            "Cinturón",
            "Ordenador",
            "Manómetro",
            "Cuchillo",
            "Silbato"
        ]

        # Convierte el pais en Mayuscula
        compra.pais = compra.pais.upper()

        # Verifica si el equipo de esqui esta permitido
        if compra.equipo not in nombres_permitidos:
            print(f"El equipo {compra.equipo} no está permitido. No se ha realizado ninguna acción.")
            return

        # Verifica si el equipo de buceo ya existe
        self.Centro_Buceo_cursor.execute('''
            SELECT * FROM Centro_Buceo
            WHERE Equipo_de_Buceo = ? AND Pais = ?
        ''', (compra.equipo, compra.pais))
        existente = self.Centro_Buceo_cursor.fetchone()

        if existente:
            print(f"El equipo {compra.equipo} ya existe para {compra.pais} y talla {compra.talla}. Actualizando...")
            # si el equipo ya existe, actualizamos la cantidad y el precio
            sql_update = f'''
                UPDATE Centro_Buceo
                SET {compra.talla} = {compra.talla} + ?,
                Precio_Compra = Precio_Compra + ? * {compra.cantidad}
                WHERE Equipo_de_Buceo = ? AND Pais = ?
            '''
            self.Centro_Buceo_cursor.execute(sql_update, (compra.cantidad, compra.precio_compra, compra.equipo, compra.pais))
        else:
            print(f"El equipo {compra.equipo} no existe para {compra.pais} y talla {compra.talla}. Insertando nueva fila...")
            # si el equipo no existe, insertamos una nueva fila
            sql_insert = f'''
                INSERT INTO Centro_Buceo (
                    Equipo_de_Buceo, Pais, {compra.talla}, Precio_Compra
                ) VALUES (?, ?, ?, ? * {compra.cantidad})
            '''
            self.Centro_Buceo_cursor.execute(sql_insert, (compra.equipo, compra.pais, compra.cantidad, compra.precio_compra))

        # Commit es para aplicar los cambios
        self.Centro_Buceo_conn.commit()


    def obtener_indice_talla(self, talla):
        tallas_disponibles = ['XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL']
        return tallas_disponibles.index(talla)+3

    def obtener_paises_Buceo(self):
            self.Centro_Buceo_cursor.execute("SELECT DISTINCT Pais FROM Centro_Buceo")
            paises = [pais[0] for pais in self.Centro_Buceo_cursor.fetchall()]
            return paises
#-------------------------------------------------------------------------------------
#Alquiler y gestion de Centros
    def restar_alquiler(self, Alquiler):
        # Lista de nombres permitidos según la actividad
        actividades_permitidas = ["ESQUIAR", "BUCEO"]
        equipos_permitidos_buceo = [
            "Traje (Neopreno)",
            "Chaleco (BCD)",
            "Regulador",
            "Tanque",
            "Máscara",
            "Aletas",
            "Cinturón",
            "Ordenador",
            "Manómetro",
            "Cuchillo",
            "Silbato"
        ]

        equipos_permitidos_esqui = [
            "Bastones", 
            "Botas de esqui",
            "Tablas de snowboard",
            "Botas de snowboard",
            "Cascos",
            "Chaquetas",
            "Pantalones"
        ]

        # Convierte el país a mayúsculas
        Alquiler.pais = Alquiler.pais.upper()

        # Verifica si la actividad está permitida
        if Alquiler.actividad.upper() not in actividades_permitidas:
            print(f"La actividad {Alquiler.actividad} no está permitida para alquiler. No se ha realizado ninguna acción.")
            return

        if Alquiler.actividad.upper() == "BUCEO":
            # Iterar sobre los equipos permitidos y restar la cantidad alquilada para cada uno
            for equipo in equipos_permitidos_buceo:
                # Verifica si el equipo de buceo existe en la base de datos para ese país y talla
                self.Centro_Buceo_cursor.execute('''
                    SELECT * FROM Centro_Buceo
                    WHERE Equipo_de_Buceo = ? AND Pais = ?
                ''', (equipo, Alquiler.pais))
                existente = self.Centro_Buceo_cursor.fetchone()

                if existente:
                    # El equipo existe, verificamos si hay suficientes unidades para alquiler
                    talla_index = self.obtener_indice_talla(Alquiler.talla)
                    cantidad_disponible = existente[talla_index]

                    if cantidad_disponible > 0 and cantidad_disponible >= Alquiler.cantidad:
                        # Suficientes unidades disponibles, restamos la cantidad alquilada
                        sql_update = f'''
                            UPDATE Centro_Buceo
                            SET {Alquiler.talla} = {Alquiler.talla} - ?
                            WHERE Equipo_de_Buceo = ? AND Pais = ?
                        '''
                        self.Centro_Buceo_cursor.execute(sql_update, (Alquiler.cantidad, equipo, Alquiler.pais))
                        print(f"Alquiler de {Alquiler.cantidad} unidades de {equipo} realizado correctamente.")
                    else:
                        print(f"No hay suficientes unidades disponibles para alquiler de {Alquiler.cantidad} unidades de {equipo}.")
                else:
                    print(f"El equipo {equipo} no existe para {Alquiler.pais} y talla {Alquiler.talla}. No se ha realizado ninguna acción.")

            # Commit es para aplicar los cambios
            self.Centro_Buceo_conn.commit()
        else:
    
            # Iterar sobre los equipos permitidos y restar la cantidad alquilada para cada uno
            for equipo in equipos_permitidos_esqui:
                # Verifica si el equipo de buceo existe en la base de datos para ese país y talla
                self.Centro_Esqui_cursor.execute('''
                    SELECT * FROM Centro_Esqui
                    WHERE Equipo_de_Esqui = ? AND Pais = ?
                ''', (equipo, Alquiler.pais))
                existente = self.Centro_Esqui_cursor.fetchone()

                if existente:
                    # El equipo existe, verificamos si hay suficientes unidades para alquiler
                    talla_index = self.obtener_indice_talla(Alquiler.talla)
                    cantidad_disponible = existente[talla_index]

                    if cantidad_disponible > 0 and cantidad_disponible >= Alquiler.cantidad:
                        # Suficientes unidades disponibles, restamos la cantidad alquilada
                        sql_update = f'''
                            UPDATE Centro_Esqui
                            SET {Alquiler.talla} = {Alquiler.talla} - ?
                            WHERE Equipo_de_Esqui = ? AND Pais = ?
                        '''
                        self.Centro_Esqui_cursor.execute(sql_update, (Alquiler.cantidad, equipo, Alquiler.pais))
                        print(f"Alquiler de {Alquiler.cantidad} unidades de {equipo} realizado correctamente.")
                    else:
                        print(f"No hay suficientes unidades disponibles para alquiler de {Alquiler.cantidad} unidades de {equipo}.")
                else:
                    print(f"El equipo {equipo} no existe para {Alquiler.pais} y talla {Alquiler.talla}. No se ha realizado ninguna acción.")

            # Commit es para aplicar los cambios
            self.Centro_Esqui_conn.commit()

    def obtener_pais_por_dni(self, dni): # en la tabla de ventas por clientes
        # Lógica para obtener el país a partir del DNI en la tabla Ventas_por_cliente
        self.Ventas_por_cliente_cursor.execute('SELECT Pais FROM Ventas_por_cliente WHERE DNI = ?', (dni,))
        resultado = self.Ventas_por_cliente_cursor.fetchone()
        if resultado:
            return resultado[0].upper()  # Convertir a mayúsculas
        else:
            return None

    def procesar_devolucion(self, dni):
            # busca la última transacción para el DNI dado
            self.Ventas_por_cliente_cursor.execute('''
                SELECT Actividad, Talla, Pais, Cantidad
                FROM Ventas_por_cliente
                WHERE DNI = ?
                ORDER BY FechaVenta DESC
                LIMIT 1
            ''', (dni,))

            ultima_transaccion = self.Ventas_por_cliente_cursor.fetchone()

            if not ultima_transaccion:
                print("No se encontraron transacciones para el DNI proporcionado.")
                return

            actividad, talla, pais, cantidad_devuelta = ultima_transaccion

            # Convierte el país a mayúsculas
            pais_mayusculas = pais.upper()

            # Verifica si la actividad está permitida
            actividades_permitidas = ["ESQUIAR", "BUCEO"] 
            equipos_permitidos_buceo = [
                "Traje (Neopreno)",
                "Chaleco (BCD)",
                "Regulador",
                "Tanque",
                "Máscara",
                "Aletas",
                "Cinturón",
                "Ordenador",
                "Manómetro",
                "Cuchillo",
                "Silbato"
            ]
            
            equipos_permitidos_esqui= [
                "Bastones", 
                "Botas de esqui",
                "Tablas de snowboard",
                "Botas de snowboard",
                "Cascos",
                "Chaquetas",
                "Pantalones"
            ]

            if actividad.upper()=="BUCEO":  #
                # Iterar sobre los equipos permitidos y sumar la cantidad devuelta para cada uno
                for equipo in equipos_permitidos_buceo:
                    # Verificar si el equipo de buceo existe en la base de datos para ese país y talla
                    self.Centro_Buceo_cursor.execute('''
                        SELECT *
                        FROM Centro_Buceo
                        WHERE Equipo_de_Buceo = ? AND Pais = ?
                    ''', (equipo, pais_mayusculas))
                    existente = self.Centro_Buceo_cursor.fetchone()

                    if existente:
                        # El equipo existe, sumamos la cantidad devuelta
                        talla_columna = talla.upper()  # Convertir la talla a mayúsculas
                        sql_update = f'''
                            UPDATE Centro_Buceo
                            SET {talla_columna} = {talla_columna} + ?
                            WHERE Equipo_de_Buceo = ? AND Pais = ?
                        '''
                        self.Centro_Buceo_cursor.execute(sql_update, (cantidad_devuelta, equipo, pais_mayusculas))
                        print(f"Devolución de {cantidad_devuelta} unidades de {equipo} para buceo realizada correctamente.")
                    else:
                        print(f"El equipo {equipo} no existe para {pais_mayusculas} y talla {talla}. No se ha realizado ninguna acción.")

                # Commit es para aplicar los cambios
                self.Centro_Buceo_conn.commit()

            else:
                # Iterar sobre los equipos permitidos y sumar la cantidad devuelta para cada uno
                for equipo in equipos_permitidos_esqui:
                    # Verificar si el equipo de buceo existe en la base de datos para ese país y talla
                    self.Centro_Esqui_cursor.execute('''
                        SELECT *
                        FROM Centro_Esqui
                        WHERE Equipo_de_Esqui = ? AND Pais = ?
                    ''', (equipo, pais_mayusculas))
                    existente = self.Centro_Esqui_cursor.fetchone()

                    if existente:
                        # El equipo existe, sumamos la cantidad devuelta
                        talla_columna = talla.upper()  # Convertir la talla a mayúsculas
                        sql_update = f'''
                            UPDATE Centro_Esqui
                            SET {talla_columna} = {talla_columna} + ?
                            WHERE Equipo_de_Esqui = ? AND Pais = ?
                        '''
                        self.Centro_Esqui_cursor.execute(sql_update, (cantidad_devuelta, equipo, pais_mayusculas))
                        print(f"Devolución de {cantidad_devuelta} unidades de {equipo} para esqui realizada correctamente.")
                    else:
                        print(f"El equipo {equipo} no existe para {pais_mayusculas} y talla {talla}. No se ha realizado ninguna acción.")

                # Commit es para aplicar los cambios
                self.Centro_Esqui_conn.commit()
    def consultar_cantidad_disponible(self, pais, talla, actividad):
        pais = pais.upper()

        # Verifica si la actividad es buceo o esquí
        tabla_equipo = "Centro_Buceo" if actividad.upper() == 'BUCEO' else "Centro_Esqui"
        columna_equipo = "Equipo_de_Buceo" if actividad.upper() == 'BUCEO' else "Equipo_de_Esqui"

        # Verifica si la talla es válida
        if talla not in ['XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL']:
            print(f"La talla {talla} no es válida.")
            return {}

        # Realiza la consulta para obtener la cantidad disponible
        columna_talla = f'"{talla}"'

        # Selecciona la base de datos correspondiente
        cursor = self.Centro_Buceo_cursor if tabla_equipo == "Centro_Buceo" else self.Centro_Esqui_cursor
        consulta_sql = f'''
            SELECT {columna_equipo}, {columna_talla} FROM {tabla_equipo}
            WHERE Pais = ?
        '''

        # Ejecuta la consulta
        cursor.execute(consulta_sql, (pais,))

        resultados = {}
        for fila in cursor.fetchall():
            equipo, cantidad_disponible = fila
            resultados[equipo] = cantidad_disponible

        if resultados:
            return resultados
        else:
            print(f"No se encontró información para {pais} y talla {talla} en la base de datos de {actividad}.")
            return {}
#--------------------------------------------------------------------------------
#Centro de Esqui
    def _crear_tabla_Centro_Esqui(self):
        self.Centro_Esqui_cursor.execute('''
            CREATE TABLE IF NOT EXISTS Centro_Esqui (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Equipo_de_Esqui TEXT,
                Pais TEXT,
                XXS INTEGER,
                XS INTEGER,
                S INTEGER,
                M INTEGER,
                L INTEGER,
                XL INTEGER,
                XXL INTEGER,
                Precio_Compra REAL
            )
        ''')
        self.Centro_Esqui_conn.commit()

    def agregar_compra_Esqui(self, compra):
        # Lista de nombres permitidos
        nombres_permitidos = [
            "Bastones", 
            "Botas de esqui",
            "Tablas de snowboard",
            "Botas de snowboard",
            "Cascos",
            "Chaquetas",
            "Pantalones"
        ]

        # Convvertimos el país a mayúsculas
        compra.pais = compra.pais.upper()

        # Verificamos si el equipo de Esqui está permitido
        if compra.equipo not in nombres_permitidos:
            print(f"El equipo {compra.equipo} no está permitido. No se ha realizado ninguna acción.")
            return

        # Verificamos si el equipo de buceo ya existe en la base de datos para ese país y talla
        self.Centro_Esqui_cursor.execute('''
            SELECT * FROM Centro_Esqui
            WHERE Equipo_de_Esqui = ? AND Pais = ?
        ''', (compra.equipo, compra.pais.upper()))
        existente = self.Centro_Esqui_cursor.fetchone()

        if existente:
            print(f"El equipo {compra.equipo} ya existe para {compra.pais} y talla {compra.talla}. Actualizando...")
            # El equipo ya existe, actualizamos la cantidad y el precio
            sql_update = f'''
                UPDATE Centro_Esqui
                SET {compra.talla} = {compra.talla} + ?,
                Precio_Compra = Precio_Compra + ? * {compra.cantidad}
                WHERE Equipo_de_Esqui = ? AND Pais = ?
            '''
            self.Centro_Esqui_cursor.execute(sql_update, (compra.cantidad, compra.precio_compra, compra.equipo, compra.pais))
        else:
            print(f"El equipo {compra.equipo} no existe para {compra.pais} y talla {compra.talla}. Insertando nueva fila...")
            # El equipo no existe, insertamos una nueva fila
            sql_insert = f'''
                INSERT INTO Centro_Esqui (
                    Equipo_de_Esqui, Pais, {compra.talla}, Precio_Compra
                ) VALUES (?, ?, ?, ?)
            '''
            self.Centro_Esqui_cursor.execute(sql_insert, (compra.equipo, compra.pais, compra.cantidad, compra.precio_compra))

        # Commit es para aplicar los cambios
        self.Centro_Esqui_conn.commit()

    def obtener_paises_Esqui(self):
        self.Centro_Esqui_cursor.execute("SELECT DISTINCT Pais FROM Centro_Esqui")
        paises = [pais[0] for pais in self.Centro_Esqui_cursor.fetchall()]
        return paises
#----------------------------------------------------------------------------------
#Venta por cliente

    def _crear_tabla_Ventas_por_cliente(self):
        # Crear la tabla en la nueva base de datos
        self.Ventas_por_cliente_cursor.execute('''
            CREATE TABLE IF NOT EXISTS Ventas_por_cliente (
                DNI TEXT,
                Nombre TEXT,
                Email TEXT,
                Actividad TEXT,
                Talla TEXT,
                Pais TEXT,
                Cantidad INTEGER,
                FechaActividad TEXT,
                FechaVenta TEXT,
                PrecioTotal NUMERIC
            )
        ''')
        self.Ventas_por_cliente_conn.commit()    

    def buscar_buzo_por_dni(self, dni):
        self.buzos_cursor.execute('SELECT DNI, Nombre, Email FROM buzos WHERE dni = ?', (dni,))
        resultado = self.buzos_cursor.fetchone()

        if resultado:
            # Devuelve los valores necesarios para insertar la venta
            return resultado[0], resultado[1], resultado[2]
        else:
            return None  
    def buscar_esquiador_por_dni(self, dni):
        self.esquiadores_cursor.execute('SELECT DNI, Nombre, Email FROM esquiadores WHERE dni = ?', (dni,))
        resultado = self.esquiadores_cursor.fetchone()

        if resultado:
            # Devuelve los valores necesarios para insertar la venta
            return resultado[0], resultado[1], resultado[2]
        else:
            return None  


    def insertar_venta_cliente(self, dni, nombre, email, actividad, talla, pais, cantidad, fecha_actividad, precio_total):
        
        if actividad.upper()=="BUCEO":

                fecha_venta = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Obtiene la fecha y hora actual
                self.Ventas_por_cliente_cursor.execute('''
                    INSERT INTO Ventas_por_cliente (DNI, Nombre, Email, Actividad, Talla, Pais, Cantidad, FechaActividad, FechaVenta, PrecioTotal)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?,?)
                ''', (dni, nombre, email, actividad, talla, pais, cantidad,fecha_actividad, fecha_venta, precio_total))
                self.Ventas_por_cliente_conn.commit()

        else:
                fecha_venta = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Obtiene la fecha y hora actual
                self.Ventas_por_cliente_cursor.execute('''
                    INSERT INTO Ventas_por_cliente (DNI, Nombre, Email, Actividad, Talla, Pais, Cantidad, FechaActividad, FechaVenta, PrecioTotal)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?,?)
                ''', (dni, nombre, email, actividad, talla, pais, cantidad,fecha_actividad, fecha_venta, precio_total))
                self.Ventas_por_cliente_conn.commit()


    def consultar_ventas_por_dni(self, dni):
        # Consultar datos de la tabla Ventas_por_cliente por DNI
        query = 'SELECT * FROM Ventas_por_cliente WHERE DNI = ?'
        self.Ventas_por_cliente_cursor.execute(query, (dni,))
        resultados = self.Ventas_por_cliente_cursor.fetchall()

        if resultados:
            return resultados
        else:
            return None
#----------------------------------------------------------
#fauna y flora

    def _crear_tabla_fauna_y_flora(self):
        self.fauna_y_flora_cursor.execute('''
            CREATE TABLE IF NOT EXISTS fauna_y_flora (
                nombre TEXT PRIMARY KEY,
                tipo TEXT,
                atlantico TEXT,
                pacifico TEXT,
                indico TEXT,
                mediterraneo TEXT,
                caribe TEXT,
                mar_rojo TEXT,
                indo_pacifico TEXT,
                foto BLOB
            )
        ''')
        self.fauna_y_flora_conn.commit()

    def agregar_fauna_y_flora(self, fauna_y_flora):
        # Verifica si el punto ya existe en la base de datos (usando el nombre como clave primaria)
        self.fauna_y_flora_cursor.execute('SELECT nombre FROM fauna_y_flora WHERE nombre = ?', (fauna_y_flora.nombre,))
        existente = self.fauna_y_flora_cursor.fetchone()

        if existente:
            print("La fauna o flora ya existe en la base de datos. No se puede agregar.")
        else:
            self.fauna_y_flora_cursor.execute('''
                INSERT INTO fauna_y_flora (nombre, tipo, atlantico, pacifico, indico, mediterraneo, caribe, mar_rojo, indo_pacifico, foto)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (fauna_y_flora.nombre, fauna_y_flora.tipo, fauna_y_flora.atlantico, fauna_y_flora.pacifico, fauna_y_flora.indico,
                  fauna_y_flora.mediterraneo, fauna_y_flora.caribe, fauna_y_flora.mar_rojo, fauna_y_flora.indo_pacifico, fauna_y_flora.foto))
            self.fauna_y_flora_conn.commit()
            print("Fauna y flora agregada correctamente")
    
    def buscar_fauna_y_flora_por_nombre(self, nombre):
        try:
            self.fauna_y_flora_cursor.execute(f"SELECT tipo,atlantico,pacifico,indico,mediterraneo,caribe,mar_rojo,indo_pacifico FROM fauna_y_flora WHERE nombre = ?", (nombre,))
            resultado = self.fauna_y_flora_cursor.fetchone()

            if resultado:
                tipo = resultado[0].upper()  # Convertimos el tipo a mayúsculas
                # Obtenemos los encabezados (nombres de las columnas)
                encabezados = [descripcion[0].upper() for descripcion in self.fauna_y_flora_cursor.description]  # Convertir los encabezados a mayúsculas

                # Filtramos los encabezados que tienen el valor "SI"
                encabezados_con_si = [encabezado for encabezado in encabezados[2:8] if resultado[encabezados.index(encabezado)] == "SI"]

                return tipo, encabezados_con_si

        except Exception as e:
            print(f"Error al buscar fauna y flora por nombre: {e}")
            return {"Mensaje": "Error en la búsqueda"}




    def buscar_por_nombre_y_aguas(self, nombre, encabezado):
        if encabezado not in ["atlantico".upper(), "pacifico".upper(), "indico".upper(), "mediterraneo".upper(), "caribe".upper(), "mar_rojo".upper(), "indo_pacifico".upper()]:
            raise ValueError("Encabezado no válido")

        query = f"SELECT {encabezado.upper()} FROM fauna_y_flora WHERE nombre = ?"
        self.fauna_y_flora_cursor.execute(query, (nombre.upper(),))
        resultado = self.fauna_y_flora_cursor.fetchone()

        if resultado and resultado[0] == 'NO':
            respuesta="NO"
        else:
            respuesta="SI"
        return respuesta


    def borrar_fauna_y_flora_por_nombre(self,nombre):
        self.fauna_y_flora_cursor.execute('SELECT * FROM fauna_y_flora WHERE nombre = ?', (nombre,))
        resultado = self.fauna_y_flora_cursor.fetchone()

        if resultado:
            self.fauna_y_flora_cursor.execute('DELETE FROM fauna_y_flora WHERE nombre = ?', (nombre,))
            self.fauna_y_flora_conn.commit()
            print("Fauna y flora borrada correctamente")
        else:
            print("Operación de borrado cancelada")


    def borrar_fauna_y_flora_por_nombre(self,nombre):
        self.fauna_y_flora_cursor.execute('SELECT * FROM fauna_y_flora WHERE nombre = ?', (nombre,))
        resultado = self.fauna_y_flora_cursor.fetchone()

        if resultado:
            self.fauna_y_flora_cursor.execute('DELETE FROM fauna_y_flora WHERE nombre = ?', (nombre,))
            self.fauna_y_flora_conn.commit()
            print("Fauna y flora borrada correctamente")
        else:
            print("Operación de borrado cancelada")

    def buscar_fauna_flora_por_H20(self, tipo_aguas):
    # Consulta SELECT para obtener nombres de fauna y flora con el tipo de aguas especificado
        consulta = f'''
            SELECT nombre
            FROM fauna_y_flora
            WHERE {tipo_aguas} = 'SI'
        '''

        try:
            # Ejecutamos la consulta
            self.fauna_y_flora_cursor.execute(consulta)

            # Obtenemos los resultados
            resultados = self.fauna_y_flora_cursor.fetchall()

            # Devuelve los nombres de fauna y flora
            return resultados
        except Exception as e:
            # Manejar excepciones (puedes querer registrar o imprimir el error)
            print(f"Error durante la búsqueda: {e}")
            return None
#----------------------------------------------------------
#EXTRACCIÓN DE LOS DATOS PARA LA ESTADISTICA 
#----------------------------------------------------------
    def ExtraccionBuzos(self):
       
        resultadoBuzos = self.buzos_cursor.execute("SELECT nombre, apellidos, nacionalidad, altura, fecha_nacimiento, peso, tipo_buzo, enfermedad FROM buzos")
        resultadosBuzos = resultadoBuzos.fetchall()

        DATOSbuzos = []
        for resultadoBuzos in resultadosBuzos:
            nombre, apellidos, nacionalidad, altura, fecha_nacimiento, peso, tipo_buzo, enfermedad = resultadoBuzos
            buzo = {
                'Nombre': nombre,
                'Apellidos': apellidos,
                'Pais': nacionalidad,
                'Altura': altura,
                'fecha_nacimiento': fecha_nacimiento,
                'Peso': peso,
                'tipo_buzo': tipo_buzo,
                'enfermedad': enfermedad
            }
            DATOSbuzos.append(buzo)
        return DATOSbuzos


    def ExtraccionEsquiadores(self):

        resultadoEsquiadores = self.esquiadores_cursor.execute("SELECT nombre, apellidos, nacionalidad, altura, fecha_nacimiento, peso, tipo_esquiador, enfermedad FROM esquiadores")
        resultadosEsquiadores = resultadoEsquiadores.fetchall()

        DATOSEsquiadores = []
        for resultadoEsquiadores in resultadosEsquiadores:
            nombre, apellidos, nacionalidad, altura, fecha_nacimiento, peso, tipo_esquiador, enfermedad = resultadoEsquiadores
            Esquiador= {
                'Nombre': nombre,
                'Apellidos': apellidos,
                'Pais': nacionalidad,
                'Altura': altura,
                'fecha_nacimiento': fecha_nacimiento,
                'Peso': peso,
                'tipo_esquiador': tipo_esquiador,
                'enfermedad': enfermedad
            }
            DATOSEsquiadores.append(Esquiador)
        return DATOSEsquiadores

    def ExtraccionVentas(self):


        resultadoVentas=self.Ventas_por_cliente_cursor.execute("SELECT nombre, actividad, talla, pais, cantidad, precioTotal FROM Ventas_por_cliente")
        resultadosVentas = resultadoVentas.fetchall()


        DatosVentas = []


        for resultadoVentas in resultadosVentas:
            nombre, actividad, talla, pais, cantidad, precio_total = resultadoVentas
            venta = {
                'Nombre': nombre,
                'Actividad': actividad,
                'Talla': talla,
                'Pais': pais,
                'Cantidad': cantidad,
                'Precio': precio_total
            }
            DatosVentas.append(venta)

        return DatosVentas

    def PaisesVenta(self):

        lista_paises_venta = self.Ventas_por_cliente_cursor.execute("SELECT DISTINCT Pais FROM Ventas_por_cliente")
        resultados_pais_ventas = lista_paises_venta.fetchall()

        # Paises unicos en la lista de ventas
        paises_unicos = [pais[0] for pais in resultados_pais_ventas]
        return paises_unicos


    def convertir_si_no(self,valor):
        return True if valor == 'SI' else False


    def Extracion_datos_fauna_flora(self):
        resultadoFF = self.fauna_y_flora_cursor.execute("SELECT nombre, tipo, atlantico, pacifico, indico, mediterraneo, caribe, mar_rojo, indo_pacifico FROM fauna_y_flora")
        resultadosFF = resultadoFF.fetchall()

        Datosfauna_flora = []
        for resultadoFF in resultadosFF:  # Corregí el nombre de la variable
            Datosfauna_flora.append({
                'Nombre': resultadoFF[0],
                'Tipo': resultadoFF[1],
                'ATLANTICO': self.convertir_si_no(resultadoFF[2]),
                'PACIFICO': self.convertir_si_no(resultadoFF[3]),
                'INDICO': self.convertir_si_no(resultadoFF[4]),
                'MEDITERRANEO': self.convertir_si_no(resultadoFF[5]),
                'CARIBE': self.convertir_si_no(resultadoFF[6]),
                'MAR ROJO': self.convertir_si_no(resultadoFF[7]),
                'INDO-PACIFICO': self.convertir_si_no(resultadoFF[8]),
            })

        return Datosfauna_flora



    def Extracion_datos_fauna_flor_sin(self):
        resultadoFF_sin = self.fauna_y_flora_cursor.execute("SELECT nombre, tipo, atlantico, pacifico, indico, mediterraneo, caribe, mar_rojo, indo_pacifico FROM fauna_y_flora")
        resultadosFF_sin = resultadoFF_sin.fetchall()

        Datosfauna_flora_sin = []
        for resultadoFF_sin in resultadosFF_sin:
            Datosfauna_flora_sin.append({
                'Fauna': resultadoFF_sin[0],
                'ATLANTICO': self.convertir_si_no(resultadoFF_sin[2]),
                'PACIFICO': self.convertir_si_no(resultadoFF_sin[3]),
                'INDICO': self.convertir_si_no(resultadoFF_sin[4]),
                'MEDITERRANEO': self.convertir_si_no(resultadoFF_sin[5]),
                'CARIBE': self.convertir_si_no(resultadoFF_sin[6]),
                'MAR ROJO': self.convertir_si_no(resultadoFF_sin[7]),
                'INDO-PACIFICO': self.convertir_si_no(resultadoFF_sin[8]),
            })

        return Datosfauna_flora_sin

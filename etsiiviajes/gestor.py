"""Acceso a la base de datos SQLite de la aplicación.

Todas las tablas están en un único archivo (``datos/etsiiviajes.db``), así que
una reserva puede restar el inventario y guardar la venta en la misma
transacción. Los valores siempre van como parámetros ``?``; los pocos nombres
de tabla o columna que se componen en el SQL salen de listas cerradas
(``config.TALLAS``, ``config.AGUAS``, ``_TABLA_USUARIOS``).
"""

import sqlite3
from datetime import datetime
from pathlib import Path

from .config import ACTIVIDADES, AGUAS, BASE_DATOS, BUCEO, EQUIPOS, ESQUI, TALLAS
from .modelos import (Alquiler, Buzo, Compra, Especie, Esquiador, PuntoEsqui,
                      PuntoInmersion, Usuario, Venta)

_TABLA_USUARIOS = {BUCEO: "buzos", ESQUI: "esquiadores"}
_CLASE_USUARIO = {BUCEO: Buzo, ESQUI: Esquiador}

ESQUEMA = f"""
CREATE TABLE IF NOT EXISTS buzos (
    dni TEXT PRIMARY KEY, nombre TEXT NOT NULL, apellidos TEXT,
    fecha_nacimiento TEXT, nacionalidad TEXT, peso INTEGER, altura INTEGER,
    telefono TEXT, email TEXT, direccion TEXT, tipo_club TEXT, nivel TEXT,
    enfermedad TEXT, foto BLOB
);
CREATE TABLE IF NOT EXISTS esquiadores (
    dni TEXT PRIMARY KEY, nombre TEXT NOT NULL, apellidos TEXT,
    fecha_nacimiento TEXT, nacionalidad TEXT, peso INTEGER, altura INTEGER,
    telefono TEXT, email TEXT, direccion TEXT, tipo_club TEXT, nivel TEXT,
    enfermedad TEXT, foto BLOB
);
CREATE TABLE IF NOT EXISTS inventario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    actividad TEXT NOT NULL, equipo TEXT NOT NULL, pais TEXT NOT NULL,
    {", ".join(f"{t} INTEGER NOT NULL DEFAULT 0 CHECK ({t} >= 0)" for t in TALLAS)},
    precio_compra REAL NOT NULL DEFAULT 0,
    UNIQUE (actividad, equipo, pais)
);
CREATE TABLE IF NOT EXISTS ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dni TEXT NOT NULL, nombre TEXT, email TEXT, actividad TEXT NOT NULL,
    talla TEXT NOT NULL, pais TEXT NOT NULL, cantidad INTEGER NOT NULL,
    fecha_actividad TEXT NOT NULL, fecha_venta TEXT NOT NULL,
    precio_unitario REAL NOT NULL, precio_total REAL NOT NULL,
    devuelto INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS puntos_inmersion (
    nombre TEXT PRIMARY KEY, pais TEXT, latitud REAL, longitud REAL,
    aguas TEXT, profundidad REAL, foto BLOB
);
CREATE TABLE IF NOT EXISTS puntos_esqui (
    nombre TEXT PRIMARY KEY, pais TEXT, latitud REAL, longitud REAL,
    km_pistas REAL, mapa_pistas BLOB
);
CREATE TABLE IF NOT EXISTS fauna_y_flora (
    nombre TEXT PRIMARY KEY, tipo TEXT,
    {", ".join(f"{a} TEXT NOT NULL DEFAULT 'NO'" for a in AGUAS)},
    foto BLOB
);
CREATE TABLE IF NOT EXISTS eventos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT NOT NULL, hora TEXT NOT NULL, nombre TEXT NOT NULL
);
"""

_COLUMNAS_USUARIO = ("dni", "nombre", "apellidos", "fecha_nacimiento", "nacionalidad",
                     "peso", "altura", "telefono", "email", "direccion", "tipo_club",
                     "nivel", "enfermedad", "foto")


class StockInsuficiente(Exception):
    """No hay unidades suficientes de algún equipo para una reserva."""

    def __init__(self, faltan: dict[str, int]):
        self.faltan = faltan
        detalle = ", ".join(f"{equipo} (quedan {n})" for equipo, n in faltan.items())
        super().__init__(f"No hay stock suficiente de: {detalle}")


def _comprobar_actividad(actividad: str) -> str:
    actividad = actividad.upper()
    if actividad not in ACTIVIDADES:
        raise ValueError(f"Actividad desconocida: {actividad}")
    return actividad


def _comprobar_talla(talla: str) -> str:
    talla = talla.upper()
    if talla not in TALLAS:
        raise ValueError(f"Talla no válida: {talla}")
    return talla


class GestorBasesDatos:
    """Punto único de acceso a los datos. Úsalo como ``with GestorBasesDatos() as g:``."""

    def __init__(self, ruta: Path | str = BASE_DATOS):
        Path(ruta).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(ruta)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.conn.executescript(ESQUEMA)

    def cerrar(self) -> None:
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.cerrar()

    # ------------------------------------------------------------------ usuarios

    def guardar_usuario(self, usuario: Usuario) -> bool:
        """Inserta un buzo o esquiador. Devuelve False si el DNI ya existe."""
        tabla = _TABLA_USUARIOS[_comprobar_actividad(usuario.actividad)]
        valores = [getattr(usuario, c) for c in _COLUMNAS_USUARIO]
        valores[0] = usuario.dni.strip().upper()
        try:
            with self.conn:
                self.conn.execute(
                    f"INSERT INTO {tabla} ({', '.join(_COLUMNAS_USUARIO)}) "
                    f"VALUES ({', '.join('?' * len(_COLUMNAS_USUARIO))})", valores)
        except sqlite3.IntegrityError:
            return False
        return True

    def obtener_usuario(self, actividad: str, dni: str) -> Usuario | None:
        actividad = _comprobar_actividad(actividad)
        fila = self.conn.execute(
            f"SELECT * FROM {_TABLA_USUARIOS[actividad]} WHERE dni = ?",
            (dni.strip().upper(),)).fetchone()
        return _CLASE_USUARIO[actividad](**dict(fila)) if fila else None

    def borrar_usuario(self, actividad: str, dni: str) -> bool:
        tabla = _TABLA_USUARIOS[_comprobar_actividad(actividad)]
        with self.conn:
            cur = self.conn.execute(f"DELETE FROM {tabla} WHERE dni = ?", (dni.strip().upper(),))
        return cur.rowcount > 0

    def listar_usuarios(self, actividad: str) -> list[Usuario]:
        actividad = _comprobar_actividad(actividad)
        filas = self.conn.execute(f"SELECT * FROM {_TABLA_USUARIOS[actividad]}").fetchall()
        return [_CLASE_USUARIO[actividad](**dict(f)) for f in filas]

    # ---------------------------------------------------------------- inventario

    def paises(self, actividad: str | None = None) -> list[str]:
        if actividad:
            filas = self.conn.execute(
                "SELECT DISTINCT pais FROM inventario WHERE actividad = ? ORDER BY pais",
                (_comprobar_actividad(actividad),))
        else:
            filas = self.conn.execute("SELECT DISTINCT pais FROM inventario ORDER BY pais")
        return [f[0] for f in filas]

    def stock(self, actividad: str, pais: str, talla: str) -> dict[str, int]:
        """Unidades disponibles de cada equipo en un país y una talla."""
        actividad, talla = _comprobar_actividad(actividad), _comprobar_talla(talla)
        filas = self.conn.execute(
            f"SELECT equipo, {talla} FROM inventario WHERE actividad = ? AND pais = ?",
            (actividad, pais.upper())).fetchall()
        orden = {e: i for i, e in enumerate(EQUIPOS[actividad])}
        return dict(sorted(((f[0], f[1]) for f in filas), key=lambda x: orden.get(x[0], 99)))

    def registrar_compra(self, compra: Compra) -> None:
        """Suma (compra) o resta (baja) unidades de un equipo.

        Lanza ``ValueError`` si el equipo no es válido o si la baja dejaría el
        stock en negativo.
        """
        actividad = _comprobar_actividad(compra.actividad)
        talla = _comprobar_talla(compra.talla)
        if compra.equipo not in EQUIPOS[actividad]:
            raise ValueError(f"Equipo no válido para {actividad}: {compra.equipo}")
        cantidad = int(compra.cantidad)
        if cantidad == 0:
            raise ValueError("La cantidad no puede ser 0")
        pais = compra.pais.strip().upper()
        coste = max(cantidad, 0) * float(compra.precio_unitario)
        with self.conn:
            fila = self.conn.execute(
                f"SELECT id, {talla} FROM inventario WHERE actividad = ? AND equipo = ? AND pais = ?",
                (actividad, compra.equipo, pais)).fetchone()
            if fila is None:
                if cantidad < 0:
                    raise ValueError(f"No hay {compra.equipo} en {pais}")
                self.conn.execute(
                    f"INSERT INTO inventario (actividad, equipo, pais, {talla}, precio_compra) "
                    "VALUES (?, ?, ?, ?, ?)", (actividad, compra.equipo, pais, cantidad, coste))
            else:
                if fila[1] + cantidad < 0:
                    raise ValueError(f"Solo quedan {fila[1]} unidades de {compra.equipo} "
                                     f"talla {talla} en {pais}")
                self.conn.execute(
                    f"UPDATE inventario SET {talla} = {talla} + ?, "
                    "precio_compra = precio_compra + ? WHERE id = ?",
                    (cantidad, coste, fila[0]))

    # ------------------------------------------------------------------ reservas

    def registrar_reserva(self, alquiler: Alquiler) -> Venta:
        """Resta un equipo completo por persona y guarda la venta, todo o nada."""
        actividad = _comprobar_actividad(alquiler.actividad)
        talla = _comprobar_talla(alquiler.talla)
        cantidad = int(alquiler.cantidad)
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que 0")
        pais = alquiler.pais.upper()
        with self.conn:
            disponible = self.stock(actividad, pais, talla)
            faltan = {e: disponible.get(e, 0) for e in EQUIPOS[actividad]
                      if disponible.get(e, 0) < cantidad}
            if faltan:
                raise StockInsuficiente(faltan)
            self.conn.execute(
                f"UPDATE inventario SET {talla} = {talla} - ? WHERE actividad = ? AND pais = ?",
                (cantidad, actividad, pais))
            fecha_venta = datetime.now().isoformat(sep=" ", timespec="seconds")
            cur = self.conn.execute(
                "INSERT INTO ventas (dni, nombre, email, actividad, talla, pais, cantidad, "
                "fecha_actividad, fecha_venta, precio_unitario, precio_total) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (alquiler.dni.upper(), alquiler.nombre, alquiler.email, actividad, talla, pais,
                 cantidad, alquiler.fecha_actividad, fecha_venta,
                 round(alquiler.precio_unitario, 2), alquiler.precio_total))
        return self.obtener_venta(cur.lastrowid)

    def obtener_venta(self, id_venta: int) -> Venta | None:
        fila = self.conn.execute("SELECT * FROM ventas WHERE id = ?", (id_venta,)).fetchone()
        return _venta(fila) if fila else None

    def ventas_por_dni(self, dni: str) -> list[Venta]:
        filas = self.conn.execute(
            "SELECT * FROM ventas WHERE dni = ? ORDER BY fecha_venta DESC, id DESC",
            (dni.strip().upper(),)).fetchall()
        return [_venta(f) for f in filas]

    def listar_ventas(self) -> list[Venta]:
        return [_venta(f) for f in self.conn.execute("SELECT * FROM ventas ORDER BY id")]

    def ultima_reserva_pendiente(self, dni: str) -> Venta | None:
        fila = self.conn.execute(
            "SELECT * FROM ventas WHERE dni = ? AND devuelto = 0 "
            "ORDER BY fecha_venta DESC, id DESC LIMIT 1", (dni.strip().upper(),)).fetchone()
        return _venta(fila) if fila else None

    def procesar_devolucion(self, dni: str) -> Venta | None:
        """Devuelve al inventario la última reserva no devuelta del cliente."""
        venta = self.ultima_reserva_pendiente(dni)
        if venta is None:
            return None
        talla = _comprobar_talla(venta.talla)
        with self.conn:
            self.conn.execute(
                f"UPDATE inventario SET {talla} = {talla} + ? WHERE actividad = ? AND pais = ?",
                (venta.cantidad, venta.actividad, venta.pais))
            self.conn.execute("UPDATE ventas SET devuelto = 1 WHERE id = ?", (venta.id,))
        venta.devuelto = True
        return venta

    # -------------------------------------------------------- puntos de interés

    def agregar_punto_inmersion(self, p: PuntoInmersion) -> bool:
        return self._insertar(
            "INSERT INTO puntos_inmersion VALUES (?, ?, ?, ?, ?, ?, ?)",
            (p.nombre.strip(), p.pais.strip().upper(), p.latitud, p.longitud,
             p.aguas, p.profundidad, p.foto))

    def obtener_punto_inmersion(self, nombre: str) -> PuntoInmersion | None:
        fila = self.conn.execute("SELECT * FROM puntos_inmersion WHERE nombre = ? COLLATE NOCASE",
                                 (nombre.strip(),)).fetchone()
        return PuntoInmersion(**dict(fila)) if fila else None

    def borrar_punto_inmersion(self, nombre: str) -> bool:
        return self._borrar("DELETE FROM puntos_inmersion WHERE nombre = ? COLLATE NOCASE", nombre)

    def puntos_inmersion(self, pais: str | None = None) -> list[PuntoInmersion]:
        if pais:
            filas = self.conn.execute("SELECT * FROM puntos_inmersion WHERE pais = ?",
                                      (pais.upper(),))
        else:
            filas = self.conn.execute("SELECT * FROM puntos_inmersion")
        return [PuntoInmersion(**dict(f)) for f in filas]

    def agregar_punto_esqui(self, p: PuntoEsqui) -> bool:
        return self._insertar(
            "INSERT INTO puntos_esqui VALUES (?, ?, ?, ?, ?, ?)",
            (p.nombre.strip(), p.pais.strip().upper(), p.latitud, p.longitud,
             p.km_pistas, p.mapa_pistas))

    def obtener_punto_esqui(self, nombre: str) -> PuntoEsqui | None:
        fila = self.conn.execute("SELECT * FROM puntos_esqui WHERE nombre = ? COLLATE NOCASE",
                                 (nombre.strip(),)).fetchone()
        return PuntoEsqui(**dict(fila)) if fila else None

    def borrar_punto_esqui(self, nombre: str) -> bool:
        return self._borrar("DELETE FROM puntos_esqui WHERE nombre = ? COLLATE NOCASE", nombre)

    def puntos_esqui(self) -> list[PuntoEsqui]:
        return [PuntoEsqui(**dict(f)) for f in self.conn.execute("SELECT * FROM puntos_esqui")]

    # ------------------------------------------------------------ fauna y flora

    def agregar_especie(self, especie: Especie) -> bool:
        columnas = ["nombre", "tipo", *AGUAS, "foto"]
        valores = [especie.nombre.strip().upper(), especie.tipo.upper(),
                   *("SI" if especie.aguas.get(a) else "NO" for a in AGUAS), especie.foto]
        return self._insertar(
            f"INSERT INTO fauna_y_flora ({', '.join(columnas)}) "
            f"VALUES ({', '.join('?' * len(columnas))})", valores)

    def obtener_especie(self, nombre: str) -> Especie | None:
        fila = self.conn.execute("SELECT * FROM fauna_y_flora WHERE nombre = ?",
                                 (nombre.strip().upper(),)).fetchone()
        return _especie(fila) if fila else None

    def borrar_especie(self, nombre: str) -> bool:
        return self._borrar("DELETE FROM fauna_y_flora WHERE nombre = ?", nombre.strip().upper())

    def listar_especies(self) -> list[Especie]:
        return [_especie(f) for f in
                self.conn.execute("SELECT * FROM fauna_y_flora ORDER BY nombre")]

    def especies_en_aguas(self, claves_aguas) -> list[Especie]:
        """Especies vistas en al menos una de las aguas indicadas."""
        claves = [c for c in claves_aguas if c in AGUAS]
        if not claves:
            return []
        condicion = " OR ".join(f"{c} = 'SI'" for c in claves)
        filas = self.conn.execute(
            f"SELECT * FROM fauna_y_flora WHERE {condicion} ORDER BY nombre")
        return [_especie(f) for f in filas]

    # ------------------------------------------------------------------- agenda

    def agregar_evento(self, fecha_iso: str, hora: str, nombre: str) -> None:
        with self.conn:
            self.conn.execute("INSERT INTO eventos (fecha, hora, nombre) VALUES (?, ?, ?)",
                              (fecha_iso, hora, nombre))

    def eventos_del_dia(self, fecha_iso: str) -> list[tuple[str, str]]:
        filas = self.conn.execute(
            "SELECT hora, nombre FROM eventos WHERE fecha = ? ORDER BY hora", (fecha_iso,))
        return [(f[0], f[1]) for f in filas]

    # ---------------------------------------------------------------- internos

    def _insertar(self, sql: str, valores) -> bool:
        try:
            with self.conn:
                self.conn.execute(sql, valores)
        except sqlite3.IntegrityError:
            return False
        return True

    def _borrar(self, sql: str, clave: str) -> bool:
        with self.conn:
            cur = self.conn.execute(sql, (clave.strip(),))
        return cur.rowcount > 0


def _venta(fila: sqlite3.Row) -> Venta:
    datos = dict(fila)
    datos.pop("precio_total")
    datos["devuelto"] = bool(datos["devuelto"])
    return Venta(**datos)


def _especie(fila: sqlite3.Row) -> Especie:
    return Especie(nombre=fila["nombre"], tipo=fila["tipo"],
                   aguas={a: fila[a] == "SI" for a in AGUAS}, foto=fila["foto"])

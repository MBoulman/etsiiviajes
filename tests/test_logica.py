"""Pruebas de la lógica de negocio (sin interfaz gráfica). Ejecutar con ``pytest``."""

import random
from datetime import date

import pytest

from etsiiviajes.config import BUCEO, EQUIPOS, ESQUI
from etsiiviajes.datos_demo import crear_base_de_trabajo
from etsiiviajes.documentos import calcular_precio, desglose_iva, generar_factura
from etsiiviajes.estadisticas import ModeloPrecio, clusters, datos_clientes, datos_ventas
from etsiiviajes.gestor import GestorBasesDatos, StockInsuficiente
from etsiiviajes.modelos import Alquiler, Buzo, Compra
from etsiiviajes.utils import validar_dni, validar_documento, validar_email


@pytest.fixture
def gestor(tmp_path):
    g = GestorBasesDatos(tmp_path / "prueba.db")
    for equipo in EQUIPOS[BUCEO]:
        g.registrar_compra(Compra(BUCEO, equipo, "España", "M", 5, 10.0))
    yield g
    g.cerrar()


def alquiler(cantidad=2, dni="DEMO00001"):
    return Alquiler(dni=dni, nombre="ANA PRUEBA", email="ana@example.com", actividad=BUCEO,
                    pais="ESPAÑA", talla="M", cantidad=cantidad,
                    fecha_actividad="2026-07-01", precio_unitario=55.5)


def test_reserva_resta_todo_el_equipo(gestor):
    venta = gestor.registrar_reserva(alquiler(cantidad=2))
    assert venta.id == 1
    assert venta.precio_total == 111.0
    assert set(gestor.stock(BUCEO, "ESPAÑA", "M").values()) == {3}


def test_sin_stock_no_se_guarda_nada(gestor):
    gestor.registrar_compra(Compra(BUCEO, "Aletas", "ESPAÑA", "M", -4))   # deja 1 aleta
    with pytest.raises(StockInsuficiente) as error:
        gestor.registrar_reserva(alquiler(cantidad=2))
    assert error.value.faltan == {"Aletas": 1}
    assert gestor.listar_ventas() == []
    assert gestor.stock(BUCEO, "ESPAÑA", "M")["Regulador"] == 5


def test_devolucion_solo_una_vez(gestor):
    gestor.registrar_reserva(alquiler(cantidad=2))
    assert gestor.procesar_devolucion("demo00001") is not None
    assert gestor.stock(BUCEO, "ESPAÑA", "M")["Tanque"] == 5
    assert gestor.procesar_devolucion("DEMO00001") is None      # ya devuelta
    assert gestor.stock(BUCEO, "ESPAÑA", "M")["Tanque"] == 5
    assert gestor.procesar_devolucion("NOEXISTE") is None


def test_baja_no_deja_stock_negativo(gestor):
    with pytest.raises(ValueError):
        gestor.registrar_compra(Compra(BUCEO, "Tanque", "ESPAÑA", "M", -6))
    assert gestor.stock(BUCEO, "ESPAÑA", "M")["Tanque"] == 5


def test_compra_suma_coste_y_valida_talla(gestor):
    gestor.registrar_compra(Compra(BUCEO, "Tanque", "ESPAÑA", "M", 3, 20.0))
    fila = gestor.conn.execute(
        "SELECT M, precio_compra FROM inventario WHERE equipo = 'Tanque'").fetchone()
    assert tuple(fila) == (8, 5 * 10.0 + 3 * 20.0)
    with pytest.raises(ValueError):
        gestor.registrar_compra(Compra(BUCEO, "Tanque", "ESPAÑA", "M; DROP TABLE ventas", 1))


def test_usuarios_alta_duplicada_y_borrado(gestor):
    buzo = Buzo("12345678Z", "ANA", "PRUEBA", "1990-05-01", "ESPAÑA", 60, 170,
                "600000000", "ana@example.com", "Calle Ficticia 1", nivel="RECREATIVO")
    assert gestor.guardar_usuario(buzo) is True
    assert gestor.guardar_usuario(buzo) is False
    assert gestor.obtener_usuario(BUCEO, "12345678z").direccion == "Calle Ficticia 1"
    assert gestor.obtener_usuario(ESQUI, "12345678Z") is None
    assert gestor.borrar_usuario(BUCEO, "12345678Z") is True
    assert gestor.borrar_usuario(BUCEO, "12345678Z") is False


def test_iva_cuadra_con_el_total():
    for total in (112.0, 99.99, 0.01, 1234.56):
        base, iva = desglose_iva(total)
        assert round(base + iva, 2) == total
    assert desglose_iva(121.0) == (100.0, 21.0)


def test_factura_usa_el_numero_de_venta(gestor, tmp_path):
    venta = gestor.registrar_reserva(alquiler())
    ruta = generar_factura(venta, tmp_path)
    assert ruta.name == f"factura_{venta.id}_{venta.fecha_venta[:4]}.pdf"
    assert ruta.stat().st_size > 0


def test_precio_entre_limites():
    rng = random.Random(0)
    for dia in range(1, 365, 7):
        precio = calcular_precio(date.fromordinal(date(2026, 1, 1).toordinal() + dia), rng)
        assert 40 <= precio <= 130


@pytest.mark.parametrize("dni,valido", [
    ("12345678Z", True), ("12345678A", False), ("X1234567L", True), ("1234", False)])
def test_validar_dni(dni, valido):
    assert validar_dni(dni) is valido


def test_validar_documento_y_email():
    assert validar_documento("DEMO00001")
    assert not validar_documento("123456789")
    assert validar_email("ana@example.com")
    assert not validar_email("ana@")


def test_base_demo_y_estadisticas(tmp_path):
    from etsiiviajes.config import CATALOGO_DB
    if not CATALOGO_DB.exists():
        pytest.skip("falta datos/catalogo.db")
    ruta = crear_base_de_trabajo(tmp_path / "demo.db", clientes=10, ventas=12)
    with GestorBasesDatos(ruta) as g:
        assert len(g.listar_usuarios(BUCEO)) == 10
        assert len(g.listar_ventas()) == 12
        assert all(u.email.endswith("@example.com") for u in g.listar_usuarios(ESQUI))
        df, figuras = clusters(datos_clientes(g, BUCEO), "Buzos")
        assert df["grupo"].nunique() == 3 and len(figuras) == 3
        modelo = ModeloPrecio(datos_ventas(g))
        assert modelo.predecir("M", "ESPAÑA", BUCEO) > 0


def test_dni_con_letra_incorrecta_no_pasa_como_pasaporte():
    assert not validar_documento("12345678A")
    assert validar_documento("12345678Z")


def test_mapa_usa_mapas_base_sin_bloqueo(tmp_path):
    from etsiiviajes.config import CATALOGO_DB
    from etsiiviajes.mapa import generar_mapa
    if not CATALOGO_DB.exists():
        pytest.skip("falta datos/catalogo.db")
    with GestorBasesDatos(CATALOGO_DB) as g:
        html = generar_mapa(g, tmp_path / "mapa.html").read_text(encoding="utf-8")
    assert "server.arcgisonline.com" in html
    assert "tile.openstreetmap.org" not in html

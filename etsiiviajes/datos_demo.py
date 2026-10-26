"""Crea la base de datos de trabajo a partir del catálogo y añade clientes ficticios.

Todos los clientes, ventas y eventos se inventan con Faker. Los documentos de
identidad tienen la forma ``DEMO00001`` y los correos usan el dominio reservado
``example.com``, para que ningún dato pueda corresponder a una persona real.
"""

import random
import sqlite3
import unicodedata
from datetime import date, timedelta
from pathlib import Path

from faker import Faker

from .config import BASE_DATOS, BUCEO, CATALOGO_DB, ESQUI, NIVELES, TALLAS, TIPOS_CLUB
from .documentos import calcular_precio
from .gestor import GestorBasesDatos, StockInsuficiente
from .modelos import Alquiler, Buzo, Esquiador

# Nacionalidad que se guarda -> configuración regional de Faker para el nombre
NACIONALIDADES = {
    "ESPAÑA": "es_ES", "FRANCIA": "fr_FR", "ITALIA": "it_IT", "ALEMANIA": "de_DE",
    "REINO UNIDO": "en_GB", "IRLANDA": "en_IE", "PORTUGAL": "pt_PT", "EEUU": "en_US",
    "MÉXICO": "es_MX", "ARGENTINA": "es_AR", "SUIZA": "de_CH", "PAÍSES BAJOS": "nl_NL",
}
PESOS_NACIONALIDAD = [10, 3, 3, 2, 2, 1, 2, 2, 2, 2, 1, 1]

EVENTOS = ["CURSO INICIAL DE ESQUI", "CURSO AVANZADO DE BUCEO", "CURSO FAUNA Y FLORA",
           "CURSO BASICO DE BUCEO", "COMPETICIÓN ESQUÍ <18"]


def _cliente(clase, numero: int, rng: random.Random, fakers: dict) -> object:
    nacionalidad = rng.choices(list(NACIONALIDADES), PESOS_NACIONALIDAD)[0]
    fake = fakers[nacionalidad]
    nombre, apellido = fake.first_name(), fake.last_name()
    altura = rng.randint(155, 195)
    nacimiento = date(1960, 1, 1) + timedelta(days=rng.randint(0, 365 * 45))
    usuario_email = unicodedata.normalize("NFKD", f"{nombre[:3]}.{apellido[:3]}{numero}")
    usuario_email = usuario_email.encode("ascii", "ignore").decode().lower().replace(" ", "")
    actividad = BUCEO if clase is Buzo else ESQUI
    return clase(
        dni=f"DEMO{numero:05d}", nombre=nombre.upper(), apellidos=apellido.upper(),
        fecha_nacimiento=nacimiento.isoformat(), nacionalidad=nacionalidad,
        peso=round(altura * rng.uniform(0.36, 0.5)), altura=altura,
        telefono=f"600 000 {numero:03d}",
        email=f"{usuario_email}@example.com",
        direccion=f"Calle Ficticia {rng.randint(1, 120)}", tipo_club=rng.choice(TIPOS_CLUB),
        nivel=rng.choice(NIVELES[actividad]), enfermedad=rng.choices(["NO", "SI"], [9, 1])[0],
    )


def crear_base_de_trabajo(destino: Path = BASE_DATOS, catalogo: Path = CATALOGO_DB,
                          clientes: int = 30, ventas: int = 45, semilla: int = 7) -> Path:
    """Copia el catálogo en ``destino`` y lo rellena con datos inventados."""
    destino.parent.mkdir(parents=True, exist_ok=True)
    if destino.exists():
        destino.unlink()
    with sqlite3.connect(catalogo) as origen, sqlite3.connect(destino) as copia:
        origen.backup(copia)

    rng = random.Random(semilla)
    Faker.seed(semilla)
    fakers = {n: Faker(loc) for n, loc in NACIONALIDADES.items()}
    with GestorBasesDatos(destino) as gestor:
        lista = []
        for i in range(1, 2 * clientes + 1):
            usuario = _cliente(Buzo if i % 2 else Esquiador, i, rng, fakers)
            gestor.guardar_usuario(usuario)
            lista.append(usuario)

        hoy = date.today()
        hechas = 0
        while hechas < ventas:
            u = rng.choice(lista)
            paises = gestor.paises(u.actividad)
            fecha = hoy + timedelta(days=rng.randint(-60, 120))
            alquiler = Alquiler(
                dni=u.dni, nombre=u.nombre_completo, email=u.email, actividad=u.actividad,
                pais=rng.choice(paises), talla=rng.choice(TALLAS[1:6]),
                cantidad=rng.randint(1, 4), fecha_actividad=fecha.isoformat(),
                precio_unitario=calcular_precio(fecha, rng))
            try:
                gestor.registrar_reserva(alquiler)
                hechas += 1
            except StockInsuficiente:
                continue

        for dias in range(0, 6):
            dia = (hoy + timedelta(days=dias)).isoformat()
            for hora in rng.sample(["10:00", "12:00", "16:00", "18:00"], 2):
                gestor.agregar_evento(dia, hora, rng.choice(EVENTOS))
    return destino


def asegurar_base_de_trabajo() -> Path:
    """Crea la base de trabajo la primera vez que se ejecuta la aplicación."""
    if not BASE_DATOS.exists():
        crear_base_de_trabajo()
    return BASE_DATOS


if __name__ == "__main__":
    print(f"Base de datos creada en {crear_base_de_trabajo()}")

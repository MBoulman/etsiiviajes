"""Análisis de clientes, ventas y especies (pandas, scikit-learn y matplotlib).

Cada función devuelve datos o figuras de matplotlib; la interfaz decide cómo
mostrarlas. Así se pueden probar sin abrir ventanas.
"""

from datetime import date

import pandas as pd
from matplotlib.figure import Figure
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from .config import AGUAS, TALLAS
from .gestor import GestorBasesDatos
from .utils import edad

COLOR = "#2a7fb8"


def _figura(titulo: str, ancho=7, alto=4.5) -> tuple[Figure, object]:
    fig = Figure(figsize=(ancho, alto), tight_layout=True)
    ax = fig.add_subplot()
    ax.set_title(titulo)
    return fig, ax


def _barras(serie: pd.Series, titulo: str, xlabel: str, ylabel: str) -> Figure:
    fig, ax = _figura(titulo)
    ax.bar(serie.index.astype(str), serie.values, color=COLOR)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(axis="x", rotation=45)
    for etiqueta in ax.get_xticklabels():
        etiqueta.set_horizontalalignment("right")
    ax.spines[["top", "right"]].set_visible(False)
    return fig


# --------------------------------------------------------------------- clientes

def datos_clientes(gestor: GestorBasesDatos, actividad: str) -> pd.DataFrame:
    usuarios = gestor.listar_usuarios(actividad)
    df = pd.DataFrame([{
        "nacionalidad": u.nacionalidad.upper(), "altura": u.altura, "peso": u.peso,
        "nivel": u.nivel, "edad": edad(date.fromisoformat(u.fecha_nacimiento)),
    } for u in usuarios])
    return df


def resumen_edad(df: pd.DataFrame) -> str:
    if df.empty:
        return "No hay clientes registrados."
    q = df["edad"].quantile([0.25, 0.5, 0.75])
    return (f"Clientes: {len(df)}\nEdad media: {df['edad'].mean():.1f} años\n"
            f"Q1: {q[0.25]:.0f} · Mediana: {q[0.5]:.0f} · Q3: {q[0.75]:.0f} años")


def grafico_nacionalidades(df: pd.DataFrame, nombre: str) -> Figure:
    return _barras(df["nacionalidad"].value_counts(), f"{nombre} por nacionalidad",
                   "Nacionalidad", "Clientes")


def grafico_niveles(df: pd.DataFrame, nombre: str) -> Figure:
    conteo = df["nivel"].value_counts()
    fig, ax = _figura(f"Nivel de los {nombre.lower()}", 6, 5)
    ax.pie(conteo.values, labels=conteo.index, autopct="%1.0f%%", startangle=90,
           wedgeprops={"edgecolor": "white"})
    ax.axis("equal")
    return fig


def clusters(df: pd.DataFrame, nombre: str, k: int = 3) -> tuple[pd.DataFrame, list[Figure]]:
    """Segmenta a los clientes con K-means a partir de altura, peso, edad y nacionalidad."""
    k = max(1, min(k, len(df)))
    preparar = ColumnTransformer([
        ("num", StandardScaler(), ["altura", "peso", "edad"]),
        ("cat", OneHotEncoder(handle_unknown="ignore"), ["nacionalidad"]),
    ])
    modelo = make_pipeline(preparar, KMeans(n_clusters=k, n_init=25, random_state=0))
    df = df.copy()
    df["grupo"] = modelo.fit_predict(df) + 1

    fig1, ax = _figura(f"{nombre}: grupos por altura y peso")
    for g, datos in df.groupby("grupo"):
        ax.scatter(datos["altura"], datos["peso"], label=f"Grupo {g}")
    ax.set_xlabel("Altura (cm)")
    ax.set_ylabel("Peso (kg)")
    ax.legend()

    fig2, ax = _figura(f"{nombre}: edad por grupo")
    grupos = sorted(df["grupo"].unique())
    ax.boxplot([df.loc[df["grupo"] == g, "edad"] for g in grupos])
    ax.set_xticks(range(1, len(grupos) + 1), [f"Grupo {g}" for g in grupos])
    ax.set_ylabel("Edad (años)")

    fig3 = Figure(figsize=(7, 5.5), tight_layout=True)
    ax3 = fig3.add_subplot(projection="3d")
    for g, datos in df.groupby("grupo"):
        ax3.scatter(datos["altura"], datos["peso"], datos["edad"], label=f"Grupo {g}")
    ax3.set_title(f"{nombre}: grupos en 3D")
    ax3.set_xlabel("Altura (cm)")
    ax3.set_ylabel("Peso (kg)")
    ax3.set_zlabel("Edad (años)")
    ax3.legend()
    return df, [fig1, fig2, fig3]


# ----------------------------------------------------------------------- ventas

def datos_ventas(gestor: GestorBasesDatos) -> pd.DataFrame:
    return pd.DataFrame([{
        "actividad": v.actividad, "talla": v.talla, "pais": v.pais,
        "cantidad": v.cantidad, "precio": v.precio_total,
    } for v in gestor.listar_ventas()])


def gasto_medio(df: pd.DataFrame) -> str:
    if df.empty:
        return "No hay ventas."
    return f"Ventas: {len(df)}\nGasto medio por reserva: {df['precio'].mean():.2f} €"


def grafico_gasto_por_pais(df: pd.DataFrame) -> Figure:
    serie = df.groupby("pais")["precio"].mean().sort_values(ascending=False)
    return _barras(serie, "Gasto medio por país del centro", "País", "€ por reserva")


def grafico_ventas_por_actividad(df: pd.DataFrame) -> Figure:
    return _barras(df.groupby("actividad")["precio"].sum(), "Facturación por actividad",
                   "Actividad", "€")


def grafico_tallas(df: pd.DataFrame) -> Figure:
    conteo = df["talla"].value_counts().reindex(TALLAS, fill_value=0)
    return _barras(conteo, "Reservas por talla", "Talla", "Reservas")


class ModeloPrecio:
    """Regresión lineal del importe de una reserva según talla, país y actividad.

    Es una demostración del flujo de trabajo (codificar, separar train/test,
    entrenar y medir R²). Con pocos datos, y con un precio que depende sobre todo
    de la fecha, el R² será bajo: la interfaz lo muestra para que se vea.
    """

    VARIABLES = ["talla", "pais", "actividad"]

    def __init__(self, df: pd.DataFrame):
        if len(df) < 5:
            raise ValueError("Hacen falta al menos 5 ventas para entrenar el modelo.")
        x, y = df[self.VARIABLES], df["precio"]
        x_tr, x_te, y_tr, y_te = train_test_split(x, y, test_size=0.2, random_state=42)
        self.modelo = make_pipeline(
            ColumnTransformer([("cat", OneHotEncoder(handle_unknown="ignore"), self.VARIABLES)]),
            LinearRegression())
        self.modelo.fit(x_tr, y_tr)
        self.r2 = r2_score(y_te, self.modelo.predict(x_te)) if len(y_te) > 1 else float("nan")
        self.n = len(df)

    def predecir(self, talla: str, pais: str, actividad: str) -> float:
        nuevo = pd.DataFrame([{"talla": talla, "pais": pais, "actividad": actividad}])
        return float(self.modelo.predict(nuevo)[0])


# ---------------------------------------------------------------- fauna y flora

def grafico_especies_por_aguas(gestor: GestorBasesDatos) -> tuple[dict[str, int], Figure]:
    especies = gestor.listar_especies()
    conteo = {nombre: sum(e.aguas[clave] for e in especies) for clave, nombre in AGUAS.items()}
    serie = pd.Series(conteo).sort_values(ascending=False)
    return conteo, _barras(serie, "Especies registradas por aguas", "Aguas", "Especies")


def especies_de_aguas(gestor: GestorBasesDatos, clave: str) -> tuple[list[str], list[str]]:
    """Nombres de fauna y de flora vistas en unas aguas."""
    especies = gestor.especies_en_aguas([clave])
    fauna = [e.nombre.capitalize() for e in especies if e.tipo == "FAUNA"]
    flora = [e.nombre.capitalize() for e in especies if e.tipo == "FLORA"]
    return fauna, flora

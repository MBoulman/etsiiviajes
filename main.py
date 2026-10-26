"""Punto de entrada de ETSIIVIAJES: ``python main.py``."""

from etsiiviajes.datos_demo import asegurar_base_de_trabajo
from etsiiviajes.gestor import GestorBasesDatos
from etsiiviajes.ui.principal import VentanaPrincipal


def main() -> None:
    gestor = GestorBasesDatos(asegurar_base_de_trabajo())
    VentanaPrincipal(gestor).mainloop()


if __name__ == "__main__":
    main()

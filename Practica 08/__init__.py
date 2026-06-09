"""
Genera un diagrama de barras con los lenguajes de programación más demandados en 2022.

Este script utiliza matplotlib para crear una gráfica de barras a partir de datos
predefinidos, la guarda como archivo PNG y la muestra en pantalla.
"""

import matplotlib.pyplot as plt
from typing import List, Tuple

# Constantes configurables
FIGURE_SIZE: Tuple[int, int] = (10, 6)
CHART_TITLE: str = "Lenguajes de Programación Más Demandados en 2022"
XLABEL: str = "Lenguajes de Programación"
YLABEL: str = "Porcentaje de Popularidad (%)"
BAR_COLOR: str = "#2E8B57"  # verde marino
FILE_NAME: str = "diagrama_barras.png"
DPI: int = 300

# Datos de entrada (pueden ser reemplazados por una fuente externa)
LENGUAJES: List[str] = ["Python", "C", "Java", "C++", "C#"]
PORCENTAJES: List[float] = [14.0, 12.0, 11.0, 10.0, 8.0]


def validar_datos(lenguajes: List[str], porcentajes: List[float]) -> None:
    """
    Valida que los datos de entrada sean consistentes.

    Args:
        lenguajes: Lista de nombres de lenguajes.
        porcentajes: Lista de valores de porcentaje.

    Raises:
        ValueError: Si las listas tienen longitudes diferentes o si algún porcentaje es inválido.
    """
    if len(lenguajes) != len(porcentajes):
        raise ValueError("Las listas de lenguajes y porcentajes deben tener la misma longitud.")
    for p in porcentajes:
        if not isinstance(p, (int, float)) or p < 0:
            raise ValueError("Todos los porcentajes deben ser números no negativos.")


def crear_grafico_barras(lenguajes: List[str], porcentajes: List[float]) -> plt.Figure:
    """
    Crea y configura la figura del diagrama de barras.

    Args:
        lenguajes: Etiquetas para el eje X.
        porcentajes: Alturas de las barras.

    Returns:
        Figura de matplotlib configurada.
    """
    validar_datos(lenguajes, porcentajes)

    # Aplicar un estilo profesional
    plt.style.use('seaborn-v0_8-darkgrid')

    fig, ax = plt.subplots(figsize=FIGURE_SIZE)

    # Gráfico de barras con mejoras estéticas
    barras = ax.bar(
        lenguajes,
        porcentajes,
        color=BAR_COLOR,
        width=0.6,
        edgecolor='white',
        linewidth=1.2,
        label="Demanda 2022"
    )

    # Agregar valores encima de cada barra
    for barra in barras:
        altura = barra.get_height()
        ax.text(
            barra.get_x() + barra.get_width() / 2,
            altura + 0.3,
            f"{altura:.1f}%",
            ha='center',
            va='bottom',
            fontsize=10,
            fontweight='bold'
        )

    # Personalizar ejes y título
    ax.set_title(CHART_TITLE, fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel(XLABEL, fontsize=12, labelpad=10)
    ax.set_ylabel(YLABEL, fontsize=12, labelpad=10)
    ax.set_ylim(0, max(porcentajes) * 1.15)  # Espacio para las etiquetas

    # Mejorar la leyenda y la cuadrícula
    ax.legend(loc='upper right', frameon=True, fancybox=True, shadow=True)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.set_axisbelow(True)  # Cuadrícula detrás de las barras

    # Rotar etiquetas del eje X si es necesario (aquí no es necesario)
    plt.xticks(rotation=0, ha='center')

    # Ajustar márgenes para evitar recortes
    plt.tight_layout()

    return fig


def guardar_grafico(fig: plt.Figure, nombre_archivo: str, dpi: int = DPI) -> None:
    """
    Guarda la figura en disco con manejo de errores.

    Args:
        fig: Figura de matplotlib a guardar.
        nombre_archivo: Nombre del archivo de salida.
        dpi: Resolución en puntos por pulgada.
    """
    try:
        fig.savefig(nombre_archivo, dpi=dpi, bbox_inches='tight')
        print(f"Gráfico guardado exitosamente como '{nombre_archivo}'")
    except Exception as e:
        print(f"Error al guardar el gráfico: {e}")


def main() -> None:
    """Función principal que orquesta la creación, guardado y visualización del gráfico."""
    try:
        fig = crear_grafico_barras(LENGUAJES, PORCENTAJES)
        guardar_grafico(fig, FILE_NAME)
        plt.show()  # Muestra la ventana interactiva
    except ValueError as ve:
        print(f"Error en los datos: {ve}")
    except Exception as e:
        print(f"Error inesperado: {e}")


if __name__ == "__main__":
    main()
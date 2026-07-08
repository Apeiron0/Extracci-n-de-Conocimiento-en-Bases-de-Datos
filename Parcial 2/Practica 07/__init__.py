#El programa generará una ventana con un gráfico de líneas que permite comparar visualmente el desempeño
#de ambas empresas. La Empresa A (línea azul) parte de ventas más altas en 2019, pero la Empresa B (línea roja)
#muestra un crecimiento más acelerado, alcanzando las mismas ventas que A en 2022.

import matplotlib.pyplot as plt
import numpy as np

# Datos más realistas: más años y tendencias ajustadas
years = np.arange(2019, 2026)  # 2019 a 2025
# Empresa A: crecimiento estable pero se ralentiza a partir de 2023
sales_a = [14.2, 18.5, 23.1, 32.0, 35.5, 37.8, 39.2]
# Empresa B: inicio más bajo pero crecimiento acelerado (innovación, expansión)
sales_b = [11.0, 12.3, 26.4, 32.0, 38.5, 44.2, 49.5]

# Configurar tamaño de figura y estilo
plt.figure(figsize=(10, 6))
plt.style.use('seaborn-v0_8-darkgrid')  # Estilo profesional

# Graficar líneas con marcadores para resaltar puntos anuales
plt.plot(years, sales_a, color='#1f77b4', linewidth=2.5, marker='o', markersize=6, label='Empresa A')
plt.plot(years, sales_b, color='#d62728', linewidth=2.5, marker='s', markersize=6, label='Empresa B')

# Añadir anotación en el punto de cruce (2022, 32.0)
plt.annotate('Igualdad de ventas en 2022', xy=(2022, 32.0), xytext=(2023, 38),
             arrowprops=dict(arrowstyle='->', color='gray', lw=1),
             fontsize=10, ha='center', bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))

# Resaltar el año 2025 con una línea vertical punteada y texto
plt.axvline(x=2025, color='green', linestyle='--', linewidth=1, alpha=0.7)
plt.text(2025.2, max(sales_b)*0.9, 'Proyección 2025', rotation=90, fontsize=9, color='green')

# Título y etiquetas con unidades y contexto
plt.title('Comparación de Ventas Anuales: Empresa A vs Empresa B\n(2019-2025)', fontsize=14, fontweight='bold')
plt.xlabel('Año', fontsize=12)
plt.ylabel('Ventas (millones de USD)', fontsize=12)

# Personalizar ticks del eje X para mostrar todos los años
plt.xticks(years, rotation=45)
plt.yticks(np.arange(10, 56, 5))

# Límites de los ejes para dar espacio a las anotaciones
plt.ylim(10, 55)

# Añadir leyenda y cuadrícula (estilo ya incluido, pero se refuerza)
plt.legend(title='Empresas', title_fontsize=11, fontsize=10, loc='upper left')
plt.grid(True, linestyle='--', alpha=0.6)

# Nota al pie de figura (contexto realista)
plt.figtext(0.5, -0.05,
            'Nota: Datos simulados basados en tendencias de crecimiento realistas.\n'
            'Empresa B acelera a partir de 2021 gracias a lanzamiento de nuevos productos.',
            wrap=True, ha='center', fontsize=9, color='gray')

# Ajustar márgenes para que la nota se vea completa
plt.tight_layout()
plt.show()
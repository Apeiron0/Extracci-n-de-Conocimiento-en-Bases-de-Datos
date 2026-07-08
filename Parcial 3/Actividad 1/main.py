#En una ciudad, la contaminación del aire (CO2) y el tráfico vehicular están
#relacionados. Supongamos que:
#La función cuadrática ( f(x)=x 2 ) representa el aumento no lineal de la contaminación a medida que crece
#el número de vehículos (x).
#Ejemplo: A mayor tráfico, la contaminación aumenta aceleradamente
#(por congestión, mala combustión, etc.).
#La función lineal
#f(x)=4x+5   modela el crecimiento lineal de la infraestructura vial (ej.
#            capacidad de vías o semáforos).
#Ejemplo: Cada nuevo carril o semáforo reduce parcialmente el problema,
#pero no lo resuelve exponencialmente.
#Objetivo:
#Encontrar el punto de equilibrio (intersección) donde la contaminación y
#la infraestructura se igualan, para determinar políticas efectivas
#(ej. límite de vehículos o inversión en transporte público).



import matplotlib.pyplot as plt
import numpy as np

# Función 1: Contaminación (crecimiento cuadrático por tráfico).
def contaminacion(x):
    return x**2  # Ejemplo: CO2 en ppm (partes por millón).

# Función 2: Infraestructura vial (crecimiento lineal).
def infraestructura(x):
    return 4*x + 5  # Ejemplo: Eficiencia vial (ej. capacidad de autos/hora).

# Rango de vehículos (miles) en la ciudad.
x = range(0, 15)  # Desde 0 hasta 15 mil vehículos.

# Graficar.
plt.plot(x, [contaminacion(i) for i in x], color="red", label="Contaminación (CO2) = x²")
plt.plot(x, [infraestructura(i) for i in x], color="blue", label="Infraestructura = 4x + 5")

# Ejes y título.
plt.axhline(0, color="black", linewidth=0.5)
plt.axvline(0, color="black", linewidth=0.5)
plt.title("Impacto del Tráfico en la Contaminación y Infraestructura")
plt.xlabel("Número de vehículos (miles)")
plt.ylabel("Nivel de impacto")
plt.grid(linestyle="--", alpha=0.6)
plt.legend()

# Resaltar punto de equilibrio (solución).
soluciones = np.roots([1, -4, -5])  # Resuelve x² = 4x + 5 ? x² -4x -5 = 0.
x_sol = [sol for sol in soluciones if sol >= 0][0]  # Tomar solución positiva.
y_sol = contaminacion(x_sol)
plt.scatter(x_sol, y_sol, color="green", zorder=5, label=f"Equilibrio: x^{x_sol:.1f}")
plt.annotate(f'Política óptima: {x_sol:.1f} mil vehículos',
             xy=(x_sol, y_sol),
             xytext=(5, 100),
             arrowprops=dict(arrowstyle="->"))

plt.show()
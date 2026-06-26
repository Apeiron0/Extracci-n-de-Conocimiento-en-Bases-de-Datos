# ==============================================================================
# ANÁLISIS DE DISPERSIÓN: HORAS DE ESTUDIO VS NOTAS (LECTURA DESDE CSV)
# ==============================================================================
# Contexto: Se analizan 50 estudiantes de un centro educativo.
# Los datos provienen de 'estudiantes.csv' (columnas: horas_estudio,
# notas_algebra, notas_quimica, horas_sueno).
# Objetivo: Visualizar la relación, calcular correlaciones y regresión.
# ==============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import seaborn as sns

# ------------------------------------------------------------------------------
# 1. CARGA DE DATOS DESDE CSV
# ------------------------------------------------------------------------------
try:
    df = pd.read_csv('estudiantes.csv', encoding='utf-8')
    print("📊 Datos cargados correctamente:")
    print(df.head(), "\n")
except FileNotFoundError:
    print("❌ Error: No se encontró el archivo 'estudiantes.csv'.")
    print("👉 Ejecuta primero el script 'generar_datos_csv.py'.")
    exit()

# Extraemos las columnas como variables (trabajamos con Series de pandas)
horas_estudio = df['horas_estudio']
notas_algebra = df['notas_algebra']
notas_quimica = df['notas_quimica']
horas_sueno = df['horas_sueno']

# ------------------------------------------------------------------------------
# 2. ESTADÍSTICOS Y CORRELACIONES
# ------------------------------------------------------------------------------
corr_algebra, p_algebra = stats.pearsonr(horas_estudio, notas_algebra)
corr_quimica, p_quimica = stats.pearsonr(horas_estudio, notas_quimica)

print("=== 📈 RESULTADOS ESTADÍSTICOS ===")
print(f"📘 Álgebra: r = {corr_algebra:.3f} (p-valor = {p_algebra:.4f})")
print(f"🧪 Química: r = {corr_quimica:.3f} (p-valor = {p_quimica:.4f})")
print(" (p < 0.05 indica correlación significativa)\n")

# ------------------------------------------------------------------------------
# 3. REGRESIÓN LINEAL (ajuste por mínimos cuadrados)
# ------------------------------------------------------------------------------
# Para Álgebra
coef_algebra = np.polyfit(horas_estudio, notas_algebra, 1)
recta_algebra = np.poly1d(coef_algebra)

# Para Química
coef_quimica = np.polyfit(horas_estudio, notas_quimica, 1)
recta_quimica = np.poly1d(coef_quimica)

print("📝 Ecuaciones de regresión:")
print(f"   Álgebra: Nota = {coef_algebra[0]:.2f} * Horas + {coef_algebra[1]:.2f}")
print(f"   Química: Nota = {coef_quimica[0]:.2f} * Horas + {coef_quimica[1]:.2f}\n")

# ------------------------------------------------------------------------------
# 4. VISUALIZACIÓN PROFESIONAL
# ------------------------------------------------------------------------------
# Configurar estilo
sns.set_style("whitegrid")
sns.set_palette("deep")

fig, ax = plt.subplots(figsize=(10, 6))

# Dispersión: el tamaño del punto refleja las horas de sueño
scatter1 = ax.scatter(horas_estudio, notas_algebra,
                      s=horas_sueno * 25, # escalamos para que se vea bien
                      color="royalblue", alpha=0.7, edgecolors='w', linewidth=0.5,
                      label="Álgebra")

scatter2 = ax.scatter(horas_estudio, notas_quimica,
                      s=horas_sueno * 25,
                      color="coral", alpha=0.7, edgecolors='w', linewidth=0.5,
                      label="Química")

# Líneas de regresión (extendemos el rango para que cruce todo el gráfico)
x_line = np.linspace(0, 13, 100)
ax.plot(x_line, recta_algebra(x_line), 'b--', linewidth=2, label="Regresión Álgebra")
ax.plot(x_line, recta_quimica(x_line), 'r--', linewidth=2, label="Regresión Química")

# Anotaciones de los coeficientes de correlación dentro del gráfico
ax.text(0.5, 18.5, f"Álgebra: r = {corr_algebra:.2f}", color='royalblue', fontsize=11, fontweight='bold')
ax.text(0.5, 17.0, f"Química: r = {corr_quimica:.2f}", color='coral', fontsize=11, fontweight='bold')

# Títulos y etiquetas (con unidad de medida)
ax.set_title("Relación entre horas de estudio y rendimiento académico\n"
             "Álgebra vs Química (n=50)", fontsize=14, fontweight='bold')
ax.set_xlabel("Horas de estudio semanales (fuera de clase)", fontsize=12)
ax.set_ylabel("Nota final (escala 0-20)", fontsize=12)

# Leyenda y cuadrícula
ax.legend(loc="lower right", framealpha=0.9)
ax.grid(True, linestyle=':', alpha=0.6)

# Ajustar límites para dar margen
ax.set_xlim(0, 13)
ax.set_ylim(0, 21)

# Nota aclaratoria sobre el tamaño de los puntos
ax.text(9.5, 1.2, "Tamaño del punto ∝ horas de sueño",
        fontsize=9, style='italic', ha='center', color='dimgray',
        bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

# Guardar la figura en alta resolución
plt.tight_layout()
plt.savefig("diagrama_dispersion_csv.png", dpi=300, bbox_inches='tight')
print("💾 Gráfico guardado como 'diagrama_dispersion_csv.png'")

# Mostrar en pantalla
plt.show()
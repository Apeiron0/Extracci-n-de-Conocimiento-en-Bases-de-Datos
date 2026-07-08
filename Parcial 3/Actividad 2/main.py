# ==============================================================================
# PROGRAMA: Temperatura diaria y su modelo sinusoidal
# OBJETIVO: Conectar a MySQL, extraer datos reales de temperatura y graficarlos
#           junto con un ajuste por función seno (coseno) para mostrar su utilidad.
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. IMPORTACIÓN DE BIBLIOTECAS
# ------------------------------------------------------------------------------
import mysql.connector          # Para conectar con MySQL
import matplotlib.pyplot as plt # Para hacer gráficos
import numpy as np              # Para operaciones matemáticas y ajuste de curvas
from scipy.optimize import curve_fit  # Para ajustar la función seno a los datos

# ------------------------------------------------------------------------------
# 2. DEFINICIÓN DE LA FUNCIÓN QUE MODELARÁ LA TEMPERATURA
#    Modelo: T(h) = A * sin(?*h + f) + C
#    donde:
#       A     = amplitud (cuánto varía la temperatura)
#       ?     = frecuencia angular (2p / periodo, periodo = 24 horas)
#       f     = fase (desfase con respecto a la hora 0)
#       C     = temperatura media (offset)
# ------------------------------------------------------------------------------
def modelo_temperatura(hora, A, omega, phi, C):
    """
    Calcula la temperatura en función de la hora usando un modelo sinusoidal.
    Parámetros:
        hora : array de horas (0 a 24)
        A    : amplitud
        omega: frecuencia angular
        phi  : fase
        C    : temperatura media
    Retorna:
        temperatura calculada
    """
    return A * np.sin(omega * hora + phi) + C

# ------------------------------------------------------------------------------
# 3. CONFIGURACIÓN DE LA CONEXIÓN A MYSQL
# ------------------------------------------------------------------------------
# (Cambia los valores según tu servidor)
config = {
    'host': 'localhost',
    'database': 'ecbd',          # Base de datos que crearemos
    'user': 'root',              # Usuario con permisos de lectura
    'password': ''
}

# Intentamos conectar
try:
    conexion = mysql.connector.connect(**config)
    print("? Conexión exitosa a MySQL")
except mysql.connector.Error as err:
    print(f"? Error al conectar: {err}")
    exit()  # Termina el programa si no hay conexión

# ------------------------------------------------------------------------------
# 4. CONSULTA SQL PARA OBTENER LOS DATOS DE TEMPERATURA
# ------------------------------------------------------------------------------
# Suponemos una tabla 'temperaturas' con columnas: id, hora (float), temp (float)
consulta = "SELECT hora, temp FROM temperaturas ORDER BY hora ASC"

cursor = conexion.cursor()
cursor.execute(consulta)
registros = cursor.fetchall()  # Lista de tuplas (hora, temp)

# Cerramos conexión y cursor (buena práctica)
cursor.close()
conexion.close()
print(f"?? Se obtuvieron {len(registros)} mediciones.")

# ------------------------------------------------------------------------------
# 5. SEPARAMOS LOS DATOS EN DOS LISTAS: horas y temperaturas
# ------------------------------------------------------------------------------
horas = []   # Lista de horas (0 a 24)
temps = []   # Lista de temperaturas en °C

for reg in registros:
    horas.append(reg[0])
    temps.append(reg[1])

# Convertimos a arrays de numpy para facilitar operaciones
horas = np.array(horas)
temps = np.array(temps)

# ------------------------------------------------------------------------------
# 6. AJUSTE DE LA CURVA SENO A LOS DATOS REALES
# ------------------------------------------------------------------------------
# Estimación inicial de parámetros (valores aproximados)
# - Amplitud: (máx - mín) / 2
# - Frecuencia: 2p / 24 (porque el periodo es 24 horas)
# - Fase: 0 (suponemos que el máximo ocurre al mediodía, ajustará)
# - Offset: promedio de las temperaturas
A_guess = (max(temps) - min(temps)) / 2
omega_guess = 2 * np.pi / 24
phi_guess = 0
C_guess = np.mean(temps)

# Realizamos el ajuste con curve_fit
param_opt, _ = curve_fit(modelo_temperatura, horas, temps,
                         p0=[A_guess, omega_guess, phi_guess, C_guess])

# Extraemos los parámetros optimizados
A_opt, omega_opt, phi_opt, C_opt = param_opt

# Mostramos los parámetros obtenidos para entender el modelo
print("\n?? Parámetros del ajuste:")
print(f"   Amplitud A = {A_opt:.2f} °C")
print(f"   Frecuencia ? = {omega_opt:.4f} rad/h")
print(f"   Fase f = {phi_opt:.2f} rad")
print(f"   Temperatura media C = {C_opt:.2f} °C")

# Generamos la curva teórica con los parámetros ajustados
horas_continuas = np.linspace(0, 24, 300)  # 300 puntos para suavidad
temps_ajustados = modelo_temperatura(horas_continuas, *param_opt)

# ------------------------------------------------------------------------------
# 7. GRÁFICO: DATOS REALES VS MODELO SENO
# ------------------------------------------------------------------------------
# Creamos la figura y los ejes
fig, ax = plt.subplots(figsize=(10, 6))

# Dibujamos los puntos de los datos reales (círculos azules)
ax.scatter(horas, temps, color='blue', s=60, label='Datos reales (mediciones)', zorder=3)

# Dibujamos la curva ajustada (línea roja)
ax.plot(horas_continuas, temps_ajustados, color='red', linewidth=2,
        label='Ajuste sinusoidal', zorder=2)

# Añadimos una línea horizontal en la temperatura media (offset)
ax.axhline(C_opt, color='gray', linestyle='--', linewidth=1,
          label=f'Temperatura media = {C_opt:.1f} °C')

# Personalizamos el gráfico
ax.set_title('??? Temperatura a lo largo del día - Modelo sinusoidal', fontsize=14)
ax.set_xlabel('Hora del día (h)', fontsize=12)
ax.set_ylabel('Temperatura (°C)', fontsize=12)
ax.grid(True, linestyle=':', alpha=0.7)
ax.legend(loc='best')
ax.set_xlim(0, 24)           # Las horas van de 0 a 24
ax.set_ylim(min(temps)-2, max(temps)+2)  # Un poco de margen

# Mostramos el gráfico
plt.tight_layout()
plt.show()

# ------------------------------------------------------------------------------
# 8. INTERPRETACIÓN PARA LOS ALUMNOS (se imprime en consola)
# ------------------------------------------------------------------------------
print("\n?? INTERPRETACIÓN:")
print(" - La curva roja muestra cómo la temperatura varía de forma sinusoidal.")
print(" - Los puntos azules son mediciones reales; si se acercan a la curva, el modelo es bueno.")
print(" - La amplitud A indica cuánto sube/baja la temperatura desde el promedio.")
print(" - La fase f indica a qué hora ocurre el máximo de temperatura.")
print(" - Este es un ejemplo de cómo las funciones trigonométricas aparecen en la naturaleza.")
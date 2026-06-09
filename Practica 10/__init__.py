# El objetivo es utilizar Python para cargar, limpiar y visualizar los datos,
# generando gráficos que permitan entender mejor la distribución y las
# relaciones entre las variables.


import pandas as pd
import matplotlib.pyplot as plt
import math

# Cargar los datos desde el archivo CSV
datos = pd.read_csv('ventas.csv', header=0, index_col=False, encoding="latin1")
print(datos)
print(datos.info())
print(datos.shape)

# Limpieza de la columna 'Sucursal'
datos['Sucursal'] = datos['Sucursal'].replace('Nte', 'Norte')
datos['Sucursal'] = datos['Sucursal'].replace('Cte', 'Centro')
datos['Sucursal'] = datos['Sucursal'].replace('Sur', 'Sur')

# Gráfico de pastel: Ventas por Sucursal
fig, plot = plt.subplots()
datos.groupby('Sucursal').count()['VentaID'].plot(kind='pie')
plt.legend(loc='best', ncol=3, framealpha=0.3, bbox_to_anchor=[1.5, 0])
plt.xlabel(None)
plt.ylabel(None)
plt.title('Ventas por Sucursal')
plt.savefig('Ventas_por_Sucursal.pdf')

# Gráfico de barras: Ventas por Vendedor
fig, plot = plt.subplots()
datos.groupby('Vendedor').count()['VentaID'].plot(kind='bar')
plt.xlabel('Vendedor')
plt.ylabel('Cantidad de Ventas')
plt.title('Ventas por Vendedor')
plt.savefig('Ventas_por_Vendedor.pdf')

# Gráfico de dispersión: Precio vs. Cantidad Vendida
fig, plot = plt.subplots()
datos.plot('Precio', 'Cantidad', kind='scatter')
plt.xlabel('Precio del Producto')
plt.ylabel('Cantidad Vendida')
plt.title('Precio vs. Cantidad Vendida')
plt.savefig('Precio_vs_Cantidad.pdf')

# Histograma: Distribución de Precios
fig, plot = plt.subplots()
rango = datos['Precio'].max() - datos['Precio'].min()
print("Rango: ", rango)
intervalos = 1 + 3.3 * math.log10(rango)
print("Intervalos: ", intervalos)
amplitud = round(rango / round(intervalos, 0))
print("Amplitud: ", amplitud)

plot.hist(x=datos['Precio'], bins=amplitud, color='red', density=False, facecolor='b')
plt.grid(True)
plt.xlabel('Precio del Producto')
plt.ylabel('Frecuencia')
plt.title('Histograma de Precios')
plt.savefig('Histograma_Precios.pdf')
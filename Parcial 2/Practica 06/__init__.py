#El programa generará una ventana con un gráfico de líneas que permite comparar visualmente el desempeño
#de ambas empresas. La Empresa A (línea azul) parte de ventas más altas en 2019, pero la Empresa B (línea roja)
#muestra un crecimiento más acelerado, alcanzando las mismas ventas que A en 2022.


#Librería
import matplotlib.pyplot as plt

#Datos
years=[2019,2020,2021,2022]
sales_a=[14,18,23,32]
sales_b=[11,12,26,32]

#Configurar las características del grafico
plt.plot(years,sales_a,color='blue',linewidth=3,label='EMPRESA A')
plt.plot(years,sales_b,color='red',linewidth=3,label='EMPRESA B')

#Definir titulo y nombre de ejes
plt.title("DIAGRAMA DE LINEA")
plt.ylabel('Ventas')
plt.xlabel('Años')
plt.xticks(years)

#Mostrar leyenda, cuadricula y figura
plt.legend()
plt.grid()
plt.show()
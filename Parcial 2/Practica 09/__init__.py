import numpy as np
import matplotlib.pyplot as plt

# Datos
x = np.linspace(0, 10, 25)
y = np.sin(x) + x/2

# Gráfico de líneas
fig, ax = plt.subplots()
ax.plot(x, y)
plt.show()

####################################

##  COLOR DE LINEA

import numpy as np
import matplotlib.pyplot as plt

# Datos
x = np.linspace(0, 10, 25)
y = np.sin(x) + x/2

# Gráfico de líneas
fig, ax = plt.subplots()
ax.plot(x, y, color = "r")
plt.show()

####################################

###  GROSOR DE LINEA

import numpy as np
import matplotlib.pyplot as plt

# Datos
x = np.linspace(0, 10, 25)
y = np.sin(x) + x/2

# Gráfico de líneas
fig, ax = plt.subplots()
ax.plot(x, y, linewidth = 4)
# ax.plot(x, y, lw = 4) # Equivalente
plt.show()

####################################

###  ESTILO DE LINEA

import numpy as np
import matplotlib.pyplot as plt

# Datos
x = np.linspace(0, 10, 25)
y = np.sin(x) + x/2

# Gráfico de líneas
fig, ax = plt.subplots()
ax.plot(x, y, linestyle = "--")
# ax.plot(x, y, ls = "--") # Equivalente
plt.show()

####################################

###  AGREGAR SIMBOLOS A LAS LINEAS

import numpy as np
import matplotlib.pyplot as plt

# Datos
x = np.linspace(0, 10, 25)
y = np.sin(x) + x/2

# Gráfico de líneas
fig, ax = plt.subplots()
ax.plot(x, y, marker = "o", markersize = 5)
# ax.plot(x, y, marker = "o", ms = 5) # Equivalente
plt.show()

####################################

##  LINEAS Y SIMBOLOS CON COLORES

import numpy as np
import matplotlib.pyplot as plt

# Datos
x = np.linspace(0, 10, 25)
y = np.sin(x) + x/2

# Gráfico de líneas
fig, ax = plt.subplots()
ax.plot(x, y, color = "r", marker = 's',
        markerfacecolor = 'black', markeredgecolor = 'black')
# ax.plot(x, y, color = "r", marker = 's', mfc = 'black', mec = 'black') # Equivalente
plt.show()

#########################################333

###  USAR FORMATO

import numpy as np
import matplotlib.pyplot as plt

# Datos
x = np.linspace(0, 10, 25)
y = np.sin(x) + x/2

# Gráfico de líneas
fig, ax = plt.subplots()
ax.plot(x, y, "*g-")
plt.show()

#########################################333

####  GRAFICA CON VARIAS LINEAS

import numpy as np
import matplotlib.pyplot as plt

# Datos
x1 = np.linspace(0, 10, 25)
y1 = np.sin(x1) + x1/2

x2 = np.linspace(0, 10, 25)
y2 = np.cos(x2) + x2/2

# Gráfico de líneas
fig, ax = plt.subplots()
ax.plot(x1, y1, marker = "o", label = "Sin(x) + x/2")
ax.plot(x2, y2, marker = "o", label = "Cos(x) + x/2")
ax.legend()

plt.show()

#########################################333

########  GRAFICA DE VARIOS NIVELES

import numpy as np
import matplotlib.pyplot as plt

# Datos
x1 = np.linspace(0, 10, 25)
y1 = np.sin(x1) + x1/2

x2 = np.linspace(0, 10, 25)
y2 = np.cos(x2) + x2/2

# Gráfico de líneas
fig, ax = plt.subplots()
ax.plot(x1, y1, "c^", x2, y2, "d--")

plt.show()

#########################################333

#####  FUNCION STEP

import numpy as np
import matplotlib.pyplot as plt

# Datos
x = np.linspace(0, 10, 25)
y = np.sin(x) + x/2

# Gráfico de líneas
fig, ax = plt.subplots()
ax.step(x, y)
plt.show()
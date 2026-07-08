#El piso de una terraza tiene 425 cm de largo por 275 cm de ancho, si se
#desea poner el menor número de mosaicos cuadrados de mármol, ¿cuáles serán
#las dimensiones máximas de cada mosaico?, ¿cuántos mosaicos se necesitan?

import math

# Dimensiones de la terraza (cm)
largo = 425
ancho = 275

# Calculamos el MCD para la dimensión del mosaico
mcd = math.gcd(largo, ancho)
dimension_mosaico = mcd

# Calculamos el número de mosaicos
num_mosaicos = (largo * ancho) // (mcd ** 2)

print(f"Dimensiones máximas de cada mosaico: {dimension_mosaico} cm x {dimension_mosaico} cm")
print(f"Número de mosaicos necesarios: {num_mosaicos}")
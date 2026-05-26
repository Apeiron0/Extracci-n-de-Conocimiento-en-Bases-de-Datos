#Luis fabrica un anuncio luminoso con focos de color rojo, amarillo y verde de tal manera que los focos rojos encienden cada 10 seg,
# los amarillos cada 6 seg y los verdes cada 15, si al probar el anuncio encienden todos los focos a la vez ¿Después de cuántos seg.
# volverán a encender juntos?

#    Rojo: c/10 seg.

#    Amarillo: c/6 seg.

#    Verde: c/15 seg.

import math

# Definimos los intervalos de tiempo en segundos para cada color de foco
foco_rojo = 10
foco_amarillo = 6
foco_verde = 15

# Calculamos el Mínimo Común Múltiplo (MCM) de los tres tiempos
tiempo_coincidencia = math.lcm(foco_rojo, foco_amarillo, foco_verde)

# Mostramos el resultado en pantalla
print(f"Los focos volverán a encender juntos después de: {tiempo_coincidencia} segundos.")
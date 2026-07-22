# ===================================================
# APRENDIZAJE POR REFUERZO - ¡El perrito que aprende!
# ¿Cómo funciona? Como cuando entrenas a un perro con premios:
# - Si hace algo bueno -> gana una galleta (RECOMPENSA)
# - Si hace algo malo -> no gana galleta (CASTIGO)
# El perrito prueba cosas (ensayo-error) y recuerda lo que le dio
# más premios para repetirlo.
# ===================================================

# 1. Importamos las herramientas necesarias
import sqlite3  # Para hablar con la base de datos SQLite
import pandas as pd  # Para manejar tablas
import random  # Para crear datos de ejemplo
import matplotlib.pyplot as plt  # Para dibujar
from sklearn.tree import DecisionTreeClassifier  # El árbol que aprenderá
from sklearn import tree  # Para dibujar el árbol
from sklearn.preprocessing import LabelEncoder  # Para convertir texto a números
import sys

# 2. CONFIGURACIÓN DE LA BASE DE DATOS
DB_FILE = 'ecbd.db'  # Nombre del archivo de base de datos SQLite


# 3. CREAR TABLA Y GENERAR EXPERIENCIAS
def crear_tabla_y_experiencias():
    conexion = sqlite3.connect(DB_FILE)
    cursor = conexion.cursor()

    # Eliminamos la tabla si ya existe para reiniciar
    cursor.execute("DROP TABLE IF EXISTS experiencias_perrito")
    print(" Tabla antigua eliminada (si existía).")

    # Creamos la tabla nueva en SQLite
    cursor.execute("""
                   CREATE TABLE experiencias_perrito
                   (
                       id           INTEGER PRIMARY KEY AUTOINCREMENT,
                       bateria      INTEGER, -- Nivel de batería del 1 al 10 (1= muy baja)
                       distancia    INTEGER, -- Distancia al dueño del 1 al 10 (1= muy cerca)
                       mejor_accion TEXT     -- 'Correr', 'Caminar' o 'Sentarse'
                   )
                   """)

    print(" Generando 50 experiencias de entrenamiento para el perrito...")
    print("   (El perrito está probando acciones y viendo cuáles le dan más premio)\n")

    # Lista de posibles acciones
    acciones = ['Correr', 'Caminar', 'Sentarse']

    # Semilla para que siempre salgan los mismos números (reproducible)
    random.seed(42)

    datos_insertar = []

    for _ in range(50):
        # El perrito se encuentra en una situación aleatoria
        bateria = random.randint(1, 10)
        distancia = random.randint(1, 10)

        # ------------------ ¡LA MAGIA DEL REFUERZO! ------------------
        # Aquí el perrito "prueba" las 3 acciones y calcula cuánto premio
        # (recompensa) obtiene con cada una.
        # La que tenga más puntos es la que debe recordar.
        # -------------------------------------------------------------

        recompensa_correr = 0
        recompensa_caminar = 0
        recompensa_sentarse = 0

        # REGLA 1: Si está LEJOS (distancia > 5)
        if distancia > 5:
            # Correr es genial si tiene batería -> +10 puntos
            if bateria >= 5:
                recompensa_correr = 10
            else:
                # Si no tiene batería, correr es malo -> -5 puntos (se queda sin pila)
                recompensa_correr = -5

            # Caminar es seguro -> +5 puntos
            recompensa_caminar = 5

            # Sentarse es muy malo si está lejos -> -10 puntos (nunca llega)
            recompensa_sentarse = -10

        # REGLA 2: Si está CERCA (distancia <= 5)
        else:
            # Correr estando cerca gasta batería tonta -> -3 puntos
            recompensa_correr = -3

            # Caminar estando cerca es perfecto -> +10 puntos
            recompensa_caminar = 10

            # Sentarse estando cerca está bien si tiene poca batería -> +5 puntos
            if bateria < 4:
                recompensa_sentarse = 5
            else:
                recompensa_sentarse = 0  # Si tiene batería, es perezoso -> 0 puntos

        # ¡El perrito elige la acción con MAYOR RECOMPENSA!
        # (Así aprende qué hacer en cada situación)
        puntuaciones = {
            'Correr': recompensa_correr,
            'Caminar': recompensa_caminar,
            'Sentarse': recompensa_sentarse
        }

        # Encontramos la acción con la puntuación más alta
        mejor_accion = max(puntuaciones, key=puntuaciones.get)

        # Guardamos esta experiencia en la lista para SQLite
        datos_insertar.append((bateria, distancia, mejor_accion))

    # Insertamos los 50 registros en la base de datos SQLite
    cursor.executemany(
        "INSERT INTO experiencias_perrito (bateria, distancia, mejor_accion) VALUES (?, ?, ?)",
        datos_insertar
    )

    conexion.commit()
    print(" 50 experiencias guardadas en la base de datos.")
    print("   (El perrito ya sabe qué hacer en 50 situaciones diferentes)\n")

    cursor.close()
    conexion.close()


# 4. CARGAR LAS EXPERIENCIAS DESDE SQLITE
def cargar_datos():
    """Lee la tabla 'experiencias_perrito' y la convierte en una tabla de pandas."""
    conexion = sqlite3.connect(DB_FILE)
    query = "SELECT bateria, distancia, mejor_accion FROM experiencias_perrito"
    df = pd.read_sql(query, conexion)
    conexion.close()
    return df


# 5. ENTRENAR EL MODELO (ÁRBOL DE DECISIÓN)
def entrenar_modelo(df):
    """
    El Árbol de Decisión aprende de las 50 experiencias.
    Así, cuando llegue una situación NUEVA, podrá predecir la mejor acción
    sin tener que probar todas otra vez.
    """
    # X = lo que el perrito observa (batería y distancia)
    X = df[['bateria', 'distancia']]
    # y = la mejor acción que descubrió el perrito
    y = df['mejor_accion']

    # Convertimos las acciones (texto) a números para que el ordenador las entienda
    # Ej: 'Correr' -> 0, 'Caminar' -> 1, 'Sentarse' -> 2
    codificador = LabelEncoder()
    y_codificado = codificador.fit_transform(y)

    # Creamos el árbol de decisión (profundidad máxima 3 para que sea fácil)
    modelo = DecisionTreeClassifier(max_depth=3, random_state=42)
    modelo.fit(X, y_codificado)  # ¡Aquí el ordenador aprende de los 50 ejemplos!

    print(" El perrito ya ha aprendido de sus 50 experiencias.")
    print("   Ahora puede predecir la mejor acción para situaciones nuevas.\n")

    return modelo, codificador


# 6. DIBUJAR EL ÁRBOL DE DECISIÓN (para que los niños lo vean)
def dibujar_arbol(modelo, codificador):
    """Muestra el árbol de decisiones que el perrito aprendió."""
    plt.figure(figsize=(12, 6))
    tree.plot_tree(modelo,
                   feature_names=['Bateria', 'Distancia'],
                   class_names=codificador.classes_.tolist(),
                   filled=True,
                   rounded=True,
                   fontsize=10)
    plt.title("Árbol de Decisión - ¿Qué debe hacer el perrito?")
    plt.show()


# 7. ¡HACER PREDICCIONES! (El perrito usa lo que aprendió)
def predecir_accion(modelo, codificador, bateria, distancia):
    """
    Dada una nueva situación (batería y distancia),
    el modelo predice la mejor acción.
    """
    # Creamos un DataFrame con los datos nuevos
    nuevo = pd.DataFrame([[bateria, distancia]], columns=['bateria', 'distancia'])

    # El modelo predice el número de la acción (0, 1 o 2)
    prediccion_codificada = modelo.predict(nuevo)[0]

    # Convertimos el número a texto ('Correr', 'Caminar' o 'Sentarse')
    accion_predicha = codificador.inverse_transform([prediccion_codificada])[0]

    # Mostramos el resultado con un mensaje bonito
    print(f"\n PREDICCIÓN para Batería={bateria}, Distancia={distancia}:")
    print(f"   El perrito dice: ¡Debo {accion_predicha}!")

    # Explicación para niños según la situación
    if accion_predicha == 'Correr':
        print("   (¡Tiene suficiente batería y está lejos! Mejor correr)")
    elif accion_predicha == 'Caminar':
        print("   (Es la opción más segura y equilibrada)")
    else:
        print("   ? (Está cerca o tiene poca batería, mejor descansar)")

    return accion_predicha


# ===================================================
# PROGRAMA PRINCIPAL (¡Aquí empieza todo!)
# ===================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print(" BIENVENIDO AL APRENDIZAJE POR REFUERZO")
    print(" (El perrito que aprende con premios y castigos)")
    print("=" * 60 + "\n")

    print("¿QUÉ ES EL APRENDIZAJE POR REFUERZO?")
    print(" - Es como cuando un perrito aprende a sentarse.")
    print(" - Si se sienta -> recibe una galleta (RECOMPENSA).")
    print(" - Si no se sienta -> no recibe galleta.")
    print(" - ¡El perrito prueba, se equivoca, y aprende a repetir lo bueno!\n")

    # Paso 1: Crear la tabla y llenar con 50 experiencias
    crear_tabla_y_experiencias()

    # Paso 2: Cargar esas experiencias
    df = cargar_datos()
    print(" Estos son los primeros 5 registros de la base de datos:")
    print(df.head())
    print("\n (Cada fila es una situación donde el perrito ya sabe qué hacer)\n")

    # Paso 3: Entrenar el modelo (el perrito aprende)
    modelo, codificador = entrenar_modelo(df)

    # Paso 4: Mostrar el árbol de decisión (opcional)
    print(" Vamos a dibujar el árbol que el perrito aprendió...")
    dibujar_arbol(modelo, codificador)

    # Paso 5: Hacer predicciones (probar al perrito)
    print("\n" + "=" * 40)
    print("   ¡AHORA EL PERRITO PREDICE!")
    print("=" * 40)

    # Ejemplo 1
    predecir_accion(modelo, codificador, bateria=8, distancia=9)

    # Ejemplo 2
    predecir_accion(modelo, codificador, bateria=2, distancia=8)

    # Ejemplo 3
    predecir_accion(modelo, codificador, bateria=5, distancia=3)

    # Ejemplo 4: Preguntar al usuario
    print("\n" + "=" * 40)
    print("   ¡AHORA PRUEBA TÚ CON EL PERRITO!")
    print("=" * 40)
    try:
        b = int(input(" Escribe la batería del perrito (1 al 10): "))
        d = int(input(" Escribe la distancia al dueño (1 al 10): "))
        predecir_accion(modelo, codificador, b, d)
    except ValueError:
        print(" (Por favor, ingresa números enteros válidos.)")
    except Exception as e:
        print(" (No te preocupes, el perrito sigue feliz aprendiendo. Error:", e, ")")

    print("\n ¡FELICIDADES! Has visto cómo funciona el aprendizaje por refuerzo:")
    print("  1. El perrito probó acciones (ensayo-error).")
    print("  2. Calculó recompensas (premios).")
    print("  3. Guardó las mejores en la base de datos.")
    print("  4. Usó un árbol de decisión para recordarlo todo.")
    print("  ¡Así es como los robots y los videojuegos aprenden solos! ")
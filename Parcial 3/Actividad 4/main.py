# =============================================================================
# MACHINE LEARNING - Clasificación de aprobados
# Aprendizaje supervisado: el ordenador aprende de ejemplos
# para predecir si un nuevo estudiante va a aprobar.
# =============================================================================


# 1. Importamos las herramientas necesarias
import sqlite3  # Para conectarnos a la base de datos SQLite
import pandas as pd  # Para manejar tablas (DataFrames)
from sklearn.tree import DecisionTreeClassifier  # El "árbol de decisiones"
from sklearn.model_selection import train_test_split  # Para separar datos
from sklearn.metrics import accuracy_score  # Para medir la precisión
from sklearn import tree  # Para dibujar el árbol

# 2. CONFIGURACIÓN DE LA BASE DE DATOS
# SQLite utiliza un archivo local en lugar de un servidor con usuario y contraseña
db_file = 'ecbd.db'  # Nombre del archivo de la base de datos local


# 3. CONEXIÓN Y CREACIÓN DE LA TABLA (si no existe)
def crear_tabla():
    """Crea la tabla 'estudiantes' con 50 registros de ejemplo."""
    conexion = sqlite3.connect(db_file)
    cursor = conexion.cursor()

    # Creamos la tabla (solo si no existe)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS estudiantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            horas_estudio INT,      -- Cuántas horas estudia al día (0-10)
            asistencia INT,         -- Porcentaje de asistencia a clase (0-100)
            aprueba BOOLEAN         -- 1 = Sí aprobó, 0 = No aprobó
        )
    """)

    # Verificamos si ya hay datos para no duplicar
    cursor.execute("SELECT COUNT(*) FROM estudiantes")
    if cursor.fetchone()[0] == 0:
        print("Insertando 50 registros de ejemplo...")
        import random
        for _ in range(50):
            horas = random.randint(0, 10)
            asis = random.randint(40, 100)
            # Regla sencilla: aprueba si estudia >= 5 horas y asiste >= 70%
            # Le añadimos un poco de "ruido" para que no sea perfecto y sea realista
            if horas >= 5 and asis >= 70:
                aprueba = 1 if random.random() < 0.9 else 0  # 90% de acierto
            else:
                aprueba = 0 if random.random() < 0.9 else 1  # 10% de excepción

            cursor.execute(
                "INSERT INTO estudiantes (horas_estudio, asistencia, aprueba) VALUES (?, ?, ?)",
                (horas, asis, aprueba)
            )
        conexion.commit()
        print("Datos insertados correctamente.")
    else:
        print("La tabla ya tiene datos, no se insertaron nuevos.")

    cursor.close()
    conexion.close()


# 4. CARGAR LOS DATOS DESDE LA BASE DE DATOS
def cargar_datos():
    """Lee la tabla 'estudiantes' y la convierte en un DataFrame de pandas."""
    conexion = sqlite3.connect(db_file)
    query = "SELECT horas_estudio, asistencia, aprueba FROM estudiantes"
    df = pd.read_sql(query, conexion)
    conexion.close()
    return df


# 5. ENTRENAR EL MODELO DE ÁRBOL DE DECISIÓN
def entrenar_modelo(df):
    """
    Separa los datos en características (X) y etiquetas (y),
    entrena un árbol de decisión y devuelve el modelo entrenado.
    """
    # X = lo que usamos para predecir (horas y asistencia)
    X = df[['horas_estudio', 'asistencia']]
    # y = lo que queremos predecir (si aprueba o no)
    y = df['aprueba']

    # Dividimos en un 80% para entrenar y 20% para probar (así vemos si aprendió bien)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Creamos el árbol de decisión (profundidad máxima 3 para que sea fácil de entender)
    modelo = DecisionTreeClassifier(max_depth=3, random_state=42)
    modelo.fit(X_train, y_train)  # ¡Aquí es donde el ordenador "aprende"!

    # Evaluamos la precisión con los datos de prueba
    predicciones = modelo.predict(X_test)
    precision = accuracy_score(y_test, predicciones)
    print(f"Precisión del modelo: {precision * 100:.2f}%")

    return modelo, X_test, y_test


# 6. MOSTRAR EL ÁRBOL DE DECISIÓN (en modo gráfico)
def mostrar_arbol(modelo, nombres_caracteristicas):
    """Imprime una representación gráfica del árbol de decisiones."""
    # Podríamos usar export_text, pero es más visual con plot_tree
    # Aquí mostramos una versión simplificada
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 6))
    tree.plot_tree(modelo, feature_names=nombres_caracteristicas,
                   class_names=['No aprueba', 'Aprueba'], filled=True)
    plt.title("Árbol de decisión - ¿Aprueba o no?")
    plt.show()


# 7. HACER PREDICCIONES PARA NUEVOS ESTUDIANTES
def predecir(modelo, horas, asistencia):
    """Predice si un estudiante con esas horas y asistencia va a aprobar."""
    # Los datos deben estar en un DataFrame con los mismos nombres de columnas
    nuevo = pd.DataFrame([[horas, asistencia]], columns=['horas_estudio', 'asistencia'])
    resultado = modelo.predict(nuevo)[0]  # 1 o 0
    prob = modelo.predict_proba(nuevo)[0]  # [prob_no, prob_si]

    print(f"\nPREDICCIÓN para horas={horas}, asistencia={asistencia}%:")
    if resultado == 1:
        print(f"    ¡APRUEBA! (probabilidad: {prob[1] * 100:.1f}%)")
    else:
        print(f"    No aprueba (probabilidad: {prob[0] * 100:.1f}%)")
    return resultado


# =============================================================================
# PROGRAMA PRINCIPAL (todo se ejecuta en orden)
# =============================================================================
if __name__ == "__main__":
    print(" BIENVENIDO AL EJEMPLO DE MACHINE LEARNING ")
    print(" Aprendaremos a predecir si un estudiante aprueba o no.\n")

    # Paso 1: Crear la base de datos y los 50 registros
    crear_tabla()

    # Paso 2: Cargar los datos desde MySQL
    df = cargar_datos()
    print(f"Datos cargados: {len(df)} registros.")
    print(" Primeros 5 registros:")
    print(df.head())

    # Paso 3: Entrenar el modelo
    modelo, X_test, y_test = entrenar_modelo(df)

    # Paso 4: Mostrar el árbol de decisión (gráfico)
    mostrar_arbol(modelo, ['Horas estudio', 'Asistencia'])

    # Paso 5: Hacer una predicción de ejemplo
    # Preguntamos al usuario (opcional)
    try:
        h = int(input("\nIntroduce horas de estudio (0-10): "))
        a = int(input(" Introduce asistencia (0-100): "))
        predecir(modelo, h, a)
    except:
        print("\nVamos a probar con un estudiante que estudia 6 horas y asiste al 80%:")
        predecir(modelo, 6, 80)

    print("\n¡Ya sabes cómo funciona el aprendizaje supervisado!")
    print(" El ordenador aprendió de los 50 ejemplos para predecir nuevos casos.")
"""
Programa: Generador de Excel desde SQL
Descripción: Lee calificaciones de una tabla SQL (10 alumnos, 7 materias, 50 registros)
             y las exporta a un archivo Excel con formato.
"""

import pandas as pd
import sqlite3
import random

# ------------------------------------------------------------
# CONFIGURACIÓN DE LA BASE DE DATOS
# ------------------------------------------------------------
DB_NAME = "ecbd.db"

# ------------------------------------------------------------
# FUNCIÓN PARA CREAR TABLA E INSERTAR DATOS DE PRUEBA
# ------------------------------------------------------------
def crear_tabla_y_datos():
    """
    Conecta a SQL, crea la tabla 'calificaciones' si no existe
    e inserta 50 registros aleatorios con 10 alumnos y 7 materias.
    """

    try:
        # Establecer conexión
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()

        # Crear la tabla si no existe
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS calificaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alumno VARCHAR(50) NOT NULL,
                materia VARCHAR(50) NOT NULL,
                puntaje DECIMAL(5,2) NOT NULL
            )
        """)

        print("Tabla 'calificaciones' verificada/creada.")

        # Vaciar la tabla para evitar duplicados (opcional)
        cursor.execute("DELETE FROM calificaciones")

        # Reiniciar el AUTOINCREMENT (opcional)
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='calificaciones'")

        # Listas de alumnos y materias
        alumnos = ['Luis', 'Andrea', 'Miguel', 'Samir', 'Valeria',
                   'Carlos', 'María', 'José', 'Ana', 'Fernanda']

        materias = ['Matemáticas', 'Física', 'Química', 'Biología',
                    'Historia', 'Lengua', 'Inglés']

        # Generar 50 registros aleatorios
        registros = []

        for _ in range(50):
            alumno = random.choice(alumnos)
            materia = random.choice(materias)
            puntaje = round(random.uniform(50, 100), 2)
            registros.append((alumno, materia, puntaje))

        # Insertar todos los registros
        cursor.executemany(
            "INSERT INTO calificaciones (alumno, materia, puntaje) VALUES (?, ?, ?)",
            registros
        )

        conexion.commit()

        print(f"Se insertaron {cursor.rowcount} registros de prueba.")

    except sqlite3.Error as e:
        print(f"Error en la base de datos: {e}")

    finally:
        cursor.close()
        conexion.close()
        print("Conexión a SQLite cerrada.")


# ------------------------------------------------------------
# FUNCIÓN PRINCIPAL: EXPORTAR A EXCEL
# ------------------------------------------------------------
def exportar_a_excel():
    """
    Lee los datos de la tabla 'calificaciones' y genera un archivo Excel
    con dos hojas: 'Datos_originales' y 'Resumen_por_alumno'.
    """

    try:
        # Conectar a SQL
        conexion = sqlite3.connect(DB_NAME)

        # Leer la tabla completa con pandas
        query = "SELECT alumno, materia, puntaje FROM calificaciones"
        df = pd.read_sql(query, conexion)

        if df.empty:
            print("No hay datos en la tabla. Ejecuta primero 'crear_tabla_y_datos()'.")
            return

        # Mostrar información básica
        print("\n--- Datos leídos ---")
        print(f"Total de registros: {len(df)}")
        print(f"Alumnos únicos: {df['alumno'].nunique()}")
        print(f"Materias únicas: {df['materia'].nunique()}")
        print(df.head())

        # Crear resumen
        resumen = df.groupby('alumno')['puntaje'].agg(['mean', 'min', 'max']).round(2)
        resumen.columns = ['Promedio', 'Mínimo', 'Máximo']

        # Guardar en Excel
        archivo_excel = "Puntajes_escuela.xlsx"

        with pd.ExcelWriter(archivo_excel, engine="openpyxl") as writer:
            df.to_excel(writer,
                        sheet_name="Datos_originales",
                        index=False)

            resumen.to_excel(writer,
                             sheet_name="Resumen_por_alumno")

        print(f"\n¡Archivo Excel generado exitosamente! -> {archivo_excel}")

    except sqlite3.Error as e:
        print(f"Error al conectar o leer SQLite: {e}")

    except Exception as e:
        print(f"Error inesperado: {e}")

    finally:
        conexion.close()
        print("Conexión a SQLite cerrada.")


# ------------------------------------------------------------
# BLOQUE PRINCIPAL DE EJECUCIÓN
# ------------------------------------------------------------
if __name__ == "__main__":

    print("=== GENERADOR DE EXCEL DESDE SQL ===\n")

    # Paso 1: Crear tabla y cargar datos de prueba
    crear_tabla_y_datos()

    # Paso 2: Exportar a Excel
    exportar_a_excel()

    print("\nPrograma finalizado.")
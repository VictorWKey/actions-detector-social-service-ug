"""
Código utilizado para la detección de saltos bruscos entre frame y frame,
preguntando al usuario si se desean eliminar dichos renglones detectados
"""

import pandas as pd

def detectar_diferencias(csv_file):
    # Leer el archivo CSV
    df = pd.read_csv(csv_file)

    # Verificar que el archivo tenga 99 columnas
    if df.shape[1] != 99:
        print("El archivo CSV no tiene el formato esperado. Debe tener 99 columnas.")
        return

    # Diccionario para almacenar los resultados
    diferencias_mayores = {}

    # Iterar sobre cada columna del DataFrame
    for col in df.columns:
        # Calcular la diferencia entre cada valor y el anterior
        diffs = df[col].diff()

        # Identificar los índices donde la diferencia es mayor a 84
        indices_diferencias = diffs[diffs.abs() > 84].index

        # Guardar los renglones donde ocurre la diferencia para esta columna
        if not indices_diferencias.empty:
            diferencias_mayores[col] = indices_diferencias.tolist()

    # Mostrar los resultados y preguntar si se desean eliminar las filas
    if diferencias_mayores:
        filas_a_eliminar = set()
        for col, filas in diferencias_mayores.items():
            print(f"Diferencias mayores en columna '{col}' en los renglones: {filas}")
            filas_a_eliminar.update(filas)

        # Preguntar al usuario si desea eliminar las filas identificadas
        respuesta = input("¿Deseas eliminar estas filas del archivo CSV? (s/n): ").strip().lower()
        if respuesta == 's':
            # Eliminar las filas y guardar el resultado
            df.drop(filas_a_eliminar, inplace=True)
            df.to_csv(csv_file, index=False)
            print("Filas eliminadas y archivo CSV actualizado.")
        else:
            print("No se realizaron cambios en el archivo CSV.")
    else:
        print("No se encontraron diferencias mayores en ninguna columna.")

# Llamar a la función con el archivo CSV de entrada
csv_file = r"cleanData/levantar_caja_abajo_Clean2/levantar_caja_abajo_05.csv" 
detectar_diferencias(csv_file)
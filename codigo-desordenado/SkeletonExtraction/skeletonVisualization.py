"""
Código utilizado para la visualización de cada uno de los frames,
aquí se contiene el diccionario de los joints así cómo las correctas
uniones entre ellos
"""

import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def plot_skeleton_3d(csv_file):
    # Diccionario con los nombres de los joints en español según MediaPipe Pose
    joint_names = {
        0: "Nariz", 1: "Ojo Izquierdo Interno", 2: "Ojo Izquierdo", 3: "Ojo Izquierdo Externo",
        4: "Ojo Derecho Interno", 5: "Ojo Derecho", 6: "Ojo Derecho Externo",
        7: "Oreja Izquierda", 8: "Oreja Derecha", 9: "Boca Izquierda", 10: "Boca Derecha",
        11: "Hombro Izquierdo", 12: "Hombro Derecho", 13: "Codo Izquierdo",
        14: "Codo Derecho", 15: "Muñeca Izquierda", 16: "Muñeca Derecha",
        17: "Meñique Izquierdo", 18: "Meñique Derecho", 19: "Índice Izquierdo", 20: "Índice Derecho",
        21: "Pulgar Izquierdo", 22: "Pulgar Derecho", 23: "Cadera Izquierda", 24: "Cadera Derecha",
        25: "Rodilla Izquierda", 26: "Rodilla Derecha", 27: "Tobillo Izquierdo", 28: "Tobillo Derecho",
        29: "Talón Izquierdo", 30: "Talón Derecho", 31: "Dedo del Pie Izquierdo", 32: "Dedo del Pie Derecho"
    }

    # Leer el archivo CSV sin cabeceras, cada fila representa un joint y las columnas son x, y, z
    df = pd.read_csv(csv_file, header=None)

    # Verificar que el archivo tenga 33 filas y 3 columnas
    if df.shape[0] != 33 or df.shape[1] != 3:
        print(f"El archivo CSV no tiene el formato esperado. Debe tener 33 filas y 3 columnas.")
        return

    # Lista para almacenar las coordenadas (x, y, z) de los joints
    joints = []

    # Recorremos las filas (cada fila es un joint con x, y, z)
    for i in range(33):  # 33 joints
        x, y, z = df.iloc[i, 0], df.iloc[i, 1], df.iloc[i, 2]
        joints.append((x, y, z))

    # Convertimos la lista de joints a un array de numpy para acceso fácil
    joints = np.array(joints)

    # Crear la figura para la gráfica 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Graficar los puntos de las juntas
    ax.scatter(joints[:, 0], joints[:, 1], joints[:, 2], c='r', marker='o')

    # Mostrar el nombre de cada joint en el gráfico
    for i, (x, y, z) in enumerate(joints):
        ax.text(x, y, z, joint_names[i], color='black', fontsize=8)

    # Conexiones anatómicas del esqueleto para MediaPipe Pose (ajusta según sea necesario)
    pose_connections = [
        [23, 11], [11, 13], [12, 14],
        [16, 22], [18, 20], [20, 22], [16, 22],
        [15, 21], [15, 17], [17, 19], [19, 21],
        [11, 12], [12, 24], [13, 15],     
        [14, 16], [16, 18], [25, 23],          
        [23, 24], [24, 26], [27, 25],        
        [26, 28], [28, 30], [28, 32],      
        [27, 31], [29, 31], [32, 30], [29, 27]       
    ]

    # Dibujar las conexiones entre los puntos (líneas entre joints)
    for connection in pose_connections:
        joint1 = joints[connection[0]]
        joint2 = joints[connection[1]]
        ax.plot([joint1[0], joint2[0]], [joint1[1], joint2[1]], [joint1[2], joint2[2]], c='b')

    # Ajustar los límites del gráfico para mejor visualización
    ax.set_xlim([np.min(joints[:, 0]), np.max(joints[:, 0])])
    ax.set_ylim([np.min(joints[:, 1]), np.max(joints[:, 1])])
    ax.set_zlim([np.min(joints[:, 2]), np.max(joints[:, 2])])

    # Etiquetas de los ejes
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Mostrar la gráfica
    plt.show()

# Llamada a la función con el archivo CSV de entrada
csv_file = r'data\saludo\2024_11_06_12_25_02\xyz\capture_1.csv' 
plot_skeleton_3d(csv_file)
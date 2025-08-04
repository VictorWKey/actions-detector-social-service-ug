"""
Código utilizado para verificar que la espina calculada por
cada frame está situada correctamente
"""
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

def plot_skeleton_animation(csv_file):
    # Leer el archivo CSV con encabezado
    df = pd.read_csv(csv_file)

    # Verificar que el archivo tenga al menos 102 columnas
    if df.shape[1] < 102:
        print("El archivo CSV no tiene el formato esperado. Debe tener al menos 102 columnas.")
        return

    # Separar las coordenadas de los joints y la espina
    joint_coords = df.iloc[:, :-3]  # Todas las columnas excepto las últimas 3
    espina_coords = df.iloc[:, -3:]  # Últimas 3 columnas

    # Calcular los límites de los ejes para toda la animación
    x_min, x_max = joint_coords.iloc[:, 0::3].min().min(), joint_coords.iloc[:, 0::3].max().max()
    y_min, y_max = joint_coords.iloc[:, 1::3].min().min(), joint_coords.iloc[:, 1::3].max().max()
    z_min, z_max = joint_coords.iloc[:, 2::3].min().min(), joint_coords.iloc[:, 2::3].max().max()

    # Crear la figura para la gráfica 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Configurar etiquetas de los ejes
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Conexiones anatómicas del esqueleto para MediaPipe Pose
    pose_connections = [
        [23, 11], [11, 13], [12, 14], [16, 22], [18, 20],
        [20, 22], [16, 22], [15, 21], [15, 17], [17, 19],
        [19, 21], [11, 12], [12, 24], [13, 15], [14, 16],
        [16, 18], [25, 23], [23, 24], [24, 26], [27, 25],
        [26, 28], [28, 30], [28, 32], [27, 31], [29, 31],
        [32, 30], [29, 27]
    ]

    # Función para actualizar el gráfico en cada cuadro de la animación
    def update(frame):
        ax.clear()  # Limpiar el gráfico anterior

        # Configurar los límites del gráfico para cada cuadro según el rango calculado
        ax.set_xlim([x_min, x_max])
        ax.set_ylim([y_min, y_max])
        ax.set_zlim([z_min, z_max])

        # Etiquetas de los ejes
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        # Mantener la vista inicial en cada cuadro
        ax.view_init(elev=90, azim=90)
        ax.set_xlim(ax.get_xlim()[::-1])  # Invierte el eje X

        # Obtener las coordenadas de los joints
        joints = []
        for i in range(0, joint_coords.shape[1], 3):
            x, y, z = joint_coords.iloc[frame, i], joint_coords.iloc[frame, i+1], joint_coords.iloc[frame, i+2]
            joints.append((x, y, z))

        # Agregar la espina al final
        espina = espina_coords.iloc[frame].values
        joints.append((espina[0], espina[1], espina[2]))

        # Convertimos a un array de numpy para facilitar el acceso
        joints = np.array(joints)

        # Graficar los puntos de las juntas
        ax.scatter(joints[:, 0], joints[:, 1], joints[:, 2], c='r', marker='o')

        # Dibujar las conexiones entre los puntos (líneas entre joints)
        for connection in pose_connections:
            joint1 = joints[connection[0]]
            joint2 = joints[connection[1]]
            ax.plot([joint1[0], joint2[0]], [joint1[1], joint2[1]], [joint1[2], joint2[2]], c='k')  # Línea negra

        # Agregar el número de línea actual en el gráfico
        ax.text2D(0.05, 0.95, f"Línea {frame + 1}", transform=ax.transAxes, fontsize=12, color='blue')

    # Crear la animación, recorriendo todas las filas del DataFrame
    ani = FuncAnimation(fig, update, frames=len(df), interval=80)  # ajustar el interval según se requiera

    # Mostrar la animación
    plt.show()

# Llamar a la función con la ruta del archivo CSV
csv_file = r"dataComplete\circulo\circulo_80.csv"
plot_skeleton_animation(csv_file)
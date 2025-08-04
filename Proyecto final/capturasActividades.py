import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_and_save_selected_frames(csv_file, output_folder):
    # Crear la carpeta de salida si no existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

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

    # Conexiones anatómicas del esqueleto para MediaPipe Pose
    pose_connections = [
        [23, 11], [11, 13], [12, 14], [16, 22], [18, 20],
        [20, 22], [16, 22], [15, 21], [15, 17], [17, 19],
        [19, 21], [11, 12], [12, 24], [13, 15], [14, 16],
        [16, 18], [25, 23], [23, 24], [24, 26], [27, 25],
        [26, 28], [28, 30], [28, 32], [27, 31], [29, 31],
        [32, 30], [29, 27]
    ]

    # Frames seleccionados (número de línea en el archivo CSV sin incluir la cabecera)
    selected_frames = [1, 20, 40, 60, 80, 100]

    # Iterar sobre los frames seleccionados
    for frame_number in selected_frames:
        frame_idx = frame_number - 1  # Convertir a índice de base 0
        if frame_idx >= len(df):
            print(f"Frame {frame_number} no existe en el archivo.")
            continue

        # Crear figura
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Configurar límites y etiquetas de los ejes
        ax.set_xlim([x_min, x_max])
        ax.set_ylim([y_min, y_max])
        ax.set_zlim([z_min, z_max])
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        # Mantener vista inicial
        ax.view_init(elev=90, azim=90)
        ax.set_xlim(ax.get_xlim()[::-1])  # Invertir eje X

        # Obtener coordenadas de los joints
        joints = []
        for i in range(0, joint_coords.shape[1], 3):
            x, y, z = joint_coords.iloc[frame_idx, i], joint_coords.iloc[frame_idx, i+1], joint_coords.iloc[frame_idx, i+2]
            joints.append((x, y, z))

        # Agregar espina
        espina = espina_coords.iloc[frame_idx].values
        joints.append((espina[0], espina[1], espina[2]))

        # Convertimos a un array de numpy para facilitar el acceso
        joints = np.array(joints)

        # Graficar los puntos de las juntas
        ax.scatter(joints[:, 0], joints[:, 1], joints[:, 2], c='r', marker='o')

        # Dibujar conexiones entre puntos
        for connection in pose_connections:
            joint1 = joints[connection[0]]
            joint2 = joints[connection[1]]
            ax.plot([joint1[0], joint2[0]], [joint1[1], joint2[1]], [joint1[2], joint2[2]], c='k')  # Línea negra

        # Guardar imagen
        output_path = f"{output_folder}/frame_{frame_number}.png"
        plt.savefig(output_path)
        plt.close(fig)
        print(f"Frame {frame_number} guardado como {output_path}.")

# Ruta del archivo CSV y carpeta de salida
csv_file = r"data/mesa_caja/mesa_caja_80.csv"
output_folder = "mesa_caja"

# Llamar a la función
plot_and_save_selected_frames(csv_file, output_folder)
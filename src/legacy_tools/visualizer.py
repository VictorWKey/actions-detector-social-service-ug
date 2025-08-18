"""
Herramientas de visualización para esqueletos y animaciones
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from ..utils.joint_utils import JOINT_NAMES, POSE_CONNECTIONS

class SkeletonVisualizer:
    def __init__(self):
        """Inicializa el visualizador de esqueletos"""
        pass
    
    def plot_skeleton_3d(self, csv_file, show_labels=True):
        """
        Visualiza un frame individual del esqueleto en 3D
        Equivalente a skeletonVisualization.py
        
        Args:
            csv_file: Ruta del archivo CSV con coordenadas
            show_labels: Si mostrar los nombres de los joints
        """
        print(f"Visualizando esqueleto: {csv_file}")
        
        try:
            # Leer el archivo CSV
            df = pd.read_csv(csv_file, header=None)
            
            # Verificar formato (33 filas, 3 columnas)
            if df.shape[0] != 33 or df.shape[1] != 3:
                print(f"Formato incorrecto. Esperado: 33x3, Actual: {df.shape[0]}x{df.shape[1]}")
                return
            
            # Extraer coordenadas
            joints = []
            for i in range(33):
                x, y, z = df.iloc[i, 0], df.iloc[i, 1], df.iloc[i, 2]
                joints.append((x, y, z))
            
            joints = np.array(joints)
            
            # Crear figura 3D
            fig = plt.figure(figsize=(10, 8))
            ax = fig.add_subplot(111, projection='3d')
            
            # Graficar puntos de joints
            ax.scatter(joints[:, 0], joints[:, 1], joints[:, 2], c='red', marker='o', s=50)
            
            # Mostrar nombres de joints si se solicita
            if show_labels:
                for i, (x, y, z) in enumerate(joints):
                    ax.text(x, y, z, JOINT_NAMES[i], fontsize=6, color='black')
            
            # Dibujar conexiones
            for connection in POSE_CONNECTIONS:
                if connection[0] < len(joints) and connection[1] < len(joints):
                    joint1 = joints[connection[0]]
                    joint2 = joints[connection[1]]
                    ax.plot([joint1[0], joint2[0]], 
                           [joint1[1], joint2[1]], 
                           [joint1[2], joint2[2]], 'b-', linewidth=2)
            
            # Configurar ejes
            ax.set_xlim([np.min(joints[:, 0]), np.max(joints[:, 0])])
            ax.set_ylim([np.min(joints[:, 1]), np.max(joints[:, 1])])
            ax.set_zlim([np.min(joints[:, 2]), np.max(joints[:, 2])])
            
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            ax.set_title(f'Esqueleto 3D - {csv_file}')
            
            plt.show()
            
        except Exception as e:
            print(f"Error al visualizar esqueleto: {e}")
    
    def plot_skeleton_animation(self, csv_file, interval=80, with_spine=False):
        """
        Crea una animación del esqueleto completo
        Equivalente a animationSkeleton.py
        
        Args:
            csv_file: Ruta del archivo CSV con múltiples frames
            interval: Intervalo entre frames en milisegundos
            with_spine: Si incluir visualización de la espina
        """
        print(f"Creando animación: {csv_file}")
        
        try:
            # Leer archivo CSV
            df = pd.read_csv(csv_file)
            
            # Determinar formato (99 columnas para joints normales, 102 con espina)
            expected_cols = 102 if with_spine else 99
            if df.shape[1] < expected_cols:
                print(f"Formato incorrecto. Esperado al menos {expected_cols} columnas, actual: {df.shape[1]}")
                return
            
            # Separar coordenadas de joints y espina
            if with_spine:
                joint_coords = df.iloc[:, :-3]  # Todas excepto las últimas 3
                espina_coords = df.iloc[:, -3:]  # Últimas 3 columnas
            else:
                joint_coords = df.iloc[:, :99]  # Primeras 99 columnas
                espina_coords = None
            
            # Calcular límites para toda la animación
            x_min = joint_coords.iloc[:, 0::3].min().min()
            x_max = joint_coords.iloc[:, 0::3].max().max()
            y_min = joint_coords.iloc[:, 1::3].min().min()
            y_max = joint_coords.iloc[:, 1::3].max().max()
            z_min = joint_coords.iloc[:, 2::3].min().min()
            z_max = joint_coords.iloc[:, 2::3].max().max()
            
            # Crear figura
            fig = plt.figure(figsize=(12, 9))
            ax = fig.add_subplot(111, projection='3d')
            
            def update(frame):
                ax.clear()
                
                # Configurar límites y vista
                ax.set_xlim([x_min, x_max])
                ax.set_ylim([y_min, y_max])
                ax.set_zlim([z_min, z_max])
                ax.set_xlabel('X')
                ax.set_ylabel('Y')
                ax.set_zlabel('Z')
                ax.view_init(elev=90, azim=90)
                ax.set_xlim(ax.get_xlim()[::-1])  # Invertir eje X
                
                # Extraer coordenadas de joints para este frame
                joints = []
                for i in range(0, joint_coords.shape[1], 3):
                    x = joint_coords.iloc[frame, i]
                    y = joint_coords.iloc[frame, i+1] 
                    z = joint_coords.iloc[frame, i+2]
                    joints.append((x, y, z))
                
                # Agregar espina si está disponible
                if with_spine and espina_coords is not None:
                    espina = espina_coords.iloc[frame].values
                    joints.append((espina[0], espina[1], espina[2]))
                
                joints = np.array(joints)
                
                # Graficar puntos
                ax.scatter(joints[:, 0], joints[:, 1], joints[:, 2], 
                          c='red', marker='o', s=50)
                
                # Dibujar conexiones
                for connection in POSE_CONNECTIONS:
                    if (connection[0] < len(joints) and 
                        connection[1] < len(joints)):
                        joint1 = joints[connection[0]]
                        joint2 = joints[connection[1]]
                        ax.plot([joint1[0], joint2[0]], 
                               [joint1[1], joint2[1]], 
                               [joint1[2], joint2[2]], 'black', linewidth=2)
                
                # Mostrar número de frame
                ax.text2D(0.05, 0.95, f"Frame {frame + 1}/{len(df)}", 
                         transform=ax.transAxes, fontsize=12, color='blue')
                
                # Resaltar espina si está incluida
                if with_spine and len(joints) > 33:
                    ax.scatter(joints[-1, 0], joints[-1, 1], joints[-1, 2], 
                              c='green', marker='*', s=100, label='Espina')
            
            # Crear animación
            ani = FuncAnimation(fig, update, frames=len(df), interval=interval, repeat=True)
            
            plt.title(f'Animación de Esqueleto - {csv_file}')
            plt.show()
            
            return ani
            
        except Exception as e:
            print(f"Error al crear animación: {e}")
            return None
    
    def save_animation(self, csv_file, output_path, **kwargs):
        """
        Guarda la animación como archivo de video
        
        Args:
            csv_file: Archivo CSV con los datos
            output_path: Ruta donde guardar el video
            **kwargs: Argumentos adicionales para plot_skeleton_animation
        """
        try:
            ani = self.plot_skeleton_animation(csv_file, **kwargs)
            if ani:
                ani.save(output_path, writer='pillow', fps=10)
                print(f"Animación guardada en: {output_path}")
                return True
        except Exception as e:
            print(f"Error al guardar animación: {e}")
        return False

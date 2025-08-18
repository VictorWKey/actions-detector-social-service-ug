"""
Diccionario y utilidades para el manejo de joints
"""

# Diccionario con los nombres de los joints según MediaPipe Pose
JOINT_NAMES = {
    0: "Nariz", 
    1: "Ojo Izquierdo Interno", 
    2: "Ojo Izquierdo", 
    3: "Ojo Izquierdo Externo",
    4: "Ojo Derecho Interno", 
    5: "Ojo Derecho", 
    6: "Ojo Derecho Externo",
    7: "Oreja Izquierda", 
    8: "Oreja Derecha", 
    9: "Boca Izquierda", 
    10: "Boca Derecha",
    11: "Hombro Izquierdo", 
    12: "Hombro Derecho", 
    13: "Codo Izquierdo",
    14: "Codo Derecho", 
    15: "Muñeca Izquierda", 
    16: "Muñeca Derecha",
    17: "Meñique Izquierdo", 
    18: "Meñique Derecho", 
    19: "Índice Izquierdo", 
    20: "Índice Derecho",
    21: "Pulgar Izquierdo", 
    22: "Pulgar Derecho", 
    23: "Cadera Izquierda", 
    24: "Cadera Derecha",
    25: "Rodilla Izquierda", 
    26: "Rodilla Derecha", 
    27: "Tobillo Izquierdo", 
    28: "Tobillo Derecho",
    29: "Talón Izquierdo", 
    30: "Talón Derecho", 
    31: "Dedo del Pie Izquierdo", 
    32: "Dedo del Pie Derecho"
}

# Conexiones anatómicas del esqueleto para visualización
POSE_CONNECTIONS = [
    [23, 11], [11, 13], [12, 14], [16, 22], [18, 20],
    [20, 22], [16, 22], [15, 21], [15, 17], [17, 19],
    [19, 21], [11, 12], [12, 24], [13, 15], [14, 16],
    [16, 18], [25, 23], [23, 24], [24, 26], [27, 25],
    [26, 28], [28, 30], [28, 32], [27, 31], [29, 31],
    [32, 30], [29, 27]
]

# Joints utilizados para calcular la espina (centroide)
SPINE_JOINTS = {
    11: "Hombro Izquierdo",
    12: "Hombro Derecho", 
    23: "Cadera Izquierda",
    24: "Cadera Derecha"
}

# Joints utilizados para extraer características (distancias y velocidades)
TARGET_JOINTS = {
    13: "Codo Izquierdo",
    14: "Codo Derecho",
    15: "Muñeca Izquierda",
    16: "Muñeca Derecha",
    25: "Rodilla Izquierda",
    26: "Rodilla Derecha",
    29: "Talón Izquierdo",
    30: "Talón Derecho"
}

def get_joint_name(joint_id):
    """
    Obtiene el nombre de un joint por su ID
    
    Args:
        joint_id: ID del joint (0-32)
        
    Returns:
        Nombre del joint en español
    """
    return JOINT_NAMES.get(joint_id, f"Joint_{joint_id}")

def get_spine_joint_ids():
    """
    Obtiene los IDs de los joints usados para calcular la espina
    
    Returns:
        Lista con los IDs de los joints de la espina
    """
    return list(SPINE_JOINTS.keys())

def get_target_joint_ids():
    """
    Obtiene los IDs de los joints usados para extraer características
    
    Returns:
        Lista con los IDs de los joints objetivo
    """
    return list(TARGET_JOINTS.keys())

def create_column_names():
    """
    Crea los nombres de columnas para un DataFrame de coordenadas
    
    Returns:
        Lista con nombres de columnas (joint0_x, joint0_y, joint0_z, ...)
    """
    columns = []
    for i in range(33):
        columns.extend([f'joint{i}_x', f'joint{i}_y', f'joint{i}_z'])
    return columns

"""
Módulo de captura de datos con cámaras RealSense y detección de poses
"""

from .pose_detector import PoseDetector
from .realsense_capture import RealSenseCapture

__all__ = ['PoseDetector', 'RealSenseCapture']

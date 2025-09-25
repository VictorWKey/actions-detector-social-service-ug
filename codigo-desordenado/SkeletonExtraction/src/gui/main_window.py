"""
Main application window
"""

import sys
import os
from PyQt5.QtWidgets import QMainWindow, QTabWidget, QWidget, QLabel
from PyQt5.QtCore import Qt

# Add the gui directory to path for relative imports
sys.path.insert(0, os.path.dirname(__file__))
from development.dev_interface import DevInterface


class ProductionInterface(QWidget):
    """Empty production interface placeholder"""
    def __init__(self):
        super().__init__()
        layout = QLabel("Interfaz de Producción\n(Próximamente)")
        layout.setAlignment(Qt.AlignCenter)
        layout.setStyleSheet("font-size: 18px; color: gray;")
        
        from PyQt5.QtWidgets import QVBoxLayout
        main_layout = QVBoxLayout()
        main_layout.addWidget(layout)
        self.setLayout(main_layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the main window"""
        self.setWindowTitle("Sistema de Reconocimiento de Acciones")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create tab widget
        tab_widget = QTabWidget()
        
        # Add development interface tab
        dev_tab = DevInterface()
        tab_widget.addTab(dev_tab, "Desarrollo")
        
        # Add production interface tab (empty for now)
        prod_tab = ProductionInterface()
        tab_widget.addTab(prod_tab, "Producción")
        
        # Set as central widget
        self.setCentralWidget(tab_widget)
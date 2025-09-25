#!/usr/bin/env python3
"""
Main entry point for the Action Recognition System
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    
    # Create and show main window
    main_window = MainWindow()
    main_window.show()
    
    # Start the application event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
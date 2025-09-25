#!/usr/bin/env python3
"""
Simple test app to verify camera integration with PyQt
"""

import sys
import os

# Add src to path
sys.path.insert(0, 'src')

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
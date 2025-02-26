#!/usr/bin/env python3
import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from IATEST.Admin import AdminPanel
from PyQt5.QtWidgets import QApplication

def main():
    try:
        # Create Qt application
        app = QApplication(sys.argv)
        
        # Create and show admin panel
        window = AdminPanel()
        window.show()
        
        # Enter Qt application main loop
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
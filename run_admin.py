#!/usr/bin/env python3
import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def run_admin():
    try:
        from PyQt5.QtWidgets import QApplication
        from IATEST.Admin.AdminProgram import AdminPanel, main
        
        print("Starting admin panel directly...")
        return main()
        
    except ImportError as e:
        print(f"Import error: {str(e)}")
        print("Trying alternative import method...")
        
        try:
            # Try direct import
            import IATEST.Admin.AdminProgram as admin_program
            
            app = QApplication(sys.argv)
            window = admin_program.AdminPanel()
            window.show()
            print("Admin panel displayed using direct import")
            return app.exec_()
            
        except Exception as e:
            print(f"Error starting admin panel: {str(e)}")
            import traceback
            traceback.print_exc()
            return 1

if __name__ == "__main__":
    sys.exit(run_admin())
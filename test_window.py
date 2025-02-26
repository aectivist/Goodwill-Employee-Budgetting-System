#!/usr/bin/env python3
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor
import sys

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Test Window")
        self.setMinimumSize(800, 600)
        
        # Set up window theme
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#0053A0"))
        palette.setColor(QPalette.WindowText, QColor("#FFFFFF"))
        self.setPalette(palette)
        
        # Create central widget and layout
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # Add test label
        label = QLabel("Test Window")
        label.setFont(QFont("Arial", 24))
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: white;")
        layout.addWidget(label)

def main():
    try:
        print("Starting test window...")
        app = QApplication(sys.argv)
        window = TestWindow()
        window.show()
        print("Window displayed")
        return app.exec_()
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
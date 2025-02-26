#!/usr/bin/env python3
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                           QLabel)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPalette
import sys

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Window")
        self.setMinimumSize(800, 600)
        
        # Set Goodwill theme
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#0053A0"))
        palette.setColor(QPalette.WindowText, QColor("#FFFFFF"))
        self.setPalette(palette)
        
        # Set up the main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Add a test label
        label = QLabel("Test Window")
        label.setFont(QFont("Arial", 24))
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: white;")
        layout.addWidget(label)

def main():
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
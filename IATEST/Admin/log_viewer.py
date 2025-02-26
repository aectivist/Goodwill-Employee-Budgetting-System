#!/usr/bin/env python3
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                           QTextEdit, QComboBox, QLabel, QFileDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import os
from datetime import datetime

class LogViewer(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.load_log_files()

    def setup_ui(self):
        """Set up the UI components"""
        self.setWindowTitle("Database Log Viewer")
        self.setMinimumSize(800, 600)
        
        # Create layout
        layout = QVBoxLayout(self)
        
        # Controls
        controls = QHBoxLayout()
        
        # Date selector
        self.date_selector = QComboBox()
        self.date_selector.currentIndexChanged.connect(self.load_selected_log)
        controls.addWidget(QLabel("Select Date:"))
        controls.addWidget(self.date_selector)
        
        # Refresh button
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.load_log_files)
        controls.addWidget(refresh_btn)
        
        # Export button
        export_btn = QPushButton("Export")
        export_btn.clicked.connect(self.export_logs)
        controls.addWidget(export_btn)
        
        # Clear button
        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.clear_display)
        controls.addWidget(clear_btn)
        
        layout.addLayout(controls)
        
        # Log display
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setFont(QFont("Courier", 10))
        layout.addWidget(self.log_display)
        
        # Status bar
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

        # Apply styles
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QPushButton {
                padding: 5px 15px;
                background-color: #0053A0;
                color: white;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #003d75;
            }
            QComboBox {
                padding: 5px;
                border: 1px solid #0053A0;
                border-radius: 3px;
                min-width: 150px;
            }
            QTextEdit {
                border: 1px solid #0053A0;
                border-radius: 3px;
                padding: 5px;
            }
        """)

    def load_log_files(self):
        """Load available log files into the date selector"""
        self.date_selector.clear()
        
        # Get logs directory
        logs_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            'logs'
        )
        
        if not os.path.exists(logs_dir):
            self.status_label.setText("No logs directory found")
            return
            
        # Find log files
        log_files = []
        for file in os.listdir(logs_dir):
            if file.startswith('database_') and file.endswith('.log'):
                date_str = file[9:-4]  # Extract date from filename
                try:
                    date = datetime.strptime(date_str, "%Y%m%d")
                    log_files.append((date, file))
                except ValueError:
                    continue
                    
        # Sort by date descending
        log_files.sort(reverse=True)
        
        # Add to selector
        for date, file in log_files:
            self.date_selector.addItem(
                date.strftime("%Y-%m-%d"),
                os.path.join(logs_dir, file)
            )
            
        if log_files:
            self.load_selected_log()
            self.status_label.setText(f"Found {len(log_files)} log files")
        else:
            self.status_label.setText("No log files found")

    def load_selected_log(self):
        """Load the currently selected log file"""
        file_path = self.date_selector.currentData()
        if not file_path:
            return
            
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                self.log_display.setText(content)
                self.status_label.setText(f"Loaded log file: {os.path.basename(file_path)}")
        except Exception as e:
            self.status_label.setText(f"Error loading log: {str(e)}")

    def export_logs(self):
        """Export logs to a file"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Logs",
            "",
            "Log Files (*.log);;Text Files (*.txt);;All Files (*.*)"
        )
        
        if file_path:
            try:
                content = self.log_display.toPlainText()
                with open(file_path, 'w') as f:
                    f.write(content)
                self.status_label.setText(f"Logs exported to: {file_path}")
            except Exception as e:
                self.status_label.setText(f"Error exporting logs: {str(e)}")

    def clear_display(self):
        """Clear the log display"""
        self.log_display.clear()
        self.status_label.setText("Display cleared")

def show_logs(parent=None):
    """Show the log viewer dialog"""
    viewer = LogViewer(parent)
    viewer.exec_()
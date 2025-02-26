#!/usr/bin/env python3
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QPushButton, QLineEdit, QMessageBox, QComboBox, 
                           QFormLayout, QDateEdit)
from PyQt5.QtCore import Qt, QDate
import psycopg2
from . import branch_operations as branch_ops

class DataEntryDialog(QDialog):
    """Base class for data entry dialogs"""
    def __init__(self, parent=None, title="Data Entry"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                color: #0053A0;
                font-weight: bold;
            }
            QLineEdit, QComboBox, QDateEdit {
                padding: 5px;
                border: 1px solid #0053A0;
                border-radius: 3px;
            }
            QPushButton {
                padding: 8px 16px;
                background-color: #0053A0;
                color: white;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #003d75;
            }
        """)

    def create_button_row(self):
        """Create and return a row of Save/Cancel buttons"""
        buttons = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.cancel_btn = QPushButton("Cancel")
        self.save_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)
        buttons.addWidget(self.save_btn)
        buttons.addWidget(self.cancel_btn)
        return buttons

class EmployeeDialog(DataEntryDialog):
    def __init__(self, parent=None, employee_data=None):
        super().__init__(parent, "Employee Details")
        self.employee_data = employee_data
        self.setup_ui()
        if employee_data:
            self.populate_data()

    def setup_ui(self):
        layout = QFormLayout(self)
        
        # Create input fields
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter employee name")
        
        self.number_input = QLineEdit()
        self.number_input.setPlaceholderText("Enter employee number")
        
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        
        self.sector_input = QComboBox()
        self.sector_input.addItems([
            'Health care',
            'Precision manufacturing',
            'Engineering',
            'Finance/accounting',
            'Information technology'
        ])
        
        self.branch_input = QComboBox()
        self.load_branches()
        
        # Add fields to form
        layout.addRow("Name:", self.name_input)
        layout.addRow("Number:", self.number_input)
        layout.addRow("Date:", self.date_input)
        layout.addRow("Sector:", self.sector_input)
        layout.addRow("Branch:", self.branch_input)
        
        # Add buttons
        layout.addRow(self.create_button_row())

    def load_branches(self):
        branches = branch_ops.load_branches(self)
        self.branch_input.clear()
        for branch_id, branch_name, _ in branches:
            self.branch_input.addItem(f"{branch_name} (ID: {branch_id})", branch_id)

    def populate_data(self):
        self.name_input.setText(self.employee_data[1])
        self.number_input.setText(self.employee_data[2])
        self.date_input.setDate(QDate.fromString(str(self.employee_data[3]), "yyyy-MM-dd"))
        self.sector_input.setCurrentText(self.employee_data[4])
        
        branch_id = self.employee_data[5]
        for i in range(self.branch_input.count()):
            if str(self.branch_input.itemData(i)) == str(branch_id):
                self.branch_input.setCurrentIndex(i)
                break

    def get_data(self):
        return {
            'name': self.name_input.text(),
            'number': self.number_input.text(),
            'date': self.date_input.date().toPyDate(),
            'sector': self.sector_input.currentText(),
            'branch_id': self.branch_input.currentData()
        }

    def validate(self):
        """Validate the input data"""
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Name is required")
            return False
        if not self.number_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Employee number is required")
            return False
        return True

    def accept(self):
        """Override accept to add validation"""
        if self.validate():
            super().accept()

class BranchDialog(DataEntryDialog):
    def __init__(self, parent=None, branch_data=None):
        super().__init__(parent, "Branch Details")
        self.branch_data = branch_data
        self.setup_ui()
        if branch_data:
            self.populate_data()

    def setup_ui(self):
        layout = QFormLayout(self)
        
        # Create input fields
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter branch name")
        
        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("Enter branch address")
        
        # Add fields to form
        layout.addRow("Branch Name:", self.name_input)
        layout.addRow("Branch Address:", self.location_input)
        
        # Add buttons
        layout.addRow(self.create_button_row())

    def populate_data(self):
        self.name_input.setText(self.branch_data[1])
        self.location_input.setText(self.branch_data[2])

    def get_data(self):
        return {
            'name': self.name_input.text(),
            'address': self.location_input.text()
        }

    def validate(self):
        """Validate the input data"""
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Branch name is required")
            return False
        if not self.location_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Branch address is required")
            return False
        return True

    def accept(self):
        """Override accept to add validation"""
        if self.validate():
            super().accept()
#!/usr/bin/env python3
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QComboBox, QLineEdit, QMessageBox, QApplication, QTabWidget, QDialog, QFormLayout,QDateEdit)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont, QPalette, QColor
import psycopg2
from datetime import datetime
import sys
try:
    from . import LoginLogsViewer  # When imported as a module
    from . import changes_log_viewer
except ImportError:
    from LoginLogsViewer import LoginLogsViewer  # When run directly
    import changes_log_viewer

class PasswordDialog(QDialog):
    def __init__(self, employee_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Change Password")
        self.employee_id = employee_id
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout(self)
        
        # Create input fields
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        
        # Add fields to form
        layout.addRow("New Password:", self.password_input)
        layout.addRow("Confirm Password:", self.confirm_password_input)
        
        # Add buttons
        buttons = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.cancel_btn = QPushButton("Cancel")
        self.save_btn.clicked.connect(self.verify_and_save)
        self.cancel_btn.clicked.connect(self.reject)
        buttons.addWidget(self.save_btn)
        buttons.addWidget(self.cancel_btn)
        layout.addRow(buttons)

        # Apply styling
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                color: #0053A0;
                font-weight: bold;
            }
            QLineEdit {
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

    def verify_and_save(self):
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if not password:
            QMessageBox.warning(self, "Warning", "Password cannot be empty")
            return

        if password != confirm_password:
            QMessageBox.warning(self, "Warning", "Passwords do not match")
            return

        try:
            connection = psycopg2.connect(
                host="localhost",
                dbname="postgres",
                user="postgres",
                password="12345",
                port=5432
            )
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO loginpaswd (employeeid, password)
                VALUES (%s, %s)
                ON CONFLICT (employeeid) DO UPDATE
                SET password = EXCLUDED.password
            """, (self.employee_id, password))
            connection.commit()
            QMessageBox.information(self, "Success", "Password updated successfully!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update password: {str(e)}")
        finally:
            if connection:
                connection.close()

class EmployeeDialog(QDialog):
    def __init__(self, parent=None, employee_data=None):
        super().__init__(parent)
        self.setWindowTitle("Employee Details")
        self.employee_data = employee_data
        self.setup_ui()
        if employee_data:
            self.populate_data()

    def setup_ui(self):
        layout = QFormLayout(self)
        
        # Create input fields
        self.name_input = QLineEdit()
        self.number_input = QLineEdit()
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        
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

        # Add password fields for new employees
        if not self.employee_data:
            self.password_input = QLineEdit()
            self.password_input.setEchoMode(QLineEdit.Password)
            self.confirm_password_input = QLineEdit()
            self.confirm_password_input.setEchoMode(QLineEdit.Password)
        else:
            # Add change password button for existing employees
            self.change_password_btn = QPushButton("Change Password")
            self.change_password_btn.clicked.connect(self.change_password)
        
        # Add fields to form
        layout.addRow("Name:", self.name_input)
        layout.addRow("Number:", self.number_input)
        layout.addRow("Date:", self.date_input)
        layout.addRow("Sector:", self.sector_input)
        layout.addRow("Branch:", self.branch_input)
        
        if not self.employee_data:
            layout.addRow("Password:", self.password_input)
            layout.addRow("Confirm Password:", self.confirm_password_input)
        else:
            layout.addRow(self.change_password_btn)
        
        # Add buttons
        buttons = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.cancel_btn = QPushButton("Cancel")
        if not self.employee_data:
            self.save_btn.clicked.connect(self.verify_and_save)
        else:
            self.save_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)
        buttons.addWidget(self.save_btn)
        buttons.addWidget(self.cancel_btn)
        layout.addRow(buttons)

        # Apply styling
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

    def load_branches(self):
        try:
            connection = psycopg2.connect( host="localhost", dbname="postgres", user="postgres",password="12345",port=5432)
            cursor = connection.cursor()
            cursor.execute("SELECT branchid, branchname FROM goodwillbranch")
            branches = cursor.fetchall()
            self.branch_input.clear()
            for branch_id, branch_name in branches:
                self.branch_input.addItem(f"{branch_name} (ID: {branch_id})", branch_id)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load branches: {str(e)}")
        finally:
            if connection:
                connection.close()

    def populate_data(self):
        # Set name, number and date
        self.name_input.setText(self.employee_data[1])
        self.number_input.setText(self.employee_data[2])
        self.date_input.setDate(QDate.fromString(str(self.employee_data[3]), "yyyy-MM-dd"))
        
        # Set sector
        self.sector_input.setCurrentText(self.employee_data[4])
        
        # Set branch - need to find the branch by ID
        branch_id = self.employee_data[5]
        for i in range(self.branch_input.count()):
            if str(self.branch_input.itemData(i)) == str(branch_id):
                self.branch_input.setCurrentIndex(i)
                break

    def verify_and_save(self):
        if not self.employee_data:  # Only for new employees
            password = self.password_input.text()
            confirm_password = self.confirm_password_input.text()

            if not password:
                QMessageBox.warning(self, "Warning", "Password cannot be empty")
                return

            if password != confirm_password:
                QMessageBox.warning(self, "Warning", "Passwords do not match")
                return

        self.accept()

    def change_password(self):
        if self.employee_data:
            dialog = PasswordDialog(self.employee_data[0], self)
            dialog.exec_()

    def get_data(self):
        branch_id = self.branch_input.currentData()
        data = {
            'name': self.name_input.text(),
            'number': self.number_input.text(),
            'date': self.date_input.date().toPyDate(),
            'sector': self.sector_input.currentText(),
            'branch_id': branch_id
        }
        
        # Include password for new employees
        if not self.employee_data:
            data['password'] = self.password_input.text()
            
        return data

class BranchDialog(QDialog):
    def __init__(self, parent=None, branch_data=None):
        super().__init__(parent)
        self.setWindowTitle("Branch Details")
        self.branch_data = branch_data
        self.setup_ui()
        if branch_data:
            self.populate_data()

    def setup_ui(self):
        layout = QFormLayout(self)
        
        self.name_input = QLineEdit()
        self.location_input = QLineEdit()
        
        layout.addRow("Branch Name:", self.name_input)
        layout.addRow("Branch Address:", self.location_input)
        
        buttons = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.cancel_btn = QPushButton("Cancel")
        self.save_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)
        buttons.addWidget(self.save_btn)
        buttons.addWidget(self.cancel_btn)
        layout.addRow(buttons)

        # Apply styling
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                color: #0053A0;
                font-weight: bold;
            }
            QLineEdit {
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

    def populate_data(self):
        self.name_input.setText(self.branch_data[1])
        self.location_input.setText(self.branch_data[2])

    def get_data(self):
        return {
            'name': self.name_input.text(),
            'address': self.location_input.text()
        }

class AdminPanel(QMainWindow):
    def __init__(self, username="ADMIN"):
        super().__init__()
        self.setWindowTitle("Admin Panel")
        self.current_user = username
        self.setMinimumSize(1200, 800)
        
        # Set Goodwill theme
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#0053A0"))
        palette.setColor(QPalette.WindowText, QColor("#FFFFFF"))
        palette.setColor(QPalette.Base, QColor("#FFFFFF"))
        palette.setColor(QPalette.AlternateBase, QColor("#e6f2ff"))
        palette.setColor(QPalette.Text, QColor("#000000"))
        palette.setColor(QPalette.Button, QColor("#0053A0"))
        palette.setColor(QPalette.ButtonText, QColor("#FFFFFF"))
        self.setPalette(palette)
        
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Title
        title = QLabel("Admin Panel")
        title.setFont(QFont("Oswald", 32, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: white; margin: 20px;")
        layout.addWidget(title)
        
        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #0053A0;
                border-radius: 10px;
                background: white;
            }
            QTabBar::tab {
                background: #0053A0;
                color: white;
                padding: 10px 20px;
                margin: 2px;
                border-radius: 5px;
            }
            QTabBar::tab:selected {
                background: #003d75;
            }
        """)
        
        # Create tabs
        self.employee_tab = self.create_employee_tab()
        self.branch_tab = self.create_branch_tab()
        self.login_logs_tab = LoginLogsViewer()
        self.changes_log_tab = changes_log_viewer.ChangesLogViewer()
        
        self.tabs.addTab(self.employee_tab, "Employee Management")
        self.tabs.addTab(self.branch_tab, "Branch Management")
        self.tabs.addTab(self.login_logs_tab, "Login Logs")
        self.tabs.addTab(self.changes_log_tab, "Changes History")
        
        # Add tabs to main layout
        layout.addWidget(self.tabs)

    def log_change(self, username, action_type, affected_table, record_id, changes):
        """Log changes made by users"""
        connection = None
        try:
            connection = psycopg2.connect(
                host="localhost",
                dbname="postgres",
                user="postgres",
                password="12345",
                port=5432
            )
            cursor = connection.cursor()
            
            # First get the employee_id associated with the username
            cursor.execute("SELECT employeeid FROM employeetable WHERE employeeid = %s", (username,))
            employee = cursor.fetchone()
            employee_id = employee[0] if employee else 'ADMIN1'  # Default to ADMIN1 if not found
            
            cursor.execute("""
                INSERT INTO change_logs
                (username, employeeid, action_type, affected_table, record_id, changes)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (username, employee_id, action_type, affected_table, record_id, changes))
            
            connection.commit()
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"Failed to log change: {str(e)}")
        finally:
            if connection:
                connection.close()

    def create_employee_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Buttons
        button_layout = QHBoxLayout()
        add_btn = QPushButton("Add Employee")
        edit_btn = QPushButton("Edit Employee")
        delete_btn = QPushButton("Delete Employee")
        refresh_btn = QPushButton("Refresh")
        
        for btn in [add_btn, edit_btn, delete_btn, refresh_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    padding: 10px 20px;
                    background-color: #0053A0;
                    color: white;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #003d75;
                }
            """)
            button_layout.addWidget(btn)
        
        layout.addLayout(button_layout)
        
        # Table
        self.employee_table = QTableWidget()
        self.employee_table.setColumnCount(6)
        self.employee_table.setHorizontalHeaderLabels([
            "ID", "Name", "Number", "Date", "Sector", "Branch ID"
        ])
        header = self.employee_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        self.employee_table.setStyleSheet("""
            QTableWidget {
                border: none;
                background-color: white;
            }
            QHeaderView::section {
                background-color: #0053A0;
                color: white;
                padding: 12px;
                border: none;
            }
            QTableWidget::item {
                padding: 10px;
            }
        """)
        
        layout.addWidget(self.employee_table)
        
        # Connect signals
        add_btn.clicked.connect(self.add_employee)
        edit_btn.clicked.connect(self.edit_employee)
        delete_btn.clicked.connect(self.delete_employee)
        refresh_btn.clicked.connect(self.load_employees)
        
        # Load initial data
        self.load_employees()
        
        return tab

    def load_employees(self):
        connection = None
        try:
            connection = psycopg2.connect(
                host="localhost",
                dbname="postgres",
                user="postgres",
                password="12345",
                port=5432
            )
            cursor = connection.cursor()
            
            cursor.execute("""
                SELECT employeeid, employeeName, employeeNumber, 
                       DateOfChange, OrganizationSector, BranchId
                FROM employeeTable
                ORDER BY employeeid
            """)
            employees = cursor.fetchall()
            
            self.employee_table.setRowCount(len(employees))
            for i, emp in enumerate(employees):
                for j, value in enumerate(emp):
                    self.employee_table.setItem(i, j, QTableWidgetItem(str(value)))
                    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load employees: {str(e)}")
        finally:
            if connection:
                connection.close()

    def get_next_employee_id(self):
        """Get the next available employee ID"""
        connection = None
        try:
            connection = psycopg2.connect(
                host="localhost",
                dbname="postgres",
                user="postgres",
                password="12345",
                port=5432
            )
            cursor = connection.cursor()
            
            # Get the highest employee ID that's not an ADMIN ID
            cursor.execute("""
                SELECT MAX(CAST(employeeid AS INTEGER))
                FROM employeeTable
                WHERE employeeid NOT LIKE 'ADMIN%'
            """)
            result = cursor.fetchone()[0]
            
            # If no existing IDs, start at 1
            next_id = 1 if result is None else result + 1
            return str(next_id)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate employee ID: {str(e)}")
            return None
        finally:
            if connection:
                connection.close()

    def reorder_employee_ids(self, start_id):
        """Reorder employee IDs after a deletion"""
        connection = None
        try:
            connection = psycopg2.connect(
                host="localhost",
                dbname="postgres",
                user="postgres",
                password="12345",
                port=5432
            )
            cursor = connection.cursor()
            
            # Get all employees after the deleted ID
            cursor.execute("""
                WITH employees_to_update AS (
                    SELECT employeeid,
                           ROW_NUMBER() OVER (ORDER BY CAST(employeeid AS INTEGER)) + %s - 1 AS new_id
                    FROM employeeTable
                    WHERE CAST(employeeid AS INTEGER) > %s
                    AND employeeid NOT LIKE 'ADMIN%%'
                )
                UPDATE employeeTable e
                SET employeeid = CAST(etu.new_id AS TEXT)
                FROM employees_to_update etu
                WHERE e.employeeid = etu.employeeid
            """, (start_id, start_id))
            
            connection.commit()
            
        except Exception as e:
            if connection:
                connection.rollback()
            QMessageBox.critical(self, "Error", f"Failed to reorder employee IDs: {str(e)}")
        finally:
            if connection:
                connection.close()

    def add_employee(self):
        dialog = EmployeeDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            connection = None
            try:
                connection = psycopg2.connect(
                    host="localhost",
                    dbname="postgres",
                    user="postgres",
                    password="12345",
                    port=5432
                )
                cursor = connection.cursor()

                # Get next available employee ID
                next_id = self.get_next_employee_id()
                if not next_id:
                    return

                # Insert new employee
                cursor.execute("""
                    INSERT INTO employeeTable
                    (employeeid, employeeName, employeeNumber, DateOfChange,
                     OrganizationSector, BranchId)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    next_id, data['name'], data['number'], data['date'],
                    data['sector'], data['branch_id']
                ))

                # Insert password into loginpaswd table
                if 'password' in data:
                    cursor.execute("""
                        INSERT INTO loginpaswd (employeeid, password)
                        VALUES (%s, %s)
                    """, (next_id, data['password']))
                connection.commit()

                # Log the addition with current admin user
                self.log_change(
                    'ADMIN1',  # Use ADMIN1 as the user performing the action
                    'ADD',
                    'employeeTable',
                    next_id,
                    str({'name': data['name'], 'number': data['number'], 'date': str(data['date']), 'sector': data['sector']})
                )

                QMessageBox.information(self, "Success",
                    f"Employee added successfully with ID: {next_id}")
                self.load_employees()
            except Exception as e:
                connection.rollback()
                QMessageBox.critical(self, "Error", f"Failed to add employee: {str(e)}")
            finally:
                if connection:
                    connection.close()

    def edit_employee(self):
        current_row = self.employee_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select an employee to edit.")
            return
            
        employee_data = []
        for col in range(6):
            employee_data.append(self.employee_table.item(current_row, col).text())
            
        # Check if trying to edit an ADMIN account
        if employee_data[0].startswith('ADMIN'):
            QMessageBox.warning(self, "Warning", "Admin accounts cannot be edited.")
            return

        dialog = EmployeeDialog(self, employee_data)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            connection = None
            try:
                connection = psycopg2.connect(
                    host="localhost",
                    dbname="postgres",
                    user="postgres",
                    password="12345",
                    port=5432
                )
                cursor = connection.cursor()
                
                # Keep the original employee ID
                employee_id = employee_data[0]
                
                # Get current employee data for change log
                cursor.execute("""
                    SELECT employeeName, employeeNumber, DateOfChange, OrganizationSector
                    FROM employeeTable WHERE employeeid = %s
                """, (employee_id,))
                old_data = cursor.fetchone()
                old_values = {
                    'name': old_data[0],
                    'number': old_data[1],
                    'date': str(old_data[2]),
                    'sector': old_data[3]
                }

                # Update employee
                cursor.execute("""
                    UPDATE employeeTable
                    SET employeeName = %s, employeeNumber = %s,
                        DateOfChange = %s, OrganizationSector = %s,
                        BranchId = %s
                    WHERE employeeid = %s
                """, (
                    data['name'], data['number'], data['date'],
                    data['sector'], data['branch_id'], employee_id
                ))
                connection.commit()

                # Log the changes
                changes = {
                    'before': old_values,
                    'after': {
                        'name': data['name'],
                        'number': data['number'],
                        'date': str(data['date']),
                        'sector': data['sector']
                    }
                }
                self.log_change(
                    'ADMIN1',  # Use ADMIN1 as the user performing the action
                    'EDIT',
                    'employeeTable',
                    employee_id,
                    str(changes)
                )

                QMessageBox.information(self, "Success", "Employee updated successfully!")
                self.load_employees()
            except Exception as e:
                connection.rollback()
                QMessageBox.critical(self, "Error", f"Failed to update employee: {str(e)}")
            finally:
                if connection:
                    connection.close()

    def delete_employee(self):
        current_row = self.employee_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select an employee to delete.")
            return
            
        employee_id = self.employee_table.item(current_row, 0).text()
        
        # Check if trying to delete an ADMIN account
        if employee_id.startswith('ADMIN'):
            QMessageBox.warning(self, "Warning", "Admin accounts cannot be deleted.")
            return
        
        reply = QMessageBox.question(self, "Confirm Delete",
                                    f"Are you sure you want to delete employee {employee_id}?",
                                    QMessageBox.Yes | QMessageBox.No)
                                    
        if reply == QMessageBox.Yes:
            connection = None
            try:
                connection = psycopg2.connect(
                    host="localhost",
                    dbname="postgres",
                    user="postgres",
                    password="12345",
                    port=5432
                )
                cursor = connection.cursor()

                # Get employee data before deletion for logging
                cursor.execute("""
                    SELECT employeeName, employeeNumber, DateOfChange, OrganizationSector
                    FROM employeeTable WHERE employeeid = %s
                """, (employee_id,))
                old_data = cursor.fetchone()

                if old_data:  # Store data before deletion
                    deleted_data = {
                        'name': old_data[0],
                        'number': old_data[1],
                        'date': str(old_data[2]),
                        'sector': old_data[3]
                    }

                    # Delete the employee
                    cursor.execute("DELETE FROM employeeTable WHERE employeeid = %s",
                                   (employee_id,))

                    # Log the deletion with admin user
                    self.log_change(
                        'ADMIN1',  # Use ADMIN1 as the user performing the action
                        'DELETE',
                        'employeeTable',
                        employee_id,
                        str(deleted_data)
                    )

                    connection.commit()
                    QMessageBox.information(self, "Success", "Employee deleted successfully!")
                    self.load_employees()
                else:
                    QMessageBox.warning(self, "Warning", "Employee not found!")
            except Exception as e:
                connection.rollback()
                QMessageBox.critical(self, "Error", f"Failed to delete employee: {str(e)}")
            finally:
                if connection:
                    connection.close()

    def create_branch_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Buttons
        button_layout = QHBoxLayout()
        add_btn = QPushButton("Add Branch")
        edit_btn = QPushButton("Edit Branch")
        delete_btn = QPushButton("Delete Branch")
        refresh_btn = QPushButton("Refresh")
        
        for btn in [add_btn, edit_btn, delete_btn, refresh_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    padding: 10px 20px;
                    background-color: #0053A0;
                    color: white;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #003d75;
                }
            """)
            button_layout.addWidget(btn)
        
        layout.addLayout(button_layout)
        
        # Table
        self.branch_table = QTableWidget()
        self.branch_table.setColumnCount(3)
        self.branch_table.setHorizontalHeaderLabels([
            "ID", "Name", "Location"
        ])
        header = self.branch_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        self.branch_table.setStyleSheet("""
            QTableWidget {
                border: none;
                background-color: white;
            }
            QHeaderView::section {
                background-color: #0053A0;
                color: white;
                padding: 12px;
                border: none;
            }
            QTableWidget::item {
                padding: 10px;
            }
        """)
        
        layout.addWidget(self.branch_table)
        
        # Connect signals
        add_btn.clicked.connect(self.add_branch)
        edit_btn.clicked.connect(self.edit_branch)
        delete_btn.clicked.connect(self.delete_branch)
        refresh_btn.clicked.connect(self.load_branches)
        
        # Load initial data
        self.load_branches()
        
        return tab

    def get_next_branch_id(self):
        """Get the next available branch ID"""
        connection = None
        try:
            connection = psycopg2.connect(
                host="localhost",
                dbname="postgres",
                user="postgres",
                password="12345",
                port=5432
            )
            cursor = connection.cursor()
            
            # Get the highest branch ID
            cursor.execute("SELECT MAX(branchid) FROM goodwillbranch")
            result = cursor.fetchone()[0]
            
            # If no existing IDs, start at 1
            next_id = 1 if result is None else result + 1
            return next_id
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate branch ID: {str(e)}")
            return None
        finally:
            if connection:
                connection.close()

    def load_branches(self):
        connection = None
        try:
            connection = psycopg2.connect(
                host="localhost",
                dbname="postgres",
                user="postgres",
                password="12345",
                port=5432
            )
            cursor = connection.cursor()
            
            cursor.execute("""
                SELECT branchid, branchname, branchaddress
                FROM goodwillbranch
                ORDER BY branchid
            """)
            branches = cursor.fetchall()
            
            self.branch_table.setRowCount(len(branches))
            for i, branch in enumerate(branches):
                for j, value in enumerate(branch):
                    self.branch_table.setItem(i, j, QTableWidgetItem(str(value)))
                    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load branches: {str(e)}")
        finally:
            if connection:
                connection.close()

    def add_branch(self):
        dialog = BranchDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            connection = None
            try:
                connection = psycopg2.connect(
                    host="localhost",
                    dbname="postgres",
                    user="postgres",
                    password="12345",
                    port=5432
                )
                cursor = connection.cursor()
                
                # Get next branch ID
                branch_id = self.get_next_branch_id()
                if not branch_id:
                    return
                
                cursor.execute("""
                    INSERT INTO goodwillbranch (branchid, branchname, branchaddress)
                    VALUES (%s, %s, %s)
                """, (branch_id, data['name'], data['address']))

                # Log the branch addition
                self.log_change(
                    'ADMIN1',  # Use ADMIN1 as the user performing the action
                    'ADD',
                    'goodwillbranch',
                    str(branch_id),
                    str({
                        'name': data['name'],
                        'address': data['address']
                    })
                )

                connection.commit()
                QMessageBox.information(self, "Success",
                    f"Branch added successfully with ID: {branch_id}")
                self.load_branches()
            except Exception as e:
                connection.rollback()
                QMessageBox.critical(self, "Error", f"Failed to add branch: {str(e)}")
            finally:
                if connection:
                    connection.close()

    def edit_branch(self):
        current_row = self.branch_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a branch to edit.")
            return
            
        branch_data = []
        for col in range(3):
            branch_data.append(self.branch_table.item(current_row, col).text())
            
        dialog = BranchDialog(self, branch_data)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            connection = None
            try:
                connection = psycopg2.connect(
                    host="localhost",
                    dbname="postgres",
                    user="postgres",
                    password="12345",
                    port=5432
                )
                cursor = connection.cursor()
                cursor.execute("""
                    UPDATE goodwillbranch
                    SET branchname = %s, branchaddress = %s
                    WHERE branchid = %s
                """, (data['name'], data['address'], branch_data[0]))
                connection.commit()
                QMessageBox.information(self, "Success", "Branch updated successfully!")
                self.load_branches()
            except Exception as e:
                connection.rollback()
                QMessageBox.critical(self, "Error", f"Failed to update branch: {str(e)}")
            finally:
                if connection:
                    connection.close()

    def delete_branch(self):
        current_row = self.branch_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a branch to delete.")
            return
            
        branch_id = self.branch_table.item(current_row, 0).text()
        connection = None
        
        try:
            connection = psycopg2.connect(
                host="localhost",
                dbname="postgres",
                user="postgres",
                password="12345",
                port=5432
            )
            cursor = connection.cursor()
            
            # Check if branch has employees
            cursor.execute("""
                SELECT COUNT(*)
                FROM employeeTable
                WHERE BranchId = %s
            """, (branch_id,))
            
            employee_count = cursor.fetchone()[0]
            
            if employee_count > 0:
                QMessageBox.warning(self, "Warning",
                    f"Cannot delete branch {branch_id}. It has {employee_count} employees assigned.")
                return
            
            # Ask for confirmation
            reply = QMessageBox.question(self, "Confirm Delete",
                f"Are you sure you want to delete branch {branch_id}?",
                QMessageBox.Yes | QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                # Simple delete
                cursor.execute("DELETE FROM goodwillbranch WHERE branchid = %s",
                             (branch_id,))
                
                connection.commit()
                QMessageBox.information(self, "Success", "Branch deleted successfully!")
                self.load_branches()
                
        except Exception as e:
            if connection:
                connection.rollback()
            QMessageBox.critical(self, "Error", f"Failed to delete branch: {str(e)}")
        finally:
            if connection:
                connection.close()

def main():
    app = QApplication(sys.argv)
    window = AdminPanel()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
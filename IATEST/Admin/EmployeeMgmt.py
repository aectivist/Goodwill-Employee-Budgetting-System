try:
    from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QLabel, QLineEdit, QComboBox, QPushButton, QTableWidget, 
                               QTableWidgetItem, QHeaderView, QMessageBox, QFrame, QDialog,
                               QDialogButtonBox)
    from PyQt5.QtGui import QFont, QPalette, QColor
    from PyQt5.QtCore import Qt
except ImportError:
    print("Error: PyQt5 is required for this application.")
    print("Please install it using: pip install PyQt5")
    import sys
    sys.exit(1)

import psycopg2
from datetime import date
import sys

class PasswordDialog(QDialog):
    def __init__(self, title, message, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setStyleSheet("""
            QDialog {
                background-color: #1a1a1a;
            }
            QLabel {
                color: white;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #0066cc;
                border-radius: 5px;
                background-color: #2d2d2d;
                color: white;
                min-width: 200px;
            }
            QPushButton {
                padding: 10px 20px;
                border-radius: 5px;
                background-color: #0066cc;
                color: white;
            }
            QPushButton:hover {
                background-color: #0052a3;
            }
        """)

        layout = QVBoxLayout(self)
        
        message_label = QLabel(message)
        layout.addWidget(message_label)
        
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)
        
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def get_password(self):
        return self.password_input.text()


class EmployeeManagement(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Employee Management")
        self.setMinimumSize(1200, 800)
        
        # Set the color scheme
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#1a1a1a"))
        palette.setColor(QPalette.WindowText, QColor("#FFFFFF"))
        palette.setColor(QPalette.Base, QColor("#2d2d2d"))
        palette.setColor(QPalette.Text, QColor("#FFFFFF"))
        palette.setColor(QPalette.Button, QColor("#0066cc"))
        palette.setColor(QPalette.ButtonText, QColor("#FFFFFF"))
        self.setPalette(palette)

        self.setup_ui()
        self._load_branches()
        self.load_employees()

    def setup_ui(self):
        """Setup the user interface"""
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title = QLabel("Employee Management")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Form container
        form_container = self._create_form_container()
        layout.addWidget(form_container)

        # Employee Table
        self.table = self._create_table()
        layout.addWidget(self.table)

    def _create_form_container(self):
        """Create the form container with input fields"""
        form_container = QFrame()
        form_container.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        form_container.setStyleSheet("""
            QFrame {
                background-color: #2d2d2d;
                border-radius: 10px;
                padding: 20px;
            }
            QLineEdit, QComboBox {
                padding: 8px;
                border: 1px solid #0066cc;
                border-radius: 5px;
                background-color: #1a1a1a;
                color: white;
                min-width: 200px;
            }
            QPushButton {
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                background-color: #0066cc;
                color: white;
            }
            QPushButton:hover {
                background-color: #0052a3;
            }
        """)
        
        form_layout = QVBoxLayout(form_container)

        # Input fields
        fields_layout = QHBoxLayout()
        fields_layout.setSpacing(20)

        # Left column
        left_column = QVBoxLayout()
        self.employee_id = self._create_input_field("Employee ID", left_column)
        self.employee_name = self._create_input_field("Employee Name", left_column)
        self.employee_number = self._create_input_field("Employee Number", left_column)
        self.password = self._create_input_field("Password", left_column, is_password=True)
        fields_layout.addLayout(left_column)

        # Right column
        right_column = QVBoxLayout()
        self._setup_sector_combo(right_column)
        self._setup_branch_combo(right_column)
        fields_layout.addLayout(right_column)
        
        form_layout.addLayout(fields_layout)
        form_layout.addLayout(self._create_buttons())
        
        return form_container

    def _create_table(self):
        """Create the employee table"""
        table = QTableWidget()
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels([
            "Employee ID", "Name", "Number", "Date of Change",
            "Organization Sector", "Branch"
        ])
        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        table.setStyleSheet("""
            QTableWidget {
                background-color: #2d2d2d;
                border-radius: 10px;
                color: white;
            }
            QHeaderView::section {
                background-color: #0066cc;
                color: white;
                padding: 8px;
                border: none;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #0052a3;
            }
        """)
        return table

    def _setup_sector_combo(self, layout):
        """Setup the organization sector combo box"""
        sector_layout = QVBoxLayout()
        sector_label = QLabel("Organization Sector")
        sector_label.setStyleSheet("color: white;")
        self.sector_combo = QComboBox()
        self.sector_combo.addItems([
            "Health care",
            "Precision manufacturing",
            "Engineering",
            "Finance/accounting",
            "Information technology"
        ])
        sector_layout.addWidget(sector_label)
        sector_layout.addWidget(self.sector_combo)
        layout.addLayout(sector_layout)

    def _setup_branch_combo(self, layout):
        """Setup the branch combo box"""
        branch_layout = QVBoxLayout()
        branch_label = QLabel("Branch")
        branch_label.setStyleSheet("color: white;")
        self.branch_combo = QComboBox()
        branch_layout.addWidget(branch_label)
        branch_layout.addWidget(self.branch_combo)
        layout.addLayout(branch_layout)

    def _create_buttons(self):
        """Create action buttons"""
        buttons_layout = QHBoxLayout()
        
        add_button = QPushButton("Add Employee")
        add_button.clicked.connect(self.add_employee)
        
        remove_button = QPushButton("Remove Employee")
        remove_button.clicked.connect(self.remove_employee)
        
        change_password_button = QPushButton("Change Password")
        change_password_button.clicked.connect(self.change_password)
        
        clear_button = QPushButton("Clear Fields")
        clear_button.setStyleSheet("""
            QPushButton {
                background-color: #4d4d4d;
            }
            QPushButton:hover {
                background-color: #666666;
            }
        """)
        clear_button.clicked.connect(self.clear_fields)
        
        buttons_layout.addWidget(add_button)
        buttons_layout.addWidget(remove_button)
        buttons_layout.addWidget(change_password_button)
        buttons_layout.addWidget(clear_button)
        
        return buttons_layout

    def _get_db_connection(self):
        """Get database connection"""
        return psycopg2.connect(
            host="localhost",
            dbname="postgres",
            user="postgres",
            password="12345",
            port=5432
        )

    def _verify_password(self, employee_id):
        """Verify employee password"""
        dialog = PasswordDialog("Verify Password", "Enter current password:", self)
        if dialog.exec_() == QDialog.Accepted:
            connection = None
            try:
                connection = self._get_db_connection()
                cursor = connection.cursor()
                cursor.execute("SELECT password FROM loginpaswd WHERE id = %s", (employee_id,))
                result = cursor.fetchone()
                if result and result[0] == dialog.get_password():
                    return True
                QMessageBox.warning(self, "Error", "Invalid password")
                return False
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to verify password: {str(e)}")
                return False
            finally:
                if connection:
                    connection.close()
        return False

    def add_employee(self):
        """Add a new employee"""
        connection = None
        try:
            # Validate input
            if not all([self.employee_id.text(), self.employee_name.text(), 
                       self.employee_number.text(), self.password.text()]):
                QMessageBox.warning(self, "Warning", "Please fill all fields")
                return

            connection = self._get_db_connection()
            cursor = connection.cursor()

            # Start transaction
            cursor.execute("BEGIN")
            try:
                # Insert new employee
                cursor.execute("""
                    INSERT INTO employeeTable 
                    (employeeid, employeeName, employeeNumber, DateOfChange, 
                     OrganizationSector, BranchId)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    self.employee_id.text(),
                    self.employee_name.text(),
                    self.employee_number.text(),
                    date.today(),
                    self.sector_combo.currentText(),
                    self.get_branch_id()
                ))

                # Insert password
                cursor.execute("""
                    INSERT INTO loginpaswd (id, password)
                    VALUES (%s, %s)
                """, (self.employee_id.text(), self.password.text()))

                cursor.execute("COMMIT")
                QMessageBox.information(self, "Success", "Employee added successfully!")
                self.load_employees()
                self.clear_fields()

            except Exception as e:
                cursor.execute("ROLLBACK")
                raise e

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add employee: {str(e)}")
        finally:
            if connection:
                connection.close()

    def remove_employee(self):
        """Remove an employee"""
        connection = None
        try:
            employee_id = self.employee_id.text()
            if not employee_id:
                QMessageBox.warning(self, "Warning", "Please enter Employee ID to remove")
                return

            # Verify password before removal
            if not self._verify_password(employee_id):
                return

            confirm = QMessageBox.question(
                self, "Confirm Removal",
                f"Are you sure you want to remove employee {employee_id}?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if confirm == QMessageBox.Yes:
                connection = self._get_db_connection()
                cursor = connection.cursor()

                # Start transaction
                cursor.execute("BEGIN")
                try:
                    # Remove from loginpaswd first (due to foreign key constraints)
                    cursor.execute("DELETE FROM loginpaswd WHERE id = %s", (employee_id,))
                    
                    # Then remove from employeeTable
                    cursor.execute("DELETE FROM employeeTable WHERE employeeid = %s", 
                                 (employee_id,))
                    
                    if cursor.rowcount == 0:
                        cursor.execute("ROLLBACK")
                        QMessageBox.warning(self, "Warning", "Employee not found")
                    else:
                        cursor.execute("COMMIT")
                        QMessageBox.information(self, "Success", "Employee removed successfully!")
                        self.load_employees()
                        self.clear_fields()

                except Exception as e:
                    cursor.execute("ROLLBACK")
                    raise e

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to remove employee: {str(e)}")
        finally:
            if connection:
                connection.close()

    def change_password(self):
        """Change employee password"""
        employee_id = self.employee_id.text()

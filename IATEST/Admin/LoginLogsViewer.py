from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                                QTableWidget, QTableWidgetItem, QHeaderView, QComboBox,
                                QLineEdit, QDateTimeEdit, QMessageBox, QApplication)
from PyQt5.QtCore import Qt, QDateTime, QTimer
from PyQt5.QtGui import QFont, QPalette, QColor
import psycopg2
from datetime import datetime, timedelta
import sys

class LoginLogsViewer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login Activity Logs")
        self.setMinimumSize(1000, 600)
        
        # Database connection
        self.connection = None
        self.cursor = None
        
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
        self.load_logs()

        # Connect cleanup handler
        self.destroyed.connect(self.cleanup_db)

    def cleanup_db(self):
        """Clean up database connections when widget is destroyed"""
        if self.cursor:
            self.cursor.close()
        if self.connection and not self.connection.closed:
            self.connection.close()

    def ensure_connection(self):
        """Ensure we have an active database connection"""
        try:
            if not self.connection or self.connection.closed:
                self.connection = psycopg2.connect(
                    host="localhost",
                    dbname="postgres",
                    user="postgres",
                    password="12345",
                    port=5432
                )
            if not self.cursor or self.cursor.closed:
                self.cursor = self.connection.cursor()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to connect to database: {str(e)}")
            raise

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title = QLabel("Login Activity Logs")
        title.setFont(QFont("Oswald", 32, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: white; margin: 10px;")
        layout.addWidget(title)

        # Filters container
        filters_container = QWidget()
        filters_container.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 10px;
            }
            QLabel {
                color: #0053A0;
                font-weight: bold;
                font-size: 14px;
                font-family: Oswald;
            }
            QLineEdit, QComboBox, QDateTimeEdit {
                padding: 10px;
                border: 2px solid #0053A0;
                border-radius: 5px;
                background-color: white;
                color: #0053A0;
                font-size: 13px;
            }
            QPushButton {
                padding: 10px 20px;
                border-radius: 5px;
                background-color: #0053A0;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #003d75;
            }
        """)
        filters_layout = QHBoxLayout(filters_container)
        filters_layout.setSpacing(20)
        
        # Username filter
        username_layout = QVBoxLayout()
        username_label = QLabel("Username:")
        self.username_filter = QLineEdit()
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_filter)
        filters_layout.addLayout(username_layout)

        # Action type filter
        action_layout = QVBoxLayout()
        action_label = QLabel("Action Type:")
        self.action_filter = QComboBox()
        self.action_filter.addItems(["All", "LOGIN_SUCCESS", "LOGIN_FAILED", "PAGE_ACCESS"])
        action_layout.addWidget(action_label)
        action_layout.addWidget(self.action_filter)
        filters_layout.addLayout(action_layout)

        # Page filter
        page_layout = QVBoxLayout()
        page_label = QLabel("Page/Feature:")
        self.page_filter = QComboBox()
        self.page_filter.addItems([
            "All", "Budget", "Inventory", "Transactions",
            "Donations", "Employee Management", "Branch Management"
        ])
        page_layout.addWidget(page_label)
        page_layout.addWidget(self.page_filter)
        filters_layout.addLayout(page_layout)

        # Date range filter
        date_layout = QVBoxLayout()
        date_label = QLabel("Date Range:")
        date_layout.addWidget(date_label)
        
        dates_layout = QHBoxLayout()
        self.start_date = QDateTimeEdit(QDateTime.currentDateTime().addDays(-7))
        self.end_date = QDateTimeEdit(QDateTime.currentDateTime())
        for date_edit in [self.start_date, self.end_date]:
            date_edit.setCalendarPopup(True)
        dates_layout.addWidget(self.start_date)
        dates_layout.addWidget(QLabel("-"))
        dates_layout.addWidget(self.end_date)
        date_layout.addLayout(dates_layout)
        filters_layout.addLayout(date_layout)

        # Apply filters button
        self.apply_button = QPushButton("Apply Filters")
        self.apply_button.clicked.connect(self.delayed_refresh)
        filters_layout.addWidget(self.apply_button)

        layout.addWidget(filters_container)

        # Logs table container
        table_container = QWidget()
        table_container.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 10px;
            }
            QTableWidget {
                border: none;
            }
            QHeaderView::section {
                background-color: #0053A0;
                color: white;
                padding: 12px;
                border: none;
                font-weight: bold;
                font-family: Oswald;
                font-size: 14px;
            }
            QTableWidget::item {
                padding: 10px;
                color: #0053A0;
                font-size: 13px;
            }
            QTableWidget::item:selected {
                background-color: #e6f2ff;
                color: #0053A0;
            }
        """)
        table_layout = QVBoxLayout(table_container)
        
        # Logs table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Employee ID", "Username", "Action Type", "Page/Feature", "Details", "Timestamp"
        ])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        table_layout.addWidget(self.table)
        layout.addWidget(table_container)

        # Setup refresh timer
        self.refresh_timer = QTimer()
        self.refresh_timer.setInterval(500)  # 500ms debounce
        self.refresh_timer.setSingleShot(True)
        self.refresh_timer.timeout.connect(self._do_refresh)

        # Load available pages
        self.load_available_pages()

        # Connect filter signals
        self.username_filter.textChanged.connect(self.delayed_refresh)
        self.action_filter.currentTextChanged.connect(self.delayed_refresh)
        self.page_filter.currentTextChanged.connect(self.delayed_refresh)
        self.start_date.dateTimeChanged.connect(self.delayed_refresh)
        self.end_date.dateTimeChanged.connect(self.delayed_refresh)

    def load_available_pages(self):
        """Load unique pages from logs"""
        try:
            self.ensure_connection()
            self.cursor.execute("""
                SELECT DISTINCT page_accessed
                FROM user_login_logs
                WHERE page_accessed IS NOT NULL
                ORDER BY page_accessed
            """)
            pages = ["All"] + [row[0] for row in self.cursor.fetchall()]
            current = self.page_filter.currentText()
            self.page_filter.clear()
            self.page_filter.addItems(pages)
            if current in pages:
                self.page_filter.setCurrentText(current)
        except Exception as e:
            QMessageBox.warning(self, "Warning", f"Failed to load pages: {str(e)}")

    def delayed_refresh(self):
        """Debounce the refresh to prevent too many database queries"""
        self.refresh_timer.start()

    def _do_refresh(self):
        """Actually perform the refresh after the timer expires"""
        self.load_logs()

    def load_logs(self):
        try:
            self.ensure_connection()

            # Build the query based on filters
            query = """
                SELECT employeeid, username, action_type,
                       page_accessed, action_details,
                       action_timestamp
                FROM user_login_logs
                WHERE 1=1
            """
            params = []

            # Username filter
            if self.username_filter.text():
                query += " AND username ILIKE %s"
                params.append(f"%{self.username_filter.text()}%")

            # Action type filter
            if self.action_filter.currentText() != "All":
                query += " AND action_type = %s"
                params.append(self.action_filter.currentText())

            # Page/Feature filter
            if self.page_filter.currentText() != "All":
                query += " AND page_accessed = %s"
                params.append(self.page_filter.currentText())

            # Date range filter
            query += " AND action_timestamp BETWEEN %s AND %s"
            params.extend([
                self.start_date.dateTime().toPyDateTime(),
                self.end_date.dateTime().toPyDateTime()
            ])

            query += " ORDER BY action_timestamp DESC"

            self.cursor.execute(query, params)
            logs = self.cursor.fetchall()

            self.table.setRowCount(len(logs))
            for i, log in enumerate(logs):
                for j, value in enumerate(log):
                    display_value = value
                    if j == 5 and isinstance(value, datetime):  # action_timestamp column
                        display_value = value.strftime("%Y-%m-%d %H:%M:%S")
                    item = QTableWidgetItem(str(display_value))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Make read-only
                    self.table.setItem(i, j, item)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load logs: {str(e)}")
            # Only close connection on error
            if self.cursor:
                self.cursor.close()
                self.cursor = None
            if self.connection and not self.connection.closed:
                self.connection.close()
                self.connection = None

def main():
    app = QApplication(sys.argv)
    window = LoginLogsViewer()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                           QTableWidget, QTableWidgetItem, QHeaderView,
                           QComboBox, QLabel, QMessageBox)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
import psycopg2
from datetime import datetime, timedelta

class ChangesLogViewer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.connection = None
        self.cursor = None
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
        """Set up the UI components"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title = QLabel("Changes History")
        title.setFont(QFont("Oswald", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #0053A0; margin: 10px;")
        layout.addWidget(title)

        # Filters container
        filters_layout = QHBoxLayout()
        
        # User filter
        self.user_filter = QComboBox()
        self.user_filter.addItem("All Users")
        filters_layout.addWidget(QLabel("User:"))
        filters_layout.addWidget(self.user_filter)

        # Action type filter
        self.action_filter = QComboBox()
        self.action_filter.addItems(["All Actions", "ADD", "EDIT", "DELETE"])
        filters_layout.addWidget(QLabel("Action:"))
        filters_layout.addWidget(self.action_filter)

        # Table filter
        self.table_filter = QComboBox()
        self.table_filter.addItems(["All Tables", "employeeTable", "goodwillbranch"])
        filters_layout.addWidget(QLabel("Table:"))
        filters_layout.addWidget(self.table_filter)

        # Time range filter
        self.time_filter = QComboBox()
        self.time_filter.addItems([
            "Last 24 Hours",
            "Last 7 Days",
            "Last 30 Days",
            "All Time"
        ])
        filters_layout.addWidget(QLabel("Time Range:"))
        filters_layout.addWidget(self.time_filter)

        # Refresh button
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.load_logs)
        filters_layout.addWidget(refresh_btn)

        layout.addLayout(filters_layout)

        # Logs table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Log ID", "Username", "Action", "Table", "Record ID", 
            "Changes", "Timestamp"
        ])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.Stretch)  # Let Changes column stretch
        
        # Style the table
        self.table.setStyleSheet("""
            QTableWidget {
                border: 2px solid #0053A0;
                border-radius: 5px;
                background-color: white;
            }
            QHeaderView::section {
                background-color: #0053A0;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 5px;
            }
        """)
        
        layout.addWidget(self.table)

        # Setup refresh timer
        self.refresh_timer = QTimer()
        self.refresh_timer.setInterval(500)  # 500ms debounce
        self.refresh_timer.setSingleShot(True)
        self.refresh_timer.timeout.connect(self._do_refresh)

        # Connect filter signals
        self.user_filter.currentTextChanged.connect(self.delayed_refresh)
        self.action_filter.currentTextChanged.connect(self.delayed_refresh)
        self.table_filter.currentTextChanged.connect(self.delayed_refresh)
        self.time_filter.currentTextChanged.connect(self.delayed_refresh)

    def delayed_refresh(self):
        """Debounce the refresh to prevent too many database queries"""
        self.refresh_timer.start()

    def _do_refresh(self):
        """Actually perform the refresh after the timer expires"""
        self.load_logs()

    def get_time_filter_condition(self):
        """Get the SQL condition for the selected time filter"""
        time_range = self.time_filter.currentText()
        if time_range == "Last 24 Hours":
            return "timestamp >= NOW() - INTERVAL '24 hours'"
        elif time_range == "Last 7 Days":
            return "timestamp >= NOW() - INTERVAL '7 days'"
        elif time_range == "Last 30 Days":
            return "timestamp >= NOW() - INTERVAL '30 days'"
        return "1=1"  # All Time

    def load_logs(self):
        """Load and display logs based on current filters"""
        try:
            self.ensure_connection()

            # First update the users filter
            self.cursor.execute("""
                SELECT DISTINCT username 
                FROM change_logs 
                ORDER BY username
            """)
            users = [row[0] for row in self.cursor.fetchall()]
            
            current = self.user_filter.currentText()
            self.user_filter.clear()
            self.user_filter.addItem("All Users")
            self.user_filter.addItems(users)
            
            if current in users:
                self.user_filter.setCurrentText(current)

            # Build query with filters
            query = "SELECT * FROM change_logs WHERE 1=1"
            params = []

            # Apply filters
            if self.user_filter.currentText() != "All Users":
                query += " AND username = %s"
                params.append(self.user_filter.currentText())

            if self.action_filter.currentText() != "All Actions":
                query += " AND action_type = %s"
                params.append(self.action_filter.currentText())

            if self.table_filter.currentText() != "All Tables":
                query += " AND affected_table = %s"
                params.append(self.table_filter.currentText())

            # Add time filter
            query += f" AND {self.get_time_filter_condition()}"

            # Order by timestamp
            query += " ORDER BY timestamp DESC"

            self.cursor.execute(query, params)
            logs = self.cursor.fetchall()

            # Update table
            self.table.setRowCount(len(logs))
            for i, log in enumerate(logs):
                for j, value in enumerate(log):
                    # Format timestamp if it's a datetime object
                    display_value = value
                    if j == 6 and isinstance(value, datetime):  # timestamp column
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

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    window = ChangesLogViewer()
    window.show()
    sys.exit(app.exec_())
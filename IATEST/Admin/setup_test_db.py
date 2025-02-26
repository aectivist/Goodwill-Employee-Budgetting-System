#!/usr/bin/env python3
import os
import sys
import time

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget
from IATEST.Admin.db_handler import get_db

# SQL Queries as before...
CREATE_TABLES = """
    CREATE TABLE IF NOT EXISTS goodwillbranch (
        branchid TEXT PRIMARY KEY,
        branchname TEXT NOT NULL,
        branchaddress TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS employeeTable (
        employeeid TEXT PRIMARY KEY,
        employeeName TEXT NOT NULL,
        employeeNumber TEXT NOT NULL,
        DateOfChange DATE NOT NULL,
        OrganizationSector TEXT NOT NULL,
        BranchId TEXT REFERENCES goodwillbranch(branchid)
    );

    CREATE TABLE IF NOT EXISTS loginpaswd (
        employeeid TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        FOREIGN KEY (employeeid) REFERENCES employeeTable(employeeid) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS user_login_logs (
        log_id SERIAL PRIMARY KEY,
        username TEXT NOT NULL,
        action_type TEXT NOT NULL,
        action_timestamp TIMESTAMP NOT NULL
    );
"""

INSERT_TEST_BRANCHES = """
    INSERT INTO goodwillbranch (branchid, branchname, branchaddress)
    VALUES 
        ('1', 'Main Branch', '123 Main St'),
        ('2', 'Downtown Branch', '456 Downtown Ave')
    ON CONFLICT (branchid) DO NOTHING;
"""

INSERT_TEST_EMPLOYEES = """
    INSERT INTO employeeTable
    (employeeid, employeeName, employeeNumber, DateOfChange, OrganizationSector, BranchId)
    VALUES
        ('ADMIN1', 'Admin User', '001', CURRENT_DATE, 'Information technology', '1'),
        ('1', 'John Doe', '002', CURRENT_DATE, 'Engineering', '1'),
        ('2', 'Jane Smith', '003', CURRENT_DATE, 'Health care', '2')
    ON CONFLICT (employeeid) DO NOTHING;
"""

INSERT_TEST_LOGINS = """
    INSERT INTO loginpaswd (employeeid, password)
    VALUES
        ('ADMIN1', '12345'),
        ('1', 'password1'),
        ('2', 'password2')
    ON CONFLICT (employeeid) DO NOTHING;
"""

class SetupWindow(QWidget):
    def __init__(self):
        super().__init__()
        print("Initializing SetupWindow...")
        self.db = get_db()
        self.setWindowTitle("Database Setup")
        self.setGeometry(100, 100, 400, 200)

    def init_test_db(self):
        try:
            print("Creating tables...")
            success, _ = self.db.execute_query(self, CREATE_TABLES, fetch=False)
            if not success:
                print("Failed to create tables")
                return False

            print("Adding test branches...")
            success, _ = self.db.execute_query(self, INSERT_TEST_BRANCHES, fetch=False)
            if not success:
                print("Failed to add test branches")
                return False

            print("Adding test employees...")
            success, _ = self.db.execute_query(self, INSERT_TEST_EMPLOYEES, fetch=False)
            if not success:
                print("Failed to add test employees")
                return False

            print("Adding test login credentials...")
            success, _ = self.db.execute_query(self, INSERT_TEST_LOGINS, fetch=False)
            if not success:
                print("Failed to add test login credentials")
                return False

            print("Database initialization completed successfully")
            return True

        except Exception as e:
            print(f"Error during database setup: {str(e)}")
            QMessageBox.critical(self, "Error", f"Database setup error: {str(e)}")
            return False

def setup_database():
    print("Starting database setup...")
    app = QApplication(sys.argv)
    setup = SetupWindow()
    setup.show()
    
    try:
        print("Testing database connection...")
        if not setup.db.test_connection(setup):
            print("Database connection failed")
            return 1
            
        print("Initializing database...")
        if setup.init_test_db():
            QMessageBox.information(setup, "Success", "Test database initialized successfully!")
            print("Database setup completed successfully")
            return 0
        else:
            QMessageBox.critical(setup, "Error", "Failed to initialize test database")
            print("Database initialization failed")
            return 1
            
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        QMessageBox.critical(setup, "Error", f"Unexpected error: {str(e)}")
        return 1
    finally:
        print("Cleaning up...")
        setup.close()
        time.sleep(1)  # Give time for the window to close

if __name__ == "__main__":
    print("Starting setup script...")
    sys.exit(setup_database())
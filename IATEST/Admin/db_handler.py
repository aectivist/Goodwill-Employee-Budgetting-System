from typing import Optional, Tuple, Any
import psycopg2
from psycopg2.extensions import connection
from PyQt5.QtWidgets import QMessageBox
from .db_logger import get_logger

class DatabaseHandler:
    """Handle database connections and errors"""
    
    def __init__(self):
        self.connection_params = {
            'host': 'localhost',
            'dbname': 'postgres',
            'user': 'postgres',
            'password': '12345',
            'port': 5432
        }
        self.logger = get_logger()

    def get_connection(self) -> Optional[connection]:
        """Get a database connection with error handling"""
        try:
            self.logger.log_operation("Database Connection", True)
            return psycopg2.connect(**self.connection_params)
        except psycopg2.Error as e:
            self.logger.log_operation("Database Connection", False, str(e))
            return None

    def execute_query(self, parent, query: str, params: Tuple = None, 
                     fetch: bool = True) -> Tuple[bool, Any]:
        """
        Execute a database query with error handling
        
        Args:
            parent: Parent widget for error messages
            query: SQL query to execute
            params: Query parameters
            fetch: Whether to fetch results
        
        Returns:
            Tuple of (success, result)
            - If fetch=True, result is fetched rows or None on error
            - If fetch=False, result is True/False indicating success
        """
        connection = None
        try:
            # Get connection
            connection = self.get_connection()
            if not connection:
                error_msg = "Could not connect to database"
                self.show_error(parent, error_msg)
                self.logger.log_error(error_msg)
                return False, None
            
            # Log query
            self.logger.log_query(query, params)
            
            # Execute query
            cursor = connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
                
            # Handle result
            if fetch:
                result = cursor.fetchall()
                connection.commit()
                self.logger.log_operation("Query Execute", True, f"Fetched {len(result)} rows")
                return True, result
            else:
                connection.commit()
                self.logger.log_operation("Query Execute", True, "No rows fetched (execute only)")
                return True, True
                
        except psycopg2.Error as e:
            if connection:
                connection.rollback()
            error_msg = f"Database error: {str(e)}"
            self.show_error(parent, error_msg)
            self.logger.log_error(error_msg)
            return False, None
            
        except Exception as e:
            if connection:
                connection.rollback()
            error_msg = f"Error: {str(e)}"
            self.show_error(parent, error_msg)
            self.logger.log_error(error_msg)
            return False, None
            
        finally:
            if connection:
                connection.close()
                self.logger.log_operation("Connection Close", True)

    def test_connection(self, parent) -> bool:
        """Test database connection and show status message"""
        connection = self.get_connection()
        if connection:
            connection.close()
            self.logger.log_operation("Connection Test", True)
            QMessageBox.information(parent, "Success", 
                                  "Successfully connected to database")
            return True
        else:
            error_msg = "Could not connect to database"
            self.show_error(parent, error_msg)
            self.logger.log_operation("Connection Test", False, error_msg)
            return False

    def show_error(self, parent, message: str):
        """Show error message to user"""
        QMessageBox.critical(parent, "Database Error", message)

# Global database handler instance
db = DatabaseHandler()

def get_db() -> DatabaseHandler:
    """Get the global database handler instance"""
    return db
import psycopg2
from datetime import datetime

class ActivityLogger:
    """Utility class for logging user activity"""

    @staticmethod
    def get_db_connection():
        return psycopg2.connect(
            host="localhost",
            dbname="postgres",
            user="postgres",
            password="12345",
            port=5432
        )

    @classmethod
    def log_login(cls, employee_id, username, success, details=None):
        """Log login attempts"""
        connection = None
        try:
            connection = cls.get_db_connection()
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO user_login_logs 
                (employeeid, username, action_type, action_details)
                VALUES (%s, %s, %s, %s)
            """, (
                employee_id,
                username,
                'LOGIN_SUCCESS' if success else 'LOGIN_FAILED',
                details
            ))

            connection.commit()
        except Exception as e:
            print(f"Failed to log login: {str(e)}")
            if connection:
                connection.rollback()
        finally:
            if connection:
                connection.close()

    @classmethod
    def log_page_access(cls, employee_id, username, page_name, details=None):
        """Log page/feature access"""
        connection = None
        try:
            connection = cls.get_db_connection()
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO user_login_logs 
                (employeeid, username, action_type, page_accessed, action_details)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                employee_id,
                username,
                'PAGE_ACCESS',
                page_name,
                details
            ))

            connection.commit()
        except Exception as e:
            print(f"Failed to log page access: {str(e)}")
            if connection:
                connection.rollback()
        finally:
            if connection:
                connection.close()

    @classmethod
    def log_change(cls, username, employee_id, action_type, affected_table, record_id, changes):
        """Log changes made to records"""
        connection = None
        try:
            connection = cls.get_db_connection()
            cursor = connection.cursor()
            
            cursor.execute("""
                INSERT INTO change_logs
                (username, employeeid, action_type, affected_table, record_id, changes)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                username,
                employee_id,
                action_type,
                affected_table,
                record_id,
                str(changes)
            ))
            
            connection.commit()
        except Exception as e:
            print(f"Failed to log change: {str(e)}")
            if connection:
                connection.rollback()
        finally:
            if connection:
                connection.close()
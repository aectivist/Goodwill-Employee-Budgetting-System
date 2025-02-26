#!/usr/bin/env python3
import logging
import os
from datetime import datetime

class DatabaseLogger:
    """Handle logging of database operations"""
    
    def __init__(self):
        # Create logs directory if it doesn't exist
        self.logs_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            'logs'
        )
        if not os.path.exists(self.logs_dir):
            os.makedirs(self.logs_dir)
        
        # Set up logger
        self.logger = logging.getLogger('DatabaseLogger')
        self.logger.setLevel(logging.INFO)
        
        # Create file handler
        log_file = os.path.join(
            self.logs_dir,
            f'database_{datetime.now().strftime("%Y%m%d")}.log'
        )
        handler = logging.FileHandler(log_file)
        handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        
        # Add handler to logger
        self.logger.addHandler(handler)
        
    def log_query(self, query: str, params: tuple = None):
        """Log a database query"""
        if params:
            self.logger.info(f"Query: {query} - Params: {params}")
        else:
            self.logger.info(f"Query: {query}")
            
    def log_error(self, error: str):
        """Log a database error"""
        self.logger.error(f"Database Error: {error}")
        
    def log_operation(self, operation: str, status: bool, details: str = None):
        """Log a database operation"""
        if status:
            self.logger.info(f"Operation: {operation} - Success")
            if details:
                self.logger.info(f"Details: {details}")
        else:
            self.logger.error(f"Operation: {operation} - Failed")
            if details:
                self.logger.error(f"Error: {details}")

# Global logger instance
db_logger = DatabaseLogger()

def get_logger() -> DatabaseLogger:
    """Get the global logger instance"""
    return db_logger
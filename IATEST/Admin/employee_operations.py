from PyQt5.QtWidgets import QMessageBox
from .db_handler import get_db

def load_employees(parent):
    """Load all employees from the database"""
    db = get_db()
    query = """
        SELECT employeeid, employeeName, employeeNumber, 
               DateOfChange, OrganizationSector, BranchId
        FROM employeeTable
        ORDER BY 
            CASE 
                WHEN employeeid LIKE 'ADMIN%' THEN 1 
                ELSE 2 
            END,
            CASE 
                WHEN employeeid LIKE 'ADMIN%' THEN employeeid 
                ELSE CAST(
                    CASE 
                        WHEN employeeid ~ '^[0-9]+$' THEN employeeid 
                        ELSE '0' 
                    END 
                AS INTEGER)::TEXT 
            END
    """
    success, result = db.execute_query(parent, query)
    return result if success else []

def get_next_employee_id(parent):
    """Get the next available employee ID"""
    db = get_db()
    query = """
        SELECT MAX(CAST(employeeid AS INTEGER))
        FROM employeeTable
        WHERE employeeid !~ '[^0-9]'  -- Only consider numeric IDs
    """
    success, result = db.execute_query(parent, query)
    
    if not success or not result:
        return None
        
    max_id = result[0][0]
    return '1' if max_id is None else str(int(max_id) + 1)

def add_employee(parent, employee_id, name, number, date, sector, branch_id):
    """Add a new employee to the database"""
    db = get_db()
    query = """
        INSERT INTO employeeTable
        (employeeid, employeeName, employeeNumber, DateOfChange,
         OrganizationSector, BranchId)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    params = (employee_id, name, number, date, sector, branch_id)
    success, _ = db.execute_query(parent, query, params, fetch=False)
    return success

def update_employee(parent, employee_id, name, number, date, sector, branch_id):
    """Update an existing employee in the database"""
    db = get_db()
    query = """
        UPDATE employeeTable
        SET employeeName = %s,
            employeeNumber = %s,
            DateOfChange = %s,
            OrganizationSector = %s,
            BranchId = %s
        WHERE employeeid = %s
    """
    params = (name, number, date, sector, branch_id, employee_id)
    success, _ = db.execute_query(parent, query, params, fetch=False)
    return success

def delete_employee(parent, employee_id):
    """Delete an employee from the database"""
    if employee_id.startswith('ADMIN'):
        QMessageBox.warning(parent, "Warning", "Admin accounts cannot be deleted.")
        return False
        
    db = get_db()
    query = "DELETE FROM employeeTable WHERE employeeid = %s"
    success, _ = db.execute_query(parent, query, (employee_id,), fetch=False)
    return success

def check_employee_exists(parent, employee_id):
    """Check if an employee exists"""
    db = get_db()
    query = "SELECT COUNT(*) FROM employeeTable WHERE employeeid = %s"
    success, result = db.execute_query(parent, query, (employee_id,))
    
    if not success:
        return False
    return result[0][0] > 0
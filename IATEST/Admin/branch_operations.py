from PyQt5.QtWidgets import QMessageBox
from .db_handler import get_db

def load_branches(parent):
    """Load all branches from the database"""
    db = get_db()
    query = """
        SELECT branchid, branchname, branchaddress
        FROM goodwillbranch
        ORDER BY CAST(branchid AS INTEGER)
    """
    success, result = db.execute_query(parent, query)
    return result if success else []

def get_next_branch_id(parent):
    """Get the next available branch ID"""
    db = get_db()
    query = """
        SELECT COALESCE(MAX(CAST(branchid AS INTEGER)), 0)
        FROM goodwillbranch
    """
    success, result = db.execute_query(parent, query)
    
    if not success or not result:
        return None
        
    return str(result[0][0] + 1)

def add_branch(parent, branch_id, name, address):
    """Add a new branch to the database"""
    db = get_db()
    query = """
        INSERT INTO goodwillbranch (branchid, branchname, branchaddress)
        VALUES (%s, %s, %s)
    """
    params = (branch_id, name, address)
    success, _ = db.execute_query(parent, query, params, fetch=False)
    return success

def update_branch(parent, branch_id, name, address):
    """Update an existing branch in the database"""
    db = get_db()
    query = """
        UPDATE goodwillbranch
        SET branchname = %s,
            branchaddress = %s
        WHERE branchid = %s
    """
    params = (name, address, branch_id)
    success, _ = db.execute_query(parent, query, params, fetch=False)
    return success

def check_branch_employees(parent, branch_id):
    """Check if a branch has any employees assigned to it"""
    db = get_db()
    query = """
        SELECT COUNT(*)
        FROM employeeTable
        WHERE BranchId = %s
    """
    success, result = db.execute_query(parent, query, (branch_id,))
    
    if not success:
        return -1  # Error condition
    return result[0][0]

def delete_branch(parent, branch_id):
    """Delete a branch from the database"""
    # First check if branch has employees
    employee_count = check_branch_employees(parent, branch_id)
    if employee_count < 0:  # Error occurred
        return False
    elif employee_count > 0:
        QMessageBox.warning(parent, "Warning",
            f"Cannot delete branch {branch_id}. It has {employee_count} employees assigned.")
        return False
    
    # Delete the branch
    db = get_db()
    query = "DELETE FROM goodwillbranch WHERE branchid = %s"
    success, _ = db.execute_query(parent, query, (branch_id,), fetch=False)
    return success

def check_branch_exists(parent, branch_id):
    """Check if a branch exists"""
    db = get_db()
    query = "SELECT COUNT(*) FROM goodwillbranch WHERE branchid = %s"
    success, result = db.execute_query(parent, query, (branch_id,))
    
    if not success:
        return False
    return result[0][0] > 0
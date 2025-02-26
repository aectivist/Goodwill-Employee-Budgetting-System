# Make IATEST.Admin a proper Python package
from .AdminProgram import AdminPanel
from .dialog_classes import EmployeeDialog, BranchDialog
from .db_handler import get_db
from .db_logger import get_logger
from . import employee_operations
from . import branch_operations

# Initialize global instances
db = get_db()
logger = get_logger()

print("Successfully imported IATEST.Admin package")
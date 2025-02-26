# Make IATEST a proper Python package
import os
import sys

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from . import Admin
    print("Successfully imported IATEST.Admin package")
except ImportError as e:
    print(f"Warning: Could not import Admin package: {e}")
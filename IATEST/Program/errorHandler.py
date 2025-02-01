import psycopg2
from datetime import datetime
from customtkinter import CTkToplevel, CTkLabel, CTkButton

def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        dbname="postgres",
        user="postgres",
        password="12345",
        port=5432
    )

def validate_budget_data(item, amount, value, branch_id):
    if not item or len(item) > 200:
        return False, "Invalid budget item name"
    try:
        amount = float(amount)
        value = float(value)
        branch_id = int(branch_id)
        if amount < 0 or value < 0:
            return False, "Amount and value must be positive"
        return True, ""
    except ValueError:
        return False, "Invalid numeric values"

def format_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return None

def execute_safe_query(cursor, query, params=None):
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return True, None
    except psycopg2.Error as e:
        return False, f"Database Error: {e}"
    except Exception as e:
        return False, f"Error: {e}"

def show_error_window(message):
    try:
        error_window = CTkToplevel()
        error_window.title("Error")
        error_window.geometry("400x150")
        error_window.resizable(False, False)
        
        # Center the window
        error_window.withdraw()  # Hide window initially
        error_window.after(0, lambda: center_error_window(error_window))
        
        # Error message
        CTkLabel(error_window, text="Error occurred:", 
                font=("Helvetica", 12, "bold")).pack(pady=10)
        CTkLabel(error_window, text=message, 
                wraplength=350).pack(pady=10)
        
        # OK button
        CTkButton(error_window, text="OK", 
                 command=error_window.destroy,
                 width=100).pack(pady=10)
        
        # Make window modal
        error_window.transient()
        error_window.grab_set()
        error_window.focus_set()
        
    except Exception as e:
        print(f"Failed to show error window: {str(e)}")
        print(f"Original error message: {message}")

def center_error_window(window):
    """Center the error window on screen"""
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')
    window.deiconify()  # Show window

def show_success_message(message, parent_widget=None):
    """Display a temporary success message that automatically disappears"""
    success_label = CTkLabel(
        parent_widget,
        text=message,
        text_color="green",
        font=("Helvetica", 10),
        height=25
    )
    success_label.place(relx=0.5, y=3, anchor='n')
    
    # Auto-destroy after 3 seconds
    if parent_widget:
        parent_widget.after(3000, success_label.destroy)

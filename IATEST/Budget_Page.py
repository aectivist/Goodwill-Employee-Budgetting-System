from customtkinter import *
import psycopg2
#https://github.com/Akascape/CTkTable

import math
from math import * #i'd like to complain about this, for some reason it won't load even tho it'scalled so please remember if ever trig or any math func is not working.
import re

from datetime import datetime 
from tkcalendar import DateEntry

from PIL import Image, ImageTk


conn=psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="12345", port=5432)

cur = conn.cursor()
window = CTk()
window.title("BUDGET")
window.geometry("600x400") #fml
window.resizable(0,0) #disable resize
set_appearance_mode("light")

#++++++++++++++++++++++++++++++ {PAGES} ++++++++++++++++++++++++++++++++++++++

# Create frames for each page
TABFRAME = CTkFrame(window, height=51, width=600, fg_color="#1E1E1E", corner_radius=0)
TABFRAME.pack(anchor=CENTER, fill=X)

#These are the individual pages, or rather, the frames

BudgetPage = CTkFrame(window)
BudgetPage.pack(fill=BOTH, expand=True)

# Create a list to hold all the pages
pages = [BudgetPage]

# Function to show a page
def show_page(page):
    page.pack(fill=BOTH, expand=True)
    window.update_idletasks()  # Update the UI
    if page == BudgetPage:
        budgetpage(BudgetPage)

#++++++++++++++++++++++++++++++ {PAGE FUNCTIONS} ++++++++++++++++++++++++++++++++++++++
#DO NOT EDIT SPACE, WILL USE SPACE FOR THE OTHER PAGES

#def clientpage(page):
#def assetpage(page):
#def calculator(page):

#IF DOES NOT WORK TRY THIS
#c:\Users\alive\OneDrive\Desktop\To-do\Internal-Assessment-Budgetting-System\.venv\Scripts\python.exe -m pip install psycopg2a

OutputCalculatorFont = CTkFont(family="Oswald", size=30, weight='bold')
EditFont = CTkFont(family="Oswald", size=15, weight='bold')

BudgetPagePost = 0
current_view = "table"  # Controls which view is shown - "table" or "add"

BudgetPageSwitcherBoolean = False

def budgetpage(page):
    global BudgetPagePost
    if BudgetPagePost == 0:
        # Create page layout
        PageMargin = CTkFrame(page)
        PageMargin.pack(expand=True)
        
        # Create main sections
        ControlsSection = CTkFrame(PageMargin, width=170, height=330, 
                                 fg_color="#dbdbdb", corner_radius=0, 
                                 border_color='#000000', border_width=1)
        ContentSection = CTkFrame(PageMargin, width=410, height=330, 
                                fg_color="#dbdbdb", corner_radius=0, 
                                border_color='#000000', border_width=1)
        
        ControlsSection.grid_propagate(False)
        ContentSection.grid_propagate(False)
        
        ControlsSection.grid(row=0, column=0, padx=5, pady=5)
        ContentSection.grid(row=0, column=1, padx=5, pady=5)

        # Summary section
        SummaryFrame = CTkFrame(ControlsSection, width=160, height=120)
        SummaryFrame.pack(pady=5, padx=5)
        
        CTkLabel(SummaryFrame, text="Budget Summary", font=EditFont).pack(pady=5)
        
        # Summary items
        summary_info = {
            "Total Budget": "₱0.00",
            "Used": "₱0.00",
            "Remaining": "₱0.00"
        }
        
        for label, value in summary_info.items():
            ItemFrame = CTkFrame(SummaryFrame)
            ItemFrame.pack(fill=X, pady=2, padx=5)
            CTkLabel(ItemFrame, text=label).pack(side=LEFT)
            CTkLabel(ItemFrame, text=value).pack(side=RIGHT)

        # Control buttons
        ButtonsFrame = CTkFrame(ControlsSection)
        ButtonsFrame.pack(pady=10, fill=X, padx=5)
        
        AddButton = CTkButton(ButtonsFrame, text="Add Budget", 
                            command=lambda: switch_view("add"))
        AddButton.pack(fill=X, pady=2)
        
        DeleteButton = CTkButton(ButtonsFrame, text="Delete Budget",
                               command=lambda: switch_view("delete"))
        DeleteButton.pack(fill=X, pady=2)
        
        ViewButton = CTkButton(ButtonsFrame, text="View All",
                             command=lambda: switch_view("table"))
        ViewButton.pack(fill=X, pady=2)

        # Content area
        TableFrame = CTkFrame(ContentSection)
        TableFrame.pack(expand=True, fill=BOTH, padx=5, pady=5)
        
        # Create table headers
        columns = ("ID", "Item", "Amount", "Value", "Issue Date", "Deadline", "Branch")
        tree = ttk.Treeview(TableFrame, columns=columns, show="headings", height=12)
        
        # Configure columns
        widths = [50, 120, 80, 80, 80, 80, 60]
        for col, width in zip(columns, widths):
            tree.column(col, width=width, anchor="center")
            tree.heading(col, text=col)
        
        # Add scrollbars
        y_scroll = ttk.Scrollbar(TableFrame, orient="vertical", command=tree.yview)
        x_scroll = ttk.Scrollbar(TableFrame, orient="horizontal", command=tree.xview)
        
        tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        
        tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")
        
        # Configure grid weights
        TableFrame.grid_rowconfigure(0, weight=1)
        TableFrame.grid_columnconfigure(0, weight=1)
        
        BudgetPagePost = 1
        refresh_budget_table(tree)
    else:
        print("Page already displayed")

def refresh_budget_table(tree):
    """Refresh the budget table with current data"""
    for item in tree.get_children():
        tree.delete(item)
    
    try:
        cur.execute("""
            SELECT b.BudgetId, b.BudgetItem, b.BudgetAmount, b.BudgetValue,
                   b.DateIssued, b.DateDeadline, g.BranchName
            FROM Budget b
            JOIN goodwillbranch g ON b.BranchId = g.BranchId
            ORDER BY b.DateIssued DESC
        """)
        
        for row in cur.fetchall():
            formatted_row = list(row)
            # Format dates
            formatted_row[4] = row[4].strftime("%Y-%m-%d")
            formatted_row[5] = row[5].strftime("%Y-%m-%d")
            # Format amounts
            formatted_row[2] = f"₱{row[2]:,.2f}"
            formatted_row[3] = f"₱{row[3]:,.2f}"
            tree.insert("", "end", values=formatted_row)
            
    except Exception as e:
        print(f"Error refreshing table: {e}")

def switch_view(view_type):
    """Switch between different views (add, delete, table)"""
    global current_view
    current_view = view_type
    
    if view_type == "add":
        show_add_budget_form()
    elif view_type == "delete":
        show_delete_budget_form()
    elif view_type == "table":
        refresh_budget_table(tree)

def show_add_budget_form():
    """Show form for adding new budget item"""
    form_window = CTkToplevel()
    form_window.title("Add Budget Item")
    form_window.geometry("400x500")
    
    # Add form fields
    CTkLabel(form_window, text="Budget Item:").pack(pady=5)
    item_entry = CTkEntry(form_window, width=300)
    item_entry.pack()
    
    CTkLabel(form_window, text="Amount:").pack(pady=5)
    amount_entry = CTkEntry(form_window, width=300)
    amount_entry.pack()
    
    CTkLabel(form_window, text="Value:").pack(pady=5)
    value_entry = CTkEntry(form_window, width=300)
    value_entry.pack()
    
    CTkLabel(form_window, text="Issue Date (YYYY-MM-DD):").pack(pady=5)
    issue_date = DateEntry(form_window, width=30)
    issue_date.pack()
    
    CTkLabel(form_window, text="Deadline (YYYY-MM-DD):").pack(pady=5)
    deadline = DateEntry(form_window, width=30)
    deadline.pack()
    
    CTkLabel(form_window, text="Branch ID:").pack(pady=5)
    branch_entry = CTkEntry(form_window, width=300)
    branch_entry.pack()
    
    def save_budget():
        try:
            cur.execute("""
                INSERT INTO Budget (BudgetId, BudgetItem, BudgetAmount, BudgetValue, 
                                 DateIssued, DateDeadline, BranchId)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                get_next_budget_id(),
                item_entry.get(),
                float(amount_entry.get()),
                float(value_entry.get()),
                issue_date.get_date(),
                deadline.get_date(),
                int(branch_entry.get())
            ))
            conn.commit()
            form_window.destroy()
            refresh_budget_table(tree)
        except Exception as e:
            show_error(str(e))
    
    CTkButton(form_window, text="Save", command=save_budget).pack(pady=20)

def show_delete_budget_form():
    """Show form for deleting budget item"""
    delete_window = CTkToplevel()
    delete_window.title("Delete Budget Item")
    delete_window.geometry("300x150")
    
    CTkLabel(delete_window, text="Budget ID:").pack(pady=5)
    id_entry = CTkEntry(delete_window, width=200)
    id_entry.pack()
    
    def delete_budget():
        try:
            cur.execute("DELETE FROM Budget WHERE BudgetId = %s", (id_entry.get(),))
            conn.commit()
            delete_window.destroy()
            refresh_budget_table(tree)
        except Exception as e:
            show_error(str(e))
    
    CTkButton(delete_window, text="Delete", command=delete_budget).pack(pady=20)

def get_next_budget_id():
    """Get next available budget ID"""
    cur.execute("SELECT MAX(BudgetId) FROM Budget")
    result = cur.fetchone()[0]
    return 1 if result is None else result + 1

def show_error(message):
    """Show error message"""
    error_window = CTkToplevel()
    error_window.title("Error")
    error_window.geometry("300x100")
    CTkLabel(error_window, text=message, wraplength=250).pack(pady=20)
    CTkButton(error_window, text="OK", command=error_window.destroy).pack()

#++++++++++++++++++++++++++++++ {TAB FUNCTIONS} ++++++++++++++++++++++++++++++++++++++

# Function to handle button clicks
def button_event(page):
    salespage(page)

SalesTab = CTkButton(TABFRAME, text="Sales", width=20)
SalesTab.grid(row=0, column=1, pady=10, padx=10, sticky="nsew")

BudgetTab = CTkButton(TABFRAME, text="Budget", width=20)
BudgetTab.grid(row=0, column=2, pady=10, padx=10, sticky="nsew")

SalesTab.configure(command=lambda: button_event(BudgetPage))
BudgetTab.configure(command=lambda: button_event(BudgetPage))

# Show the first page by default
show_page(BudgetPage)

window.mainloop()

#am cooked

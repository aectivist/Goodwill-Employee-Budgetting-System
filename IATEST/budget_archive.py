from customtkinter import *
from tkinter import ttk
import psycopg2
from datetime import datetime

class BudgetArchive:
    def __init__(self, page):
        self.page = page
        self.conn = psycopg2.connect(
            host="localhost",
            dbname="postgres",
            user="postgres",
            password="12345",
            port=5432
        )
        self.cur = self.conn.cursor()
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        self.main_frame = CTkFrame(self.page)
        self.main_frame.pack(expand=True, fill=BOTH, padx=5, pady=5)
        
        # Setup treeview
        self.setup_treeview()
        self.load_archives()

    def setup_treeview(self):
        columns = ("Item", "Amount", "Value", "Issued", "Deadline", "Branch", "Archived", "Method")
        self.tree = ttk.Treeview(self.main_frame, columns=columns, show="headings")
        
        # Configure columns
        widths = {
            "Item": 150,
            "Amount": 100,
            "Value": 100,
            "Issued": 100,
            "Deadline": 100,
            "Branch": 80,
            "Archived": 100,
            "Method": 150
        }
        
        for col, width in widths.items():
            self.tree.column(col, width=width)
            self.tree.heading(col, text=col)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def load_archives(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Load data
        self.cur.execute("""
            SELECT a_BudgetItem, a_BudgetAmount, a_BudgetValue, 
                   TO_CHAR(a_DateIssued, 'YYYY-MM-DD'), 
                   TO_CHAR(a_DateDeadline, 'YYYY-MM-DD'),
                   BranchId, TO_CHAR(DateArchived, 'YYYY-MM-DD'),
                   MethodOfArchival
            FROM archived 
            ORDER BY DateArchived DESC
        """)
        
        for row in self.cur.fetchall():
            self.tree.insert("", "end", values=row)
            
    def archive_budgets(self, budgets, method="Manual Archive"):
        """
        Archive selected budgets
        budgets: list of tuples containing budget data (BudgetId, BudgetItem, etc.)
        method: string indicating the method of archival
        """
        try:
            for budget in budgets:
                budget_id = budget[0]
                
                # Insert into archived table
                self.cur.execute("""
                    INSERT INTO archived (
                        a_BudgetItem, a_BudgetAmount, a_BudgetValue,
                        a_DateIssued, a_DateDeadline, BranchId,
                        DateArchived, MethodOfArchival
                    )
                    SELECT 
                        BudgetItem, BudgetAmount, BudgetValue,
                        DateIssued, DateDeadline, BranchId,
                        CURRENT_DATE, %s
                    FROM Budget
                    WHERE BudgetId = %s
                """, (method, budget_id))
                
                # Delete from Budget table
                self.cur.execute("DELETE FROM Budget WHERE BudgetId = %s", (budget_id,))
                
            self.conn.commit()
            self.load_archives()
            return True
        except Exception as e:
            print(f"Error archiving budgets: {e}")
            self.conn.rollback()
            return False
            
    def check_deadlines(self):
        """
        Check for budgets that have reached their deadline and archive them
        """
        now = datetime.now()
        if now.strftime("%H:%M:%S") == "12:00:00":
            try:
                self.cur.execute("""
                    SELECT BudgetId, BudgetItem, BudgetAmount, BudgetValue, 
                           DateIssued, DateDeadline, BranchId
                    FROM Budget
                    WHERE DateDeadline <= CURRENT_DATE
                """)
                
                expired_budgets = self.cur.fetchall()
                if expired_budgets:
                    self.archive_budgets(expired_budgets, "Automatic Archive - Deadline Reached")
                    
            except Exception as e:
                print(f"Error in deadline check: {e}")

    def __del__(self):
        """
        Cleanup database connections
        """
        if hasattr(self, 'cur'):
            self.cur.close()
        if hasattr(self, 'conn'):
            self.conn.close()
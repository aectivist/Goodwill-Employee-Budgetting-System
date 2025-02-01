from customtkinter import *
from tkinter import ttk

class ArchiveTable:
    def __init__(self, parent, cursor):
        self.parent = parent
        self.cur = cursor
        
        # Create frame for Treeview and scrollbars
        self.frame = CTkFrame(parent)
        self.frame.pack(fill=BOTH, expand=True)
        
        self.setup_table()
        self.load_data()
        
    def setup_table(self):
        # Create Treeview
        self.tree = ttk.Treeview(self.frame, 
                                columns=("Item", "Amount", "Value", "Issued", "Deadline", 
                                       "Branch", "Archived", "Method"),
                                show="headings")

        # Configure headings and columns
        columns = {
            "Item": ("Item", 150),
            "Amount": ("Amount", 80),
            "Value": ("Value", 80),
            "Issued": ("Issued Date", 100),
            "Deadline": ("Deadline", 100),
            "Branch": ("Branch", 80),
            "Archived": ("Archive Date", 100),
            "Method": ("Archive Method", 150)
        }
        
        for col, (text, width) in columns.items():
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width)

        # Add scrollbars
        y_scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        x_scrollbar = ttk.Scrollbar(self.frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

        # Grid layout
        self.tree.grid(row=0, column=0, sticky="nsew")
        y_scrollbar.grid(row=0, column=1, sticky="ns")
        x_scrollbar.grid(row=1, column=0, sticky="ew")

        # Configure grid weights
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

    def load_data(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Fetch and insert archived data
        self.cur.execute("""
            SELECT a_BudgetItem, a_BudgetAmount, a_BudgetValue, 
                   TO_CHAR(a_DateIssued, 'YYYY-MM-DD'), 
                   TO_CHAR(a_DateDeadline, 'YYYY-MM-DD'),
                   BranchId, TO_CHAR(DateArchived, 'YYYY-MM-DD'),
                   MethodOfArchival
            FROM archived 
            ORDER BY DateArchived DESC
        """)
        
        for item in self.cur.fetchall():
            self.tree.insert("", "end", values=item)

    def refresh(self):
        self.load_data()

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

    def pack_forget(self):
        self.frame.pack_forget()

    def grid(self, **kwargs):
        self.frame.grid(**kwargs)

    def grid_forget(self):
        self.frame.grid_forget()
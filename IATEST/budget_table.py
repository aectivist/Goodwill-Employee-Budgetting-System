from customtkinter import *
from tkinter import ttk

class BudgetTable:
    def __init__(self, parent, cursor, on_selection_change=None):
        self.parent = parent
        self.cur = cursor
        self.on_selection_change = on_selection_change
        
        # Create frame for Treeview and scrollbars
        self.frame = CTkFrame(parent)
        self.frame.pack(fill=BOTH, expand=True)
        
        self.setup_table()
        self.load_data()
        
    def setup_table(self):
        # Create Treeview
        self.tree = ttk.Treeview(self.frame, 
                                columns=("ID", "Item", "Amount", "Value", "Date Issued", "Deadline", "Branch"), 
                                show="headings", 
                                selectmode="extended")

        # Configure headings
        headings = {
            "ID": ("ID", 50),
            "Item": ("Item", 150),
            "Amount": ("Amount", 80),
            "Value": ("Value", 80),
            "Date Issued": ("Date Issued", 100),
            "Deadline": ("Deadline", 100),
            "Branch": ("Branch", 80)
        }
        
        for col, (text, width) in headings.items():
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

        # Bind selection event
        if self.on_selection_change:
            self.tree.bind('<<TreeviewSelect>>', self.on_select)

    def on_select(self, event):
        if self.on_selection_change:
            selected_items = self.tree.selection()
            selected_data = []
            for item in selected_items:
                values = self.tree.item(item)['values']
                selected_data.append(values)
            self.on_selection_change(selected_data)

    def load_data(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Fetch and insert data
        self.cur.execute("""
            SELECT BudgetId, BudgetItem, BudgetAmount, BudgetValue, 
                   TO_CHAR(DateIssued, 'YYYY-MM-DD'), 
                   TO_CHAR(DateDeadline, 'YYYY-MM-DD'),
                   BranchId 
            FROM Budget 
            ORDER BY BudgetId
        """)
        
        for item in self.cur.fetchall():
            self.tree.insert("", "end", values=item)

    def get_selected_items(self):
        selected_items = self.tree.selection()
        return [self.tree.item(item)['values'] for item in selected_items]

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
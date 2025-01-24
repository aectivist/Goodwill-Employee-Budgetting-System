from customtkinter import *
from tkinter import ttk
import psycopg2
from datetime import datetime

class BudgetManagement:
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
        
        # Buttons frame
        self.button_frame = CTkFrame(self.main_frame)
        self.button_frame.pack(fill=X, pady=5)
        
        # Action buttons
        CTkButton(self.button_frame, text="Create Budget", 
                 command=self.create_budget).pack(side=LEFT, padx=5)
        CTkButton(self.button_frame, text="Edit Budget", 
                 command=self.edit_budget).pack(side=LEFT, padx=5)
        CTkButton(self.button_frame, text="Delete Budget", 
                 command=self.delete_budget).pack(side=LEFT, padx=5)
        
        # Setup treeview
        self.setup_treeview()
        self.load_budgets()

    def setup_treeview(self):
        columns = ("ID", "Item", "Amount", "Value", "Date Issued", "Deadline", "Branch")
        self.tree = ttk.Treeview(self.main_frame, columns=columns, show="headings")
        
        # Configure columns
        self.tree.column("ID", width=50)
        self.tree.column("Item", width=150)
        self.tree.column("Amount", width=100)
        self.tree.column("Value", width=100)
        self.tree.column("Date Issued", width=100)
        self.tree.column("Deadline", width=100)
        self.tree.column("Branch", width=80)
        
        # Configure headings
        for col in columns:
            self.tree.heading(col, text=col)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def load_budgets(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Load data
        self.cur.execute("""
            SELECT BudgetId, BudgetItem, BudgetAmount, BudgetValue, 
                   TO_CHAR(DateIssued, 'YYYY-MM-DD'), 
                   TO_CHAR(DateDeadline, 'YYYY-MM-DD'),
                   BranchId 
            FROM Budget 
            ORDER BY BudgetId
        """)
        
        for row in self.cur.fetchall():
            self.tree.insert("", "end", values=row)

    def create_budget(self):
        dialog = CTkToplevel(self.page)
        dialog.title("Create Budget")
        dialog.geometry("400x500")
        dialog.grab_set()

        frame = CTkFrame(dialog)
        frame.pack(expand=True, fill=BOTH, padx=10, pady=10)

        labels = ["Budget Item:", "Budget Amount:", "Budget Value:", 
                 "Date Issued (YYYY-MM-DD):", "Date Deadline (YYYY-MM-DD):", "Branch ID:"]
        entries = []

        for label in labels:
            CTkLabel(frame, text=label).pack(pady=(10,0))
            entry = CTkEntry(frame, width=300)
            entry.pack(pady=(0,10))
            entries.append(entry)

        def submit():
            try:
                values = [
                    entries[0].get(),
                    float(entries[1].get()),
                    float(entries[2].get()),
                    entries[3].get(),
                    entries[4].get(),
                    int(entries[5].get())
                ]
                self.cur.execute("""
                    INSERT INTO Budget (BudgetItem, BudgetAmount, BudgetValue, 
                                    DateIssued, DateDeadline, BranchId)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, values)
                self.conn.commit()
                dialog.destroy()
                self.load_budgets()
            except Exception as e:
                print(f"Error creating budget: {e}")

        CTkButton(frame, text="Create", command=submit, width=200).pack(pady=20)

    def edit_budget(self):
        selected = self.tree.selection()
        if not selected:
            print("Please select a budget to edit")
            return

        item = self.tree.item(selected[0])
        budget_id = item['values'][0]

        dialog = CTkToplevel(self.page)
        dialog.title("Edit Budget")
        dialog.geometry("400x500")
        dialog.grab_set()

        frame = CTkFrame(dialog)
        frame.pack(expand=True, fill=BOTH, padx=10, pady=10)

        labels = ["Budget Item:", "Budget Amount:", "Budget Value:", 
                 "Date Issued (YYYY-MM-DD):", "Date Deadline (YYYY-MM-DD):", "Branch ID:"]
        entries = []

        for label, value in zip(labels, item['values'][1:]):
            CTkLabel(frame, text=label).pack(pady=(10,0))
            entry = CTkEntry(frame, width=300)
            entry.insert(0, str(value))
            entry.pack(pady=(0,10))
            entries.append(entry)

        def save_changes():
            try:
                values = [entry.get() for entry in entries]
                self.cur.execute("""
                    UPDATE Budget 
                    SET BudgetItem = %s, BudgetAmount = %s, BudgetValue = %s,
                        DateIssued = %s, DateDeadline = %s, BranchId = %s
                    WHERE BudgetId = %s
                """, (*values, budget_id))
                self.conn.commit()
                dialog.destroy()
                self.load_budgets()
            except Exception as e:
                print(f"Error saving changes: {e}")

        CTkButton(frame, text="Save Changes", command=save_changes, width=200).pack(pady=20)

    def delete_budget(self):
        selected = self.tree.selection()
        if not selected:
            print("Please select a budget to delete")
            return

        if len(selected) > 1:
            print("Please select only one budget to delete")
            return

        budget_id = self.tree.item(selected[0])['values'][0]

        dialog = CTkToplevel(self.page)
        dialog.title("Delete Budget")
        dialog.geometry("300x150")
        dialog.grab_set()

        CTkLabel(dialog, text="Are you sure you want to delete this budget?").pack(pady=20)

        def confirm_delete():
            try:
                self.cur.execute("DELETE FROM Budget WHERE BudgetId = %s", (budget_id,))
                self.conn.commit()
                dialog.destroy()
                self.load_budgets()
            except Exception as e:
                print(f"Error deleting budget: {e}")

        CTkButton(dialog, text="Delete", command=confirm_delete, width=100).pack(pady=10)
        CTkButton(dialog, text="Cancel", command=dialog.destroy, width=100).pack(pady=10)
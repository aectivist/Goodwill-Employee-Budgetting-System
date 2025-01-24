from customtkinter import *
from tkinter import ttk, messagebox
import psycopg2
from datetime import datetime
from tkcalendar import DateEntry

class BudgetPage:
    def __init__(self, page):
        self.page = page
        self.current_status = "budget"
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
        # Clear existing content
        for widget in self.page.winfo_children():
            widget.destroy()

        # Main container
        self.main_frame = CTkFrame(self.page)
        self.main_frame.pack(expand=True, fill=BOTH)

        # Status toggle frame at top
        self.status_frame = CTkFrame(self.main_frame)
        self.status_frame.pack(fill=X, padx=5, pady=5)

        # Content frame below status
        self.content_frame = CTkFrame(self.main_frame)
        self.content_frame.pack(expand=True, fill=BOTH, padx=5, pady=5)

        # Status toggle buttons
        self.budget_btn = CTkButton(
            self.status_frame,
            text="Budget Status",
            command=lambda: self.switch_status("budget")
        )
        self.budget_btn.pack(side=LEFT, expand=True, padx=5)

        self.archive_btn = CTkButton(
            self.status_frame,
            text="Archive Status",
            command=lambda: self.switch_status("archive")
        )
        self.archive_btn.pack(side=LEFT, expand=True, padx=5)

    def create_budget_dialog(self):
        dialog = CTkToplevel(self.page)
        dialog.title("Create Budget")
        dialog.geometry("400x600")
        dialog.grab_set()

        # Main frame with scrollbar
        canvas = CTkCanvas(dialog)
        scrollbar = ttk.Scrollbar(dialog, orient="vertical", command=canvas.yview)
        frame = CTkFrame(canvas)

        frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Form title
        title_label = CTkLabel(frame, text="Create New Budget", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=(20, 20))

        # Form fields frame
        fields_frame = CTkFrame(frame)
        fields_frame.pack(fill=X, padx=20)

        # Budget Item
        CTkLabel(fields_frame, text="Budget Item:").pack(anchor=W, pady=(10,0))
        item_entry = CTkEntry(fields_frame, width=300)
        item_entry.pack(fill=X, pady=(0,10))

        # Budget Amount
        CTkLabel(fields_frame, text="Budget Amount:").pack(anchor=W, pady=(10,0))
        amount_entry = CTkEntry(fields_frame, width=300)
        amount_entry.pack(fill=X, pady=(0,10))

        # Budget Value
        CTkLabel(fields_frame, text="Budget Value:").pack(anchor=W, pady=(10,0))
        value_entry = CTkEntry(fields_frame, width=300)
        value_entry.pack(fill=X, pady=(0,10))

        # Date Issued
        CTkLabel(fields_frame, text="Date Issued:").pack(anchor=W, pady=(10,0))
        issued_frame = CTkFrame(fields_frame, fg_color="transparent")
        issued_frame.pack(fill=X, pady=(0,10))
        issued_date = DateEntry(issued_frame, width=47, background='darkblue',
                              foreground='white', borderwidth=2)
        issued_date.pack()

        # Date Deadline
        CTkLabel(fields_frame, text="Date Deadline:").pack(anchor=W, pady=(10,0))
        deadline_frame = CTkFrame(fields_frame, fg_color="transparent")
        deadline_frame.pack(fill=X, pady=(0,10))
        deadline_date = DateEntry(deadline_frame, width=47, background='darkblue',
                                foreground='white', borderwidth=2)
        deadline_date.pack()

        # Branch ID
        CTkLabel(fields_frame, text="Branch ID:").pack(anchor=W, pady=(10,0))
        branch_entry = CTkEntry(fields_frame, width=300)
        branch_entry.pack(fill=X, pady=(0,10))

        def submit():
            if not item_entry.get().strip():
                messagebox.showerror("Error", "Please enter a Budget Item")
                return

            try:
                # Generate new budget ID
                self.cur.execute("SELECT MAX(BudgetId) FROM Budget")
                result = self.cur.fetchone()
                new_budget_id = 1 if result[0] is None else result[0] + 1

                values = [
                    new_budget_id,
                    item_entry.get().strip(),
                    float(amount_entry.get()),
                    float(value_entry.get()),
                    issued_date.get_date().strftime('%Y-%m-%d'),
                    deadline_date.get_date().strftime('%Y-%m-%d'),
                    int(branch_entry.get())
                ]

                self.cur.execute("""
                    INSERT INTO Budget (BudgetId, BudgetItem, BudgetAmount, BudgetValue,
                                    DateIssued, DateDeadline, BranchId)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, values)
                self.conn.commit()
                
                messagebox.showinfo("Success", "Budget created successfully!")
                dialog.destroy()
                self.show_budget_content()
                
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric values")
            except Exception as e:
                messagebox.showerror("Error", f"Error creating budget: {str(e)}")
                print(f"Error creating budget: {e}")

        # Buttons frame
        button_frame = CTkFrame(frame, fg_color="transparent")
        button_frame.pack(pady=20)

        CTkButton(button_frame, text="Confirm", command=submit, width=100).pack(side=LEFT, padx=10)
        CTkButton(button_frame, text="Cancel", command=dialog.destroy, width=100).pack(side=LEFT, padx=10)

        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")

    def create_tree_with_scrollbars(self, parent, columns, show="headings"):
        # Create frame for Treeview and scrollbars
        tree_frame = CTkFrame(parent)
        tree_frame.pack(fill=BOTH, expand=True)

        # Create Treeview
        tree = ttk.Treeview(tree_frame, columns=columns, show=show, selectmode="extended")

        # Add scrollbars
        y_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        x_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

        # Grid layout
        tree.grid(row=0, column=0, sticky="nsew")
        y_scrollbar.grid(row=0, column=1, sticky="ns")
        x_scrollbar.grid(row=1, column=0, sticky="ew")

        # Configure grid weights
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        return tree

    def edit_budget_dialog(self):
        selected = self.budget_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a budget to edit")
            return

        if len(selected) > 1:
            messagebox.showwarning("Warning", "Please select only one budget to edit")
            return

        values = self.budget_tree.item(selected[0])['values']
        budget_id = values[0]

        dialog = CTkToplevel(self.page)
        dialog.title("Edit Budget")
        dialog.geometry("400x600")
        dialog.grab_set()

        # Main frame with scrollbar
        canvas = CTkCanvas(dialog)
        scrollbar = ttk.Scrollbar(dialog, orient="vertical", command=canvas.yview)
        frame = CTkFrame(canvas)

        frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Form title
        title_label = CTkLabel(frame, text="Edit Budget", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=(20, 20))

        # Form fields frame
        fields_frame = CTkFrame(frame)
        fields_frame.pack(fill=X, padx=20)

        # Budget Item
        CTkLabel(fields_frame, text="Budget Item:").pack(anchor=W, pady=(10,0))
        item_entry = CTkEntry(fields_frame, width=300)
        item_entry.insert(0, values[1])
        item_entry.pack(fill=X, pady=(0,10))

        # Budget Amount
        CTkLabel(fields_frame, text="Budget Amount:").pack(anchor=W, pady=(10,0))
        amount_entry = CTkEntry(fields_frame, width=300)
        amount_entry.insert(0, values[2])
        amount_entry.pack(fill=X, pady=(0,10))

        # Budget Value
        CTkLabel(fields_frame, text="Budget Value:").pack(anchor=W, pady=(10,0))
        value_entry = CTkEntry(fields_frame, width=300)
        value_entry.insert(0, values[3])
        value_entry.pack(fill=X, pady=(0,10))

        # Date Issued
        CTkLabel(fields_frame, text="Date Issued:").pack(anchor=W, pady=(10,0))
        issued_frame = CTkFrame(fields_frame, fg_color="transparent")
        issued_frame.pack(fill=X, pady=(0,10))
        issued_date = DateEntry(issued_frame, width=47, background='darkblue',
                              foreground='white', borderwidth=2)
        issued_date.set_date(datetime.strptime(values[4], '%Y-%m-%d'))
        issued_date.pack()

        # Date Deadline
        CTkLabel(fields_frame, text="Date Deadline:").pack(anchor=W, pady=(10,0))
        deadline_frame = CTkFrame(fields_frame, fg_color="transparent")
        deadline_frame.pack(fill=X, pady=(0,10))
        deadline_date = DateEntry(deadline_frame, width=47, background='darkblue',
                                foreground='white', borderwidth=2)
        deadline_date.set_date(datetime.strptime(values[5], '%Y-%m-%d'))
        deadline_date.pack()

        # Branch ID
        CTkLabel(fields_frame, text="Branch ID:").pack(anchor=W, pady=(10,0))
        branch_entry = CTkEntry(fields_frame, width=300)
        branch_entry.insert(0, values[6])
        branch_entry.pack(fill=X, pady=(0,10))

        def save_changes():
            if not item_entry.get().strip():
                messagebox.showerror("Error", "Please enter a Budget Item")
                return

            try:
                values = [
                    item_entry.get().strip(),
                    float(amount_entry.get()),
                    float(value_entry.get()),
                    issued_date.get_date().strftime('%Y-%m-%d'),
                    deadline_date.get_date().strftime('%Y-%m-%d'),
                    int(branch_entry.get()),
                    budget_id
                ]

                self.cur.execute("""
                    UPDATE Budget
                    SET BudgetItem = %s, BudgetAmount = %s, BudgetValue = %s,
                        DateIssued = %s, DateDeadline = %s, BranchId = %s
                    WHERE BudgetId = %s
                """, values)
                self.conn.commit()
                
                messagebox.showinfo("Success", "Budget updated successfully!")
                dialog.destroy()
                self.refresh_budget_table()
                
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric values")
            except Exception as e:
                messagebox.showerror("Error", f"Error updating budget: {str(e)}")
                print(f"Error updating budget: {e}")

        # Buttons frame
        button_frame = CTkFrame(frame, fg_color="transparent")
        button_frame.pack(pady=20)

        CTkButton(button_frame, text="Save", command=save_changes, width=100).pack(side=LEFT, padx=10)
        CTkButton(button_frame, text="Cancel", command=dialog.destroy, width=100).pack(side=LEFT, padx=10)

        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")

    def show_budget_content(self):
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Button frame
        button_frame = CTkFrame(self.content_frame)
        button_frame.pack(fill=X, pady=5)

        # Action buttons
        CTkButton(button_frame, text="Create Budget",
                 command=self.create_budget_dialog).pack(side=LEFT, padx=5)
        CTkButton(button_frame, text="Edit Budget",
                 command=self.edit_budget_dialog).pack(side=LEFT, padx=5)
        CTkButton(button_frame, text="Delete Budget",
                 command=self.delete_budget).pack(side=LEFT, padx=5)
        CTkButton(button_frame, text="Archive Selected",
                 command=self.archive_selected).pack(side=LEFT, padx=5)

        # Create Treeview with scrollbars
        columns = ("ID", "Item", "Amount", "Value", "Date Issued", "Deadline", "Branch")
        self.budget_tree = self.create_tree_with_scrollbars(self.content_frame, columns)

        # Configure columns
        columns_config = {
            "ID": (50, "ID"),
            "Item": (150, "Item"),
            "Amount": (80, "Amount"),
            "Value": (80, "Value"),
            "Date Issued": (100, "Date Issued"),
            "Deadline": (100, "Deadline"),
            "Branch": (80, "Branch")
        }

        for col, (width, text) in columns_config.items():
            self.budget_tree.heading(col, text=text)
            self.budget_tree.column(col, width=width)

        # Load data
        self.refresh_budget_table()

    def refresh_budget_table(self):
        # Clear existing items
        for item in self.budget_tree.get_children():
            self.budget_tree.delete(item)

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
            self.budget_tree.insert("", "end", values=item)

    def delete_budget(self):
        selected = self.budget_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a budget to delete")
            return

        if len(selected) > 1:
            messagebox.showwarning("Warning", "Please select only one budget to delete")
            return

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this budget?"):
            try:
                budget_id = self.budget_tree.item(selected[0])['values'][0]
                self.cur.execute("DELETE FROM Budget WHERE BudgetId = %s", (budget_id,))
                self.conn.commit()
                self.refresh_budget_table()
                messagebox.showinfo("Success", "Budget deleted successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting budget: {str(e)}")
                self.conn.rollback()

    def archive_selected(self):
        selected = self.budget_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "No budgets selected for archiving")
            return

        try:
            for item in selected:
                values = self.budget_tree.item(item)['values']
                budget_id = values[0]
                
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
                        CURRENT_DATE, 'Manual Archive'
                    FROM Budget
                    WHERE BudgetId = %s
                """, (budget_id,))
                
                # Delete from Budget table
                self.cur.execute("DELETE FROM Budget WHERE BudgetId = %s", (budget_id,))
                
            self.conn.commit()
            self.refresh_budget_table()
            messagebox.showinfo("Success", "Selected budgets archived successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Error archiving budgets: {str(e)}")
            self.conn.rollback()

    def show_archive_content(self):
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Create frame for Treeview and scrollbars
        columns = ("Item", "Amount", "Value", "Issued", "Deadline", "Branch", "Archived", "Method")
        self.archive_tree = self.create_tree_with_scrollbars(self.content_frame, columns)

        # Configure columns
        columns_config = {
            "Item": (150, "Item"),
            "Amount": (80, "Amount"),
            "Value": (80, "Value"),
            "Issued": (100, "Issued Date"),
            "Deadline": (100, "Deadline"),
            "Branch": (80, "Branch"),
            "Archived": (100, "Archive Date"),
            "Method": (150, "Archive Method")
        }

        for col, (width, text) in columns_config.items():
            self.archive_tree.heading(col, text=text)
            self.archive_tree.column(col, width=width)

        # Load archive data
        self.refresh_archive_table()

    def refresh_archive_table(self):
        # Clear existing items
        for item in self.archive_tree.get_children():
            self.archive_tree.delete(item)

        # Fetch and insert archive data
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
            self.archive_tree.insert("", "end", values=item)

    def start_deadline_checker(self):
        self.check_deadlines()
        self.page.after(1000, self.start_deadline_checker)

    def check_deadlines(self):
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
                for budget in expired_budgets:
                    budget_id = budget[0]
                    budget_data = budget[1:]
                    
                    self.cur.execute("""
                        INSERT INTO archived (
                            a_BudgetItem, a_BudgetAmount, a_BudgetValue,
                            a_DateIssued, a_DateDeadline, BranchId,
                            DateArchived, MethodOfArchival
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, CURRENT_DATE, 'Automatic Archive - Deadline Reached')
                    """, budget_data)
                    
                    self.cur.execute("DELETE FROM Budget WHERE BudgetId = %s", (budget_id,))
                    self.conn.commit()
                
                if expired_budgets:
                    if self.current_status == "budget":
                        self.refresh_budget_table()
                    else:
                        self.refresh_archive_table()
                    print(f"Auto-archived {len(expired_budgets)} expired budgets")
                    
            except Exception as e:
                print(f"Error in deadline check: {e}")

    def __init__(self, page):
        self.page = page
        self.current_status = "budget"
        self.conn = psycopg2.connect(
            host="localhost",
            dbname="postgres",
            user="postgres",
            password="12345",
            port=5432
        )
        self.cur = self.conn.cursor()
        self.setup_ui()
        self.start_deadline_checker()  # Start the deadline checker

    def switch_status(self, status):
        self.current_status = status
        if status == "budget":
            self.budget_btn.configure(fg_color="#2B2B2B")
            self.archive_btn.configure(fg_color="#4B4B4B")
            self.show_budget_content()
        else:
            self.budget_btn.configure(fg_color="#4B4B4B")
            self.archive_btn.configure(fg_color="#2B2B2B")
            self.show_archive_content()

def budgetpage(page):
    return BudgetPage(page)

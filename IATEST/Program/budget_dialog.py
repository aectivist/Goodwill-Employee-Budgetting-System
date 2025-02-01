from customtkinter import *
from tkcalendar import DateEntry
from tkinter import messagebox
from datetime import datetime

class BudgetDialog:
    def __init__(self, parent, cursor, conn, on_success):
        self.dialog = CTkToplevel(parent)
        self.dialog.title("Create Budget")
        self.dialog.geometry("400x550")
        self.dialog.grab_set()
        
        self.cur = cursor
        self.conn = conn
        self.on_success = on_success
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        frame = CTkFrame(self.dialog)
        frame.pack(expand=True, fill=BOTH, padx=20, pady=20)

        # Form title
        title_label = CTkLabel(frame, text="Create New Budget", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=(0, 20))

        # Form fields frame
        fields_frame = CTkFrame(frame)
        fields_frame.pack(fill=X, padx=10)

        # Budget Item
        self.create_field(fields_frame, "Budget Item:", "item")

        # Budget Amount
        self.create_field(fields_frame, "Budget Amount:", "amount")

        # Budget Value
        self.create_field(fields_frame, "Budget Value:", "value")

        # Date Issued
        self.create_date_field(fields_frame, "Date Issued:", "issued")

        # Date Deadline
        self.create_date_field(fields_frame, "Date Deadline:", "deadline")

        # Branch ID
        self.create_field(fields_frame, "Branch ID:", "branch")

        # Buttons frame
        button_frame = CTkFrame(frame, fg_color="transparent")
        button_frame.pack(pady=20)

        confirm_btn = CTkButton(button_frame, text="Confirm", command=self.submit, width=100)
        confirm_btn.pack(side=LEFT, padx=10)

        cancel_btn = CTkButton(button_frame, text="Cancel", command=self.dialog.destroy, width=100)
        cancel_btn.pack(side=LEFT, padx=10)

    def create_field(self, parent, label_text, field_name):
        label = CTkLabel(parent, text=label_text)
        label.pack(anchor=W, pady=(10, 0))
        entry = CTkEntry(parent, width=300)
        entry.pack(fill=X, pady=(0, 10))
        setattr(self, f"{field_name}_entry", entry)

    def create_date_field(self, parent, label_text, field_name):
        label = CTkLabel(parent, text=label_text)
        label.pack(anchor=W, pady=(10, 0))
        frame = CTkFrame(parent, fg_color="transparent")
        frame.pack(fill=X, pady=(0, 10))
        date_entry = DateEntry(frame, width=47, background='darkblue',
                             foreground='white', borderwidth=2)
        date_entry.pack()
        setattr(self, f"{field_name}_date", date_entry)

    def validate_inputs(self):
        if not self.item_entry.get().strip():
            messagebox.showerror("Error", "Please enter a Budget Item")
            return False

        try:
            float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid Budget Amount")
            return False

        try:
            float(self.value_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid Budget Value")
            return False

        try:
            int(self.branch_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid Branch ID")
            return False

        return True

    def submit(self):
        if not self.validate_inputs():
            return

        try:
            values = [
                self.item_entry.get().strip(),
                float(self.amount_entry.get()),
                float(self.value_entry.get()),
                self.issued_date.get_date().strftime('%Y-%m-%d'),
                self.deadline_date.get_date().strftime('%Y-%m-%d'),
                int(self.branch_entry.get())
            ]

            self.cur.execute("""
                INSERT INTO Budget (BudgetItem, BudgetAmount, BudgetValue, 
                                DateIssued, DateDeadline, BranchId)
                VALUES (%s, %s, %s, %s, %s, %s)
                """, values)
            self.conn.commit()
            
            messagebox.showinfo("Success", "Budget created successfully!")
            self.dialog.destroy()
            if self.on_success:
                self.on_success()
                
        except Exception as e:
            messagebox.showerror("Error", f"Error creating budget: {str(e)}")
            print(f"Error creating budget: {e}")
from customtkinter import *
import psycopg2
import random
from datetime import datetime
from tkcalendar import DateEntry
from errorHandler import execute_safe_query, show_error_window, show_success_message
from tkinter import ttk
import tkinter as tk

# Add these imports at the top
from PIL import Image, ImageTk
import threading
import time
from queue import Queue

# Database connection
conn = psycopg2.connect(
    host="localhost",
    dbname="postgres",
    user="postgres",
    password="12345",
    port=5432
)
cur = conn.cursor()

def validate_branch_id(branch_id):
    """Validate branch ID exists"""
    try:
        if not branch_id or not str(branch_id).isdigit():
            return False, "Branch ID must be a number"
        success, error = execute_safe_query(
            cur,
            "SELECT EXISTS(SELECT 1 FROM goodwillbranch WHERE BranchId = %s)",
            (int(branch_id),)
        )
        if not success:
            return False, error
        exists = cur.fetchone()[0]
        return exists, None if exists else "Branch ID does not exist"
    except Exception as e:
        return False, str(e)

def validate_dates(issue_date, deadline_date):
    """Validate dates are in correct format and logical"""
    try:
        issue = datetime.strptime(issue_date, '%Y-%m-%d').date()
        deadline = datetime.strptime(deadline_date, '%Y-%m-%d').date()
        if deadline < issue:
            return False, "Deadline cannot be before issue date"
        return True, None
    except ValueError:
        return False, "Invalid date format. Use YYYY-MM-DD"
    except Exception as e:
        return False, str(e)

# Move budgetpage function definition before the BudgetApp class
def budgetpage(page):
    global budgetPagePost, currentView
    budgetPagePost = CTkFrame(page)
    budgetPagePost.pack(fill=BOTH, expand=True)
    
    headerFrame = CTkFrame(budgetPagePost, height=40, corner_radius=0, fg_color="#FFFFFF")
    headerFrame.pack(fill=X, padx=5, pady=2)
    
    titleLabel = CTkLabel(headerFrame, text="Budget Management", font=("Helvetica", 14, "bold"))
    titleLabel.pack(side=LEFT, padx=5)
    
    scrollFrame = CTkScrollableFrame(budgetPagePost, height=300, corner_radius=0)
    scrollFrame.pack(fill=BOTH, expand=True, padx=5, pady=2)
    
    selectButton = CTkButton(headerFrame, text="Select", command=lambda: archiveSelectedItems(), height=25, corner_radius=0, border_color="#000000", border_width=1, fg_color="#ffffff", text_color="#000000")
    archivesListButton = CTkButton(headerFrame, text="Archives List", command=lambda: toggleArchivesList(), height=25, corner_radius=0, border_color="#000000", border_width=1, fg_color="#ffffff", text_color="#000000")
    addButton = CTkButton(headerFrame, text="Add New Budget", command=lambda: switchView("add"), height=25, corner_radius=0, border_color="#000000", border_width=1, fg_color="#ffffff", text_color="#000000")
    editButton = CTkButton(headerFrame, text="Edit Budget", command=lambda: switchView("edit"), height=25, corner_radius=0, border_color="#000000", border_width=1, fg_color="#ffffff", text_color="#000000")
    archiveButton = CTkButton(headerFrame, text="Archive", command=lambda: toggleArchiveMode(), height=25, corner_radius=0, border_color="#000000", border_width=1, fg_color="#ffffff", text_color="#000000")
    
    addButton.pack(side=RIGHT, padx=5)
    editButton.pack(side=RIGHT, padx=5)
    archiveButton.pack(side=RIGHT, padx=5)
    
    archive_mode = {"active": False, "showing_archives": False}

    def toggleArchiveMode():
        archive_mode["active"] = not archive_mode["active"]
        archive_mode["showing_archives"] = False
        
        if archive_mode["active"]:
            addButton.pack_forget()
            editButton.pack_forget()
            archivesListButton.pack(side=RIGHT, padx=5)
            selectButton.pack(side=RIGHT, padx=5)
            archiveButton.configure(text="Back",fg_color="#5991eb")
        else:
            selectButton.pack_forget()
            archivesListButton.pack_forget()
            addButton.pack(side=RIGHT, padx=5)
            editButton.pack(side=RIGHT, padx=5)
            archiveButton.configure(text="Archive", fg_color="#ffffff")
        refreshTableView(archive_mode["active"])

    def toggleArchivesList():
        archive_mode["showing_archives"] = not archive_mode["showing_archives"]
        
        if archive_mode["showing_archives"]:
            selectButton.pack_forget()
            showArchivedTable()
        else:
            refreshTableView(True)
            selectButton.pack(side=RIGHT, padx=5)

    def showArchivedTable():
        """Display archived budget items with additional columns"""
        for widget in scrollFrame.winfo_children():
            widget.destroy()

        # Define columns for archived view
        columns = [
            "Item", "Amount", "Value", "Issue Date", "Deadline",
            "Branch", "Date Archived", "Archive Method"
        ]
        
        tree = ttk.Treeview(scrollFrame, columns=columns, show="headings", height=10)
        
        # Configure column widths and headings
        column_widths = {
            "Item": 150,
            "Amount": 80,
            "Value": 80,
            "Issue Date": 100,
            "Deadline": 100,
            "Branch": 80,
            "Date Archived": 100,
            "Archive Method": 100
        }
        
        for col, width in column_widths.items():
            tree.column(col, width=width, anchor="center")
            tree.heading(col, text=col)

        try:
            # Fetch archived data with proper branch name join
            success, error = execute_safe_query(
                cur,
                """
                SELECT
                    a_BudgetItem,
                    CAST(a_BudgetAmount AS VARCHAR),
                    CAST(a_BudgetValue AS VARCHAR),
                    TO_CHAR(a_DateIssued, 'YYYY-MM-DD'),
                    TO_CHAR(a_DateDeadline, 'YYYY-MM-DD'),
                    g.BranchName,
                    TO_CHAR(DateArchived, 'YYYY-MM-DD'),
                    MethodOfArchival
                FROM archived a
                LEFT JOIN goodwillbranch g ON a.a_BranchId = g.BranchId
                ORDER BY DateArchived DESC
                """
            )
            
            if not success:
                show_error_window(error)
                return
            
            # Add data to tree
            for row in cur.fetchall():
                tree.insert("", "end", values=row)
            
            # Add scrollbars
            y_scrollbar = ttk.Scrollbar(scrollFrame, orient="vertical", command=tree.yview)
            x_scrollbar = ttk.Scrollbar(scrollFrame, orient="horizontal", command=tree.xview)
            tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

            # Grid layout
            tree.grid(row=0, column=0, sticky="nsew")
            y_scrollbar.grid(row=0, column=1, sticky="ns")
            x_scrollbar.grid(row=1, column=0, sticky="ew")
            
            scrollFrame.grid_rowconfigure(0, weight=1)
            scrollFrame.grid_columnconfigure(0, weight=1)

        except Exception as e:
            show_error_window(f"Error displaying archived items: {str(e)}")

    def refreshTableView(show_checkboxes=False):
        for widget in scrollFrame.winfo_children():
            widget.destroy()

        columns = ["ID", "Item", "Amount", "Value", "Issue", "Deadline", "Branch"]
        if show_checkboxes:
            columns.insert(0, "Select")
        
        tree = ttk.Treeview(scrollFrame, columns=columns, show="headings", height=10)
        
        # Configure column widths and tooltips
        column_widths = {
            "Select": 60 if show_checkboxes else 0,
            "ID": 80,
            "Item": 150,
            "Amount": 80,
            "Value": 80,
            "Issue": 100,
            "Deadline": 100,
            "Branch": 80
        }

        # Create tooltip text
        tooltip = CTkLabel(
            scrollFrame,
            text="Click ID to copy",
            font=("Helvetica", 10),
            fg_color="yellow",
            text_color="black",
            corner_radius=5
        )

        def handle_mouse(event):
            """Handle mouse events for tooltips and row highlighting"""
            col = tree.identify_column(event.x)
            row_id = tree.identify_row(event.y)
            
            # Check if we're on the ID column
            is_id_col = (col == '#1' and not show_checkboxes) or (col == '#2' and show_checkboxes)
            
            if is_id_col and row_id:
                x = tree.winfo_rootx() + event.x + 5
                y = tree.winfo_rooty() + event.y + 5
                tooltip.place(x=x, y=y)
                tree.configure(cursor="hand2")
                tree.selection_set(row_id)
            else:
                tooltip.place_forget()
                tree.configure(cursor="")
                if tree.selection():
                    tree.selection_remove(tree.selection())

        def reset_ui(event):
            """Reset UI elements when mouse leaves tree"""
            tooltip.place_forget()
            tree.configure(cursor="")
            if tree.selection():
                tree.selection_remove(tree.selection())

        # Bind mouse events
        tree.bind('<Motion>', handle_mouse)
        tree.bind('<Leave>', reset_ui)

        # Configure columns
        
        # Add click handler for copying ID
        def copy_id(event):
            col = tree.identify_column(event.x)
            row_id = tree.identify_row(event.y)
            
            # Check if we clicked the ID column
            is_id_col = (col == '#1' and not show_checkboxes) or (col == '#2' and show_checkboxes)
            
            if is_id_col and row_id:
                values = tree.item(row_id)['values']
                id_index = 1 if show_checkboxes else 0
                budget_id = str(values[id_index])
                
                # Copy to clipboard
                scrollFrame.clipboard_clear()
                scrollFrame.clipboard_append(budget_id)
                show_success_message("Budget ID copied to clipboard", budgetPagePost)
                
                # Visual feedback
                tree.selection_set(row_id)
                tree.after(500, lambda: tree.selection_remove(row_id))

        tree.bind('<Button-1>', copy_id)
        
        # Configure columns with visual hints
        for col in columns:
            if col == "ID":
                tree.heading(col, text="📋 " + col + " (Click to Copy)")  # Add clipboard icon and hint
                tree.tag_configure("id_column", foreground="blue")
            else:
                tree.heading(col, text=col)
            tree.column(col, width=column_widths.get(col, 80), anchor="center")

        # Add blue color tag for ID values
        def format_row(values):
            """Format row data and ensure ID is properly displayed"""
            budget_id = str(values[0])
            remaining_values = list(values[1:])
            
            if show_checkboxes:
                return ["□", budget_id] + remaining_values
            return [budget_id] + remaining_values

        success, error = execute_safe_query(
            cur, 
            "SELECT BudgetId, BudgetItem, BudgetAmount, BudgetValue, DateIssued, DateDeadline, BranchId FROM Budget ORDER BY DateIssued DESC"
        )
        
        if not success:
            show_error_window(error)
            return
        
        for row in cur.fetchall():
            budget_id = str(row[0])
            display_row = format_row(row)
            tree.insert("", "end", values=display_row, tags=("id_column",))
            
            if show_checkboxes:
                values = ["□"] + display_row
                item_id = tree.insert("", "end", values=values, tags=(str(budget_id),))
            else:
                tree.insert("", "end", values=display_row, tags=(str(budget_id),))
        
        tree.pack(fill=BOTH, expand=True)
        
        def copy_id(event):
            item_id = tree.identify_row(event.y)
            if item_id:
                col = tree.identify_column(event.x)
                if col == '#1':  # ID column
                    budget_id = tree.item(item_id)['values'][0 if not show_checkboxes else 1]
                    scrollFrame.clipboard_clear()
                    scrollFrame.clipboard_append(str(budget_id))
                    show_success_message("Budget ID copied to clipboard", budgetPagePost)

        if show_checkboxes:
            def toggle_checkbox(event):
                item_id = tree.identify_row(event.y)
                col = tree.identify_column(event.x)
                if item_id and col == '#1':  # Select column
                    current = tree.item(item_id)['values']
                    if current and current[0] == "□":
                        tree.set(item_id, "Select", "☑")
                    else:
                        tree.set(item_id, "Select", "□")
                elif col == '#2':  # ID column when checkboxes shown
                    copy_id(event)
            
            tree.bind('<Button-1>', toggle_checkbox)
        else:
            tree.bind('<Button-1>', copy_id)

    def switchView(viewType):
        global currentView
        for widget in scrollFrame.winfo_children():
            widget.destroy()
        
        if viewType == "table":
            refreshTableView()
        elif viewType == "add":
            showAddView()
        elif viewType == "edit":
            showEditView()
        currentView = viewType

    def archiveSelectedItems():
        """Archive selected budget items"""
        try:
            # Find the treeview widget
            tree = None
            for widget in scrollFrame.winfo_children():
                if isinstance(widget, ttk.Treeview):
                    tree = widget
                    break
            
            if not tree:
                show_error_window("No items to archive")
                return
            
            # Begin transaction
            success, error = execute_safe_query(cur, "BEGIN")
            if not success:
                show_error_window(error)
                return
            
            items_archived = False
            archive_date = datetime.now().date()
            
            # Process each selected item
            for item_id in tree.get_children():
                if tree.set(item_id, "Select") == "☑":
                    budget_id = tree.item(item_id)['tags'][0]
                    
                    # Insert into archived table
                    success, error = execute_safe_query(cur, """
                        WITH budget_data AS (
                            SELECT
                                BudgetItem,
                                BudgetAmount,
                                BudgetValue,
                                DateIssued,
                                DateDeadline,
                                BranchId
                            FROM Budget
                            WHERE BudgetId = %s
                            FOR UPDATE
                        )
                        INSERT INTO archived (
                            a_BudgetItem,
                            a_BudgetAmount,
                            a_BudgetValue,
                            a_DateIssued,
                            a_DateDeadline,
                            a_BranchId,
                            DateArchived,
                            MethodOfArchival
                        )
                        SELECT
                            BudgetItem,
                            BudgetAmount,
                            BudgetValue,
                            DateIssued,
                            DateDeadline,
                            BranchId,
                            %s,
                            %s
                        FROM budget_data
                        RETURNING a_BudgetItem
                    """, (budget_id, archive_date, "Manual Archive"))
                    
                    if not success:
                        cur.execute("ROLLBACK")
                        show_error_window(f"Error archiving item: {error}")
                        return
                    
                    # Delete from Budget table
                    success, error = execute_safe_query(
                        cur,
                        "DELETE FROM Budget WHERE BudgetId = %s",
                        (budget_id,)
                    )
                    if not success:
                        cur.execute("ROLLBACK")
                        show_error_window(f"Error deleting budget: {error}")
                        return
                        
                    items_archived = True
            
            if items_archived:
                success, error = execute_safe_query(cur, "COMMIT")
                if not success:
                    show_error_window(error)
                    cur.execute("ROLLBACK")
                    return
                    
                selectButton.pack_forget()
                refreshTableView(False)  # Refresh main table view
                show_success_message("Selected items archived successfully", budgetPagePost)
            else:
                cur.execute("ROLLBACK")
                show_error_window("No items selected for archiving")
            
        except Exception as e:
            try:
                cur.execute("ROLLBACK")
            except:
                pass
            show_error_window(f"Error during archiving: {str(e)}")

    def addBudget():
        try:
            # Validate required fields
            if not all([itemEntry.get(), amountEntry.get(), valueEntry.get(), branchEntry.get()]):
                show_error_window("All fields are required")
                return
                
            # Validate numeric values
            try:
                amount = float(amountEntry.get())
                value = float(valueEntry.get())
                if amount < 0 or value < 0:
                    show_error_window("Amount and value must be positive")
                    return
            except ValueError:
                show_error_window("Amount and value must be numbers")
                return
                
            # Validate branch ID
            valid_branch, error = validate_branch_id(branchEntry.get())
            if not valid_branch:
                show_error_window(error)
                return
                
            # Validate dates
            valid_dates, error = validate_dates(
                issueDate.get_date().strftime('%Y-%m-%d'),
                deadlineDate.get_date().strftime('%Y-%m-%d')
            )
            if not valid_dates:
                show_error_window(error)
                return
                
            # Generate unique ID
            nextId = random.randint(10000, 99999)
            while True:
                success, error = execute_safe_query(
                    cur,
                    "SELECT EXISTS(SELECT 1 FROM Budget WHERE BudgetId = %s)",
                    (nextId,)
                )
                if not success:
                    show_error_window(error)
                    return
                if not cur.fetchone()[0]:
                    break
                nextId = random.randint(10000, 99999)
            
            # Insert new budget with transaction
            success, error = execute_safe_query(cur, "BEGIN")
            if not success:
                show_error_window(error)
                return
                
            try:
                success, error = execute_safe_query(
                    cur,
                    """
                    INSERT INTO Budget (
                        BudgetId, BudgetItem, BudgetAmount, BudgetValue, 
                        DateIssued, DateDeadline, BranchId
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        nextId,
                        itemEntry.get().strip(),
                        amount,
                        value,
                        issueDate.get_date(),
                        deadlineDate.get_date(),
                        int(branchEntry.get())
                    )
                )
                
                if not success:
                    cur.execute("ROLLBACK")
                    show_error_window(error)
                    return
                    
                cur.execute("COMMIT")
                show_success_message("Budget added successfully", budgetPagePost)
                switchView("table")
                
            except Exception as e:
                cur.execute("ROLLBACK")
                show_error_window(f"Error adding budget: {str(e)}")
                
        except Exception as e:
            show_error_window(f"Unexpected error: {str(e)}")

    def showAddView():
        labels = ["Item:", "Amount:", "Value:", "Branch:"]
        
        for i, label in enumerate(labels):
            CTkLabel(scrollFrame, text=label, font=("Helvetica", 10)).grid(row=i, column=0, padx=2, pady=2, sticky='e')
        
        global itemEntry, amountEntry, valueEntry, branchEntry, issueDate, deadlineDate
        
        itemEntry = CTkEntry(scrollFrame, width=150, height=25)
        itemEntry.grid(row=0, column=1, columnspan=2, padx=2, pady=2)
        
        amountEntry = CTkEntry(scrollFrame, width=150, height=25)
        amountEntry.grid(row=1, column=1, columnspan=2, padx=2, pady=2)
        
        valueEntry = CTkEntry(scrollFrame, width=150, height=25)
        valueEntry.grid(row=2, column=1, columnspan=2, padx=2, pady=2)
        
        branchEntry = CTkEntry(scrollFrame, width=150, height=25)
        branchEntry.grid(row=3, column=1, columnspan=2, padx=2, pady=2)
        
        CTkLabel(scrollFrame, text="Issue:", font=("Helvetica", 10)).grid(row=4, column=0, padx=2, pady=2, sticky='e')
        issueDate = DateEntry(scrollFrame, width=12, date_pattern='yyyy-mm-dd')
        issueDate.grid(row=4, column=1, columnspan=2, padx=2, pady=2)
        
        CTkLabel(scrollFrame, text="Deadline:", font=("Helvetica", 10)).grid(row=5, column=0, padx=2, pady=2, sticky='e')
        deadlineDate = DateEntry(scrollFrame, width=12, date_pattern='yyyy-mm-dd')
        deadlineDate.grid(row=5, column=1, columnspan=2, padx=2, pady=2)
        
        buttonFrame = CTkFrame(scrollFrame)
        buttonFrame.grid(row=6, column=0, columnspan=3, pady=5)
        
        submitBtn = CTkButton(buttonFrame, text="Add", command=addBudget, width=70, height=25, corner_radius=0, border_color="#000000", border_width=1, fg_color="#ffffff", text_color="#000000")
        submitBtn.pack(side=LEFT, padx=2)
        
        backBtn = CTkButton(buttonFrame, text="Back", command=lambda: switchView("table"), width=70, height=25, corner_radius=0, border_color="#000000", border_width=1, fg_color="#ffffff", text_color="#000000")
        backBtn.pack(side=LEFT, padx=2)

    def showEditView():
        global itemEntry, amountEntry, valueEntry, branchEntry, issueDate, deadlineDate, budgetIDEntry
        
        # Create search frame
        searchFrame = CTkFrame(scrollFrame)
        searchFrame.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        CTkLabel(searchFrame, text="Budget ID:", font=("Helvetica", 10)).pack(side=LEFT, padx=2)
        budgetIDEntry = CTkEntry(searchFrame, width=100, height=25)
        budgetIDEntry.pack(side=LEFT, padx=2)
        
        searchBtn = CTkButton(searchFrame, text="Search", command=loadBudgetData,
                            width=70, height=25, corner_radius=0,
                            border_color="#000000", border_width=1,
                            fg_color="#ffffff", text_color="#000000")
        searchBtn.pack(side=LEFT, padx=2)

        # Labels and entry fields
        labels = [
            ("Item:", 1), ("Amount:", 2), ("Value:", 3),
            ("Branch:", 4), ("Issue Date:", 5), ("Deadline:", 6)
        ]
        
        for label, row in labels:
            CTkLabel(scrollFrame, text=label, font=("Helvetica", 10)).grid(
                row=row, column=0, padx=2, pady=2, sticky='e'
            )
        
        # Create entry fields
        itemEntry = CTkEntry(scrollFrame, width=150, height=25)
        itemEntry.grid(row=1, column=1, columnspan=2, padx=2, pady=2)
        
        amountEntry = CTkEntry(scrollFrame, width=150, height=25)
        amountEntry.grid(row=2, column=1, columnspan=2, padx=2, pady=2)
        
        valueEntry = CTkEntry(scrollFrame, width=150, height=25)
        valueEntry.grid(row=3, column=1, columnspan=2, padx=2, pady=2)
        
        branchEntry = CTkEntry(scrollFrame, width=150, height=25)
        branchEntry.grid(row=4, column=1, columnspan=2, padx=2, pady=2)
        
        issueDate = DateEntry(scrollFrame, width=12, date_pattern='yyyy-mm-dd')
        issueDate.grid(row=5, column=1, columnspan=2, padx=2, pady=2)
        
        deadlineDate = DateEntry(scrollFrame, width=12, date_pattern='yyyy-mm-dd')
        deadlineDate.grid(row=6, column=1, columnspan=2, padx=2, pady=2)
        
        # Create button frame
        buttonFrame = CTkFrame(scrollFrame)
        buttonFrame.grid(row=7, column=0, columnspan=3, pady=5)
        
        submitBtn = CTkButton(buttonFrame, text="Save Changes",
                            command=lambda: editBudget() if validateInput() else None,
                            width=100, height=25, corner_radius=0,
                            border_color="#000000", border_width=1,
                            fg_color="#ffffff", text_color="#000000")
        submitBtn.pack(side=LEFT, padx=2)
        
        deleteBtn = CTkButton(buttonFrame, text="Delete", command=deleteBudget,
                            width=70, height=25, corner_radius=0,
                            border_color="#000000", border_width=1,
                            fg_color="#ff0000", text_color="#ffffff")
        deleteBtn.pack(side=LEFT, padx=2)
        
        backBtn = CTkButton(buttonFrame, text="Back", command=lambda: switchView("table"),
                          width=70, height=25, corner_radius=0,
                          border_color="#000000", border_width=1,
                          fg_color="#ffffff", text_color="#000000")
        backBtn.pack(side=LEFT, padx=2)
    def clearFields():
        """Clear all entry fields"""
        global itemEntry, amountEntry, valueEntry, branchEntry
        for field in [itemEntry, amountEntry, valueEntry, branchEntry]:
            if field and field.winfo_exists():
                field.delete(0, 'end')

    def loadBudgetData():
        """Load budget data when searching by ID"""
        budget_id = budgetIDEntry.get().strip()
        if not budget_id:
            show_error_window("Please enter a Budget ID")
            return
            
        try:
            success, error = execute_safe_query(
                cur,
                """
                SELECT BudgetItem, BudgetAmount, BudgetValue,
                       DateIssued, DateDeadline, BranchId
                FROM Budget
                WHERE BudgetId = %s
                """,
                (budget_id,)
            )
            
            if not success:
                show_error_window(error)
                return
                
            result = cur.fetchone()
            if not result:
                show_error_window("Budget ID not found")
                clearFields()
                return
                
            # Populate fields with data
            itemEntry.delete(0, 'end')
            itemEntry.insert(0, result[0])
            
            amountEntry.delete(0, 'end')
            amountEntry.insert(0, str(result[1]))
            
            valueEntry.delete(0, 'end')
            valueEntry.insert(0, str(result[2]))
            
            branchEntry.delete(0, 'end')
            branchEntry.insert(0, str(result[5]))
            
            # Set dates
            issueDate.set_date(result[3])
            deadlineDate.set_date(result[4])
            
        except Exception as e:
            show_error_window(f"Error loading budget data: {str(e)}")

    def validateInput():
        """Validate all input fields before saving changes"""
        try:
            # Check required fields
            if not all([
                budgetIDEntry.get(), itemEntry.get(),
                amountEntry.get(), valueEntry.get(),
                branchEntry.get()
            ]):
                show_error_window("All fields are required")
                return False

            # Validate numeric values
            try:
                amount = float(amountEntry.get())
                value = float(valueEntry.get())
                if amount < 0 or value < 0:
                    show_error_window("Amount and value must be positive")
                    return False
            except ValueError:
                show_error_window("Amount and value must be numbers")
                return False

            # Validate branch ID
            valid_branch, error = validate_branch_id(branchEntry.get())
            if not valid_branch:
                show_error_window(error)
                return False

            # Validate dates
            valid_dates, error = validate_dates(
                issueDate.get_date().strftime('%Y-%m-%d'),
                deadlineDate.get_date().strftime('%Y-%m-%d')
            )
            if not valid_dates:
                show_error_window(error)
                return False

            return True

        except Exception as e:
            show_error_window(f"Validation error: {str(e)}")
            return False

    def editBudget():
        """Update budget record with validated data"""
        try:
            # Begin transaction
            success, error = execute_safe_query(cur, "BEGIN")
            if not success:
                show_error_window(error)
                return

            # Update budget record
            success, error = execute_safe_query(
                cur,
                """
                UPDATE Budget
                SET BudgetItem = %s,
                    BudgetAmount = %s,
                    BudgetValue = %s,
                    DateIssued = %s,
                    DateDeadline = %s,
                    BranchId = %s
                WHERE BudgetId = %s
                RETURNING BudgetId
                """,
                (
                    itemEntry.get().strip(),
                    float(amountEntry.get()),
                    float(valueEntry.get()),
                    issueDate.get_date(),
                    deadlineDate.get_date(),
                    int(branchEntry.get()),
                    int(budgetIDEntry.get())
                )
            )
            
            if not success:
                cur.execute("ROLLBACK")
                show_error_window(error)
                return

            # Check if any row was updated
            result = cur.fetchone()
            if not result:
                cur.execute("ROLLBACK")
                show_error_window("Budget record not found")
                return

            # Commit transaction
            success, error = execute_safe_query(cur, "COMMIT")
            if not success:
                show_error_window(error)
                cur.execute("ROLLBACK")
                return

            show_success_message("Budget updated successfully", budgetPagePost)
            clearFields()
            switchView("table")
            
        except Exception as e:
            cur.execute("ROLLBACK")
            show_error_window(f"Error updating budget: {str(e)}")
            success, error = execute_safe_query(
                cur,
                """
                UPDATE Budget
                SET BudgetItem = %s, BudgetAmount = %s, BudgetValue = %s, 
                    DateIssued = %s, DateDeadline = %s, BranchId = %s
                WHERE BudgetId = %s
                """,
                (
                    itemEntry.get(),
                    float(amountEntry.get()),
                    float(valueEntry.get()),
                    issueDate.get_date(),
                    deadlineDate.get_date(),
                    int(branchEntry.get()),
                    int(budgetIDEntry.get())
                )
            )
            
            if not success:
                show_error_window(error)
                return
                
            conn.commit()
            show_success_message("Budget edited successfully", budgetPagePost)
            switchView("table")
            
        except ValueError:
            show_error_window("Please enter valid numbers for Amount, Value, and Branch ID")
        except Exception as e:
            show_error_window(f"Unexpected error: {str(e)}")
            conn.rollback()

    def deleteBudget():
        try:
            budget_id = budgetIDEntry.get().strip()
            if not budget_id:
                show_error_window("Please enter a Budget ID")
                return
            
            success, error = execute_safe_query(
                cur,
                "DELETE FROM Budget WHERE BudgetId = %s",
                (budget_id,)
            )
            
            if not success:
                show_error_window(error)
                return
                
            conn.commit()
            show_success_message("Budget deleted successfully", budgetPagePost)
            switchView("table")
            
        except Exception as e:
            show_error_window(f"Unexpected error: {str(e)}")
            conn.rollback()

    def autoArchiveBudgets():
        try:
            # Begin transaction
            success, error = execute_safe_query(cur, "BEGIN")
            if not success:
                show_error_window(error)
                return
                
            try:
                # Get items to archive
                success, error = execute_safe_query(
                    cur,
                    """
                    SELECT BudgetId, BudgetItem 
                    FROM Budget 
                    WHERE DateDeadline <= CURRENT_DATE
                    """
                )
                if not success:
                    cur.execute("ROLLBACK")
                    show_error_window(error)
                    return
                    
                items = cur.fetchall()
                if not items:
                    return  # No items to archive
                    
                # Archive items
                for budget_id, item_name in items:
                    success, error = execute_safe_query(
                        cur,
                        """
                        WITH budget_data AS (
                            SELECT
                                BudgetItem,
                                BudgetAmount,
                                BudgetValue,
                                DateIssued,
                                DateDeadline,
                                BranchId
                            FROM Budget
                            WHERE BudgetId = %s
                            FOR UPDATE
                        )
                        INSERT INTO archived (
                            a_BudgetItem,
                            a_BudgetAmount,
                            a_BudgetValue,
                            a_DateIssued,
                            a_DateDeadline,
                            a_BranchId,
                            DateArchived,
                            MethodOfArchival
                        )
                        SELECT
                            BudgetItem,
                            BudgetAmount,
                            BudgetValue,
                            DateIssued,
                            DateDeadline,
                            BranchId,
                            CURRENT_DATE,
                            'Auto Archive - Deadline Reached'
                        FROM budget_data
                        RETURNING a_BudgetItem
                        FROM Budget
                        WHERE BudgetId = %s
                        RETURNING a_BudgetItem
                        """,
                        (budget_id,)
                    )
                    
                    if not success:
                        cur.execute("ROLLBACK")
                        show_error_window(f"Error archiving {item_name}: {error}")
                        return
                        
                    success, error = execute_safe_query(
                        cur,
                        "DELETE FROM Budget WHERE BudgetId = %s",
                        (budget_id,)
                    )
                    
                    if not success:
                        cur.execute("ROLLBACK")
                        show_error_window(f"Error removing {item_name}: {error}")
                        return
                
                cur.execute("COMMIT")
                if items:
                    show_success_message(f"Archived {len(items)} expired budget items", budgetPagePost)
                refreshTableView()
                
            except Exception as e:
                cur.execute("ROLLBACK")
                show_error_window(f"Error during auto-archive: {str(e)}")
                
        except Exception as e:
            show_error_window(f"Database error: {str(e)}")

    autoArchiveBudgets()
    refreshTableView()

# Update the BudgetApp class to remove references to LoadingScreen
class BudgetApp:
    def __init__(self):
        self.window = CTk()
        self.window.title("BUDGET")
        self.window.geometry("600x400")
        self.window.resizable(0, 0)
        set_appearance_mode("light")
        
        # Remove loading screen initialization
        # self.loading_screen = LoadingScreen(self.window)
        # self.loading_screen.loading_window.wait_window()
        
        # Move font definitions here
        self.OutputCalculatorFont = CTkFont(family="Oswald", size=25, weight='bold')
        self.EditFont = CTkFont(family="Oswald", size=15, weight='bold')

        # Create frames
        self.TABFRAME = CTkFrame(self.window, height=51, width=600, fg_color="#1E1E1E", corner_radius=0)
        self.TABFRAME.pack(anchor=CENTER, fill=X)

        self.budgetPage = CTkFrame(self.window)
        self.budgetPage.pack(fill=BOTH, expand=True)

        # Create buttons
        self.salesTab = CTkButton(
            self.TABFRAME, 
            text="Sales", 
            width=20,
            corner_radius=0,
            border_color="#000000",
            border_width=1,
            fg_color="#ffffff",
            text_color="#000000",
            command=lambda: self.buttonEvent(self.budgetPage)
        )
        self.salesTab.grid(row=0, column=1, pady=10, padx=10, sticky="nsew")

        self.budgetTab = CTkButton(
            self.TABFRAME,
            text="Budget",
            width=20,
            corner_radius=0,
            border_color="#000000",
            border_width=1,
            fg_color="#ffffff",
            text_color="#000000",
            command=lambda: self.buttonEvent(self.budgetPage)
        )
        self.budgetTab.grid(row=0, column=2, pady=10, padx=10, sticky="nsew")

        # Initialize the budget page
        self.showPage(self.budgetPage)

    def buttonEvent(self, page):
        if page == self.budgetPage:
            budgetpage(page)

    def showPage(self, page):
        page.pack(fill=BOTH, expand=True)
        self.window.update_idletasks()
        if page == self.budgetPage:
            budgetpage(self.budgetPage)

    def run(self):
        try:
            self.window.mainloop()
        except Exception as e:
            print(f"Error in mainloop: {e}")
        finally:
            if conn:
                conn.close()

# Initialize and run the application
if __name__ == "__main__":
    try:
        app = BudgetApp()
        app.run()
    except Exception as e:
        print(f"Application Error: {e}")


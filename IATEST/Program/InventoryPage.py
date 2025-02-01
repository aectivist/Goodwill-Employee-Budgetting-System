from customtkinter import *
import random
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from errorHandler import execute_safe_query, show_error_window, show_success_message

# Database connection
conn = None
cur = None

def init_db(db_conn, db_cur):
    """Initialize database connection"""
    global conn, cur
    conn = db_conn
    cur = db_cur

# Font configurations
TitleFont = CTkFont(family="Oswald", size=15, weight='bold')
EditFont = CTkFont(family="Oswald", size=15, weight='bold')
BTNFont = CTkFont(family="Oswald", size=13)
ErrorFont = CTkFont(size=10)

# Page state trackers
InventoryPagePost = 0
vieweditemflag = False
viewederror = 0
ErrorBoolean = False
currentmode = ""

# Mode existence trackers
InvAddExist = False
InvEditExist = False
InvDeleteExist = False

# For search functionality
ConfirmedChoiceForSearch = ""

# Entry holders and flags for inventory items
InvIDHolder = ""
InvNameHolder = ""
InvValueHolder = ""
InvTypeHolder = ""
BranchIDHolder = ""
StatusHolder = "Bought"  # Changed from "Available"

# Flags for validation
InvIDFlag = False
InvNameFlag = False
InvValueFlag = False
InvTypeFlag = False
BranchIDFlag = False
StatusFlag = False

# UI state trackers
diffvalue = 0
enteronce = 0
enteronceforcombo = 0
mode = ""

# For ID creation
keyCreatedChecker = False

def I_show_page(parent, page_frame):
    """Initialize and show the inventory page"""
    global InventoryPagePost
    
    # Show the page
    page_frame.pack(fill=BOTH, expand=True)
    parent.update_idletasks()
    
    # Initialize content only once
    if InventoryPagePost == 0:
        inventorypage(page_frame)

def inventorypage(page):
    """Create and initialize the inventory page layout"""
    global InventoryPagePost, OutputEditContent, SearchRequestContent

    if InventoryPagePost == 0:
        # Create page layout
        PageMargin = CTkFrame(page)
        PageMargin.pack(expand=True)
        
        # Create main sections
        RequestPadding = CTkFrame(PageMargin, width=170, height=330, fg_color="#dbdbdb", 
                                corner_radius=0, border_color='#000000', border_width=1)
        OutputPadding = CTkFrame(PageMargin, width=410, height=330, fg_color="#dbdbdb", 
                               corner_radius=0, border_color='#000000', border_width=1)
        
        RequestPadding.grid_propagate(0)
        OutputPadding.grid_propagate(0)
        RequestPadding.grid(row=0, column=0)
        OutputPadding.grid(row=0, column=1)

        # Create content frames for search and edit sections
        SearchRequestContent = CTkFrame(RequestPadding, width=170, height=165, 
                                      fg_color="#FFFFFF", corner_radius=0, 
                                      border_color='#000000', border_width=1)
        EditsRequestContent = CTkFrame(RequestPadding, width=170, height=165, 
                                     fg_color="#FFFFFF", corner_radius=0,
                                     border_color='#000000', border_width=1)
        
        SearchRequestContent.grid_propagate(0)
        EditsRequestContent.grid_propagate(0)
        SearchRequestContent.grid(row=0, column=0)
        EditsRequestContent.grid(row=1, column=0)

        # Configure grid weights
        for i in range(1):
            EditsRequestContent.grid_columnconfigure(i, weight=1, uniform="column")
            EditsRequestContent.grid_rowconfigure(0, minsize=51)
            SearchRequestContent.grid_columnconfigure(i, weight=1, uniform="column")
            SearchRequestContent.grid_rowconfigure(0, minsize=51)

        # Setup output content area
        global OutputTableScrollbarContent
        OutputEditContent = CTkFrame(OutputPadding, width=410, height=115, 
                                   fg_color="#FFFFFF", corner_radius=0, 
                                   border_color='#000000', border_width=1)
        OutputEditContent.grid(row=0, column=0)
        
        LabelInventoryAdd = CTkLabel(OutputEditContent, text="INVENTORY", font=EditFont)
        LabelInventoryAdd.place(x=5, y=1)

        # Setup table content area
        OutputTableContent = CTkFrame(OutputPadding, width=410, height=215, 
                                    fg_color="#a6a6a6", corner_radius=0, 
                                    border_color='#000000', border_width=1)
        OutputTableContent.grid(row=1, column=0)
        OutputEditContent.grid_propagate(0)
        OutputTableContent.grid_propagate(0)

        # Setup scrollable content
        OutputTableScrollbarContent = CTkFrame(OutputTableContent, width=410, height=215)
        OutputTableScrollbarContent.pack(fill="both", expand=True)
        OutputTableScrollbarContent.grid_propagate(0)

        canvas = CTkCanvas(OutputTableScrollbarContent, width=410, height=215, 
                          highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = CTkScrollableFrame(canvas, width=387)
        scrollbar.grid(rowspan=100, row=0, column=0, sticky='nsew')

        # Setup edit buttons
        EditLabelRequest = CTkLabel(EditsRequestContent, text="EDITS", font=EditFont)
        EditLabelRequest.grid(row=0, column=0)

        AddButtonRequest = CTkButton(EditsRequestContent, text="ADD", corner_radius=0,
                                   command=lambda: I_outputContentGivenButtons(OutputEditContent, 1),
                                   font=BTNFont, text_color='#000000', fg_color='#FFFFFF',
                                   border_color='#000000', border_width=1, hover_color='#e6e6e6')
        AddButtonRequest.grid(row=1, column=0, padx=10, pady=4, sticky='nsew')

        EditButtonRequest = CTkButton(EditsRequestContent, text="EDIT", corner_radius=0,
                                    command=lambda: I_outputContentGivenButtons(OutputEditContent, 2),
                                    font=BTNFont, fg_color='#FFFFFF', text_color='#000000',
                                    border_color='#000000', border_width=1, hover_color='#e6e6e6')
        EditButtonRequest.grid(row=2, column=0, padx=10, pady=1, sticky='nsew')

        DeleteButtonRequest = CTkButton(EditsRequestContent, text="DELETE", corner_radius=0,
                                      command=lambda: I_outputContentGivenButtons(OutputEditContent, 3),
                                      font=BTNFont, fg_color='#FFFFFF', text_color='#000000',
                                      border_color='#000000', border_width=1, hover_color='#e6e6e6')
        DeleteButtonRequest.grid(row=3, column=0, padx=10, pady=2, sticky='nsew')

        # Setup search section
        SearchLabel = CTkLabel(SearchRequestContent, text="INVENTORY", font=EditFont)
        SearchLabel.grid(row=0, column=0, padx=10, pady=0)

        SearchEntry = CTkEntry(SearchRequestContent, corner_radius=0,
                             border_color='#000000', border_width=1,
                             placeholder_text="Search")
        SearchEntry.grid(row=1, column=0, padx=10, pady=4)

        SearchButton = CTkButton(SearchRequestContent, text="Search", fg_color='#0053A0',
                               corner_radius=0, text_color='#FFFFFF', border_color='#000000',
                               border_width=1, hover_color='#0051ff',
                               command=lambda: InventorySearch(SearchEntry))
        SearchButton.grid(row=2, column=0, padx=10, pady=1)

        # Setup search combo box
        comboVal = StringVar(value="Inventory ID")
        SearchComboChoices = CTkComboBox(SearchRequestContent, 
            values=["Inventory ID", "Inventory Name", "Inventory Type", "Branch ID"],
            command=InventorySearch_ComboCallback, variable=comboVal, corner_radius=1)
        SearchComboChoices.set("Inventory ID")
        SearchComboChoices.grid(row=3, column=0, padx=10, pady=2)
        SearchComboChoices.configure(state="readonly")

        InventoryPagePost = 1
    else:
        print("Page has already been outputted!")

def InventorySearch_ComboCallback(choice):    #"""Handle search combo box selection"""
    global ConfirmedChoiceForSearch
    search_types = {
        "Inventory ID": "Inventory ID",
        "Inventory Name": "Inventory Name",
        "Inventory Type": "Inventory Type",
        "Branch ID": "Branch ID"
    }
    if choice in search_types:
        ConfirmedChoiceForSearch = search_types[choice]
    else:
        ConfirmedChoiceForSearch = "Inventory ID"

def InventorySearch(SearchEntry):
    """Search inventory based on selected criteria"""
    global ConfirmedChoiceForSearch, OutputTableScrollbarContent
    for widget in OutputTableScrollbarContent.winfo_children():
        widget.destroy()
    
    try:
        search_value = SearchEntry.get().strip()
        params = {'search_value': search_value}
        
        base_query = """
        SELECT 
            i.InventoryId,
            i.InventoryName,
            i.InventoryValue,
            i.InventoryType,
            i.BranchId,
            i.GoodsStatus,
            g.BranchName
        FROM Inventory i
        LEFT JOIN goodwillbranch g ON i.BranchId = g.BranchId
        WHERE 1=1
        """
        
        search_conditions = {
            "Inventory ID": "i.InventoryId = %(search_value)s",
            "Inventory Name": "LOWER(i.InventoryName) LIKE LOWER(%(like_value)s)",
            "Inventory Type": "LOWER(i.InventoryType) LIKE LOWER(%(like_value)s)",
            "Branch ID": "i.BranchId = %(search_value)s"
        }

        if search_value and ConfirmedChoiceForSearch in search_conditions:
            condition = search_conditions[ConfirmedChoiceForSearch]
            if ConfirmedChoiceForSearch in ["Inventory ID", "Branch ID"]:
                if not search_value.isdigit():
                    raise ValueError(f"{ConfirmedChoiceForSearch} must be a number")
                params['search_value'] = int(search_value)
            else:
                params['like_value'] = f"%{search_value}%"
            base_query += f" AND {condition}"

        success, error = execute_safe_query(cur, base_query, params)
        if not success:
            show_error_window(error)
            return

        rows = cur.fetchall()

        if rows:
            tree = ttk.Treeview(OutputTableScrollbarContent, show="headings", height=10)
            columns = ["InvID", "Name", "Value", "Type", "BranchID", "Status", "BranchName"]
            tree["columns"] = columns
            
            # Configure column widths and headers
            column_widths = {
                "InvID": 70,
                "Name": 150,
                "Value": 80,
                "Type": 80,
                "BranchID": 70,
                "Status": 80,
                "BranchName": 120
            }
            
            for col, width in column_widths.items():
                tree.column(col, width=width, anchor="center")
                tree.heading(col, text=col)

            # Insert data
            for row in rows:
                tree.insert("", "end", values=row)

            # Add scrollbars
            y_scrollbar = ttk.Scrollbar(OutputTableScrollbarContent, orient="vertical", command=tree.yview)
            x_scrollbar = ttk.Scrollbar(OutputTableScrollbarContent, orient="horizontal", command=tree.xview)
            tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

            # Grid layout
            tree.grid(row=0, column=0, sticky="nsew")
            y_scrollbar.grid(row=0, column=1, sticky="ns")
            x_scrollbar.grid(row=1, column=0, sticky="ew")
            
            OutputTableScrollbarContent.grid_rowconfigure(0, weight=1)
            OutputTableScrollbarContent.grid_columnconfigure(0, weight=1)
        else:
            error_label = CTkLabel(OutputTableScrollbarContent, 
                                 text="No results found", 
                                 text_color="red")
            error_label.grid(row=0, column=0, sticky="nsew")

    except ValueError as ve:
        error_label = CTkLabel(OutputTableScrollbarContent, 
                             text=str(ve), 
                             text_color="red")
        error_label.grid(row=0, column=0, sticky="nsew")
        
    except Exception as e:
        error_label = CTkLabel(OutputTableScrollbarContent, 
                             text=f"An error occurred: {str(e)}", 
                             text_color="red")
        error_label.grid(row=0, column=0, sticky="nsew")

def I_outputContentGivenButtons(OutputEditContent, value):
    """Handle button clicks for Add/Edit/Delete operations"""
    global vieweditemflag, currentmode, mode
    
    if value == 1:
        mode = "add"
    elif value == 2:
        mode = "edit"
    elif value == 3:
        mode = "delete"
        
    if currentmode == mode:
        return
        
    I_clearcurrentmode()
    
    if currentmode == "":
        vieweditemflag = 0
        
    if mode == "add":
        I_addmodeui()
    elif mode == "edit":
        I_editmodeui()
    elif mode == "delete":
        I_deletemodeui()
        
    currentmode = mode

def clear_previous_entries():
    """Clear previous entry widgets based on mode and diffvalue"""
    try:
        # Define all possible widgets that need to be cleared
        all_widgets = {
            'add': {
                1: ['InvValueEntryBox'],
                2: ['InvTypeCombobox'],
                3: ['BranchIDEntryBox'],
                4: ['StatusCombobox']
            },
            'edit': {
                1: ['EditNameEntryBox'],
                2: ['EditValueEntryBox'],
                3: ['EditTypeCombobox'],
                4: ['EditBranchIDEntryBox'],
                5: ['EditStatusCombobox']
            }
        }

        # Get the widgets to clear based on current mode and diffvalue
        mode_widgets = all_widgets.get(mode, {})
        widgets_to_clear = mode_widgets.get(diffvalue, [])

        # Clear the specified widgets
        for widget_name in widgets_to_clear:
            if widget_name in globals() and globals()[widget_name] is not None:
                try:
                    widget = globals()[widget_name]
                    if hasattr(widget, 'winfo_exists') and widget.winfo_exists():
                        widget.place_forget()
                except Exception:
                    pass

        # Additional cleanup for specific widgets
        common_widgets = [
            'AddSearchBoxEnter', 'EditSearchBoxEnter',
            'inventorytypebox', 'statusbox'
        ]
        
        for widget_name in common_widgets:
            if widget_name in globals() and globals()[widget_name] is not None:
                try:
                    widget = globals()[widget_name]
                    if hasattr(widget, 'winfo_exists') and widget.winfo_exists():
                        if widget_name.endswith('BoxEnter'):
                            widget.destroy()
                        else:
                            widget.place_forget()
                except Exception:
                    pass
                    
    except Exception as e:
        print(f"Error clearing entries: {e}")

def I_clearcurrentmode():
    """Clean up UI elements when switching modes"""
    global InvAddExist, InvEditExist, InvDeleteExist, diffvalue
    global viewederror, ErrorBoolean
    global Inventory_inputbutton, InventoryNameBox, Inventory_combobox, SearchComboChoices

    # List of all possible widgets to clean up
    widgets_to_cleanup = {
        'add': [
            ('InventoryNameBox', 'place_forget'),
            ('Inventory_combobox', 'place_forget'),
            ('ItemTypeCombobox', 'place_forget'),
            ('InvValueEntryBox', 'place_forget'),
            ('InvTypeCombobox', 'place_forget'),
            ('BranchIDEntryBox', 'place_forget'),
            ('StatusCombobox', 'place_forget'),
            ('AddSearchBoxEnter', 'destroy'),
            ('Inventory_inputbutton', 'destroy')  # Added Inventory_inputbutton
        ],
        'edit': [
            ('InventoryIDEdit', 'destroy'),
            ('Inventory_combobox', 'destroy'),
            ('EditNameEntryBox', 'place_forget'),
            ('EditValueEntryBox', 'place_forget'),
            ('EditTypeCombobox', 'place_forget'),
            ('EditBranchIDEntryBox', 'place_forget'),
            ('EditStatusCombobox', 'place_forget'),
            ('EditSearchBoxEnter', 'destroy'),
            ('Inventory_inputbutton', 'destroy')  # Added Inventory_inputbutton
        ],
        'delete': [
            ('InventoryIDDelete', 'destroy'),
            ('Inventory_inputbutton', 'destroy')  # Added Inventory_inputbutton
        ]
    }

    # Clean up mode-specific widgets
    current_mode = 'add' if InvAddExist else 'edit' if InvEditExist else 'delete' if InvDeleteExist else None
    if current_mode:
        for widget_name, action in widgets_to_cleanup[current_mode]:
            try:
                if widget_name in globals() and globals()[widget_name] is not None:
                    widget = globals()[widget_name]
                    if hasattr(widget, 'winfo_exists') and widget.winfo_exists():
                        getattr(widget, action)()
            except Exception as e:
                print(f"Error cleaning up {widget_name}: {e}")

    # Reset state flags
    InvAddExist = False
    InvEditExist = False
    InvDeleteExist = False

    # Clear error state
    try:
        if ErrorBoolean and 'Error' in globals() and Error.winfo_exists():
            Error.destroy()
            viewederror = 0
            ErrorBoolean = False
    except Exception:
        pass

    # Reset diffvalue
    diffvalue = 0

def I_addmodeui():
    """Initialize add mode interface"""
    global InvAddExist, InventoryNameBox, Inventory_inputbutton, Inventory_combobox
    global InvNameHolder, InvValueHolder, InvTypeHolder, BranchIDHolder, StatusHolder
    global ItemTypeCombobox  # Add this

    # Initialize holders
    InvNameHolder = ""
    InvValueHolder = ""
    InvTypeHolder = "None"
    BranchIDHolder = ""
    StatusHolder = "Bought"

    # Initialize flags
    global InvNameFlag, InvValueFlag, InvTypeFlag, BranchIDFlag, StatusFlag
    InvNameFlag = False
    InvValueFlag = False
    InvTypeFlag = False
    BranchIDFlag = False
    StatusFlag = False

    global enteronce, diffvalue, enteronceforcombo
    enteronce = 0
    diffvalue = 0
    enteronceforcombo = 0

    # Create Add-specific widgets
    InventoryNameBox = CTkEntry(OutputEditContent, corner_radius=0, 
                              border_color='#000000', border_width=1,
                              placeholder_text="Inventory Name", width=390, height=25)
    InventoryNameBox.place(x=5, y=25)
    
    # Add Item/Cash selection combobox
    itemTypeVal = StringVar(value="Item")
    ItemTypeCombobox = CTkComboBox(OutputEditContent,
                                  values=["Item", "Cash"],
                                  variable=itemTypeVal, height=25,
                                  command=handle_item_type_change,
                                  corner_radius=1, width=110)
    ItemTypeCombobox.set("Item")
    ItemTypeCombobox.place(x=5, y=53)
    ItemTypeCombobox.configure(state="readonly")

    # Move original combobox down but keep Add button in original position
    comboVal = StringVar(value="Select")
    Inventory_combobox = CTkComboBox(OutputEditContent, 
                                   values=["Value", "Type", "Branch ID", "Status"],
                                   command=I_callback, variable=comboVal, height=25,
                                   corner_radius=1, width=110)
    Inventory_combobox.set("Select")
    Inventory_combobox.place(x=5, y=82)  # Changed y position
    Inventory_combobox.configure(state="readonly")

    Inventory_inputbutton = CTkButton(OutputEditContent, text="Add",
                                    corner_radius=0,
                                    command=lambda: I_handleaddinventory(),
                                    font=BTNFont, text_color='#000000',
                                    fg_color='#FFFFFF',
                                    border_color='#000000', border_width=1,
                                    hover_color='#e6e6e6', width=100, height=27)
    Inventory_inputbutton.place(x=295, y=82)  # Kept original y position

    InvAddExist = True

def handle_item_type_change(choice):
    """Handle changes to item type selection"""
    if choice == "Cash":
        InventoryNameBox.delete(0, END)
        InventoryNameBox.insert(0, "Balance")
        InventoryNameBox.configure(state="disabled")
    else:
        InventoryNameBox.configure(state="normal")
        InventoryNameBox.delete(0, END)
        InventoryNameBox.configure(placeholder_text="Inventory Name")

def I_editmodeui():
    """Initialize edit mode interface"""
    global InvEditExist, InventoryIDEdit, Inventory_combobox, Inventory_inputbutton
    global InvIDHolder, InvNameHolder, InvValueHolder, InvTypeHolder, BranchIDHolder, StatusHolder

    # Initialize holders
    InvIDHolder = ""
    InvNameHolder = ""
    InvValueHolder = ""
    InvTypeHolder = "None"
    BranchIDHolder = ""
    StatusHolder = "Bought"

    # Initialize flags
    global InvIDFlag, InvNameFlag, InvValueFlag, InvTypeFlag, BranchIDFlag, StatusFlag
    InvIDFlag = False
    InvNameFlag = False
    InvValueFlag = False
    InvTypeFlag = False
    BranchIDFlag = False
    StatusFlag = False

    global enteronce, diffvalue, enteronceforcombo
    enteronce = 0
    diffvalue = 0
    enteronceforcombo = 0

    # Create Edit-specific widgets
    InventoryIDEdit = CTkEntry(OutputEditContent, corner_radius=0,
                              border_color='#000000', border_width=1,
                              placeholder_text="Inventory ID", width=390, height=25)
    InventoryIDEdit.place(x=5, y=25)

    comboVal = StringVar(value="Select")
    Inventory_combobox = CTkComboBox(OutputEditContent,
                                   values=["Name", "Value", "Type", "Branch ID", "Status"],
                                   command=I_callback, variable=comboVal, height=25,
                                   corner_radius=1, width=110)
    Inventory_combobox.set("Select")
    Inventory_combobox.place(x=5, y=53)
    Inventory_combobox.configure(state="readonly")

    Inventory_inputbutton = CTkButton(OutputEditContent, text="Edit",
                                    corner_radius=0,
                                    command=lambda: I_handleeditinventory(),
                                    font=BTNFont, text_color='#000000',
                                    fg_color='#FFFFFF',
                                    border_color='#000000', border_width=1,
                                    hover_color='#e6e6e6', width=100, height=27)
    Inventory_inputbutton.place(x=295, y=82)

    InvEditExist = True

# Update the get_next_inventory_id function to generate 5-digit IDs
def get_next_inventory_id():
    """Get next available 5-digit inventory ID"""
    while True:
        next_id = random.randint(10000, 99999)
        success, error = execute_safe_query(cur, """
            SELECT EXISTS(SELECT 1 FROM Inventory WHERE InventoryId = %s)
        """, (next_id,))
        if not success:
            show_error_window(error)
            return None
        if not cur.fetchone()[0]:
            return next_id

def I_handleaddinventory():
    """Handle adding new inventory items"""
    # Validate inventory name
    inv_name = InventoryNameBox.get().strip()
    if not inv_name:
        show_error_window("Inventory name is required")
        return
        
    # Validate required fields
    if not all([InvValueFlag, InvTypeFlag, BranchIDFlag, StatusFlag]):
        show_error_window("Please fill in all required fields")
        return

    try:
        # Get next ID
        next_id = get_next_inventory_id()
        if next_id is None:
            return

        # Begin transaction
        success, error = execute_safe_query(cur, "BEGIN")
        if not success:
            show_error_window(error)
            return
            
        # Insert new inventory
        success, error = execute_safe_query(
            cur,
            """
            INSERT INTO Inventory (
                InventoryId, InventoryName, InventoryValue, 
                InventoryType, BranchId, GoodsStatus
            ) VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                next_id,
                inv_name,
                float(InvValueHolder),
                InvTypeHolder,
                int(BranchIDHolder),
                StatusHolder
            )
        )
        
        if not success:
            execute_safe_query(cur, "ROLLBACK")
            show_error_window(error)
            return

        # Commit transaction
        success, error = execute_safe_query(cur, "COMMIT")
        if not success:
            show_error_window(error)
            return
            
        # Clear UI and show success
        I_clear_ui_elements()
        show_success_message("Inventory item added successfully", OutputEditContent)
        
    except ValueError:
        execute_safe_query(cur, "ROLLBACK")
        show_error_window("Please enter valid numeric values")
    except Exception as e:
        execute_safe_query(cur, "ROLLBACK")
        show_error_window(f"Error adding inventory: {str(e)}")

def I_handleeditinventory():
    """Handle the inventory edit operation"""
    global ErrorBoolean, Error, viewederror, successful_transaction
    
    inventory_id = InventoryIDEdit.get().strip()
    
    # Check if ID is provided
    if inventory_id:
        try:
            # Check if inventory exists
            success, error = execute_safe_query(cur, """
                SELECT EXISTS(SELECT 1 FROM Inventory WHERE InventoryId = %s)
            """, (inventory_id,))
            if not success:
                show_error_window(error)
                return
            result = cur.fetchone()
            
            if result and result[0]:
                InvIDFlag = True
                InvIDHolder = inventory_id
                # Clear any existing error
                try:
                    if ErrorBoolean:
                        Error.destroy()
                        viewederror = 0
                        ErrorBoolean = False
                except Exception:
                    pass
            else:
                show_error_window("Inventory ID does not exist")
                return
                
        except Exception as e:
            show_error_window(f"Database error: {str(e)}")
            return
            
        if diffvalue > 0:  # Check if user has selected something to edit
            try:
                success, error = execute_safe_query(cur, "BEGIN")
                if not success:
                    show_error_window(error)
                    return
                updates_made = False
                
                # Handle updates based on what was edited
                if InvNameFlag:
                    success, error = execute_safe_query(cur, """
                        UPDATE Inventory 
                        SET InventoryName = %s 
                        WHERE InventoryId = %s
                    """, (InvNameHolder, inventory_id))
                    if not success:
                        show_error_window(error)
                        return
                    updates_made = True
                    
                if InvValueFlag:
                    if not InvValueHolder.replace('.', '').isdigit():
                        show_error_window("Value must be a number")
                        execute_safe_query(cur, "ROLLBACK")
                        return
                    success, error = execute_safe_query(cur, """
                        UPDATE Inventory 
                        SET InventoryValue = %s 
                        WHERE InventoryId = %s
                    """, (float(InvValueHolder), inventory_id))
                    if not success:
                        show_error_window(error)
                        return
                    updates_made = True
                    
                if InvTypeFlag:
                    success, error = execute_safe_query(cur, """
                        UPDATE Inventory 
                        SET InventoryType = %s 
                        WHERE InventoryId = %s
                    """, (InvTypeHolder, inventory_id))
                    if not success:
                        show_error_window(error)
                        return
                    updates_made = True
                
                if BranchIDFlag:
                    # Verify branch exists
                    success, error = execute_safe_query(cur, """
                        SELECT EXISTS(
                            SELECT 1 FROM goodwillbranch 
                            WHERE BranchId = %s
                        )
                    """, (BranchIDHolder,))
                    if not success:
                        show_error_window(error)
                        return
                    if cur.fetchone()[0]:
                        success, error = execute_safe_query(cur, """
                            UPDATE Inventory 
                            SET BranchId = %s 
                            WHERE InventoryId = %s
                        """, (BranchIDHolder, inventory_id))
                        if not success:
                            show_error_window(error)
                            return
                        updates_made = True
                    else:
                        execute_safe_query(cur, "ROLLBACK")
                        show_error_window("Invalid Branch ID")
                        return
                        
                if StatusFlag:
                    success, error = execute_safe_query(cur, """
                        UPDATE Inventory 
                        SET GoodsStatus = %s 
                        WHERE InventoryId = %s
                    """, (StatusHolder, inventory_id))
                    if not success:
                        show_error_window(error)
                        return
                    updates_made = True
                
                if updates_made:
                    success, error = execute_safe_query(cur, "COMMIT")
                    if not success:
                        show_error_window(error)
                        return
                    successful_transaction = True
                    I_clear_ui_elements()
                    show_success_message("Inventory updated successfully", OutputEditContent)
                else:
                    execute_safe_query(cur, "ROLLBACK")
                    show_error_window("No changes made")
                    
            except Exception as e:
                execute_safe_query(cur, "ROLLBACK")
                show_error_window(f"Error updating inventory: {str(e)}")
        else:
            show_error_window("Please select at least one field to update")
    else:
        show_error_window("Please enter an Inventory ID")

def I_deletemodeui():
    """Initialize delete mode interface"""
    global InvDeleteExist, InventoryIDDelete, Inventory_inputbutton
    InventoryIDDelete = CTkEntry(OutputEditContent, corner_radius=0,
                                border_color='#000000', border_width=1,
                                placeholder_text="Enter Inventory ID to delete",
                                width=390, height=25)
    InventoryIDDelete.place(x=5, y=25)

    Inventory_inputbutton = CTkButton(OutputEditContent, text="Delete",
                                    command=lambda: I_handledeleteinventory(InventoryIDDelete, Inventory_inputbutton),
                                    corner_radius=0, font=BTNFont,
                                    text_color='#000000', fg_color='#FFFFFF',
                                    border_color='#000000', border_width=1,
                                    hover_color='#e6e6e6', width=100, height=27)
    Inventory_inputbutton.place(x=295, y=82)
    InvDeleteExist = True

def I_callback(choice):
    """Handle combobox selection"""
    global enteronce, enteronceforcombo, diffvalue
    global InvNameHolder, InvValueHolder, InvTypeHolder, BranchIDHolder, StatusHolder
    global ErrorBoolean, Error, viewederror
    
    enteronce = enteronce + 1
    enteronceforcombo = enteronceforcombo + 1

    # Clear any existing errors
    if ErrorBoolean:
        Error.destroy()
        viewederror = 0
        ErrorBoolean = False

    if mode == "add":
        global AddValueEntryBox, AddTypeCombobox, AddBranchIDEntryBox, AddStatusCombobox, AddSearchBoxEnter
        
        if enteronce > 1:
            try:
                AddSearchBoxEnter.destroy()
            except:
                print('no searchbox')
            enteronce = 1
            
        if enteronce == 1:
            AddSearchBoxEnter = CTkButton(OutputEditContent, text="Confirm",
                                        corner_radius=0, font=BTNFont,
                                        command=lambda: I_confirmyourchoice(choice, AddSearchBoxEnter),
                                        text_color='#000000', fg_color='#FFFFFF',
                                        border_color='#000000', border_width=1,
                                        hover_color='#e6e6e6', width=100, height=27)
            AddSearchBoxEnter.place(x=190, y=82)

        # Clear previous entries
        if enteronceforcombo > 1:
            clear_previous_entries()
            enteronceforcombo = 1

        # Create new entry based on choice
        if enteronceforcombo == 1:
            create_entry_widget(choice)
    elif mode == "edit":
        global EditValueEntryBox, EditTypeCombobox, EditBranchIDEntryBox, EditStatusCombobox, EditSearchBoxEnter
        
        if enteronce > 1:
            try:
                EditSearchBoxEnter.destroy()
            except:
                print('no searchbox')
            enteronce = 1
            
        if enteronce == 1:
            EditSearchBoxEnter = CTkButton(OutputEditContent, text="Confirm",
                                        corner_radius=0, font=BTNFont,
                                        command=lambda: I_confirmyourchoice(choice, EditSearchBoxEnter),
                                        text_color='#000000', fg_color='#FFFFFF',
                                        border_color='#000000', border_width=1,
                                        hover_color='#e6e6e6', width=100, height=27)
            EditSearchBoxEnter.place(x=190, y=82)

        # Clear previous entries
        if enteronceforcombo > 1:
            clear_previous_entries()
            enteronceforcombo = 1

        # Create new entry based on choice
        if enteronceforcombo == 1:
            create_entry_widget(choice)

def create_entry_widget(choice):
    """Create appropriate entry widget based on selection"""
    global diffvalue
    
    if mode == "add":
        if choice == "Value":
            diffvalue = 1
            create_value_entry()
        elif choice == "Type":
            diffvalue = 2
            create_type_entry()
        elif choice == "Branch ID":
            diffvalue = 3
            create_branch_entry()
        elif choice == "Status":
            diffvalue = 4
            create_status_entry()
    elif mode == "edit":
        if choice == "Name":
            diffvalue = 1
            edit_name_entry()
        elif choice == "Value": 
            diffvalue = 2
            edit_value_entry()
        elif choice == "Type":
            diffvalue = 3
            edit_type_entry()
        elif choice == "Branch ID":
            diffvalue = 4
            edit_branch_entry()
        elif choice == "Status":
            diffvalue = 5
            edit_status_entry()

def create_value_entry():
    """Create value entry widget for add mode"""
    global InvValueEntryBox
    InvValueEntryBox = CTkEntry(OutputEditContent, corner_radius=0,border_color='#000000', border_width=1,placeholder_text="Inventory Value",width=275, height=25)
    InvValueEntryBox.place(x=120, y=53)
    if InvValueHolder:
        InvValueEntryBox.insert(0, InvValueHolder)

def create_type_entry():
    """Create type selection widget for add mode"""
    global InvTypeCombobox
    typeVal = StringVar(value="None")
    InvTypeCombobox = CTkComboBox(OutputEditContent,
                                 values=["None", "Asset", "Liability"],
                                 variable=typeVal, height=25,
                                 corner_radius=1, width=275)
    InvTypeCombobox.place(x=120, y=53)
    InvTypeCombobox.set(InvTypeHolder)
    InvTypeCombobox.configure(state="readonly")

def create_branch_entry():
    """Create branch ID entry widget"""
    global BranchIDEntryBox
    BranchIDEntryBox = CTkEntry(OutputEditContent, corner_radius=0,
                               border_color='#000000', border_width=1,
                               placeholder_text="Branch ID",
                               width=275, height=25)
    BranchIDEntryBox.place(x=120, y=53)
    if BranchIDHolder:
        BranchIDEntryBox.insert(0, BranchIDHolder)

def create_status_entry():
    """Create status selection widget with corrected status options"""
    global StatusCombobox
    statusVal = StringVar(value="Bought")  # Changed default value
    StatusCombobox = CTkComboBox(OutputEditContent,
                                values=["Bought", "Sold", "Donated"], # Changed status options
                                variable=statusVal, height=25,
                                corner_radius=1, width=275)
    StatusCombobox.place(x=120, y=53)
    StatusCombobox.set(StatusHolder)
    StatusCombobox.configure(state="readonly")

def edit_name_entry():
    """Create name entry widget for edit mode"""
    global EditNameEntryBox
    EditNameEntryBox = CTkEntry(OutputEditContent, corner_radius=0,
                               border_color='#000000', border_width=1,
                               placeholder_text="New Inventory Name",
                               width=275, height=25)
    EditNameEntryBox.place(x=120, y=53)
    if InvNameHolder:
        EditNameEntryBox.insert(0, InvNameHolder)

def edit_value_entry():
    """Create value entry widget for edit mode"""
    global EditValueEntryBox
    EditValueEntryBox = CTkEntry(OutputEditContent, corner_radius=0,
                                border_color='#000000', border_width=1,
                                placeholder_text="New Value",
                                width=275, height=25)
    EditValueEntryBox.place(x=120, y=53)
    if InvValueHolder:
        EditValueEntryBox.insert(0, InvValueHolder)

def edit_type_entry():
    """Create type selection widget for edit mode"""
    global EditTypeCombobox
    typeVal = StringVar(value=InvTypeHolder)
    EditTypeCombobox = CTkComboBox(OutputEditContent,
                                  values=["None", "Asset", "Liability"],
                                  variable=typeVal, height=25,
                                  corner_radius=1, width=275)
    EditTypeCombobox.place(x=120, y=53)
    EditTypeCombobox.configure(state="readonly")

def edit_branch_entry():
    """Create branch ID entry widget for edit mode"""
    global EditBranchIDEntryBox
    EditBranchIDEntryBox = CTkEntry(OutputEditContent, corner_radius=0,
                                   border_color='#000000', border_width=1,
                                   placeholder_text="New Branch ID",
                                   width=275, height=25)
    EditBranchIDEntryBox.place(x=120, y=53)
    if BranchIDHolder:
        EditBranchIDEntryBox.insert(0, BranchIDHolder)

def edit_status_entry():
    """Create status selection widget for edit mode with corrected status options"""
    global EditStatusCombobox
    statusVal = StringVar(value=StatusHolder)
    EditStatusCombobox = CTkComboBox(OutputEditContent,
                                    values=["Bought", "Sold", "Donated"], # Changed status options
                                    variable=statusVal, height=25,
                                    corner_radius=1, width=275)
    EditStatusCombobox.place(x=120, y=53)
    EditStatusCombobox.configure(state="readonly")

def clear_previous_entries():
    """Clear previous entry widgets based on mode and diffvalue"""
    try:
        if mode == "add":
            widgets_to_clear = {
                1: ['InvValueEntryBox'],
                2: ['InvTypeCombobox'],
                3: ['BranchIDEntryBox'],
                4: ['StatusCombobox']
            }
        else:  # edit mode
            widgets_to_clear = {
                1: ['EditNameEntryBox'],
                2: ['EditValueEntryBox'],
                3: ['EditTypeCombobox'],
                4: ['EditBranchIDEntryBox'],
                5: ['EditStatusCombobox']
            }

        if diffvalue in widgets_to_clear:
            for widget_name in widgets_to_clear[diffvalue]:
                if widget_name in globals() and globals()[widget_name] is not None:
                    try:
                        globals()[widget_name].place_forget()
                    except Exception:
                        pass
                        
    except Exception as e:
        print(f"Error clearing entries: {e}")

def I_clear_ui_elements():
    """Clear all UI elements and reset error states"""
    global viewederror, ErrorBoolean
    
    # Clear mode-specific widgets
    if mode == "add":
        widgets_to_clear = [InventoryNameBox, Inventory_combobox, Inventory_inputbutton, ItemTypeCombobox]  # Added ItemTypeCombobox
        for widget in widgets_to_clear:
            try:
                widget.place_forget()
            except Exception:
                pass
                
    elif mode == "edit":
        widgets_to_clear = [InventoryIDEdit, Inventory_combobox, Inventory_inputbutton]
        for widget in widgets_to_clear:
            try:
                widget.destroy()
            except Exception:
                pass
                
    elif mode == "delete":
        widgets_to_clear = [InventoryIDDelete, Inventory_inputbutton]
        for widget in widgets_to_clear:
            try:
                widget.destroy()
            except Exception:
                pass
    
    # Clear any error messages
    if 'Error' in globals() and Error.winfo_exists():
        Error.destroy()
        viewederror = 0
        ErrorBoolean = False

def I_confirmyourchoice(choice, SearchBoxEnter):
    """Handle confirmation of entry values"""
    global InvNameHolder, InvValueHolder, InvTypeHolder, BranchIDHolder, StatusHolder
    global InvNameFlag, InvValueFlag, InvTypeFlag, BranchIDFlag, StatusFlag
    
    if mode == "add":
        if choice == "Value":
            value = InvValueEntryBox.get().strip()
            if value and value.replace('.', '', 1).isdigit():
                InvValueHolder = value
                InvValueFlag = True
                clear_entry_and_button(choice, SearchBoxEnter)
            else:
                show_error_window("Value must be a valid number")

        elif choice == "Type":
            InvTypeHolder = InvTypeCombobox.get()
            InvTypeFlag = True
            clear_entry_and_button(choice, SearchBoxEnter)

        elif choice == "Branch ID":
            branch_id = BranchIDEntryBox.get().strip()
            if branch_id and branch_id.isdigit():
                # Verify branch exists
                success, error = execute_safe_query(
                    cur,
                    "SELECT EXISTS(SELECT 1 FROM goodwillbranch WHERE BranchId = %s)",
                    (branch_id,)
                )
                if not success:
                    show_error_window(error)
                    return
                    
                if cur.fetchone()[0]:
                    BranchIDHolder = branch_id
                    BranchIDFlag = True
                    clear_entry_and_button(choice, SearchBoxEnter)
                else:
                    show_error_window("Branch ID does not exist")
            else:
                show_error_window("Branch ID must be a number")

        elif choice == "Status":
            StatusHolder = StatusCombobox.get()
            StatusFlag = True
            clear_entry_and_button(choice, SearchBoxEnter)
    elif mode == "edit":
        if choice == "Name":
            InvNameHolder = EditNameEntryBox.get().strip()
            if InvNameHolder:
                InvNameFlag = True
                clear_entry_and_button(choice, SearchBoxEnter)
            else:
                show_error_window("Name cannot be empty")

        elif choice == "Value":
            value = EditValueEntryBox.get().strip()
            if value and value.replace('.', '', 1).isdigit():
                InvValueHolder = value
                InvValueFlag = True
                clear_entry_and_button(choice, SearchBoxEnter)
            else:
                show_error_window("Value must be a valid number")

        elif choice == "Type":
            InvTypeHolder = EditTypeCombobox.get()
            InvTypeFlag = True
            clear_entry_and_button(choice, SearchBoxEnter)

        elif choice == "Branch ID":
            branch_id = EditBranchIDEntryBox.get().strip()
            if branch_id and branch_id.isdigit():
                success, error = execute_safe_query(
                    cur,
                    "SELECT EXISTS(SELECT 1 FROM goodwillbranch WHERE BranchId = %s)",
                    (branch_id,)
                )
                if not success:
                    show_error_window(error)
                    return
                    
                if cur.fetchone()[0]:
                    BranchIDHolder = branch_id
                    BranchIDFlag = True
                    clear_entry_and_button(choice, SearchBoxEnter)
                else:
                    show_error_window("Branch ID does not exist")
            else:
                show_error_window("Branch ID must be a number")

        elif choice == "Status":
            StatusHolder = EditStatusCombobox.get()
            StatusFlag = True
            clear_entry_and_button(choice, SearchBoxEnter)

def clear_entry_and_button(choice, button):
    """Clear specific entry widget and confirmation button"""
    if mode == "add":
        if choice == "Value":
            InvValueEntryBox.place_forget()
        elif choice == "Type":
            InvTypeCombobox.place_forget()
        elif choice == "Branch ID":
            BranchIDEntryBox.place_forget()
        elif choice == "Status":
            StatusCombobox.place_forget()
    elif mode == "edit":
        if choice == "Name":
            EditNameEntryBox.place_forget()
        elif choice == "Value":
            EditValueEntryBox.place_forget()
        elif choice == "Type":
            EditTypeCombobox.place_forget()
        elif choice == "Branch ID":
            EditBranchIDEntryBox.place_forget()
        elif choice == "Status":
            EditStatusCombobox.place_forget()
    
    button.destroy()

# Update the delete function to fix the SQL syntax error
def I_handledeleteinventory(InventoryIDDelete, deleteinputbutton):
    """Handle the inventory deletion operation"""
    inventory_id = InventoryIDDelete.get().strip()
    
    if not inventory_id:
        show_error_window("Please enter inventory ID")
        return
    
    if inventory_id == 0:
        show_error_window("Inventory ID cannot be deleted.")
        return
        
    try:
        success, error = execute_safe_query(cur, "BEGIN")
        if not success:
            show_error_window(error)
            return
        
        # Check if inventory exists and can be deleted
        success, error = execute_safe_query(cur, """
            SELECT EXISTS(
                SELECT 1 FROM Inventory 
                WHERE InventoryId = %s 
                AND GoodsStatus = 'Sold'
            )
        """, (inventory_id,))
        if not success:
            show_error_window(error)
            return
        
        if cur.fetchone()[0]:
            success, error = execute_safe_query(cur, "DELETE FROM Inventory WHERE InventoryId = %s", (inventory_id,))
            if not success:
                show_error_window(error)
                return
            success, error = execute_safe_query(cur, "COMMIT")
            if not success:
                show_error_window(error)
                return
            I_clear_ui_elements()
            show_success_message("Inventory deleted successfully", OutputEditContent)
        else:
            execute_safe_query(cur, "ROLLBACK")
            show_error_window("Inventory not found or must be sold before deletion")
            
    except Exception as e:
        execute_safe_query(cur, "ROLLBACK")
        show_error_window(f"Error deleting inventory: {str(e)}")


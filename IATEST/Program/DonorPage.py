from customtkinter import *
import psycopg2
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


# Global variables
TitleFont = CTkFont(family="Oswald", size=15, weight='bold')
EditFont = CTkFont(family="Oswald", size=15, weight='bold')
BTNFont = CTkFont(family="Oswald", size=13)
ErrorFont = CTkFont(size=10)
DonorPagePost = 0

# Required datatypes
vieweditemflag = False
A_vieweditemflag = 0 
E_vieweditemflag = 0
D_vieweditemflag = 0 
viewederror = 0
ErrorBoolean = False
successful_transaction = False
currentmode = ""
DonorAddExist = False
DonorEditExist = False
DonorDeleteExist = False
ConfirmedChoiceForSearch = ""

# Add these global variables
DonAddExist = False
DonEditExist = False
DonDeleteExist = False
DonorAddExist = False
DonorEditExist = False
DonorDeleteExist = False

# For tracking entry states
AddAddressEntryBox = None
AddPhoneEntryBox = None
AddOrgEntryBox = None
AddDonationEntryBox = None
AddDonationTypeBox = None
AddSearchBoxEnter = None
EditSearchBoxEnter = None
DonorNameBox = None
Donor_combobox = None
Donor_inputbutton = None
DonorIDEdit = None
DonorIDDelete = None

# For tracking holder values
DonorIDHolder = ""
DonationIDHolder = ""
AddressHolder = ""
PhoneHolder = ""
OrgHolder = ""
DonationHolder = ""
DonationTypeHolder = "Item"
DateHolder = ""  # Add this line
BranchIDHolder = ""  # Add this line
DonNameHolder = ""  # Add this line

# For tracking flags
DonaIDFlag = False
DonaNameFlag = False #Added
DonaAddressFlag = False
DonaPhoneFlag = False
DonaOrgFlag = False
DonaDonationFlag = False
DonaBranchFlag = False  # Add this line

# For tracking mode and state
diffvalue = 0
enteronce = 0
enteronceforcombo = 0
mode = ""

def D_show_page(parent, page_frame):
    """Initialize and show the Donor page"""
    global DonorPagePost
    
    # Show the page
    page_frame.pack(fill=BOTH, expand=True)
    parent.update_idletasks()
    
    # Initialize content only once
    if DonorPagePost == 0:
        Donorpage(page_frame)

def Donorpage(page):
    global DonorPagePost, OutputEditContent, SearchRequestContent
    if DonorPagePost == 0:
        # Create page layout
        PageMargin = CTkFrame(page)
        PageMargin.pack(expand=True)
        
        RequestPadding = CTkFrame(PageMargin, width=170, height=330, fg_color="#dbdbdb", corner_radius=0, border_color='#000000', border_width=1)
        OutputPadding = CTkFrame(PageMargin, width=410, height=330, fg_color="#dbdbdb", corner_radius=0, border_color='#000000', border_width=1)
        
        RequestPadding.grid_propagate(0)
        OutputPadding.grid_propagate(0)
        
        RequestPadding.grid(row=0, column=0)
        OutputPadding.grid(row=0, column=1)

        # Create content frames
        SearchRequestContent = CTkFrame(RequestPadding, width=170, height=165, fg_color="#FFFFFF", corner_radius=0, border_color='#000000', border_width=1)
        EditsRequestContent = CTkFrame(RequestPadding, width=170, height=165, fg_color="#FFFFFF", corner_radius=0,border_color='#000000', border_width=1)
        
        SearchRequestContent.grid_propagate(0)
        EditsRequestContent.grid_propagate(0)
        
        SearchRequestContent.grid(row=0, column=0)
        EditsRequestContent.grid(row=1, column=0)
        
        # Grid configurations
        for i in range(1):
            EditsRequestContent.grid_columnconfigure(i, weight=1, uniform="column")
            EditsRequestContent.grid_rowconfigure(0, minsize=51)
        
        for i in range(1):
            SearchRequestContent.grid_columnconfigure(i, weight=1, uniform="column")
            SearchRequestContent.grid_rowconfigure(0, minsize=51)

        # Output Content setup
        global OutputTableScrollbarContent
        OutputEditContent = CTkFrame(OutputPadding, width=410, height=115, fg_color="#FFFFFF", corner_radius=0, border_color='#000000', border_width=1)
        OutputEditContent.grid(row=0, column=0)
        LabelDonorAdd = CTkLabel(OutputEditContent, text="DONORS", font=EditFont)
        LabelDonorAdd.place(x=5, y=1)

        OutputTableContent = CTkFrame(OutputPadding, width=410, height=215, fg_color="#a6a6a6", corner_radius=0, border_color='#000000', border_width=1)
        OutputTableContent.grid(row=1, column=0)
        OutputEditContent.grid_propagate(0)
        OutputTableContent.grid_propagate(0)

        # Setup scrollable content
        OutputTableScrollbarContent = CTkFrame(OutputTableContent, width=410, height=215)
        OutputTableScrollbarContent.pack(fill="both", expand=True)
        OutputTableScrollbarContent.grid_propagate(0)

        canvas = CTkCanvas(OutputTableScrollbarContent, width=410, height=215, highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = CTkScrollableFrame(canvas, width=387)
        scrollbar.grid(rowspan=100, row=0, column=0, sticky='nsew')

        # Setup Edit buttons section
        EditLabelRequest = CTkLabel(EditsRequestContent, text="EDITS", font=EditFont)
        EditLabelRequest.grid(row=0, column=0)

        AddButtonRequest = CTkButton(EditsRequestContent, text="ADD", corner_radius=0,command=lambda: D_outputContentGivenButtons(OutputEditContent, 1),font=BTNFont, text_color='#000000', fg_color='#FFFFFF',border_color='#000000', border_width=1, hover_color='#e6e6e6')
        AddButtonRequest.grid(row=1, column=0, padx=10, pady=4, sticky='nsew')

        EditButtonRequest = CTkButton(EditsRequestContent, text="EDIT", corner_radius=0,command=lambda: D_outputContentGivenButtons(OutputEditContent, 2),font=BTNFont, fg_color='#FFFFFF', text_color='#000000',border_color='#000000', border_width=1, hover_color='#e6e6e6')
        EditButtonRequest.grid(row=2, column=0, padx=10, pady=1, sticky='nsew')

        DeleteButtonRequest = CTkButton(EditsRequestContent, text="DELETE", corner_radius=0,command=lambda: D_outputContentGivenButtons(OutputEditContent, 3),font=BTNFont, fg_color='#FFFFFF', text_color='#000000',border_color='#000000', border_width=1, hover_color='#e6e6e6')
        DeleteButtonRequest.grid(row=3, column=0, padx=10, pady=2, sticky='nsew')

        # Setup Search section
        SearchLabel = CTkLabel(SearchRequestContent, text="DONORS", font=EditFont)
        SearchLabel.grid(row=0, column=0, padx=10, pady=0)

        SearchEntry = CTkEntry(SearchRequestContent, corner_radius=0,border_color='#000000', border_width=1,placeholder_text="Search")
        SearchEntry.grid(row=1, column=0, padx=10, pady=4)

        SearchButton = CTkButton(SearchRequestContent, text="Search", fg_color='#0053A0', corner_radius=0,  text_color='#FFFFFF', border_color='#000000',border_width=1, hover_color='#0051ff',command=lambda: DonorSearch(SearchEntry))
        SearchButton.grid(row=2, column=0, padx=10, pady=1)

        comboVal = StringVar(value="Donor Name")
        SearchComboChoices = CTkComboBox(SearchRequestContent, 
            values=["Donor Name", "Donation Name", "Date"],  # Simplified search options
            command=DonorSearch_ComboCallback, variable=comboVal, corner_radius=1)
        SearchComboChoices.set("Donor Name")
        SearchComboChoices.grid(row=3, column=0, padx=10, pady=2)
        SearchComboChoices.configure(state="readonly")

        DonorPagePost = 1
    else:
        print("Page has already been outputted!")

def DonorSearch_ComboCallback(choice):
    global ConfirmedChoiceForSearch
    search_types = {
        "Donor Name": "Donor Name",
        "Donation Name": "Donation Name",
        "Date": "Date"
    }
    if choice in search_types:
        ConfirmedChoiceForSearch = search_types[choice]
    else:
        ConfirmedChoiceForSearch = "Donor Name"

def DonorSearch(SearchEntry):
    global ConfirmedChoiceForSearch, OutputTableScrollbarContent
    for widget in OutputTableScrollbarContent.winfo_children():
        widget.destroy()
    
    try:
        search_value = SearchEntry.get().strip()
        params = {'search_value': search_value}
        
        base_query = """
        SELECT 
            d.DonorID,
            d.DonorName,
            d.DonorAddress,
            d.DonorPhoneNumber,
            d.DonorOrganization,
            i.InventoryId as DonationID,
            i.InventoryName as DonationName,
            i.InventoryValue as DonationAmount,
            i.InventoryType as DonationType,
            g.BranchId,
            g.BranchName
        FROM Donor d
        LEFT JOIN Inventory i ON d.DonationID = i.InventoryId
        LEFT JOIN goodwillbranch g ON i.BranchId = g.BranchId
        WHERE 1=1
        """
        
        search_conditions = {
            "Donor Name": "LOWER(d.DonorName) LIKE LOWER(%(like_value)s)",
            "Donation Name": "LOWER(i.InventoryName) LIKE LOWER(%(like_value)s)",
            "Date": "DATE(i.DateCreated) = %(search_value)s"  # Assuming you have a date field
        }

        if search_value and ConfirmedChoiceForSearch in search_conditions:
            condition = search_conditions[ConfirmedChoiceForSearch]
            if ConfirmedChoiceForSearch == "Date":
                try:
                    datetime.strptime(search_value, "%Y/%m/%d")
                    params['search_value'] = search_value
                except ValueError:
                    raise ValueError("Date format must be YYYY/MM/DD")
            else:
                params['like_value'] = f"%{search_value}%"
            base_query += f" AND {condition}"

        cur.execute(base_query, params)
        rows = cur.fetchall()

        if rows:
            tree = ttk.Treeview(OutputTableScrollbarContent, show="headings", height=10, selectmode="browse")
            columns = [
                # Donor columns
                "DonorID", "DonorName", "DonorAddress", "PhoneNumber", "Organization",
                # Inventory columns
                "DonationID", "DonationName", "DonationAmount", "DonationType",
                # Branch columns
                "BranchID", "BranchName"
            ]
            tree["columns"] = columns
            
            # Adjust column widths and order
            column_widths = {
                # Donor info
                "DonorID": 80,
                "DonorName": 250,
                "DonorAddress": 350,
                "PhoneNumber": 120,
                "Organization": 150,
                # Inventory info
                "DonationID": 80,
                "DonationName": 150,
                "DonationAmount": 100,
                "DonationType": 100,
                # Branch info
                "BranchID": 80,
                "BranchName": 150
            }
            
            
            style = ttk.Style()
            style.configure("Treeview")  # Increase row height
            # Configure columns with sections
            sections = {
                "Donor Info": ["DonorID", "DonorName", "DonorAddress", "PhoneNumber", "Organization"],
                "Donation Info": ["DonationID", "DonationName", "DonationAmount", "DonationType"],
                "Branch Info": ["BranchID", "BranchName"]
            }
            
            for col, width in column_widths.items():
                tree.column(col, width=width, anchor="w")  # Left align
                # Add section prefix to column headers
                for section, cols in sections.items():
                    if col in cols:
                        tree.heading(col, text=f"{col}")
                        break
            
            # Configure horizontal scrolling
            tree.configure(xscrollcommand=lambda *args: x_scrollbar.set(*args))
            x_scrollbar = ttk.Scrollbar(OutputTableScrollbarContent, orient="horizontal", command=tree.xview)
            x_scrollbar.grid(row=1, column=0, sticky="ew")
            
            for row in rows:
                tree.insert("", "end", values=row)
            
            # Add scrollbars
            y_scrollbar = ttk.Scrollbar(OutputTableScrollbarContent, orient="vertical", command=tree.yview)
            x_scrollbar = ttk.Scrollbar(OutputTableScrollbarContent, orient="horizontal", command=tree.xview)
            tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
            
            tree.grid(row=0, column=0, sticky="nsew")
            y_scrollbar.grid(row=0, column=1, sticky="ns")
            x_scrollbar.grid(row=1, column=0, sticky="ew")
            
            OutputTableScrollbarContent.grid_rowconfigure(0, weight=1)
            OutputTableScrollbarContent.grid_columnconfigure(0, weight=1)
        else:
            error_label = CTkLabel(OutputTableScrollbarContent, text="No results found", text_color="red")
            error_label.grid(row=0, column=0, sticky="nsew")
            
    except ValueError as ve:
        error_label = CTkLabel(OutputTableScrollbarContent, text=str(ve), text_color="red")
        error_label.grid(row=0, column=0, sticky="nsew")
    except Exception as e:
        error_label = CTkLabel(OutputTableScrollbarContent, text=f"An error occurred: {str(e)}", text_color="red")
        error_label.grid(row=0, column=0, sticky="nsew")

def D_outputContentGivenButtons(OutputEditContent, value):
    global vieweditemflag, A_vieweditemflag, E_vieweditemflag, D_vieweditemflag, currentmode, mode
    if value == 1:
        mode = "add"
    elif value == 2:
        mode = "edit"
    elif value == 3:
        mode = "delete"
        
    if currentmode == mode:
        return
        
    D_clearcurrentmode()
    
    if currentmode == "":
        vieweditemflag = 0
        
    if mode == "add":
        D_addmodeui()
    elif mode == "edit":
        D_editmodeui()
    elif mode == "delete":
        D_deletemodeui()
        
    currentmode = mode

def D_clearcurrentmode():
    global DonAddExist, DonEditExist, DonDeleteExist, diffvalue, viewederror, ErrorBoolean
    global Donor_inputbutton, DonorNameBox, Donor_combobox
    global AddAddressEntryBox, AddPhoneEntryBox, AddOrgEntryBox, AddDonationEntryBox, AddDonationTypeBox
    global AddSearchBoxEnter, DonorIDEdit, EditSearchBoxEnter, DonorIDDelete

    # Handle Add mode cleanup
    if DonAddExist:
        try:
            if 'DonorNameBox' in globals() and DonorNameBox is not None:
                DonorNameBox.place_forget()
            if 'Donor_combobox' in globals() and Donor_combobox is not None:
                Donor_combobox.place_forget()
        except Exception as e:
            print(f"Add cleanup error: {e}")

        # Clear error messages
        try:
            if ErrorBoolean and 'Error' in globals():
                Error.destroy()
                viewederror = 0
                ErrorBoolean = False
        except Exception:
            pass

        # Clear entry boxes based on diffvalue
        try:
            if diffvalue == 1 and 'AddAddressEntryBox' in globals():
                AddAddressEntryBox.place_forget()
            elif diffvalue == 2 and 'AddPhoneEntryBox' in globals():
                AddPhoneEntryBox.place_forget()
            elif diffvalue == 3 and 'AddOrgEntryBox' in globals():
                AddOrgEntryBox.place_forget()
            elif diffvalue == 4:
                if 'AddDonationEntryBox' in globals():
                    AddDonationEntryBox.place_forget()
                if 'AddDonationTypeBox' in globals():
                    AddDonationTypeBox.place_forget()
                if 'DonationNameEntryBox' in globals() and DonationNameEntryBox is not None:
                    DonationNameEntryBox.place_forget()  # Add this line
            elif diffvalue == 5 and 'AddDateEntryBox' in globals():
                    AddDateEntryBox.place_forget()
            elif diffvalue == 6 and 'AddBranchIDEntryBox' in globals():
                    AddBranchIDEntryBox.place_forget()
            if diffvalue > 0 and 'AddSearchBoxEnter' in globals():
                AddSearchBoxEnter.destroy()
        except Exception as e:
            print(f"Entry cleanup error: {e}")

        DonAddExist = False

    # Handle Edit mode cleanup
    if DonEditExist:
        try:
            if 'DonorIDEdit' in globals() and DonorIDEdit is not None:
                DonorIDEdit.destroy()
            if 'Donor_combobox' in globals() and Donor_combobox is not None:
                Donor_combobox.destroy()
            if 'EditDonationEntryBox' in globals() and EditDonationEntryBox is not None:
                EditDonationEntryBox.destroy()
            if 'EditDonationTypeBox' in globals() and EditDonationTypeBox is not None:
                EditDonationTypeBox.destroy()
            if 'EditDonationIDEntryBox' in globals() and EditDonationIDEntryBox is not None:
                EditDonationIDEntryBox.destroy()
        except Exception as e:
            print(f"Edit cleanup error: {e}")
        
        try:
            if ErrorBoolean and 'Error' in globals():
                Error.destroy()
                viewederror = 0
                ErrorBoolean = False
        except Exception:
            pass

        # Clear entry boxes based on diffvalue
        try:
            if diffvalue == 1 and 'EditNameEntryBox' in globals():
                EditNameEntryBox.place_forget()
            elif diffvalue == 2 and 'EditAddressEntryBox' in globals():
                EditAddressEntryBox.place_forget()
            elif diffvalue == 3 and 'EditPhoneEntryBox' in globals():
                EditPhoneEntryBox.place_forget()
            elif diffvalue == 4 and 'EditOrgEntryBox' in globals():
                EditOrgEntryBox.place_forget()
            elif diffvalue == 5:
                if 'EditDonationEntryBox' in globals():
                    EditDonationEntryBox.place_forget()
                if 'EditDonationTypeBox' in globals():
                    EditDonationTypeBox.place_forget()
            elif diffvalue == 6 and 'EditBranchIDEntryBox' in globals():
                    EditBranchIDEntryBox.place_forget()
            
            if diffvalue > 0 and 'AddSearchBoxEnter' in globals():
                EditSearchBoxEnter.destroy()
        except Exception as e:
            print(f"Entry cleanup error: {e}")

        DonEditExist = False

    # Handle Delete mode cleanup
    if DonDeleteExist:
        try:
            if 'DonorIDDelete' in globals() and DonorIDDelete is not None:
                DonorIDDelete.destroy()
        except Exception:
            pass
        DonDeleteExist = False

    # Clean up common elements
    try:
        if 'Donor_inputbutton' in globals() and Donor_inputbutton is not None:
            Donor_inputbutton.destroy()
    except Exception:
        pass

def D_addmodeui():
    global DonAddExist, DonorNameBox, Donor_inputbutton, Donor_combobox, successful_transaction
    global AddressHolder, PhoneHolder, OrgHolder, DonationHolder, DonationTypeHolder
    
    # Initialize holders
    AddressHolder = ""
    PhoneHolder = ""
    OrgHolder = ""
    DonationHolder = ""
    DonationTypeHolder = "Item"
    successful_transaction = False

    # Initialize flags
    global DonaAddressFlag, DonaPhoneFlag, DonaOrgFlag, DonaDonationFlag
    DonaAddressFlag = False
    DonaPhoneFlag = False
    DonaOrgFlag = False
    DonaDonationFlag = False

    global enteronce, diffvalue, enteronceforcombo
    enteronce = 0
    diffvalue = 0
    enteronceforcombo = 0

    # Create Add-specific widgets
    DonorNameBox = CTkEntry(OutputEditContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="Donor Name", width=390, height=25)
    DonorNameBox.place(x=5, y=25)

    comboVal = StringVar(value="Select")
    Donor_combobox = CTkComboBox(OutputEditContent, values=["Address", "Phone Number", "Organization", "Donation", "Date", "Branch ID"], command=D_callback, variable=comboVal, height=25, corner_radius=1, width=110)
    Donor_combobox.set("Select")
    Donor_combobox.place(x=5, y=53)
    Donor_combobox.configure(state="readonly")

    Donor_inputbutton = CTkButton(OutputEditContent, text="Add",  corner_radius=0, command=lambda: D_handleaddDonor(), font=BTNFont, text_color='#000000', fg_color='#FFFFFF', border_color='#000000',border_width=1, hover_color='#e6e6e6',width=100, height=27)
    Donor_inputbutton.place(x=295, y=82)

    DonAddExist = True

def D_editmodeui():
    global DonEditExist, DonorIDEdit, Donor_combobox, Donor_inputbutton, successful_transaction
    global DonorIDHolder, DonorNameHolder, AddressHolder, PhoneHolder, OrgHolder, DonationHolder, DonationTypeHolder,DonationIDHolder
    
        # Initialize holders
    DonorIDHolder = ""
    DonationIDHolder = ""
    DonorNameHolder = ""  #Added
    AddressHolder = ""
    PhoneHolder = ""
    OrgHolder = ""
    DonationHolder = ""
    DonationTypeHolder = "Item"
    successful_transaction = False

    # Initialize flags
    global DonaIDFlag,DonaNameFlag, DonaAddressFlag, DonaPhoneFlag, DonaOrgFlag, DonaDonationFlag
    DonaIDFlag = False
    DonaNameFlag = False #Added
    DonaAddressFlag = False
    DonaPhoneFlag = False
    DonaOrgFlag = False
    DonaDonationFlag = False

    global enteronce, diffvalue, enteronceforcombo
    enteronce = 0
    diffvalue = 0
    enteronceforcombo = 0
    
    # Similar setup to addmodeui but for editing
    DonorIDEdit = CTkEntry(OutputEditContent, corner_radius=0,border_color='#000000', border_width=1,placeholder_text="Donor ID", width=390, height=25)
    DonorIDEdit.place(x=5, y=25)

    
    comboVal = StringVar(value="Select")
    Donor_combobox = CTkComboBox(OutputEditContent,values=["Name", "Address", "Phone Number", "Organization", "Donation ID", "Branch ID"], command=D_callback, variable=comboVal, height=25, corner_radius=1, width=110)
    Donor_combobox.set("Select")
    Donor_combobox.place(x=5, y=53)
    Donor_combobox.configure(state="readonly")

    Donor_inputbutton = CTkButton(OutputEditContent, text="Edit",corner_radius=0, command=lambda: D_handleeditDonor(), font=BTNFont, text_color='#000000', fg_color='#FFFFFF', border_color='#000000', border_width=1, hover_color='#e6e6e6',width=100, height=27)
    Donor_inputbutton.place(x=295, y=82)

    DonEditExist = True

def D_deletemodeui():
    global DonDeleteExist, DonorIDDelete, Donor_inputbutton
    DonorIDDelete = CTkEntry(OutputEditContent, corner_radius=0,border_color='#000000', border_width=1,placeholder_text="Enter Donor ID to delete",width=390, height=25)
    DonorIDDelete.place(x=5, y=25)

    Donor_inputbutton = CTkButton(OutputEditContent, text="Delete", command=lambda: D_handledeleteDonor(DonorIDDelete, Donor_inputbutton), corner_radius=0, font=BTNFont,text_color='#000000', fg_color='#FFFFFF',border_color='#000000', border_width=1, hover_color='#e6e6e6', width=100, height=27)
    Donor_inputbutton.place(x=295, y=82)
    DonDeleteExist = True

def D_callback(choice):
    global enteronce, enteronceforcombo, diffvalue
    global AddressHolder, PhoneHolder, OrgHolder, DonationHolder, DonationTypeHolder
    global ErrorBoolean, Error, viewederror
    
    enteronce = enteronce + 1
    enteronceforcombo = enteronceforcombo + 1

    # Clear any existing errors
    if ErrorBoolean:
        Error.destroy()
        viewederror = 0
        ErrorBoolean = False

    if mode == "add":
        global AddAddressEntryBox, AddPhoneEntryBox, AddOrgEntryBox, AddDonationEntryBox, AddDonationTypeBox, AddSearchBoxEnter
        
        if enteronce > 1:
            try:
                AddSearchBoxEnter.destroy()
            except:
                print('no searchbox')
            enteronce = 1
            
        if enteronce == 1:
            AddSearchBoxEnter = CTkButton(OutputEditContent, text="Confirm", corner_radius=0, font=BTNFont,command=lambda: D_confirmyourchoice(choice, AddSearchBoxEnter),text_color='#000000', fg_color='#FFFFFF',border_color='#000000', border_width=1,hover_color='#e6e6e6', width=100, height=27)
            AddSearchBoxEnter.place(x=190, y=82)

        # Clear previous entries
        if enteronceforcombo > 1:
            clear_previous_entries()
            enteronceforcombo = 1

        # Create new entry based on choice
        if enteronceforcombo == 1:
            create_entry_widget(choice)
            
    elif mode == "edit":
        global EditAddressEntryBox, EditPhoneEntryBox, EditOrgEntryBox, EditDonationEntryBox, EditDonationTypeBox, EditSearchBoxEnter
        
        if enteronce > 1:
            try:
                EditSearchBoxEnter.destroy()
            except:
                print('no searchbox')
            enteronce = 1
            
        if enteronce == 1:
            EditSearchBoxEnter = CTkButton(OutputEditContent, text="Confirm", corner_radius=0, font=BTNFont,command=lambda: D_confirmyourchoice(choice, EditSearchBoxEnter),text_color='#000000', fg_color='#FFFFFF',border_color='#000000', border_width=1,hover_color='#e6e6e6', width=100, height=27)
            EditSearchBoxEnter.place(x=190, y=82)

        # Clear previous entries
        if enteronceforcombo > 1:
            clear_previous_entries()
            enteronceforcombo = 1

        # Create new entry based on choice
        if enteronceforcombo == 1:
            create_entry_widget(choice)

    elif mode == "delete":
        pass

def clear_previous_entries():
    global diffvalue
    try:
        if mode == "add":
            widgets_to_clear = {
                1: ['AddAddressEntryBox'],
                2: ['AddPhoneEntryBox'],
                3: ['AddOrgEntryBox'],
                4: ['AddDonationEntryBox', 'AddDonationTypeBox', 'DonationNameEntryBox'],  # Add DonationNameEntryBox here
                5: ['AddDateEntryBox'],
                6: ['AddBranchIDEntryBox']
            }
        else:  # edit mode
            widgets_to_clear = {
                1: ['EditNameEntryBox'],
                2: ['EditAddressEntryBox'],
                3: ['EditPhoneEntryBox'],
                4: ['EditOrgEntryBox'],
                5: ['EditDonationEntryBox', 'EditDonationTypeBox', 'EditDonationIDEntryBox'],
                6: ['EditBranchIDEntryBox']
            }

        # Only clear widgets for current diffvalue
        if diffvalue in widgets_to_clear:
            for widget_name in widgets_to_clear[diffvalue]:
                if widget_name in globals() and globals()[widget_name] is not None:
                    try:
                        widget = globals()[widget_name]
                        if widget.winfo_exists():  # Check if widget still exists
                            widget.place_forget()
                    except Exception:
                        pass  # Widget already destroyed or doesn't exist
                        
    except Exception as e:
        print(f"Error clearing entries: {e}")

def create_entry_widget(choice):
    global diffvalue, AddressHolder, PhoneHolder, OrgHolder, DonationHolder
    if mode == "add":   #If the mode is  add then itll run -----------------------------------------------------------------------------------------------------------
        if choice == "Address": #the choice for address
            diffvalue = 1
            CreateAddressEntry() #which is moves to the createaddressentry function
        elif choice == "Phone Number":
            diffvalue = 2 #the choice for phone number
            CreatePhoneEntry()
        elif choice == "Organization":
            diffvalue = 3 #this is the choice for adding organization name (should allow N/A or EMPTY)
            CreateOrgEntry()
        elif choice == "Donation":
            diffvalue = 4 #this is the choice for adding donation
            CreateDonationEntry()
            
        elif choice == "Date":
            diffvalue = 5 #this is the choice for adding date
            CreateDateEntry()
        elif choice == "Branch ID":
            diffvalue = 6
            CreateBranchIDEntry()
    elif mode == "edit": #if the mode is edit then itll run----------------------------------------------------------------------------------------------------------------
        if choice == "Name":
            diffvalue = 1 
            EditNameEntry()
        if choice == "Address":
            diffvalue = 2
            EditAddressEntry()
        elif choice == "Phone Number":
            diffvalue = 3
            EditPhoneEntry()
        elif choice == "Organization":
            diffvalue = 4
            EditOrgEntry()
        elif choice == "Donation ID":
            diffvalue = 5
            EditDonationIDEntry()
        elif choice == "Branch ID":
            diffvalue = 6
            EditBranchIDEntry()
   
#EDIT FUNCTIONSSSSS===================================================================-=-=-=-0)+_+)+_+_+)+_

def EditNameEntry():
    global EditNameEntryBox
    EditNameEntryBox = CTkEntry(OutputEditContent, corner_radius=0,border_color='#000000', border_width=1,placeholder_text="Donor Name",width=275, height=25)
    EditNameEntryBox.place(x=120, y=53)
    if DonorNameHolder == "":
        EditNameEntryBox.delete(0,END)
        EditNameEntryBox.configure(placeholder_text= "Donor Name")
    else:
        EditNameEntryBox.insert(0, DonorNameHolder)
    
def EditAddressEntry():
    global EditAddressEntryBox
    EditAddressEntryBox = CTkEntry(OutputEditContent, corner_radius=0,border_color='#000000', border_width=1,placeholder_text="Donor Address",width=275, height=25)
    EditAddressEntryBox.place(x=120, y=53)
    if AddressHolder == "":
        EditAddressEntryBox.delete(0,END)
        EditAddressEntryBox.configure(placeholder_text= "Donor Address")
    else:
        EditAddressEntryBox.insert(0, AddressHolder)

def EditPhoneEntry():
    global EditPhoneEntryBox
    EditPhoneEntryBox = CTkEntry(OutputEditContent, corner_radius=0,border_color='#000000', border_width=1,placeholder_text="Phone Number",width=275, height=25)
    EditPhoneEntryBox.place(x=120, y=53)
    if PhoneHolder == "":
        EditPhoneEntryBox.delete(0,END)
        EditPhoneEntryBox.configure(placeholder_text= "Phone Number")
    else:
        EditPhoneEntryBox.insert(0, PhoneHolder)
    
def EditOrgEntry():
    global EditOrgEntryBox
    EditOrgEntryBox = CTkEntry(OutputEditContent, corner_radius=0,border_color='#000000', border_width=1,placeholder_text="Organization Name",width=275, height=25)
    EditOrgEntryBox.place(x=120, y=53)
    if OrgHolder == "":
        EditOrgEntryBox.delete(0,END)
        EditOrgEntryBox.configure(placeholder_text="Organization Name")
    else:
        EditOrgEntryBox.insert(0, OrgHolder)

def EditDonationEntry():
    global EditDonationEntryBox, EditDonationTypeBox, EditDonationIDEntryBox
    EditDonationEntryBox = CTkEntry(OutputEditContent, corner_radius=0, border_color='#000000', border_width=1,placeholder_text="Donation Amount/Item", width=275, height=25)
    EditDonationEntryBox.place(x=120, y=53)
    EditDonationEntryBox.insert(0, DonationHolder)
    

    if DonationHolder == "" or DonationIDHolder == "":
        if DonationHolder == "":
            EditDonationEntryBox.delete(0, END)
            EditDonationEntryBox.configure(placeholder_text="Donation ID")
    else:
        if DonationHolder != "":
            EditDonationEntryBox.insert(0, DonationHolder)

def EditDateEntry():
    global EditDateEntryBox
    EditDateEntryBox = CTkEntry(OutputEditContent, corner_radius=0,border_color='#000000', border_width=1,placeholder_text="Date",width=275, height=25)
    EditDateEntryBox.place(x=120, y=53)
    if DateHolder == "":
        EditDateEntryBox.delete(0,END)
        EditDateEntryBox.configure(placeholder_text= "Date")
    else:
        EditDateEntryBox.insert(0, DateHolder)

def EditBranchIDEntry():
    global EditBranchIDEntryBox
    EditBranchIDEntryBox = CTkEntry(OutputEditContent, corner_radius=0,
        border_color='#000000', border_width=1,
        placeholder_text="Branch ID", width=275, height=25)
    EditBranchIDEntryBox.place(x=120, y=53)
    if BranchIDHolder:
        EditBranchIDEntryBox.insert(0, BranchIDHolder)

def EditDonationIDEntry():
    global EditDonationIDEntryBox
    EditDonationIDEntryBox = CTkEntry(OutputEditContent, corner_radius=0,
        border_color='#000000', border_width=1,
        placeholder_text="Donation ID", width=275, height=25)
    EditDonationIDEntryBox.place(x=120, y=53)
    if DonationIDHolder:
        EditDonationIDEntryBox.insert(0, DonationIDHolder)
        
#ADD FUNCTIONSSSSS===================================================================-=-=-=-0)+_+)+_+_+)+_

def CreateAddressEntry():
    global AddAddressEntryBox
    AddAddressEntryBox = CTkEntry(OutputEditContent, corner_radius=0,border_color='#000000', border_width=1,placeholder_text="Donor Address",width=275, height=25)
    AddAddressEntryBox.place(x=120, y=53)
    if AddressHolder == "":
        AddAddressEntryBox.delete(0,END)
        AddAddressEntryBox.configure(placeholder_text= "Donor Address")
    else:
        AddAddressEntryBox.insert(0, AddressHolder)

def CreatePhoneEntry():
    global AddPhoneEntryBox
    AddPhoneEntryBox = CTkEntry(OutputEditContent, corner_radius=0,border_color='#000000', border_width=1,placeholder_text="Phone Number",width=275, height=25)
    AddPhoneEntryBox.place(x=120, y=53)
    if PhoneHolder == "":
        AddPhoneEntryBox.delete(0,END)
        AddPhoneEntryBox.configure(placeholder_text= "Phone Number")
    else:
        AddPhoneEntryBox.insert(0, PhoneHolder)
    

def CreateOrgEntry():
    global AddOrgEntryBox
    AddOrgEntryBox = CTkEntry(OutputEditContent, corner_radius=0,border_color='#000000', border_width=1,placeholder_text="Organization Name",width=275, height=25)
    AddOrgEntryBox.place(x=120, y=53)
    if OrgHolder == "":
        AddOrgEntryBox.delete(0,END)
        AddOrgEntryBox.configure(placeholder_text="Organization Name")
    else:
        AddOrgEntryBox.insert(0, OrgHolder)

def CreateDonationEntry():
    global AddDonationEntryBox, AddDonationTypeBox, DonationNameEntryBox, DonNameHolder, DonationHolder
    AddDonationEntryBox = CTkEntry(OutputEditContent, corner_radius=0, border_color='#000000', border_width=1,placeholder_text="Donation Amount/Item", width=132, height=25)
    AddDonationEntryBox.place(x=120, y=53)
       
    DonationNameEntryBox = CTkEntry(OutputEditContent, corner_radius=0, border_color='#000000', border_width=1,placeholder_text="Donation Name", width=132, height=25)
    DonationNameEntryBox.place(x=260, y=53)
    
    comboVal = StringVar(value=DonationTypeHolder)
    AddDonationTypeBox = CTkComboBox(OutputEditContent,values=["Item", "Funds"],variable=comboVal,height=25, corner_radius=1, width=110)
    AddDonationTypeBox.place(x=5, y=82)
    AddDonationTypeBox.configure(state="readonly")
 
    # Display saved values
    if DonationHolder:
        AddDonationEntryBox.delete(0, END)
        AddDonationEntryBox.insert(0, DonationHolder)
    
    if DonNameHolder:
        DonationNameEntryBox.delete(0, END)
        DonationNameEntryBox.insert(0, DonNameHolder)

def CreateDateEntry():
    global AddDateEntryBox, DateHolder
    AddDateEntryBox = CTkEntry(OutputEditContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="Date (YYYY/MM/DD)", width=275, height=25)
    AddDateEntryBox.place(x=120, y=53)
    
    if DateHolder:
        AddDateEntryBox.insert(0, DateHolder)

def CreateBranchIDEntry():
    global AddBranchIDEntryBox
    AddBranchIDEntryBox = CTkEntry(OutputEditContent, corner_radius=0,
        border_color='#000000', border_width=1,
        placeholder_text="Branch ID", width=275, height=25)
    AddBranchIDEntryBox.place(x=120, y=53)
    if BranchIDHolder:
        AddBranchIDEntryBox.insert(0, BranchIDHolder)

def D_confirmyourchoice(choice, SearchBoxEnter):
    global AddressHolder, PhoneHolder, OrgHolder, DonationHolder, DonationTypeHolder, DonorNameHolder, DateHolder, DonorIDHolder,DonationIDHolder, BranchIDHolder
    global DonaNameFlag, DonaIDFlag, DonaAddressFlag, DonaPhoneFlag, DonaOrgFlag, DonaDonationFlag, DonaIDFlag, DonaBranchFlag
    
    if mode == "add":
        if choice == "Address":
            AddressHolder = AddAddressEntryBox.get()
            clear_entry_and_button(choice, SearchBoxEnter)
            DonaAddressFlag = True
            
        elif choice == "Phone Number":
            PhoneHolder = AddPhoneEntryBox.get()
            if PhoneHolder.isdigit() and len (PhoneHolder) >= 5 and len(PhoneHolder) <= 15:
                clear_entry_and_button(choice, SearchBoxEnter)
                DonaPhoneFlag = True
            else:
                if PhoneHolder.isdigit() == False: #IF PHONE HOLDER IS NOT A NUMBER
                    show_error("Phone number must be a number")
                    return
                elif len(PhoneHolder) < 5 or len(PhoneHolder) > 15: #IF PHONE HOLDER HAS LESS THAN 5 BUT MORE THAN 15 (out of bounds for phone number)
                    show_error("Phone number must be between 5 and 15 digits")
                return
                
        elif choice == "Organization":
            OrgHolder = AddOrgEntryBox.get()
            if OrgHolder == "": #IF ORG HOLDER IS EMPTY
                OrgHolder = "N/A"#THIS WILL RUN
            DonaOrgFlag = True
            clear_entry_and_button(choice, SearchBoxEnter)
            
        elif choice == "Donation":
            global DonNameHolder  # Ensure we use the global variable
            temp_donation = AddDonationEntryBox.get()
            temp_name = DonationNameEntryBox.get()
            temp_type = AddDonationTypeBox.get()
            
            # Validate based on donation type
            if temp_type == "Funds":
                if not temp_donation.isdigit():
                    show_error("Funds must be a number")
                    return
                DonNameHolder = "Funds"  # For funds, use standard name
            else:  # Item donation
                if not temp_name:
                    show_error("Please enter a name for the donation item")
                    return
                DonNameHolder = temp_name  # Set the donation name
                
            # After validation, set the holders
            DonationHolder = temp_donation
            DonationTypeHolder = temp_type
            DonaDonationFlag = True
            clear_entry_and_button(choice, SearchBoxEnter)
        
        elif choice == "Date":
            DateHolder = AddDateEntryBox.get()  
            try:
                # Try to convert the input to a datetime object using the desired format
                datetime.strptime(DateHolder, "%Y/%m/%d")  # format: YYYY/MM/DD
                DonaDonationFlag = True 
                AddDateEntryBox.place_forget()
                AddSearchBoxEnter.destroy()
                try:
                    Error.destroy()
                except Exception as e:
                    print("Error does not exist")
            except ValueError:
                show_error("Date format: YYYY/MM/DD.")
                
        elif choice == "Branch ID":
            branch_id = AddBranchIDEntryBox.get()
            if branch_id.isdigit():
                cur.execute("SELECT BranchId FROM goodwillbranch WHERE BranchId = %s", (branch_id,))
                if cur.fetchone():
                    BranchIDHolder = branch_id
                    DonaBranchFlag = True
                    clear_entry_and_button(choice, SearchBoxEnter)
                else:
                    show_error("Branch ID does not exist")
            else:
                show_error("Branch ID must be a number")

    elif mode == "edit":
        if choice == "Name":
            DonorNameHolder = EditNameEntryBox.get()
            if DonorNameHolder:
                DonaNameFlag = True
                clear_entry_and_button(choice, SearchBoxEnter)
            else:
                show_error("Please enter a name")
                return

        elif choice == "Address":
            AddressHolder = EditAddressEntryBox.get()
            if AddressHolder:
                DonaAddressFlag = True
                clear_entry_and_button(choice, SearchBoxEnter)
            else:
                show_error("Please enter an address")
                return

        elif choice == "Phone Number":
            PhoneHolder = EditPhoneEntryBox.get()
            if PhoneHolder.isdigit() and len(PhoneHolder) >= 5 and len(PhoneHolder) <= 15:
                DonaPhoneFlag = True
                clear_entry_and_button(choice, SearchBoxEnter)
            else:
                if not PhoneHolder.isdigit():
                    show_error("Phone number must be a number")
                else:
                    show_error("Phone number must be between 5 and 15 digits")
                return

        elif choice == "Organization":
            OrgHolder = EditOrgEntryBox.get()
            if OrgHolder == "":
                OrgHolder = "N/A"
            DonaOrgFlag = True
            clear_entry_and_button(choice, SearchBoxEnter)

        elif choice == "Donation ID":
            donation_id = EditDonationIDEntryBox.get()
            if donation_id.isdigit():
                cur.execute("SELECT InventoryId FROM Inventory WHERE InventoryId = %s", (donation_id,))
                if cur.fetchone():
                    DonationIDHolder = donation_id
                    DonaDonationFlag = True
                    clear_entry_and_button(choice, SearchBoxEnter)
                else:
                    show_error("Donation ID does not exist")
                    return
            else:
                show_error("Donation ID must be a number")
                return

        elif choice == "Branch ID":
            branch_id = EditBranchIDEntryBox.get()
            if branch_id.isdigit():
                cur.execute("SELECT BranchId FROM goodwillbranch WHERE BranchId = %s", (branch_id,))
                if cur.fetchone():
                    BranchIDHolder = branch_id
                    DonaBranchFlag = True
                    clear_entry_and_button(choice, SearchBoxEnter)
                else:
                    show_error("Branch ID does not exist")
                    return
            else:
                show_error("Branch ID must be a number")
                return

        # Clear any existing error messages after successful confirmation
        try:
            if ErrorBoolean:
                Error.destroy()
                viewederror = 0
                ErrorBoolean = False
        except Exception:
            pass

def show_error(message):
    global ErrorBoolean, Error, viewederror
    if viewederror == 0:
        ErrorBoolean = True
        # Create error label with word wrapping
        Error = CTkLabel(OutputEditContent, text=message, text_color="red", height=13,width=200,  wraplength=200)  # Enable word wrapping
        # Center the error message horizontally and keep it near the top
        Error.place(relx=0.5, y=3, anchor='n')
        viewederror = 1
def show_success_message(message):
    try:
        success_label = CTkLabel(OutputEditContent, text=message, text_color="green", height=13,width=200, wraplength=200)
        success_label.place(relx=0.5, y=3, anchor='n')
        OutputEditContent.after(3000, lambda: safe_destroy(success_label))
    except Exception as e:
        print(f"Error showing success message: {e}")

def show_error_message(message):
    global ErrorBoolean, Error, viewederror
    try:
        if viewederror == 0:
            ErrorBoolean = True
            Error = CTkLabel(OutputEditContent, text=message, text_color="red", height=13,width=200, wraplength=200)
            Error.place(relx=0.5, y=3, anchor='n')
            viewederror = 1
    except Exception as e:
        print(f"Error showing error message: {e}")

def safe_destroy(widget):
    """Safely destroy a widget if it exists and is valid"""
    try:
        if widget and widget.winfo_exists():
            widget.destroy()
    except Exception as e:
        print(f"Error destroying widget: {e}")

def clear_entry_and_button(choice, button):
    if choice == "Address":
        if mode == "add":
            AddAddressEntryBox.place_forget()
        else:
            EditAddressEntryBox.place_forget()
    elif choice == "Phone Number":
        if mode == "add":
            AddPhoneEntryBox.place_forget()
        else:
            EditPhoneEntryBox.place_forget()
    elif choice == "Organization":
        if mode == "add":
            AddOrgEntryBox.place_forget()
        else: 
            EditOrgEntryBox.place_forget()
    elif choice == "Donation":
        if mode == "add":
            AddDonationEntryBox.place_forget()
            AddDonationTypeBox.place_forget()
            if 'DonationNameEntryBox' in globals() and DonationNameEntryBox is not None:
                DonationNameEntryBox.place_forget()  # Add this line
        else:
            EditDonationEntryBox.place_forget()
            EditDonationTypeBox.place_forget()
    elif choice == "Name":
                EditNameEntryBox.place_forget()  
    elif choice == "Branch ID":
        if mode == "add":
            AddBranchIDEntryBox.place_forget()
        else:
            EditBranchIDEntryBox.place_forget()
    button.destroy()

# Add these global variables after the existing globals
keyCreatedChecker = False  # For checking if key creation is successful
InvBalIDHolder = 0  # For inventory/balance ID
DonorIDHolder = 0  # For Donor ID

def get_random_integer(min_value, max_value):
    return random.randint(min_value, max_value)

def DonorIDcreator():
    global keyCreatedChecker, InvBalIDHolder, DonorIDHolder
    
    if mode == "add":
        ID = []  # Donor id
        RID = []  # inventory id

        # Generate Donor ID
        idCharLimit = 5
        while idCharLimit >= 0:
            I = get_random_integer(0, 9)
            RandInt = str(I)
            idCharLimit = idCharLimit - 1
            ID.append(RandInt)
        DonorIDHolder = ''.join(ID)
        
        # Generate Inventory ID
        idCharLimit2 = 5
        while idCharLimit2 >= 0:
            N = get_random_integer(0, 9)
            idCharLimit2 = idCharLimit2 - 1
            RandInt = str(N)
            RID.append(RandInt)
        InvBalIDHolder = ''.join(RID)

        # Ensure IDs are within the allowed length
        DonorIDHolder = DonorIDHolder[:7]
        InvBalIDHolder = InvBalIDHolder[:7]

        # Check if IDs already exist
        cur.execute("""SELECT * FROM ALREADYCREATEDKEYS""")
        results = cur.fetchall()
        
        if not results:
            keyCreatedChecker = True
        else:
            for row in results:
                if len(row) < 2:
                    print("Invalid row in ALREADYCREATEDKEYS")
                    continue
                if row[0] == DonorIDHolder or row[1] == InvBalIDHolder:
                    keyCreatedChecker = False
                    break
            else:
                keyCreatedChecker = True
        
        if keyCreatedChecker:
            cur.execute("""INSERT INTO ALREADYCREATEDKEYS (keyId_T, keyId_IorB)
            VALUES (%s, %s)""", (DonorIDHolder, InvBalIDHolder))
            return True
        else:
            return DonorIDcreator()  # Try again with new IDs

def D_handleaddDonor():
    global ErrorBoolean, Error, viewederror
    global DonaAddressFlag, DonaPhoneFlag, DonaOrgFlag, DonaDonationFlag, DonaBranchFlag
    
    Donor_name = DonorNameBox.get().strip()
    
    if not Donor_name:
        show_error("Please enter Donor name")
        return
        
    if diffvalue > 0:
        all_valid = (DonaAddressFlag and DonaPhoneFlag and
                    DonaOrgFlag and DonaDonationFlag and DonaBranchFlag)
        
        if all_valid:
            try:
                # Start transaction
                success, error = execute_safe_query(cur, "BEGIN")
                if not success:
                    show_error_window(error)
                    return
                
                # Generate IDs
                if not DonorIDcreator():
                    execute_safe_query(cur, "ROLLBACK")
                    show_error("Failed to create unique IDs")
                    return

                try:
                    # Handle inventory insertion based on donation type
                    if DonationTypeHolder == 'Funds':
                        try:
                            inventory_value = float(DonationHolder)
                            success, error = execute_safe_query(
                                cur,
                                """INSERT INTO Inventory (InventoryId, InventoryName, InventoryValue, InventoryType, BranchId, GoodsStatus)
                                VALUES (%s, %s, %s, %s, %s, %s)
                                RETURNING InventoryId""",
                                [InvBalIDHolder, 'Funds', inventory_value, DonationTypeHolder, BranchIDHolder, 'donation']
                            )
                        except ValueError:
                            execute_safe_query(cur, "ROLLBACK")
                            show_error("Invalid fund amount")
                            return
                    else:  # Item donation
                        if not DonNameHolder:
                            execute_safe_query(cur, "ROLLBACK")
                            show_error("Donation name is required for items")
                            return
                            
                        # For items, store both name and description/amount
                        success, error = execute_safe_query(
                            cur,
                            """INSERT INTO Inventory (InventoryId, InventoryName, InventoryValue, InventoryType, BranchId, GoodsStatus)
                            VALUES (%s, %s, %s, %s, %s, %s)
                            RETURNING InventoryId""",
                            [InvBalIDHolder, DonNameHolder, 0, DonationTypeHolder, BranchIDHolder, 'donation']
                        )
                    
                    if not success:
                        execute_safe_query(cur, "ROLLBACK")
                        show_error_window(error)
                        return

                    inventory_id = cur.fetchone()[0]

                    # Insert Donor with reference to inventory
                    success, error = execute_safe_query(
                        cur,
                        """INSERT INTO Donor (DonorID, DonorName, DonorAddress, DonorPhoneNumber, DonorOrganization, DonationID)
                        VALUES (%s, %s, %s, %s, %s, %s)""",
                        [DonorIDHolder, Donor_name, AddressHolder, PhoneHolder, OrgHolder, inventory_id]
                    )
                    
                    if not success:
                        execute_safe_query(cur, "ROLLBACK")
                        show_error_window(error)
                        return

                    success, error = execute_safe_query(cur, "COMMIT")
                    if success:
                        D_clear_ui_elements()
                        show_success_message("Donor and donation added successfully")
                    else:
                        execute_safe_query(cur, "ROLLBACK")
                        show_error_window(error)

                except Exception as e:
                    execute_safe_query(cur, "ROLLBACK")
                    show_error(f"Error processing donation: {str(e)}")
            except Exception as e:
                show_error(f"Error adding Donor: {str(e)}")
        else:
            show_error("Please complete all fields")
    else:
        show_error("Please select additional information")

def D_handleeditDonor(): #Handles edit donor
    global ErrorBoolean, Error, viewederror, successful_transaction
    global DonaIDFlag, DonaNameFlag, DonaAddressFlag, DonaPhoneFlag, DonaOrgFlag, DonaDonationFlag, DonaBranchFlag
    
    Donor_id = DonorIDEdit.get().strip()
    
    if not Donor_id:
        show_error_message("Please enter a Donor ID")
        return

    if diffvalue == 0:
        show_error_message("Please select at least one field to update")
        return

    try:
        def transaction():
            nonlocal Donor_id
            # Verify Donor exists
            cur.execute("SELECT EXISTS(SELECT 1 FROM Donor WHERE DonorID = %s)", (Donor_id,))
            if not cur.fetchone()[0]:
                raise ValueError("Donor ID does not exist")

            updates = []
            params = []
            
            # Build update query dynamically
            if DonaNameFlag:
                updates.append("DonorName = %s")
                params.append(DonorNameHolder)
            
            if DonaAddressFlag:
                updates.append("DonorAddress = %s")
                params.append(AddressHolder)
                
            if DonaPhoneFlag:
                updates.append("DonorPhoneNumber = %s")
                params.append(PhoneHolder)
                
            if DonaOrgFlag:
                updates.append("DonorOrganization = %s")
                params.append(OrgHolder)
                
            if DonaDonationFlag:
                # Verify donation exists
                cur.execute("SELECT EXISTS(SELECT 1 FROM Inventory WHERE InventoryId = %s)", (DonationIDHolder,))
                if not cur.fetchone()[0]:
                    raise ValueError("Invalid Donation ID")
                updates.append("DonationID = %s")
                params.append(DonationIDHolder)
                
            # Handle branch ID update separately since it belongs to Inventory table
            if DonaBranchFlag:
                # Verify branch exists
                cur.execute("SELECT EXISTS(SELECT 1 FROM goodwillbranch WHERE BranchId = %s)", (BranchIDHolder,))
                if not cur.fetchone()[0]:
                    raise ValueError("Invalid Branch ID")
                    
                # Get the donation ID for this donor
                cur.execute("SELECT DonationID FROM Donor WHERE DonorID = %s", (Donor_id,))
                donation_result = cur.fetchone()
                if not donation_result or not donation_result[0]:
                    raise ValueError("No donation found for this donor")
                    
                # Update branch ID in Inventory table
                cur.execute("""
                    UPDATE Inventory
                    SET BranchId = %s
                    WHERE InventoryId = %s""",
                    (BranchIDHolder, donation_result[0])
                )
            
            # Handle other donor table updates
            if updates:
                query = f"""
                    UPDATE Donor
                    SET {', '.join(updates)}
                    WHERE DonorID = %s
                """
                params.append(Donor_id)
                cur.execute(query, tuple(params))
                
            # Return True if we either updated branch or donor info
            return bool(updates) or DonaBranchFlag
            
            return True

        success, error = execute_safe_query(cur, "BEGIN")
        if not success:
            show_error_message(error)
            return
            
        if transaction():
            success, error = execute_safe_query(cur, "COMMIT")
            if success:
                successful_transaction = True
                D_clear_ui_elements()
                show_success_message("Donor updated successfully")
            else:
                execute_safe_query(cur, "ROLLBACK")
                show_error_message(error)
        else:
            execute_safe_query(cur, "ROLLBACK")
            show_error_message("No changes made")
            
    except ValueError as ve:
        show_error_message(str(ve))
    except Exception as e:
        show_error_message(f"Error updating Donor: {str(e)}")

def D_handledeleteDonor(DonorIDDelete, deleteinputbutton):
    Donor_id = DonorIDDelete.get().strip()
    
    if not Donor_id:
        show_error("Please enter Donor ID")
        return
    
    try:
        def transaction():
            # First verify Donor exists and get related IDs
            cur.execute("""
                SELECT d.DonorID, d.DonationID
                FROM Donor d
                WHERE d.DonorID = %s
            """, (Donor_id,))
            
            Donor = cur.fetchone()
            if not Donor:
                raise ValueError("Donor ID not found")
                
            donation_id = Donor[1]
            
            # Delete from Donor table first (child table)
            cur.execute("""
                DELETE FROM Donor
                WHERE DonorID = %s
                RETURNING DonationID
            """, (Donor_id,))
            
            # Then delete associated donation from Inventory table (parent table) if exists
            if donation_id:
                cur.execute("""
                    DELETE FROM Inventory
                    WHERE InventoryId = %s
                """, (donation_id,))
            
            # Clean up ALREADYCREATEDKEYS
            cur.execute("""
                DELETE FROM ALREADYCREATEDKEYS
                WHERE keyId_T = %s
                OR (keyId_IorB = %s AND %s IS NOT NULL)
            """, (Donor_id, donation_id, donation_id))
            
            return True

        if execute_safe_query(transaction):
            D_clear_ui_elements()
            show_success_message("Donor and associated records deleted successfully")
        else:
            show_error("Failed to delete Donor")
            
    except ValueError as ve:
        show_error(str(ve))
    except Exception as e:
        show_error(f"Error deleting Donor: {str(e)}")

def D_clear_ui_elements():
    """Safely clear UI elements based on current mode"""
    global viewederror, ErrorBoolean, mode
    
    try:
        # Define widget groups for each mode
        mode_widgets = {
            "add": [
                (DonorNameBox, "place_forget"),
                (Donor_combobox, "place_forget"),
                (Donor_inputbutton, "place_forget")
            ],
            "edit": [
                (DonorIDEdit, "destroy"),
                (Donor_combobox, "destroy"),
                (Donor_inputbutton, "destroy")
            ],
            "delete": [
                (DonorIDDelete, "destroy"),
                (Donor_inputbutton, "destroy")
            ]
        }
        
        # Clear mode-specific widgets
        if mode in mode_widgets:
            for widget, action in mode_widgets[mode]:
                try:
                    if widget and widget.winfo_exists():
                        if action == "place_forget":
                            widget.place_forget()
                        else:
                            widget.destroy()
                except Exception as e:
                    print(f"Error clearing widget in {mode} mode: {e}")
        
        # Clear error message if it exists
        try:
            if ErrorBoolean and 'Error' in globals() and Error and Error.winfo_exists():
                Error.destroy()
                viewederror = 0
                ErrorBoolean = False
        except Exception as e:
            print(f"Error clearing error message: {e}")
            
    except Exception as e:
        print(f"Error in clear_ui_elements: {e}")
# Remove duplicate functions - we already have better versions with error handling

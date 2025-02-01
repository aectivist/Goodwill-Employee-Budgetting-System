from customtkinter import *
import psycopg2
import random
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from errorHandler import execute_safe_query, show_error_window, show_success_message



#Database connection
conn = None
cur = None

def init_db(db_conn, db_cur):
    """Initialize database connection"""
    global conn, cur
    conn = db_conn
    cur = db_cur


#REQUIRED DATATYPES _------------------------------------------------------------------- 
#SQL
InvBalIDHolder = 0 #Create INV/BAL ID HOLDER
GenTransID = 0 #Create General Transaction ID
        
#checks if items has been viewed
vieweditemflag = False
A_vieweditemflag = 0 #for add
E_vieweditemflag = 0#for edit
D_vieweditemflag = 0 #for delete
viewederror = 0 #This is for the error

ErrorBoolean = False #If error statement has already been set

#to check whether or not an item had a successful transaction
sucessful_transaction = False


#for knowing which mode the user is currently on
currentmode = ""

TransAddExist = False #Allows us to know the existence, whether or not add is being accessed, edit or delete similarly.
TransEditExist = False
TransDeleteExist = False

TrueInventoryIDFlag = False #Checks for EDIT PANEL if the GOODS and TYPE are interdependent amongst each other. You can find it most notably on handleedittrans

ConfirmedChoiceForSearch = "" #Confirmed for choice for search is used to see whether or not the user has confirmed their choice for search. If they have, then it will be used to search for the item.

keyCreatedChecker = False#For the key creation to see whether or not it has been created or not. If it is created, the checker stays false. Else if it is true, then it will continue to add the keys.

#FOR SEARCH
ErrorLabelBoolean = False #NOTE: This is for the error label. If the error label is already set, then it will not be set again. This is to prevent multiple error labels from being set.

# Function to show a page
def T_show_page(parent, page_frame):
    """Initialize and show the donator page"""
    global TransactionsPagePost
    
    # Show the page
    page_frame.pack(fill=BOTH, expand=True)
    parent.update_idletasks()
    
    # Initialize content only once
    if TransactionsPagePost == 0:
        transactionpage(page_frame)




TitleFont = CTkFont(family="Oswald", size=15, weight='bold')
EditFont = CTkFont(family="Oswald", size=15, weight='bold')
BTNFont = CTkFont(family="Oswald", size=13)
ErrorFont = CTkFont( size=10)
TransactionsPagePost = 0 #so the page only posts once and not multiple times


def transactionpage(page): #TO BE UPDATED
    global TransactionsPagePost, OutputEditContent, SearchRequestContent
    if TransactionsPagePost==0:
        
        #START MASTER 
        PageMargin = CTkFrame(page)
        PageMargin.pack(expand=True)
        RequestPadding = CTkFrame(PageMargin, width=170, height=330, fg_color="#dbdbdb", corner_radius=0, border_color='#000000', border_width=1)
        OutputPadding = CTkFrame(PageMargin, width=410, height=330, fg_color="#dbdbdb", corner_radius=0, border_color='#000000', border_width=1)
        RequestPadding.grid_propagate(0)
        OutputPadding.grid_propagate(0)
        
        RequestPadding.grid(row=0, column=0)
        OutputPadding.grid(row=0, column=1) 

        #Requested Content
        SearchRequestContent = CTkFrame(RequestPadding, width=170, height=165, fg_color="#FFFFFF", corner_radius=0, border_color='#000000', border_width=1)
        SearchRequestContent.grid_propagate(0)
        
        EditsRequestContent = CTkFrame(RequestPadding, width=170, height=165, fg_color="#FFFFFF", corner_radius=0, border_color='#000000', border_width=1)
        EditsRequestContent.grid_propagate(0)
        
        SearchRequestContent.grid(row=0, column=0)
        EditsRequestContent.grid(row=1, column=0) 
        
        #Fixes all Buttons
        for i in range(1):
            EditsRequestContent.grid_columnconfigure(i, weight=1, uniform="column")
            EditsRequestContent.grid_rowconfigure(0, minsize=51)
        
        for i in range(1):
            SearchRequestContent.grid_columnconfigure(i, weight=1, uniform="column")
            SearchRequestContent.grid_rowconfigure(0, minsize=51)
        
        
        

        #Output Content
        global OutputTableScrollbarContent
        OutputEditContent = CTkFrame(OutputPadding, width=410, height=115, fg_color="#FFFFFF", corner_radius=0, border_color='#000000', border_width=1)
        OutputEditContent.grid(row = 0, column = 0)
        LabelTransactionAdd = CTkLabel(OutputEditContent, text="TRANSACTIONS",font = EditFont)
        LabelTransactionAdd.place(x=5, y=1)
        

        OutputTableContent = CTkFrame(OutputPadding, width=410, height=215, fg_color="#a6a6a6", corner_radius=0, border_color='#000000', border_width=1)
        OutputTableContent.grid(row = 1, column = 0) 
        OutputEditContent.grid_propagate(0)
        OutputTableContent.grid_propagate(0)
        
        
        OutputTableScrollbarContent = CTkFrame(OutputTableContent, width=410, height=215)
        OutputTableScrollbarContent.pack(fill="both", expand=True)
        OutputTableScrollbarContent.grid_propagate(0)
        
        
        canvas = CTkCanvas(OutputTableScrollbarContent, width=410, height=215, highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)
        
        scrollbar = CTkScrollableFrame(canvas, width =387)
        scrollbar.grid(rowspan=100, row = 0, column = 0, sticky='nsew')

        EditLabelRequest = CTkLabel(EditsRequestContent, text="EDITS", font=EditFont)
        EditLabelRequest.grid(row=0, column=0, )
        
        
        #important buttons for requesting
        AddButtonRequest = CTkButton(EditsRequestContent, text="ADD",corner_radius=0, command=lambda: T_outputContentGivenButtons(OutputEditContent, 1),font=BTNFont, text_color='#000000', fg_color='#FFFFFF', border_color='#000000', border_width=1, hover_color='#e6e6e6')
        AddButtonRequest.grid(row=1,column=0,padx = 10, pady = 4, sticky='nsew')
        
        EditButtonRequest = CTkButton(EditsRequestContent, text="EDIT",corner_radius=0, command=lambda: T_outputContentGivenButtons(OutputEditContent, 2), font=BTNFont, fg_color='#FFFFFF', text_color='#000000', border_color='#000000', border_width=1, hover_color='#e6e6e6')
        EditButtonRequest.grid(row=2,column=0,padx = 10, pady = 1, sticky='nsew')
        
        DeleteButtonRequest = CTkButton(EditsRequestContent, text="DELETE",  corner_radius=0,command=lambda: T_outputContentGivenButtons(OutputEditContent, 3), font=BTNFont, fg_color='#FFFFFF', text_color='#000000', border_color='#000000', border_width=1, hover_color='#e6e6e6')
        DeleteButtonRequest.grid(row=3,column=0,padx = 10, pady = 2, sticky='nsew')
        
        #VALYES FOR SEARCHING
    


        #SearchRequestContentItems

        SearchLabel = CTkLabel(SearchRequestContent, text="TRANSACTIONS", font=EditFont)
        SearchLabel.grid(row=0, column=0, padx = 10, pady = 0,)
        
        SearchEntry = CTkEntry(SearchRequestContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="Search")
        SearchEntry.grid(row=1, column=0, padx = 10, pady = 4,)
        
        SearchButton = CTkButton(SearchRequestContent, text="Search", fg_color='#0053A0', corner_radius=0, text_color='#FFFFFF', border_color='#000000', border_width=1, hover_color='#0051ff', command= lambda: TransactionSearch(SearchEntry))
        SearchButton.grid(row=2,column=0, padx = 10, pady = 1,)

        comboVal = StringVar(value="Transaction ID")
        SearchComboChoices = CTkComboBox(SearchRequestContent, values=["Transaction ID","Transaction From", "Transaction To", "Date"], command=TransactionSearch_ComboCallback, variable=comboVal, corner_radius=1)
        SearchComboChoices.set("Transaction ID")
        SearchComboChoices.grid(row = 3, column=0, padx=10,pady=2)
        SearchComboChoices.configure(state="readonly")
        TransactionsPagePost=1
    else:
        print("Page has already been outputted!")


def TransactionSearch_ComboCallback(choice):
    global ConfirmedChoiceForSearch
    
    # Map choices to search types
    search_types = {
        "Transaction ID": "Transaction ID",
        "Transaction From": "Transaction From", 
        "Transaction To": "Transaction To",
        "Date": "Date"
    }
    
    # Update confirmed choice if valid
    if choice in search_types:
        ConfirmedChoiceForSearch = search_types[choice]
        print(f"Search type set to: {ConfirmedChoiceForSearch}")
    else:
        print(f"Invalid search type: {choice}")
        ConfirmedChoiceForSearch = "Transaction ID" # Default

def TransactionSearch(SearchEntry):
    global ConfirmedChoiceForSearch, OutputTableScrollbarContent
    
    # Clear previous results and errors
    for widget in OutputTableScrollbarContent.winfo_children():
        widget.destroy()
    
    try:
        search_value = SearchEntry.get().strip()
        params = {}
        
        # Base query with common transaction information
        base_query = """
        SELECT 
            t.TransactionId,
            t.TransactorFrom,
            t.TransactionTo,
            t.TransactionDate,
            t.transactiontype
            ,CASE 
                WHEN t.transactiontype = 'Item' THEN i.InventoryId
                WHEN t.transactiontype = 'Cash' THEN b.BalanceID
            END as ID_inv_or_bal,
            CASE 
                WHEN t.transactiontype = 'Item' THEN i.InventoryName
                WHEN t.transactiontype = 'Cash' THEN 'Balance'
            END as Name_or_Amount,
            CASE 
                WHEN t.transactiontype = 'Item' THEN CAST(i.InventoryValue AS VARCHAR)
                WHEN t.transactiontype = 'Cash' THEN CAST(b.BalanceAmount AS VARCHAR)
            END as Value_or_Date,
            CASE 
                WHEN t.transactiontype = 'Item' THEN i.InventoryType
                ELSE 'N/A'
            END as Inv_Type,
            CASE 
                WHEN t.transactiontype = 'Item' THEN i.GoodsStatus
                ELSE 'N/A'
            END as Status,
            CASE 
                WHEN t.transactiontype = 'Item' THEN i.BranchId
                WHEN t.transactiontype = 'Cash' THEN b.BranchID
            END as Branch_ID
        FROM transactionTable t
        LEFT JOIN transactionType tt ON t.transactionTypeId = tt.transactionTypeId
        LEFT JOIN Inventory i ON tt.InventoryId = i.InventoryId AND t.transactiontype = 'Item'
        LEFT JOIN Balance b ON tt.BalanceId = b.BalanceId AND t.transactiontype = 'Cash'
        WHERE 1=1
        """
        
        # Add search conditions based on user selection and input validation
        if search_value:  # Only add condition if search entry is not empty
            if ConfirmedChoiceForSearch == "Transaction ID":
                if not search_value.isdigit():
                    raise ValueError("Transaction ID must be a number")
                base_query += " AND t.TransactionId = %(search_value)s"
                params['search_value'] = int(search_value)
                
            elif ConfirmedChoiceForSearch in ["Transaction From", "Transaction To"]:
                field = "t.TransactorFrom" if ConfirmedChoiceForSearch == "Transaction From" else "t.TransactionTo"
                base_query += f" AND {field} ILIKE %(search_value)s"
                params['search_value'] = f"%{search_value}%"
                
            elif ConfirmedChoiceForSearch == "Date":
                try:
                    search_date = datetime.strptime(search_value, "%Y/%m/%d")
                    base_query += " AND t.TransactionDate = %(search_value)s"
                    params['search_value'] = search_date.strftime("%Y-%m-%d")
                except ValueError:
                    raise ValueError("Date must be in YYYY/MM/DD format")

        # Execute query
        success, error = execute_safe_query(cur, base_query, params)
        if not success:
            show_error_window(error)
            return

        rows = cur.fetchall()

        if rows:
            # Create and configure treeview
            tree = ttk.Treeview(OutputTableScrollbarContent, show="headings", height=10)
            
            # Configure columns
            columns = ["TransID", "From", "To", "Date", "Type", 
                      "ID_inv_or_bal", "Name_or_Amount", "Value_or_Date", 
                      "Inv_Type", "Status", "Branch"]
            tree["columns"] = columns
            
            # Configure column widths and headers
            column_widths = {
                "TransID": 70, "From": 100, "To": 100, "Date": 80, "Type": 60,
                "ID_inv_or_bal": 70, "Name_or_Amount": 100, "Value_or_Date": 80,
                "Inv_Type": 80, "Status": 70, "Branch": 70
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


def T_outputContentGivenButtons(OutputEditContent, value): 
    global vieweditemflag, A_vieweditemflag, E_vieweditemflag, D_vieweditemflag, currentmode, mode
    if value == 1:
        mode = "add"
        print(A_vieweditemflag)

    elif value == 2:
        mode = "edit"
        

    elif value == 3:
        mode = "delete"
    
    if currentmode == mode:
        return
    
    T_clearcurrentmode ()

    if currentmode == "":
        vieweditemflag = 0
    print(mode)
    
    if mode == "add":
        T_addmodeui()
    elif mode == "edit":
        T_editmodeui()
    elif mode == "delete":
        T_deletemodeui()

    currentmode = mode
    



def T_clearcurrentmode ():
    global TransAddExist, TransEditExist, TransDeleteExist, diffvalue, viewederror, ErrorBoolean

    # Destroy Add mode widgets if they exist
    if TransAddExist:
        try:
            TransactionNameBoxFrom.place_forget()
            TransactionNameBoxTo.place_forget()
            Transaction_combobox.place_forget()
        except Exception as e:
            print(f"Add is not working. Error: {e}" )
        try:
            if ErrorBoolean==True:
                Error.destroy()
                viewederror=0
                ErrorBoolean = False
        except Exception as e:
            print(f"Deletion Error not working. Error: {e}" )
        #Deletion is necessary.
        try:
            if diffvalue == 0:
                print("y")
            elif diffvalue == 1:
                AddDateEntryBox.place_forget()
            elif diffvalue == 2:
                AddGoodsEntryBox.place_forget()
                try:
                    inventorytypebox.place_forget()
                except Exception as e:
                    print("inventorytypebox does not exist")
            elif diffvalue == 3:
                typebox.place_forget()
                amtinput.place_forget()
                try:
                    statusbox.place_forget()
                except Exception as e:
                    print("Already destroyed.")
            elif diffvalue == 4:
                AddBranchEntryBox.place_forget()
            if diffvalue > 0:
                AddSearchBoxEnter.destroy()
            if ErrorBoolean == True:
                Error.destroy()
        except Exception as e:
            print(f"Not working. Error: {e}")

        TransAddExist = False
    # Destroy Edit mode widgets if they exist
    if TransEditExist:
        try:
            TransactionIDEdit.destroy()
            Transaction_combobox.destroy()
        except Exception as e:
            print(f"Error destroying Transaction_combobox and TransactionIDEdit: {e}")
        try:
            if 'Error' in globals() and Error.winfo_exists():
                Error.place_forget()
                viewederror = 0
                ErrorBoolean = False
        except Exception as e:
            print(f"Deletion Error not working. Error: {e}" )

        try:
            if diffvalue == 0:
                print("has not used combobox yet")
            elif diffvalue == 1:
                EditDateEntryBox.place_forget()
            elif diffvalue == 2:
                EditGoodsEntryBox.place_forget()
                inventorytypebox.place_forget()
            elif diffvalue == 3:
                typebox.place_forget()
                amtinputEdit.place_forget()
                try:
                    statusbox.place_forget()
                except Exception as e:
                    print("Already destroyed.")
            elif diffvalue == 4:
                EditBranchEntryBox.place_forget()
            elif diffvalue == 5:
                PartyToEntryBox.place_forget()
                PartyForEntryBox.place_forget()
            if diffvalue > 0:
                EditSearchBoxEnter.place_forget() 
            if ErrorBoolean == True:
                Error.destroy()
        except Exception as e:
            print("ERROR")
        
        TransEditExist = False

    if TransDeleteExist:
        TransactionIDDelete.destroy()
        TransDeleteExist = False
        try:
            if 'Error' in globals() and Error.winfo_exists():
                Error.place_forget()
                viewederror = 0
                ErrorBoolean = False
        except Exception as e:
            print(f"Deletion Error not working. Error: {e}" )      

    # Destroy the common input button if it exists
    try:
        Transaction_inputbutton.destroy()
    except NameError:
        pass  # Handle case where button isn't created yet

        

def T_addmodeui():
    vieweditemflag = 1
    
    global TransAddExist, TransactionNameBoxFrom, TransactionNameBoxTo, Transaction_inputbutton, Transaction_combobox, sucessful_transaction,GoodsIDHolder
    global DateHolder, GoodsHolder, BranchHolder, TypeHolder, AmountHolder, StatusHolder, InvTypHolder,TransIDHolder
    DateHolder=""
    GoodsIDHolder=0 #just in case inv/bal is not selected, and it selects the 0 id within the database (which exists)
    GoodsHolder=""
    BranchHolder=""
    TypeHolder="Item"
    AmountHolder = "0"
    StatusHolder = "Bought"
    InvTypHolder="None"

    sucessful_transaction = False
    
    #All Flags
    global Trans_DateFlag, Trans_GoodsFlag, Trans_TypeFlag, Trans_BranchFlag
    Trans_DateFlag=False
    Trans_GoodsFlag=False
    Trans_TypeFlag=False
    Trans_BranchFlag=False

   
    global StatusChecker
    StatusChecker=1 #Whether sold or bought ONLY IF the item is selected

    global TypeChecker, typewaschecked
    TypeChecker = True #whether item or cash
    typewaschecked = False #checks whether or not type in combo box was checked or not

    global enteronce, diffvalue, enteronceforcombo

    enteronce = 0
    diffvalue = 0 #to findout which combo is working orn ot
    enteronceforcombo = 0 

    


    # Create Add-specific widgets
    TransactionNameBoxFrom = CTkEntry(OutputEditContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="Transaction From", width=190, height=25)
    TransactionNameBoxFrom.place(x=5, y=25)

    TransactionNameBoxTo = CTkEntry(OutputEditContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="Transaction To", width=190, height=25)
    TransactionNameBoxTo.place(x=205, y=25)

    comboVal = StringVar(value="Select")
    Transaction_combobox = CTkComboBox(OutputEditContent, values=["Date", "Object Name", "Type", "Branch ID"], command=T_callback, variable=comboVal, height = 25, corner_radius=1, width=110)
    Transaction_combobox.set("Select")
    Transaction_combobox.place(x=5, y = 53)
    Transaction_combobox.configure(state="readonly")
    
    Transaction_inputbutton = CTkButton(OutputEditContent, text="Add", corner_radius=0, font=BTNFont, text_color='#000000', fg_color='#FFFFFF', border_color='#000000', border_width=1,hover_color='#e6e6e6', width=100, height=27,command= lambda: T_handleaddtrans())
    Transaction_inputbutton.place(x=295, y=82)
    

    TransAddExist = True  # Mark Add mode as active

def T_editmodeui():
    
    vieweditemflag = 1
    global TransEditExist, TransactionIDEdit, Transaction_combobox, Transaction_inputbutton, sucessful_transaction
    global DateHolder, GoodsIDHolder, BranchHolder, TypeHolder, AmountHolder, PartyToHolder, PartyForHolder, StatusHolder, InvTypHolder,TransIDHolder, GoodsHolder
    TransIDHolder=""
    DateHolder=""
    GoodsIDHolder=0 #just in case inv/bal is not selected, and it selects the 0 id within the database (which exists)
    GoodsHolder="" #js adding so that it isnt left out (coz it goes balistic in transactionsql if it isnt used correctly)
    BranchHolder=0
    TypeHolder="Item"
    AmountHolder = 0
    PartyToHolder=""
    PartyForHolder=""
    StatusHolder ="Bought"
    InvTypHolder="None"
    
    
    sucessful_transaction = False

    #All Flags
    global Trans_DateFlag, Trans_GoodsFlag, Trans_TypeFlag, Trans_BranchFlag, Trans_IDFlag, Trans_PartyFlag, TransactionNameToFlag, TransactionNameForFlag
    Trans_DateFlag=False
    Trans_GoodsFlag=False
    Trans_TypeFlag=False
    Trans_BranchFlag=False
    Trans_IDFlag = False
    Trans_PartyFlag = False
    TransactionNameToFlag = False
    TransactionNameForFlag = False
    
    global StatusChecker
    StatusChecker=1 #Whether sold or bought ONLY IF the item is selected
    
    global TypeChecker, typewaschecked
    TypeChecker = True #whether item or cash
    typewaschecked = False #checks whether or not type in combo box was checked or not

    global enteronce, diffvalue, enteronceforcombo
    enteronce = 0
    diffvalue = 0 #to findout which combo is working orn ot
    enteronceforcombo = 0 

    # Create Edit specific widgets
    TransactionIDEdit = CTkEntry(OutputEditContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="Transaction ID", width=390, height=25)
    TransactionIDEdit.place(x=5, y=25)

    comboVal = StringVar(value="Select")
    Transaction_combobox = CTkComboBox(OutputEditContent, values=["Date", "Inventory/Balance ID", "Type", "Branch ID", "Parties"], command=T_callback, variable=comboVal, height = 25, corner_radius=1, width=110)
    Transaction_combobox.set("Select")
    Transaction_combobox.place(x=5, y = 53)
    Transaction_combobox.configure(state="readonly")

    Transaction_inputbutton = CTkButton(OutputEditContent, text="Edit", corner_radius=0, font=BTNFont, text_color='#000000', fg_color='#FFFFFF', border_color='#000000', border_width=1, hover_color='#e6e6e6', width=100, height=27, command=lambda: T_handleedittrans())
    Transaction_inputbutton.place(x=295, y=82)
    


    TransEditExist = True  # Mark Edit mode as active

def T_deletemodeui():
    global TransactionIDDelete, Transaction_inputbutton, TransDeleteExist
    TransactionIDDelete = CTkEntry(OutputEditContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="enter Transaction ID to delete", width=390, height = 25)
    TransactionIDDelete.place(x=5,y=25)

    Transaction_inputbutton = CTkButton(OutputEditContent, text = "Delete", command = lambda: T_handledeletetrans(TransactionIDDelete, Transaction_inputbutton), corner_radius=0,font=BTNFont, text_color='#000000', fg_color='#FFFFFF', border_color='#000000', border_width=1, hover_color='#e6e6e6', width=100, height = 27)
    Transaction_inputbutton.place (x=295, y = 82)
    TransDeleteExist = True


            
            

def T_handledeletetrans(TransactionIDDelete, deleteinputbutton):
    global deletebuttonrequestchecker, ErrorBoolean, Error, viewederror
    ItemToDelete = TransactionIDDelete.get()
    if ItemToDelete != "":
        # Verify if the transaction ID exists in the database
        success, error = execute_safe_query(cur, "SELECT EXISTS(SELECT 1 FROM transactionTable WHERE transactionId = %s)", (ItemToDelete,))
        if not success:
            show_error_window(error)
            return
        exists = cur.fetchone()[0]
        
        if exists:
            print("Item is deleted. Transaction =" + str(ItemToDelete))
            T_clearcurrentmode()
            DeleteSQL(ItemToDelete)
        else:
            if viewederror == 0:
                ErrorBoolean = True
                Error = CTkLabel(OutputEditContent, text="Transaction ID does not exist.", text_color="red", height=13)
                Error.place(x=200, y=3)
                viewederror = 1
    else:
        if viewederror == 0:
            ErrorBoolean = True
            Error = CTkLabel(OutputEditContent, text="Please enter correct field properly.", text_color="red", height=13)
            Error.place(x=200, y=3)
            viewederror = 1

def DeleteSQL(ItemToDelete):
    try:
        # First get the transactionTypeId
        success, error = execute_safe_query(cur, """SELECT transactionTypeId FROM transactionTable WHERE transactionId = %s""", (ItemToDelete,))
        if not success:
            show_error_window(error)
            return
        result = cur.fetchone()
        if not result:
            print("No transaction found")
            return
        transactionTypeId = result[0]
        
        # Then get balance and inventory IDs
        success, error = execute_safe_query(cur, """SELECT balanceid, inventoryid FROM transactionType WHERE transactionTypeId = %s""", (transactionTypeId,))
        if not success:
            show_error_window(error)
            return
        result = cur.fetchone()
        if not result:
            print("No transaction type found")
            return
            
        balanceid = result[0] if result[0] else None
        inventoryid = result[1] if result[1] else None
        
        # Perform deletions in correct order
        success, error = execute_safe_query(cur, "DELETE FROM transactionTable WHERE transactionId = %s", (ItemToDelete,))
        if not success:
            show_error_window(error)
            return
        success, error = execute_safe_query(cur, "DELETE FROM transactionType WHERE transactionTypeId = %s", (transactionTypeId,))
        if not success:
            show_error_window(error)
            return
        
        if balanceid:
            success, error = execute_safe_query(cur, "DELETE FROM balance WHERE balanceid = %s", (balanceid,))
            if not success:
                show_error_window(error)
                return
        if inventoryid:
            success, error = execute_safe_query(cur, "DELETE FROM inventory WHERE inventoryid = %s", (inventoryid,))
            if not success:
                show_error_window(error)
                return
            
        conn.commit()
        print("Item has been deleted.")
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()

def T_callback(choice): #COMBO BOX FUNCTIONALITIES
    global enteronce, enteronceforcombo, inventorytypebox, diffvalue, typebox
    global DateHolder, GoodsHolder, TransIDHolder, BranchHolder, TypeHolder, AmountHolder, InvTypHolder, typewaschecked
    global ErrorBoolean, Error, viewederror
    
    enteronce = enteronce + 1
    enteronceforcombo = enteronceforcombo + 1

    # Handle error cleanup
    try:
        if ErrorBoolean:
            Error.destroy()
            viewederror = 0
            ErrorBoolean = False
    except Exception as e:
        print(f"Deletion Error not working. Error: {e}")
        
    if mode == "add": #ADD============================COMBO
        global AddDateEntryBox, AddGoodsEntryBox, AddBranchEntryBox, amtinput, statusbox, AddSearchBoxEnter
    
        
        print (enteronce)
        if enteronce > 1:
            AddSearchBoxEnter.destroy()
            enteronce = 1
            print (enteronce)
            
            
        if enteronce == 1:
            AddSearchBoxEnter = CTkButton(OutputEditContent, text = "Confirm", corner_radius=0,font=BTNFont, text_color='#000000', fg_color='#FFFFFF', border_color='#000000', border_width=1, hover_color='#e6e6e6', width=100, height = 27, command=lambda: T_confirmyourchoice(choice, AddSearchBoxEnter))
            AddSearchBoxEnter.place(x=190,y=82)

        if enteronceforcombo>1: #Deletes anything else if its greater than 1, in which case it shouldnt be greater than one. (Placed for redundancy and security)
            if diffvalue == 1:
                AddDateEntryBox.place_forget()
            elif diffvalue == 2:
                AddGoodsEntryBox.place_forget()
                try:
                    inventorytypebox.place_forget()
                except Exception as e:
                    print("inventorytypebox does not exist")
            elif diffvalue == 3:
                typebox.place_forget()
                amtinput.place_forget()
                try:
                    statusbox.place_forget()
                except Exception as e:
                    print("Already destroyed.")
            elif diffvalue == 4:
                AddBranchEntryBox.place_forget()

            enteronceforcombo = 1
            print (enteronceforcombo)

        if enteronceforcombo == 1: 
            if choice == "Date": #For DATE
                diffvalue = 1
                AddDateEntryBox = CTkEntry(OutputEditContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="Date of Transaction", width=275, height = 25)
                AddDateEntryBox.place(x=120, y = 53)
                AddDateEntryBox.configure(state="normal")
                AddDateEntryBox.insert(0,DateHolder)
                
                
            elif choice == "Object Name": #for Inventory
                diffvalue = 2
                AddGoodsEntryBox = CTkEntry(OutputEditContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="Inventory/Balance ID", width=275, height = 25)
                AddGoodsEntryBox.place(x=120, y = 53)
                AddGoodsEntryBox.configure(state="normal")
                AddGoodsEntryBox.insert(0,GoodsHolder)

                if TypeHolder == "Item":
                    inventorytypeVal = StringVar(value="None")
                    inventorytypebox = CTkComboBox(OutputEditContent, values=["None", "Liability","Asset"], command=boolforinvtypcheck, variable=inventorytypeVal, height = 27, corner_radius=1, width=180) #whether none asset or liability 
                    inventorytypebox.place(x=5, y = 82)
                    inventorytypebox.set(InvTypHolder)
                    inventorytypebox.configure(state="readonly")
                else:
                    try:
                        inventorytypebox.place_forget()
                    except Exception as e:
                        print("inventorytypebox does not exist")

                
            elif choice == "Type": #for TYPE
                diffvalue = 3
                 #this means that type was checked in terms of viewed is true, hence it will:
                if TypeHolder == "Item":
                    comboVal = StringVar(value="Item") #set combo select to item as initial
                elif TypeHolder == "Cash":
                    comboVal = StringVar(value="Cash") #set combo select to item as initial
                   
                typebox = CTkComboBox(OutputEditContent, values=["Item", "Cash"], command=boolfortypecheck, variable=comboVal, height = 25, corner_radius=1, width=275) #whether item or cash 
                typebox.place(x=120, y = 53)
                typebox.configure(state="readonly")
                
                amtinput = CTkEntry(OutputEditContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="Enter Amount", width=80, height = 27)
                amtinput.place(x=5, y = 82)
                amtinput.configure(state="normal")
                amtinput.insert(0, AmountHolder)

                if TypeChecker == True:
                    comboStatusVal = StringVar(value="Bought")
                    statusbox = CTkComboBox(OutputEditContent, values=["Bought", "Sold","Donation"], command=boolforstatuscheck, variable=comboStatusVal, height = 27, corner_radius=1, width=80) #whether item or cash 
                    statusbox.place(x=95, y = 82)

                    statusbox.set(StatusHolder)
                    statusbox.configure(state="readonly")

                
            elif choice == "Branch ID": #certain BRANCH
                diffvalue = 4
                AddBranchEntryBox = CTkEntry(OutputEditContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="Branch Id", width=275, height = 25)
                AddBranchEntryBox.place(x=120, y = 53)
                AddBranchEntryBox.insert(0,BranchHolder)

            
        
        
        print ("diffvalue: " + str(diffvalue))


        #FOR ADDING ITEMS WITHIN THE ENTRY BOXES, OR LEAVING THEM WITH PLACEHOLDER TEXTS.
        
        if BranchHolder == "" or DateHolder == "" or GoodsHolder == "" or AmountHolder == "": #if one of these is empty, then:
            if DateHolder ==""and diffvalue == 1: #if its date holder is empty and its on the same
                AddDateEntryBox.delete(0, END)
                AddDateEntryBox.configure(placeholder_text="Date of Transaction")
            elif GoodsHolder ==""and diffvalue == 2:
                if TypeHolder == "Item":
                    AddGoodsEntryBox.delete(0, END)
                    AddGoodsEntryBox.configure(placeholder_text="Object Name")
                elif TypeHolder=="Cash":
                    AddGoodsEntryBox.delete(0, END)
                    AddGoodsEntryBox.configure(placeholder_text="Balance")
                    AddGoodsEntryBox.configure(state="readonly")

            elif TypeHolder == ""and diffvalue == 3:
                amtinput.delete(0, END)
                amtinput.configure(placeholder_text="Enter Amount")
                typebox.configure(state="readonly")
            elif BranchHolder == "" and diffvalue == 4:
                AddBranchEntryBox.delete(0, END)
                AddBranchEntryBox.configure(placeholder_text="Branch Id")
        else:
            if BranchHolder != "" and diffvalue==4:
                AddBranchEntryBox.delete(0, END)
                AddBranchEntryBox.insert(0,BranchHolder)
            elif DateHolder !="" and diffvalue ==1:
                AddDateEntryBox.delete(0, END)
                AddDateEntryBox.insert(0,DateHolder)
            elif GoodsHolder ==""and diffvalue == 2:#This is so that if Goods holder is not empty, and diff value chooses the good choice, then it'll input every data held.
                if TypeHolder == "Item":#checks if this is an item, then it'll replace the item with what's already held. Im actually gonna morb.
                    AddGoodsEntryBox.delete(0, END)
                    AddGoodsEntryBox.insert(0, GoodsHolder)
                elif TypeHolder=="Cash": #otherwise, it would only place balance if it is cash (since CASH cannot have any other name other than it being run against the balance)
                    AddGoodsEntryBox.configure(state="normal")
                    AddGoodsEntryBox.delete(0, END)
                    AddGoodsEntryBox.configure(placeholder_text="Balance")
                    GoodsHolder = "Balance"
                    AddGoodsEntryBox.configure(state="readonly")
                
            elif TypeHolder != "" and diffvalue==3: #This is so that if type holder is not empty, and diff value chooses the type choice, then it'll input every data held. 
                typebox.delete(0, END)
                typebox.insert(0, TypeHolder)
                amtinput.delete(0, END)
                amtinput.insert(0, AmountHolder)
                statusbox.delete(0, END)
                statusbox.insert(0,StatusHolder)
    else: #EDIT============================COMBO
        global PartyForEntryBox, PartyToEntryBox, EditDateEntryBox, EditGoodsEntryBox, EditBranchEntryBox, amtinputEdit, PartyForHolder, PartyToHolder,  EditSearchBoxEnter
        
        
        print (enteronce)
        if enteronce > 1:
            try:
                if EditSearchBoxEnter.winfo_exists():
                    EditSearchBoxEnter.destroy()
            except Exception as e:
                print(f"Error destroying EditSearchBoxEnter: {e}")
            enteronce = 1
            
        
        if enteronce == 1:
            EditSearchBoxEnter = CTkButton(OutputEditContent, text = "Confirm", corner_radius=0,font=BTNFont, text_color='#000000', fg_color='#FFFFFF', border_color='#000000', border_width=1, hover_color='#e6e6e6', width=100, height = 27, command=lambda: T_confirmyourchoice(choice, EditSearchBoxEnter))
            EditSearchBoxEnter.place(x=190,y=82)

        if enteronceforcombo>1:
            try:
                if diffvalue == 1 and 'EditDateEntryBox' in globals() and EditDateEntryBox.winfo_exists():
                    EditDateEntryBox.place_forget()
                elif diffvalue == 2:
                    if 'EditGoodsEntryBox' in globals() and EditGoodsEntryBox.winfo_exists():
                        EditGoodsEntryBox.place_forget()
                    if 'inventorytypebox' in globals() and inventorytypebox.winfo_exists():
                        inventorytypebox.place_forget()
                elif diffvalue == 3:
                    if 'typebox' in globals() and typebox.winfo_exists():
                        typebox.place_forget()
                    if 'amtinputEdit' in globals() and amtinputEdit.winfo_exists():
                        amtinputEdit.place_forget()
                    if 'statusbox' in globals() and statusbox.winfo_exists():
                        statusbox.place_forget()
                elif diffvalue == 4 and 'EditBranchEntryBox' in globals() and EditBranchEntryBox.winfo_exists():
                    EditBranchEntryBox.place_forget()
                elif diffvalue == 5:
                    if 'PartyToEntryBox' in globals() and PartyToEntryBox.winfo_exists():
                        PartyToEntryBox.place_forget()
                    if 'PartyForEntryBox' in globals() and PartyForEntryBox.winfo_exists():
                        PartyForEntryBox.place_forget()
            except Exception as e:
                print(f"Error cleaning up widgets: {e}")

            enteronceforcombo = 1

        if enteronceforcombo == 1:
            if choice == "Date": #For DATE
                diffvalue = 1
                EditDateEntryBox = CTkEntry(OutputEditContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="Date of Transaction", width=275, height = 25)
                EditDateEntryBox.place(x=120, y = 53)
                EditDateEntryBox.configure(state="normal")
                EditDateEntryBox.insert(0,DateHolder)
                
                
            elif choice == "Inventory/Balance ID": #for GOODS
                diffvalue = 2
                EditGoodsEntryBox = CTkEntry(OutputEditContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="Inventory/Balance ID", width=275, height = 25)
                EditGoodsEntryBox.place(x=120, y = 53)
                EditGoodsEntryBox.configure(state="normal")
                EditGoodsEntryBox.insert(0,GoodsIDHolder)

                if TypeHolder == "Item":
                    inventorytypeVal = StringVar(value="None")
                    inventorytypebox = CTkComboBox(OutputEditContent, values=["None", "Liability","Asset"], command=boolforinvtypcheck, variable=inventorytypeVal, height = 27, corner_radius=1, width=180) #whether none asset or liability 
                    inventorytypebox.place(x=5, y = 82)
                    inventorytypebox.set(InvTypHolder)
                    inventorytypebox.configure(state="readonly")
                else:
                    try:
                        inventorytypebox.place_forget()
                    except Exception as e:
                        print("inventorytypebox does not exist")
                
            elif choice == "Type": #for TYPE
                diffvalue = 3
                comboVal = StringVar(value="Item")
                typebox = CTkComboBox(OutputEditContent, values=["Item", "Cash"], command=boolfortypecheck, variable=comboVal, height = 25, corner_radius=1, width=275)
                typebox.place(x=120, y = 53)
                
                if TypeChecker == True:
                    comboStatusVal = StringVar(value="Bought")
                    statusbox = CTkComboBox(OutputEditContent, values=["Bought", "Sold","Donation"], command=boolforstatuscheck, variable=comboStatusVal, height = 27, corner_radius=1, width=80) #whether item or cash 
                    statusbox.place(x=95, y = 82)

                    statusbox.set(StatusHolder)
                    statusbox.configure(state="readonly")

                amtinputEdit = CTkEntry(OutputEditContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="Enter Amount", width=80, height = 27)
                amtinputEdit.place(x=5, y = 82)
                amtinputEdit.insert(0, AmountHolder)


                typebox.set(TypeHolder)
                typebox.configure(state="readonly")
                
                statusbox.configure(state="readonly")
                
            elif choice == "Branch ID": #certain BRANCH
                diffvalue = 4
                EditBranchEntryBox = CTkEntry(OutputEditContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="Branch Id", width=275, height = 25)
                EditBranchEntryBox.place(x=120, y = 53)
                EditBranchEntryBox.insert(0,BranchHolder)
            elif choice == "Parties": #EDITS WHO SENT AND WHOS SENDING TRANSACTION
                diffvalue = 5
                PartyForEntryBox = CTkEntry(OutputEditContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="Transaction For", width=132, height = 25)
                PartyForEntryBox.place(x=120, y = 53)
                PartyForEntryBox.insert(0,PartyForHolder)
                PartyToEntryBox = CTkEntry(OutputEditContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="Transaction To", width=132, height = 25)
                PartyToEntryBox.place(x=260, y = 53)
                PartyToEntryBox.insert(0,PartyToHolder)

        if typewaschecked == True and choice != "Type":
            amtinputEdit.destroy()
            typewaschecked = False
        
        
            
        if BranchHolder == 0 or DateHolder == "" or GoodsIDHolder == 0 or AmountHolder == 0 or PartyForHolder == "" or PartyToHolder == "": #if blank is empty, then delete items in it
            if DateHolder ==""and diffvalue == 1:
                EditDateEntryBox.delete(0, END)
                EditDateEntryBox.configure(placeholder_text="Date of Transaction")
            elif GoodsIDHolder ==0 and diffvalue == 2:
                EditGoodsEntryBox.delete(0, END)
                EditGoodsEntryBox.configure(placeholder_text="Inventory/Balance ID")
            elif TypeHolder == ""and diffvalue == 3:
                amtinputEdit.delete(0, END)
                amtinputEdit.configure(placeholder_text="Amount")
            elif BranchHolder == 0 and diffvalue == 4:
                EditBranchEntryBox.delete(0, END)
                EditBranchEntryBox.configure(placeholder_text="Branch Id")
            elif diffvalue == 5:
                if PartyForHolder == "" and PartyToHolder == "":
                    PartyForEntryBox.delete(0, END)
                    PartyForEntryBox.configure(placeholder_text="Transaction From")
                if PartyToHolder == "":
                    PartyToEntryBox.delete(0, END)
                    PartyToEntryBox.configure(placeholder_text="Transaction To")
        else: #basically checks if blank is not empty, input item already in it
            
            if DateHolder !="" and diffvalue ==1:
                EditDateEntryBox.insert(0,DateHolder)
            elif GoodsIDHolder !=""and diffvalue == 2:
                EditGoodsEntryBox.insert(0, GoodsIDHolder)
                inventorytypebox.set(InvTypHolder)
            elif TypeHolder != "" and diffvalue==3:
                typebox.set(TypeHolder)
                amtinputEdit.insert(0, AmountHolder)
                statusbox.set(StatusHolder)
            elif BranchHolder != "" and diffvalue==4: 
                EditBranchEntryBox.insert(0,BranchHolder)
            elif PartyToHolder != "" and diffvalue == 5:
                PartyToEntryBox.insert(0,PartyToHolder)
            elif PartyForHolder != "" and diffvalue == 5:
                PartyForEntryBox.insert(0,PartyForHolder)
            
        
        print ("diffvalue: " + str(diffvalue))


def T_confirmyourchoice(choice, AddSearchBoxEnter):
    global DateHolder, GoodsHolder, BranchHolder, TypeChecker, TypeHolder, typebox, AmountHolder
    global TransIDHolder, PartyForHolder, InvTypHolder, PartyToHolder, Trans_PartyFlag, StatusHolder, StatusChecker, GoodsIDHolder
    global Trans_DateFlag, Trans_GoodsFlag, Trans_TypeFlag, Trans_BranchFlag, Trans_IDFlag, TransactionNameToFlag, TransactionNameForFlag
    global ErrorBoolean, Error, viewederror, amountedit
    
    if mode == "add": #ADD=========================================================#####################################################
        if choice == "Date":  # DATE ----------
            DateHolder = AddDateEntryBox.get()
            
            try:
                # Try to convert the input to a datetime object using the desired format
                datetime.strptime(DateHolder, "%Y/%m/%d")  # format: YYYY/MM/DD
                Trans_DateFlag = True 
                AddDateEntryBox.place_forget()
                AddSearchBoxEnter.destroy()
                try:
                    Error.destroy()
                except Exception as e:
                    print("Error does not exist")
            except ValueError:
                if viewederror == 0:
                    Trans_DateFlag = False
                    ErrorBoolean = True
                    Error = CTkLabel(OutputEditContent, text="Date format: YYYY/MM/DD.", text_color="red", height=13)
                    Error.place(x=200, y=3)
                    viewederror = 1
                    

        elif choice == "Object Name":  # GOODS ---------
            if TypeChecker:
                GoodsHolder = AddGoodsEntryBox.get()
                InvTypHolder = inventorytypebox.get()
            else:
                GoodsHolder = "Balance"
            AddGoodsEntryBox.place_forget()
            try:
                inventorytypebox.place_forget()
            except Exception:
                pass
            Trans_GoodsFlag = True
            AddSearchBoxEnter.destroy()

        elif choice == "Type":  # TYPE ----------
            AmountHolder=amtinput.get()
            typebox.place_forget()
            amtinput.place_forget()
            TypeHolder = "Item" if TypeChecker else "Cash"
            Trans_TypeFlag = True
            try:
                statusbox.place_forget()
            except Exception:
                pass
            AddSearchBoxEnter.destroy()

        elif choice == "Branch ID":
            if AddBranchEntryBox.get() == '':
                show_error_window("Please enter a branch ID")
                show_error_window("Invalid Branch ID")
            else:
                BranchHolder = AddBranchEntryBox.get()
            
            if BranchHolder:
                success, error = execute_safe_query(cur, """
                    SELECT EXISTS(
                        SELECT 1 FROM goodwillBranch 
                        WHERE branchId = %(branchId)s
                    )
                """, {'branchId': BranchHolder})
                if not success:
                    show_error_window(error)
                    return
                branch_exists = cur.fetchone()[0]
                
                if branch_exists:
                    try:
                        AddBranchEntryBox.place_forget()
                        Trans_BranchFlag = True
                        AddSearchBoxEnter.destroy()
                        # Commit the transaction if successful
                        success, error = execute_safe_query(cur, "COMMIT")
                        if not success:
                            show_error_window(error)
                            return
                        try:
                            Error.destroy()
                        except Exception as e:
                            print("Error does not exist")
                    except Exception as e:
                        # Rollback on error
                        success, error = execute_safe_query(cur, "ROLLBACK")
                        if not success:
                            show_error_window(error)
                            return
                        show_error_window(f"Transaction failed: {str(e)}")
                else:
                    # Rollback if branch doesn't exist
                    success, error = execute_safe_query(cur, "ROLLBACK")
                    if not success:
                        show_error_window(error)
                        return
                    show_error_window("Invalid Branch ID")
 
    elif mode == "edit": #EDIT=========================================================#####################################################
        if choice == "Date":
            DateHolder = EditDateEntryBox.get()
            try:
                # Try to convert the input to a datetime object using the desired format
                datetime.strptime(DateHolder, "%Y/%m/%d")  # format: YYYY/MM/DD
                Trans_DateFlag = True 
                EditSearchBoxEnter.destroy()
                try:
                    Error.destroy()
                except Exception as e:
                    print("Error does not exist")
            except ValueError:
                if viewederror == 0:
                    Trans_DateFlag = False
                    ErrorBoolean = True
                    Error = CTkLabel(OutputEditContent, text="Date format: YYYY/MM/DD.", text_color="red", height=13)
                    Error.place(x=200, y=3)
                    viewederror = 1
            
        elif choice == "Inventory/Balance ID" :
            if EditGoodsEntryBox.get() == '':
                show_error_window("Please enter an inventory/balance ID")
                show_error_window("Invalid Inventory/Balance ID")
                print("Invalid!!!")
            else:
                try: #adding this for the above, in case the error message exists
                    Error.destroy()
                except Exception as e:
                    print("Error does not exist")
                GoodsIDHolder = EditGoodsEntryBox.get()
                if TypeChecker == True:
                    success, error = execute_safe_query(cur, """
                            SELECT EXISTS(
                                SELECT 1 FROM transactionType 
                                WHERE inventoryid = %(inventoryid)s
                            )
                        """, {'inventoryid': GoodsIDHolder})
                    if not success:
                        show_error_window(error)
                        return
                    goods_exists = cur.fetchone()[0]
                        
                    if goods_exists:
                        try:
                            GoodsIDHolder = EditGoodsEntryBox.get()
                            InvTypHolder = inventorytypebox.get()
                            Trans_GoodsFlag = True
                            EditGoodsEntryBox.configure(state="readonly")        
                            EditSearchBoxEnter.destroy()
                            try:
                                Error.destroy()
                            except Exception as e:
                                print("Error does not exist")
                        except Exception as e:
                            # Rollback on error
                            success, error = execute_safe_query(cur, "ROLLBACK")
                            if not success:
                                show_error_window(error)
                                return
                            show_error_window(f"Transaction failed: {str(e)}")
                    else:
                        GoodsIDHolder = 0
                        # Rollback if branch doesn't exist
                        success, error = execute_safe_query(cur, "ROLLBACK")
                        if not success:
                            show_error_window(error)
                            return
                        show_error_window("Invalid Inventory/Balance ID")
                elif TypeChecker == False:
                    GoodsIDHolder = EditGoodsEntryBox.get()
                    success, error = execute_safe_query(cur, """
                            SELECT EXISTS(
                                SELECT 1 FROM transactionType 
                                WHERE balanceid = %(balanceid)s
                            )
                        """, {'balanceid': GoodsIDHolder})
                    if not success:
                        show_error_window(error)
                        return
                    goods_exists = cur.fetchone()[0]
                        
                    if goods_exists:
                        try:
                            GoodsIDHolder = EditGoodsEntryBox.get()
                            Trans_GoodsFlag = True
                            EditGoodsEntryBox.configure(state="readonly")        
                            EditSearchBoxEnter.destroy()
                            try:
                                Error.destroy()
                            except Exception as e:
                                print("Error does not exist")
                        except Exception as e:
                            # Rollback on error
                            success, error = execute_safe_query(cur, "ROLLBACK")
                            if not success:
                                show_error_window(error)
                                return
                            show_error_window(f"Transaction failed: {str(e)}")
                    else:
                        GoodsIDHolder = 0
                        # Rollback if branch doesn't exist
                        success, error = execute_safe_query(cur, "ROLLBACK")
                        if not success:
                            show_error_window(error)
                            return
                        show_error_window("Invalid Inventory/Balance ID")
                
        elif choice == "Branch ID":
            if EditBranchEntryBox.get() == '':
                show_error_window("Please enter a branch ID")
                show_error_window("Invalid Branch ID")
            else:
                BranchHolder = EditBranchEntryBox.get()
            
            if BranchHolder:
                success, error = execute_safe_query(cur, """
                    SELECT EXISTS(
                        SELECT 1 FROM goodwillBranch 
                        WHERE branchId = %(branchId)s
                    )
                """, {'branchId': BranchHolder})
                if not success:
                    show_error_window(error)
                    return
                branch_exists = cur.fetchone()[0]
                
                if branch_exists:
                    try:
                        BranchHolder = EditBranchEntryBox.get()
                        Trans_BranchFlag = True
                        EditBranchEntryBox.configure(state="readonly")
                        # Commit the transaction if successful
                        success, error = execute_safe_query(cur, "COMMIT")
                        if not success:
                            show_error_window(error)
                            return
                        try:
                            Error.destroy()
                        except Exception as e:
                            print("Error does not exist")
                    except Exception as e:
                        # Rollback on error
                        success, error = execute_safe_query(cur, "ROLLBACK")
                        if not success:
                            show_error_window(error)
                            return
                        show_error_window(f"Transaction failed: {str(e)}")
                else:
                    # Rollback if branch doesn't exist
                    success, error = execute_safe_query(cur, "ROLLBACK")
                    if not success:
                        show_error_window(error)
                        return
                    show_error_window("Invalid Branch ID")

        elif choice == "Type":
            TypeHolder = "Item" if TypeChecker else "Cash"
            StatusHolder = {1: "Bought", 2: "Sold", 3: "Donation"}.get(StatusChecker, "Bought")
            Trans_TypeFlag = True
            AmountHolder = amtinputEdit.get()
            amtinputEdit.configure(state="readonly")
            EditSearchBoxEnter.destroy()
            
            
        elif choice == "Parties":
            if PartyForEntryBox.get() and PartyToEntryBox.get():
                PartyForHolder = PartyForEntryBox.get()
                PartyToHolder = PartyToEntryBox.get()
                PartyForEntryBox.configure(state="readonly")
                PartyToEntryBox.configure(state="readonly")
                Trans_PartyFlag = True
                EditSearchBoxEnter.destroy()

def T_handleaddtrans():
    global ErrorBoolean, Error, viewederror, amountedit
    global Trans_DateFlag, Trans_GoodsFlag, Trans_TypeFlag, Trans_BranchFlag
    
    global TransAddExist, TransactionNameBoxFrom, TransactionNameBoxTo, Transaction_inputbutton, Transaction_combobox, sucessful_transaction 
    global TransactorFromHolder, TransactorToHolder
    outputFlag=False
    
    TransactorToHolder =  TransactionNameBoxTo.get()
    TransactorFromHolder = TransactionNameBoxFrom.get()
    
    

    if TransactorToHolder and TransactorFromHolder != "": #if the transactor to and transactor from is NOT empty, then it'll post as true.
        TransactionNameForFlag = True
        TransactionNameToFlag = True
        
        if diffvalue > 0:
            # Validate all required fields
            all_valid = (Trans_DateFlag and Trans_GoodsFlag and 
                        Trans_TypeFlag and Trans_BranchFlag and 
                        TransactionNameToFlag and TransactionNameForFlag and 
                        AmountHolder.isnumeric())
            
            if all_valid:
                # Verify branch exists
                success, error = execute_safe_query(cur, """
                    SELECT EXISTS(
                        SELECT 1 FROM goodwillBranch 
                        WHERE branchId = %(branchId)s
                    )
                """, {'branchId': BranchHolder})
                if not success:
                    show_error_window(error)
                    return
                branch_exists = cur.fetchone()[0]
                
                if branch_exists:
                    try:
                        # Begin transaction
                        success, error = execute_safe_query(cur, "BEGIN")
                        if not success:
                            show_error_window(error)
                            return
                        
                        # Clear UI elements
                        T_clear_ui_elements()
                        transactionIDcreator()
                        
                        success, error = execute_safe_query(cur, "COMMIT")
                        if not success:
                            show_error_window(error)
                            return
                        show_success_message("Transaction completed successfully", OutputEditContent)
                    except Exception as e:
                        success, error = execute_safe_query(cur, "ROLLBACK")
                        if not success:
                            show_error_window(error)
                            return
                        show_error_window(f"Transaction failed: {str(e)}")
                else:
                    show_error_window("Invalid Branch ID")
            else:
                show_error_window("Please input ALL entries correctly")
        else:
            show_error_window("Please select transaction type")
    else:
        show_error_window("Please enter transaction parties")














def T_handleedittrans():
    global ErrorBoolean, Error, viewederror, amountedit
    global Trans_DateFlag, Trans_GoodsFlag, Trans_TypeFlag, Trans_BranchFlag, Trans_IDFlag, Trans_PartyFlag, amountedit, diffvalue
    global amountedit, ErrorBoolean, Error, viewederror, sucessful_transaction, Transaction_inputbutton, TrueInventoryIDFlag,TransactionNameToFlag, TransactionNameForFlag
    global DateHolder, GoodsIDHolder, TransIDHolder, BranchHolder, TypeHolder, AmountHolder, InvTypHolder, StatusHolder, PartyForHolder, PartyToHolder, GoodsHolder
    if TransactionIDEdit.get() != "":  # Ensure Transaction ID is provided MAINLY------------------------
        try: #Try basically checks if the transaction ID exists in the database
            success, error = execute_safe_query(cur, """SELECT EXISTS(SELECT 1 FROM transactionTable WHERE transactionId = %s)""", (TransactionIDEdit.get(),))
            if not success:
                show_error_window(error)
                return
            result = cur.fetchone()
            if result and result[0]:  # Check both result exists and its value
                Trans_IDFlag = True
                TransIDHolder = TransactionIDEdit.get()
            else:
                Trans_IDFlag = False
                show_error_window("Transaction ID does not exist.")
        except Exception as e: #If there is an error, then it'll print the below
            show_error_window(f"Database error: {str(e)}")

        if diffvalue == 3: #to check if amount holder is a number
            if AmountHolder.isnumeric() and Trans_TypeFlag:
                amountedit = True #NOTE: MAKE SURE TO RUN AN ERROR FUNCTION IF THE AMOUNT IS NOT A NUMBER 111111111111111111e4i21u4u12y4812g
            else:
                show_error_window("Please input a valid amount")

    elif viewederror == 0: #If there is no error, but the id section is empty, then it'll print the below
        print("Please Input the id entry.")
        ErrorBoolean = True
        Error = CTkLabel(OutputEditContent, text="Please Input the transaction entry.", text_color="red", height=13)
        Error.place(x=200, y=3)
        viewederror = 1
        print(viewederror) #-------------------------------
            
    if Trans_DateFlag or Trans_GoodsFlag or Trans_TypeFlag or Trans_BranchFlag or TransactionNameToFlag or TransactionNameForFlag:
        if Trans_GoodsFlag and Trans_TypeFlag: #INVENTORY CHANGER
            if TypeChecker == True: #If the type checker is true, or if it is an item, then it'll check the inventory id
                success, error = execute_safe_query(cur, """SELECT EXISTS(SELECT 1 FROM transactionType WHERE inventoryid = %s)""", (GoodsIDHolder,))
                if not success:
                    show_error_window(error)
                    return
                result = cur.fetchone()
                if result and result[0]:
                    TrueInventoryIDFlag = True
                else:
                    TrueInventoryIDFlag = False 
                    if viewederror == 0:
                        print("Please Input the correct entries.")
                        ErrorBoolean = True
                        Error = CTkLabel(OutputEditContent, text="Please fill the correct Inv/Bal ID.", text_color="red", height=13)
                        Error.place(x=120, y=3)
                        viewederror = 1
                        print(viewederror)
            elif TypeChecker == False: #If the type checker is false, or if it is cash, then it'll check the balance id
                success, error = execute_safe_query(cur, """SELECT EXISTS(SELECT 1 FROM transactionType WHERE balanceid = %s)""", (GoodsIDHolder,))
                if not success:
                    show_error_window(error)
                    return
                result = cur.fetchone()
                if result and result[0]:
                    TrueInventoryIDFlag = True
                else:
                    TrueInventoryIDFlag = False
                    if viewederror == 0:
                        print("Please Input the correct entries.")
                        ErrorBoolean = True
                        Error = CTkLabel(OutputEditContent, text="Please fill the correct Inv/Bal ID.", text_color="red", height=13)
                        Error.place(x=120, y=3)
                        viewederror = 1
                        print(viewederror)
        elif Trans_BranchFlag: #If the inventory flag is false, then it'll print the below
            if viewederror == 0:
                    print("Please Input the correct entries.")
                    ErrorBoolean = True
                    Error = CTkLabel(OutputEditContent, text="Successfully editted", text_color="green", height=13)
                    Error.place(x=120, y=3)
                    viewederror = 1
                    print(viewederror)
        else:
            TrueInventoryIDFlag = False
            if viewederror == 0:
                    print("Please Input the correct entries.")
                    ErrorBoolean = True
                    Error = CTkLabel(OutputEditContent, text="Please fill the correct entries.", text_color="red", height=13)
                    Error.place(x=120, y=3)
                    viewederror = 1
                    print(viewederror)

        if PartyForHolder and PartyToHolder: #make error checker
            Trans_PartyFlag = True

    print(f"Date= {Trans_DateFlag}, Inventory= {TrueInventoryIDFlag}, Type= {Trans_TypeFlag}, Branch= {Trans_BranchFlag}, Party= {Trans_PartyFlag}")

    if diffvalue > 0:
        if Trans_IDFlag and (Trans_DateFlag or TrueInventoryIDFlag or Trans_BranchFlag or Trans_PartyFlag):  # Ensure at least one other flag is set
            print("Successfully Submitted.")
            print(f"TransactionID: {TransIDHolder}")
            if Trans_DateFlag:
                print(f"Date: {DateHolder}")
            if TrueInventoryIDFlag:
                print(f"Goods: {GoodsIDHolder}")
                print(f"Inventory Type: {InvTypHolder}")
            if Trans_TypeFlag:
                print(f"Type: {TypeHolder}")
                print(f"Amount of type: {AmountHolder}")
                print(f"Good status: {StatusHolder}")
            if Trans_BranchFlag:
                print(f"Branch ID: {BranchHolder}")
            if Trans_PartyFlag:
                print(f"Party For: {PartyForHolder}")
                print(f"Party To: {PartyToHolder}")
            
            transactionIDcreator()

            if Transaction_inputbutton.winfo_exists():
                Transaction_inputbutton.destroy()
            try:
                TransactionIDEdit.place_forget()
                Transaction_combobox.destroy()
            except Exception as e:
                print(f"Error destroying Transaction_combobox and TransactionIDEdit: {e}")

            try:
                try:
                    for widget in [Transaction_inputbutton,EditSearchBoxEnter]:
                        if widget.winfo_exists():
                            widget.place_forget()
                    if diffvalue == 1:
                        EditDateEntryBox.place_forget()
                    elif diffvalue == 2:
                        EditGoodsEntryBox.place_forget()
                    elif diffvalue==3:
                        typebox.place_forget()
                        amtinputEdit.place_forget()
                    elif diffvalue==4:
                        EditBranchEntryBox.place_forget()
                    elif diffvalue==5:
                        PartyToEntryBox.place_forget()
                        PartyForEntryBox.place_forget()
                    try:
                        inventorytypebox.place_forget()
                    except Exception as e:
                        print("inventorytypebox does not exist")
                    statusbox.place_forget()
                except Exception as e:
                    print(f"Error destroying widgets: {e}")
            except Exception as e:
                print(f"ERROR:{e}")

        else:  # Print an error
            if viewederror == 0:
                print("Please Input the correct entries.")
                ErrorBoolean = True
                Error = CTkLabel(OutputEditContent, text="Please Input the correct entries.", text_color="red", height=13)
                Error.place(x=200, y=3)
                viewederror = 1
                print(viewederror)

    else:  # Print an error
        if viewederror == 0:
            print("Please Input an entry.")
            ErrorBoolean = True
            Error = CTkLabel(OutputEditContent, text="Please Input an entry.", text_color="red", height=13)
            Error.place(x=200, y=3)
            viewederror = 1
            print(viewederror)


        
def T_clear_ui_elements():
    global viewederror, ErrorBoolean
    if mode == "add":
        # Clear main transaction fields
        for widget in [TransactionNameBoxTo, TransactionNameBoxFrom, 
                    Transaction_combobox, Transaction_inputbutton]:
            widget.place_forget()
        
        # Clear entry fields based on type
        for widget in [AddBranchEntryBox, AddDateEntryBox, 
                    AddGoodsEntryBox, typebox, amtinput]:
            try:
                widget.place_forget()
            except Exception:
                pass
                

    
    # Clear any error messages
    if 'Error' in globals() and Error.winfo_exists():
        Error.place_forget()
        viewederror = 0
        ErrorBoolean = False


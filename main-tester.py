from customtkinter import *
import psycopg2
import threading
#https://github.com/Akascape/CTkTable

import math
from math import *
import re
import random
import tkinter as tk
from tkinter import ttk
from datetime import datetime
        



def play_sound():
    global soundpath
    global playingbool
    if playingbool == False:
        print("yea")
    else:
        print("nah")

conn=psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="12345", port=5432)

loginaccess = False
LOGIN = None
EDITFLAG = False #FOR EDITTING


cur = conn.cursor()
window = CTk()
window.title("BUDGET")
window.geometry("600x400") #fml
window.resizable(0,0) #disable resize
set_appearance_mode("light")


#++++++++++++++++++++++++++++++ {PAGES} ++++++++++++++++++++++++++++++++++++++

# Create frames for each page
TABFRAME = CTkFrame(window, height=51, width=600, fg_color="#1E1E1E", corner_radius=0, bg_color='#231F20')
TABFRAME.pack(anchor=CENTER, fill=X)

#These are the individual pages, or rather, the frames
LoadingPage = CTkFrame(window, corner_radius=0) #implement later
HomePage = CTkFrame(window, corner_radius=0)
TransactionsPage = CTkFrame(window, corner_radius=0)
ClientPage = CTkFrame(window, corner_radius=0)
InventoryPage = CTkFrame(window, corner_radius=0)
BudgetPage = CTkFrame(window, corner_radius=0)
CalculatorPage = CTkFrame(window, corner_radius=0)
LoginPage = CTkFrame(window, corner_radius=0, bg_color='#0053A0')
LoadingPage = CTkFrame(window, corner_radius=0) #implement later

# Create a list to hold all the pages
pages = [HomePage, TransactionsPage, ClientPage, InventoryPage, BudgetPage, CalculatorPage]

# Function to show a page
def show_page(page, loginaccess):
    event = threading.Event()
    for p in pages:
        p.pack_forget()
        event.wait(0.1)
    page.pack(fill=BOTH, expand=True)
    
    print(page)
    
    window.update_idletasks()  # Update the UI

    if loginaccess == False and page == LoginPage and page != HomePage:
        loginpage(LoginPage,loginaccess)
    elif page == HomePage:
        LoginPage.pack_forget()
        homepage(HomePage)
    elif page == CalculatorPage:
        LoginPage.pack_forget()
        calculatorpage(CalculatorPage)
   
        

         
#++++++++++++++++++++++++++++++ {PAGE FUNCTIONS} ++++++++++++++++++++++++++++++++++++++
#DO NOT EDIT SPACE, WILL USE SPACE FOR THE OTHER PAGES


#def clientpage(page):
#def assetpage(page):


# ////////////////////////////{{CALCULATOR PAGE}}
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
        AddButtonRequest = CTkButton(EditsRequestContent, text="ADD",corner_radius=0, command=lambda: outputContentGivenButtons(OutputEditContent, 1),font=BTNFont, text_color='#000000', fg_color='#FFFFFF', border_color='#000000', border_width=1, hover_color='#e6e6e6')
        AddButtonRequest.grid(row=1,column=0,padx = 10, pady = 4, sticky='nsew')
        
        EditButtonRequest = CTkButton(EditsRequestContent, text="EDIT",corner_radius=0, command=lambda: outputContentGivenButtons(OutputEditContent, 2), font=BTNFont, fg_color='#FFFFFF', text_color='#000000', border_color='#000000', border_width=1, hover_color='#e6e6e6')
        EditButtonRequest.grid(row=2,column=0,padx = 10, pady = 1, sticky='nsew')
        
        DeleteButtonRequest = CTkButton(EditsRequestContent, text="DELETE",  corner_radius=0,command=lambda: outputContentGivenButtons(OutputEditContent, 3), font=BTNFont, fg_color='#FFFFFF', text_color='#000000', border_color='#000000', border_width=1, hover_color='#e6e6e6')
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
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
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
        cur.execute(base_query, params)
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


def outputContentGivenButtons(OutputEditContent, value): 
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
    
    clearcurrentmode ()

    if currentmode == "":
        vieweditemflag = 0
    print(mode)
    
    if mode == "add":
        addmodeui()
    elif mode == "edit":
        editmodeui()
    elif mode == "delete":
        deletemodeui()

    currentmode = mode
    



def clearcurrentmode ():
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

        

def addmodeui():
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
    Transaction_combobox = CTkComboBox(OutputEditContent, values=["Date", "Object Category", "Type", "Branch ID"], command=callback, variable=comboVal, height = 25, corner_radius=1, width=110)
    Transaction_combobox.set("Select")
    Transaction_combobox.place(x=5, y = 53)
    Transaction_combobox.configure(state="readonly")
    
    Transaction_inputbutton = CTkButton(OutputEditContent, text="Add", corner_radius=0, font=BTNFont, text_color='#000000', fg_color='#FFFFFF', border_color='#000000', border_width=1,hover_color='#e6e6e6', width=100, height=27,command= lambda: handleaddtrans())
    Transaction_inputbutton.place(x=295, y=82)
    

    TransAddExist = True  # Mark Add mode as active

def editmodeui():
    
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
    Transaction_combobox = CTkComboBox(OutputEditContent, values=["Date", "Inventory/Balance ID", "Type", "Branch ID", "Parties"], command=callback, variable=comboVal, height = 25, corner_radius=1, width=110)
    Transaction_combobox.set("Select")
    Transaction_combobox.place(x=5, y = 53)
    Transaction_combobox.configure(state="readonly")

    Transaction_inputbutton = CTkButton(OutputEditContent, text="Edit", corner_radius=0, font=BTNFont, text_color='#000000', fg_color='#FFFFFF', border_color='#000000', border_width=1, hover_color='#e6e6e6', width=100, height=27, command=lambda: handleedittrans())
    Transaction_inputbutton.place(x=295, y=82)
    


    TransEditExist = True  # Mark Edit mode as active

def deletemodeui():
    global TransactionIDDelete, Transaction_inputbutton, TransDeleteExist
    TransactionIDDelete = CTkEntry(OutputEditContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="enter Transaction ID to delete", width=390, height = 25)
    TransactionIDDelete.place(x=5,y=25)

    Transaction_inputbutton = CTkButton(OutputEditContent, text = "Delete", command = lambda: handledeletetrans(TransactionIDDelete, Transaction_inputbutton), corner_radius=0,font=BTNFont, text_color='#000000', fg_color='#FFFFFF', border_color='#000000', border_width=1, hover_color='#e6e6e6', width=100, height = 27)
    Transaction_inputbutton.place (x=295, y = 82)
    TransDeleteExist = True


            
            

def handledeletetrans(TransactionIDDelete, deleteinputbutton):
    global deletebuttonrequestchecker, ErrorBoolean, Error, viewederror
    ItemToDelete = TransactionIDDelete.get()
    if ItemToDelete != "":
        # Verify if the transaction ID exists in the database
        cur.execute("SELECT EXISTS(SELECT 1 FROM transactionTable WHERE transactionId = %s)", (ItemToDelete,))
        exists = cur.fetchone()[0]
        
        if exists:
            print("Item is deleted. Transaction =" + str(ItemToDelete))
            clearcurrentmode()
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
        cur.execute("""SELECT transactionTypeId FROM transactionTable WHERE transactionId = %s""", (ItemToDelete,))
        result = cur.fetchone()
        if not result:
            print("No transaction found")
            return
        transactionTypeId = result[0]
        
        # Then get balance and inventory IDs
        cur.execute("""SELECT balanceid, inventoryid FROM transactionType WHERE transactionTypeId = %s""", (transactionTypeId,))
        result = cur.fetchone()
        if not result:
            print("No transaction type found")
            return
            
        balanceid = result[0] if result[0] else None
        inventoryid = result[1] if result[1] else None
        
        # Perform deletions in correct order
        cur.execute("DELETE FROM transactionTable WHERE transactionId = %s", (ItemToDelete,))
        cur.execute("DELETE FROM transactionType WHERE transactionTypeId = %s", (transactionTypeId,))
        
        if balanceid:
            cur.execute("DELETE FROM balance WHERE balanceid = %s", (balanceid,))
        if inventoryid:
            cur.execute("DELETE FROM inventory WHERE inventoryid = %s", (inventoryid,))
            
        conn.commit()
        print("Item has been deleted.")
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()

def callback(choice): #COMBO BOX FUNCTIONALITIES
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
            AddSearchBoxEnter = CTkButton(OutputEditContent, text = "Confirm", corner_radius=0,font=BTNFont, text_color='#000000', fg_color='#FFFFFF', border_color='#000000', border_width=1, hover_color='#e6e6e6', width=100, height = 27, command=lambda: confirmyourchoice(choice, AddSearchBoxEnter))
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
                
                
            elif choice == "Object Category": #for Inventory
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
                    AddGoodsEntryBox.configure(placeholder_text="Object Category")
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
            EditSearchBoxEnter = CTkButton(OutputEditContent, text = "Confirm", corner_radius=0,font=BTNFont, text_color='#000000', fg_color='#FFFFFF', border_color='#000000', border_width=1, hover_color='#e6e6e6', width=100, height = 27, command=lambda: confirmyourchoice(choice, EditSearchBoxEnter))
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


def confirmyourchoice(choice, AddSearchBoxEnter):
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
                    

        elif choice == "Object Category":  # GOODS ---------
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
                show_error_message("Please enter a branch ID")
                show_error_message("Invalid Branch ID")
            else:
                BranchHolder = AddBranchEntryBox.get()
            
            if BranchHolder:
                cur.execute("""
                    SELECT EXISTS(
                        SELECT 1 FROM goodwillBranch 
                        WHERE branchId = %(branchId)s
                    )
                """, {'branchId': BranchHolder})
                branch_exists = cur.fetchone()[0]
                
                if branch_exists:
                    try:
                        AddBranchEntryBox.place_forget()
                        Trans_BranchFlag = True
                        AddSearchBoxEnter.destroy()
                        # Commit the transaction if successful
                        cur.execute("COMMIT")
                        try:
                            Error.destroy()
                        except Exception as e:
                            print("Error does not exist")
                    except Exception as e:
                        # Rollback on error
                        cur.execute("ROLLBACK")
                        show_error_message(f"Transaction failed: {str(e)}")
                else:
                    # Rollback if branch doesn't exist
                    cur.execute("ROLLBACK")
                    show_error_message("Invalid Branch ID")
 
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
                show_error_message("Please enter an inventory/balance ID")
                show_error_message("Invalid Inventory/Balance ID")
                print("Invalid!!!")
            else:
                try: #adding this for the above, in case the error message exists
                    Error.destroy()
                except Exception as e:
                    print("Error does not exist")
                GoodsIDHolder = EditGoodsEntryBox.get()
                if TypeChecker == True:
                    cur.execute("""
                            SELECT EXISTS(
                                SELECT 1 FROM transactionType 
                                WHERE inventoryid = %(inventoryid)s
                            )
                        """, {'inventoryid': GoodsIDHolder})
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
                            cur.execute("ROLLBACK")
                            show_error_message(f"Transaction failed: {str(e)}")
                    else:
                        GoodsIDHolder = 0
                        # Rollback if branch doesn't exist
                        cur.execute("ROLLBACK")
                        show_error_message("Invalid Inventory/Balance ID")
                elif TypeChecker == False:
                    GoodsIDHolder = EditGoodsEntryBox.get()
                    cur.execute("""
                            SELECT EXISTS(
                                SELECT 1 FROM transactionType 
                                WHERE balanceid = %(balanceid)s
                            )
                        """, {'balanceid': GoodsIDHolder})
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
                            cur.execute("ROLLBACK")
                            show_error_message(f"Transaction failed: {str(e)}")
                    else:
                        GoodsIDHolder = 0
                        # Rollback if branch doesn't exist
                        cur.execute("ROLLBACK")
                        show_error_message("Invalid Inventory/Balance ID")
                
        elif choice == "Branch ID":
            if EditBranchEntryBox.get() == '':
                show_error_message("Please enter a branch ID")
                show_error_message("Invalid Branch ID")
            else:
                BranchHolder = EditBranchEntryBox.get()
            
            if BranchHolder:
                cur.execute("""
                    SELECT EXISTS(
                        SELECT 1 FROM goodwillBranch 
                        WHERE branchId = %(branchId)s
                    )
                """, {'branchId': BranchHolder})
                branch_exists = cur.fetchone()[0]
                
                if branch_exists:
                    try:
                        BranchHolder = EditBranchEntryBox.get()
                        Trans_BranchFlag = True
                        EditBranchEntryBox.configure(state="readonly")
                        # Commit the transaction if successful
                        cur.execute("COMMIT")
                        try:
                            Error.destroy()
                        except Exception as e:
                            print("Error does not exist")
                    except Exception as e:
                        # Rollback on error
                        cur.execute("ROLLBACK")
                        show_error_message(f"Transaction failed: {str(e)}")
                else:
                    # Rollback if branch doesn't exist
                    cur.execute("ROLLBACK")
                    show_error_message("Invalid Branch ID")

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

def handleaddtrans():
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
                cur.execute("""
                    SELECT EXISTS(
                        SELECT 1 FROM goodwillBranch 
                        WHERE branchId = %(branchId)s
                    )
                """, {'branchId': BranchHolder})
                branch_exists = cur.fetchone()[0]
                
                if branch_exists:
                    try:
                        # Begin transaction
                        cur.execute("BEGIN")
                        
                        # Clear UI elements
                        clear_ui_elements()
                        transactionIDcreator()
                        
                        cur.execute("COMMIT")
                        show_success_message()
                    except Exception as e:
                        cur.execute("ROLLBACK")
                        show_error_message(f"Transaction failed: {str(e)}")
                else:
                    show_error_message("Invalid Branch ID")
            else:
                show_error_message("Please input ALL entries correctly")
        else:
            show_error_message("Please select transaction type")
    else:
        show_error_message("Please enter transaction parties")












def handleedittrans():
    global ErrorBoolean, Error, viewederror, amountedit
    global Trans_DateFlag, Trans_GoodsFlag, Trans_TypeFlag, Trans_BranchFlag, Trans_IDFlag, Trans_PartyFlag, amountedit, diffvalue
    global amountedit, ErrorBoolean, Error, viewederror, sucessful_transaction, Transaction_inputbutton, TrueInventoryIDFlag,TransactionNameToFlag, TransactionNameForFlag
    global DateHolder, GoodsIDHolder, TransIDHolder, BranchHolder, TypeHolder, AmountHolder, InvTypHolder, StatusHolder, PartyForHolder, PartyToHolder, GoodsHolder
    if TransactionIDEdit.get() != "":  # Ensure Transaction ID is provided MAINLY------------------------
        try: #Try basically checks if the transaction ID exists in the database
            cur.execute("""SELECT EXISTS(SELECT 1 FROM transactionTable WHERE transactionId = %s)""", (TransactionIDEdit.get(),))
            result = cur.fetchone()
            if result and result[0]:  # Check both result exists and its value
                Trans_IDFlag = True
                TransIDHolder = TransactionIDEdit.get()
            else:
                Trans_IDFlag = False
                show_error_message("Transaction ID does not exist.")
        except Exception as e: #If there is an error, then it'll print the below
            show_error_message(f"Database error: {str(e)}")

        if diffvalue == 3: #to check if amount holder is a number
            if AmountHolder.isnumeric() and Trans_TypeFlag:
                amountedit = True #NOTE: MAKE SURE TO RUN AN ERROR FUNCTION IF THE AMOUNT IS NOT A NUMBER 111111111111111111e4i21u4u12y4812g
            else:
                show_error_message("Please input a valid amount")

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
                cur.execute("""SELECT EXISTS(SELECT 1 FROM transactionType WHERE inventoryid = %s)""", (GoodsIDHolder,))
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
                cur.execute("""SELECT EXISTS(SELECT 1 FROM transactionType WHERE balanceid = %s)""", (GoodsIDHolder,))
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


def clear_ui_elements():
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
                
        # Clear optional widgets
        
    
    # Clear any error messages
    if 'Error' in globals() and Error.winfo_exists():
        Error.place_forget()
        viewederror = 0
        ErrorBoolean = False

def show_success_message():
    success_label = CTkLabel(
        OutputEditContent, 
        text="Transaction completed successfully",
        text_color="green", 
        height=13
    )
    success_label.place(x=200, y=3)
    OutputEditContent.after(3000, success_label.destroy)

def show_error_message(message):
    global ErrorBoolean, Error, viewederror
    if viewederror == 0:
        ErrorBoolean = True
        Error = CTkLabel(
            OutputEditContent, 
            text=message,
            text_color="red", 
            height=13
        )
        Error.place(x=200, y=3)
        viewederror = 1

#FOR CHECKING WHETHER DESIRED TRANSACTION ITEM IS CASH OR AN ITEM~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def boolfortypecheck(choice):
    global TypeChecker, Trans_TypeFlag, statusbox, GoodsHolder
    if choice == "Item":
        TypeChecker=True
        print("Item")
        
    elif choice == "Cash":
        TypeChecker=False
        print("Cash")
        GoodsHolder = "" #This is so that Goods holder becomes empty. Once empty, the code above will replace it with "Balance."

    
    if TypeChecker == False:
        statusbox.destroy()
    else:
        comboStatusVal = StringVar(value="Bought")
        statusbox = CTkComboBox(OutputEditContent, values=["Bought", "Sold","Donation"], command=boolforstatuscheck, variable=comboStatusVal, height = 27, corner_radius=1, width=80) #whether item or cash 
        statusbox.place(x=95, y = 82)
        statusbox.place(x=95, y = 82)
        

def boolforstatuscheck(choice):
    global StatusChecker
    
    print (str(choice) + "Status")
    if choice == "Bought":
        StatusChecker = 1
    elif choice == "Sold":
        StatusChecker = 2
    elif choice == "Donation":
        StatusChecker = 3
    print (str(StatusChecker) + "Status")

def boolforinvtypcheck(choice): #used for switching and giving value to invtype
    global InvTypHolder
    print (str(choice) + "Type")
    if choice == "None":
        InvTypHolder=""
    elif choice == "Asset":
        InvTypHolder = str(choice)
    elif choice == "Liability":
        InvTypHolder = str(choice)
    print (str(InvTypHolder) + "Type")



#-------------------SQL MODE------------------------------------------------------------------------------

def get_random_integer(min_value, max_value):
    return random.randint(min_value, max_value)

def transactionIDcreator():
    global PartyForHolder, PartyToHolder, GoodsHolder, AmountHolder, InvTypHolder, BranchHolder, StatusHolder
    global keyCreatedChecker
    global GenTransID, InvBalIDHolder, GoodsIDHolder
    
    if mode == "add": #To ensure that ID generation happens for ONLY add functions
        
        
        ID = [] #trans id
        RID = [] #goods generator (inv or bal)

        idCharLimit = 5 #Transaction ID generator
        while idCharLimit >=0: 
            I= get_random_integer(0, 9)
            RandInt = str(I)
            idCharLimit =idCharLimit-1
            ID.append(RandInt)
        GenTransID = ''.join(ID)
        print(int(GenTransID))

    
        idCharLimit2=5
        while idCharLimit2 >=0: #Goods ID generator
            N= get_random_integer(0, 9)
            idCharLimit2 =idCharLimit2-1
            RandInt = str(N)
            RID.append(RandInt)
        InvBalIDHolder = ''.join(RID)
        print(int(InvBalIDHolder))

        print("This worked")
        cur.execute("""SELECT * FROM ALREADYCREATEDKEYS""")
        results = cur.fetchall()
        
        print (results)
        print("This too")
        if not results:  # Check if results is empty
            keyCreatedChecker = True
        else:
            for row in results: #FOR ROWS IN RESULTS
                if len(row) < 3:  # Check if row has enough elements
                    print("Invalid row in ALREADYCREATEDKEYS")
                    keyCreatedChecker = True
                    continue
                if row[1] == GenTransID or row[2] == InvBalIDHolder:  # Check if the generated IDs already exist
                    keyCreatedChecker = False
                    break
        
        if keyCreatedChecker: #If the key is created, then it'll insert the key into the database
            print("This ran!")
            cur.execute("""INSERT INTO ALREADYCREATEDKEYS (keyId_T, keyId_IorB)
            VALUES (%s, %s)""", (GenTransID, InvBalIDHolder))
            print(GenTransID, InvBalIDHolder)
            transactionsql(mode, GenTransID, InvBalIDHolder, GoodsIDHolder, GoodsHolder, AmountHolder, InvTypHolder, BranchHolder, StatusHolder)
            return 

        else:
            return transactionIDcreator()  # Try again with new IDs
    else:
        transactionsql(mode, GenTransID, InvBalIDHolder, GoodsIDHolder, GoodsHolder, AmountHolder, InvTypHolder, BranchHolder, StatusHolder)
        return

def transactionsql(mode, GenTransID, InvBalIDHolder, GoodsIDHolder, GoodsHolder, AmountHolder, InvTypHolder, BranchHolder, StatusHolder):
    global PartyForHolder, PartyToHolder
    global TransactorFromHolder, TransactorToHolder
    TransTypeIDHolder = InvBalIDHolder
    print(TransTypeIDHolder)
    
    if GoodsIDHolder == "":
        GoodsIDHolder = 0
        print("Inv ID: " + str(GoodsIDHolder))
    try:
        if mode == "add":
            if TypeHolder == "Item": 
                cur.execute("""
                INSERT INTO Inventory (InventoryId, InventoryName, InventoryValue, InventoryType, BranchId, GoodsStatus) 
                VALUES (%(InvID)s, %(InvName)s, %(Value)s, %(InvTyp)s, %(BranchId)s, %(Status)s)
                """, {'InvID': InvBalIDHolder, 'InvName': GoodsHolder, 'Value': AmountHolder, 
                  'InvTyp': InvTypHolder, 'BranchId': BranchHolder, 'Status': StatusHolder}) #INVENTORY-
                
                cur.execute("""
                    INSERT INTO transactionType (transactionTypeId, balanceID, InventoryId)
                    VALUES (%(transTypeId)s, 0, %(InvID)s)""", {"transTypeId":TransTypeIDHolder, "InvID":InvBalIDHolder}) #TRANSACTION TYPE--
                

            elif TypeHolder == "Cash":     #NOTE THIS ERROR: 12312321321332133
                cur.execute("""
                    INSERT INTO balance (balanceid, balanceamount, dateofchange, branchid) 
                    VALUES (%(GoodsIDHolder)s, %(Amt)s, %(dateofchange)s, %(BranchID)s)
                """, {'GoodsIDHolder': InvBalIDHolder, 'Amt': AmountHolder, 
                     'dateofchange': DateHolder, 'BranchID': BranchHolder})
                
                cur.execute("""
                    INSERT INTO transactionType (transactionTypeId, balanceID, InventoryId)
                    VALUES (%(transTypeId)s, %(BalID)s, 0)
                """, {"transTypeId": TransTypeIDHolder, "BalID": InvBalIDHolder})

            cur.execute("""
                INSERT INTO transactionTable (transactionId, transactorFrom, transactionTo, transactionDate, transactionType, transactionTypeID) 
                VALUES (%(TransID)s, %(From)s, %(To)s, %(transactionDate)s, %(Typ)s, %(TransTypID)s)
            """, {'TransID': GenTransID, 'From': TransactorFromHolder, 'To': TransactorToHolder, 'transactionDate': DateHolder,'Typ':TypeHolder, 'TransTypID': TransTypeIDHolder}) #UPDATE TRANSACTION TABLE
            
            conn.commit()
            print("EXECUTED")
        elif mode == "edit":
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
            # Edit functionality
            if Trans_DateFlag:
                cur.execute("""
                    UPDATE transactionTable
                    SET transactionDate = %(transactionDate)s
                    WHERE transactionId = %(TransID)s
                """, {'transactionDate': DateHolder, 'TransID': TransIDHolder})

            if Trans_GoodsFlag:
                if TypeHolder == "Item":
                    cur.execute("""
                        UPDATE Inventory
                        SET InventoryName = %(InvName)s, InventoryValue = %(Value)s, InventoryType = %(InvTyp)s, BranchId = %(BranchId)s, GoodsStatus = %(Status)s
                        WHERE InventoryId = %(InvID)s
                    """, {'InvName': GoodsHolder, 'Value': AmountHolder, 'InvTyp': InvTypHolder, 'BranchId': BranchHolder, 'Status': StatusHolder, 'InvID': GoodsIDHolder})
                elif TypeHolder == "Cash":
                    cur.execute("""
                        UPDATE balance
                        SET balanceamount = %(Amt)s
                        WHERE balanceid = %(BalID)s
                    """, {'Amt': AmountHolder, 'BalID': GoodsIDHolder})
            
            if Trans_TypeFlag:
                cur.execute("""
                    UPDATE transactionTable
                    SET transactionType = %(Typ)s
                    WHERE transactionId = %(TransID)s
                """, {'Typ': TypeHolder, 'TransID': TransIDHolder})
                
                if TypeHolder == "Cash":
                    cur.execute("""
                        UPDATE balance
                        SET balanceamount = %(Amt)s
                        WHERE balanceid = %(BalID)s
                    """, {'Amt': AmountHolder, 'BalID': GoodsIDHolder})
            
            if Trans_BranchFlag:
                if TypeHolder == "Cash":
                    cur.execute("""
                        UPDATE balance
                        SET branchid = %(BranchId)s
                        WHERE balanceid = %(BalID)s
                    """, {'BranchId': BranchHolder, 'BalID': GoodsIDHolder})
                elif TypeHolder == "Item":
                    cur.execute("""
                    UPDATE Inventory
                    SET BranchId = %(BranchId)s
                    WHERE InventoryId = %(InvID)s
                """, {'BranchId': BranchHolder, 'InvID': GoodsIDHolder})
                    
            if Trans_PartyFlag:
                cur.execute(""" 
                    UPDATE transactionTable
                    SET transactorFrom = %(From)s, transactionTo = %(To)s
                    WHERE transactionId = %(TransID)s
                """, {'From': PartyForHolder, 'To': PartyToHolder, 'TransID': TransIDHolder})
            
            conn.commit()
            print("EDIT EXECUTED")
            
    except Exception as e:
        print(f"An error occurred: {e}")

# ////////////////////////////{{CALCULATOR PAGE}}
mode_var = StringVar(value="Degrees")  # Default to Degrees
active_color = "#b8d4e0"  # Green for active
inactive_color = "#FFFFFF"  # White for inactive

def set_degrees():
    global mode_var
    mode_var.set("Degrees")
    button_degrees.configure(fg_color=active_color, text_color="#000000")  # Active button
    button_radians.configure(fg_color=inactive_color, text_color="#000000")  # Inactive button
    print("Mode set to Degrees")
    

def set_radians():
    global mode_var
    mode_var.set("Radians")
    button_radians.configure(fg_color=active_color, text_color="#000000")  # Active button
    button_degrees.configure(fg_color=inactive_color, text_color="#000000")  # Inactive button
    print("Mode set to Radians")


OutputCalculatorFont = CTkFont(family="Oswald", size=30, weight='bold')
EditFont = CTkFont(family="Oswald", size=15, weight='bold')

ViewedPost=0

def calculatorpage(page):
    global ViewedPost
    if ViewedPost == 0:
        global button_degrees, button_radians, button_EXP, HistoryToggleButton, HistorySideBar, HistoryScrollbar
        #START MASTER
        CalculatorMargin = CTkFrame(page)
        CalculatorMargin.pack(expand=True)
        #LEFT BAR
        HistorySideBar = CTkFrame(CalculatorMargin, width=150, height=320, border_color="#000000", border_width=1,fg_color="#FFFFFF")
        HistorySideBar.grid(row=0,column=0)
        HistorySideBar.grid_propagate(0)
        HistoryScrollbar = CTkScrollableFrame(HistorySideBar, width=140, height=270, border_width=1, fg_color="#FFFFFF",corner_radius=0)
        HistoryScrollbar.grid(row=1,column=0)
        HistoryToggleButton = CTkButton(HistorySideBar,text="EQUATION HISTORY",command=set_History,height=45, width=160, border_color="#000000", border_width=1,corner_radius=0, fg_color="#FFFFFF",text_color='#000000')
        HistoryToggleButton.grid(row=0,column=0)
        HistoryToggleButton.grid_propagate(0)
        

        #RIGHT BAR
        CalculatorSide = CTkFrame(CalculatorMargin, width=410, height=320, border_color="#000000", border_width=1)
        CalculatorSide.grid(row=0,column=1)
        CalculatorSide.grid_propagate(0)    
        #RIGHT BAR UI
        OutputCalculations = CTkEntry(CalculatorSide ,font=OutputCalculatorFont, width=410, height=120, border_color="#000000", border_width=1,corner_radius=0)
        OutputCalculations.grid(row=0,column=0)
        OutputCalculations.configure(state="readonly")
        
        OutputCalculations.ans = 0
        OutputCalculations.radians = True
        OutputCalculations.trig_input = ""

        OutputCalculations.degrees_button = None
        OutputCalculations.radians_button = None


        ButtonsForCalculationsFrame = CTkFrame(CalculatorSide, width=410, height=200, border_color="#000000", border_width=1,corner_radius=0)
        ButtonsForCalculationsFrame.grid(row=1, column=0)
        ButtonsForCalculationsFrame.grid_propagate(0)
        
        for i in range(6):
            ButtonsForCalculationsFrame.grid_columnconfigure(i, weight=1, uniform="column")
            ButtonsForCalculationsFrame.grid_rowconfigure(0, minsize=40)
        ViewedPost+=1
    else:
        print("Calculator page has been printed!")
    

    
    #Welcome to a programmer's worst nightmare LMFAOOOOO
    button_radians = CTkButton(ButtonsForCalculationsFrame,corner_radius=0, text="Rad",height=40, width=60,command=set_radians, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_radians.grid(row=0, column=0)
    button_EXP = CTkButton(ButtonsForCalculationsFrame, corner_radius=0,text="Play",height=40, width=60,command=play_sound, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_EXP.grid(row=1, column=0)
    button_pi = CTkButton(ButtonsForCalculationsFrame, corner_radius=0,text="π",height=40, width=60,command=lambda: appendtoentry("π", OutputCalculations, "pi"), border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_pi.grid(row=2, column=0)
    button_e = CTkButton(ButtonsForCalculationsFrame,corner_radius=0, text="e",height=40, width=60,command=lambda: appendtoentry("e", OutputCalculations, "e"), border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_e.grid(row=3, column=0)
    button_Ans = CTkButton(ButtonsForCalculationsFrame,corner_radius=0, text="Ans",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_Ans.grid(row=4, column=0)

    button_degrees = CTkButton(ButtonsForCalculationsFrame, corner_radius=0,text="Deg",height=40, width=60,command=set_degrees, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_degrees.grid(row=0, column=1)
    button_sin = CTkButton(ButtonsForCalculationsFrame,corner_radius=0, text="sin", height=40, width=60,command=lambda: appendtoentry("sin", OutputCalculations, "trig"), border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_sin.grid(row=1, column=1)

    button_cos = CTkButton(ButtonsForCalculationsFrame,corner_radius=0, text="cos", height=40, width=60,command=lambda: appendtoentry("cos", OutputCalculations, "trig"), border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_cos.grid(row=2, column=1)

    button_tan = CTkButton(ButtonsForCalculationsFrame,corner_radius=0, text="tan", height=40, width=60,command=lambda: appendtoentry("tan", OutputCalculations, "trig"), border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_tan.grid(row=3, column=1)
    button_del = CTkButton(ButtonsForCalculationsFrame,corner_radius=0, text="del",height=40, width=60,command=lambda: delete(OutputCalculations), border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_del.grid(row=4, column=1)
    #troll
    button6 = CTkButton(ButtonsForCalculationsFrame,corner_radius=0, text="x!",height=40, width=60,command=lambda: appendtoentry("!", OutputCalculations, "factorial"), border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button6.grid(row=0, column=2)
    button_natlog = CTkButton(ButtonsForCalculationsFrame,corner_radius=0, text="ln",height=40, width=60, command=lambda: appendtoentry("ln", OutputCalculations, "natlog"), border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_natlog.grid(row=1, column=2)
    button_log = CTkButton(ButtonsForCalculationsFrame,corner_radius=0, text="log",height=40, width=60,command=lambda: appendtoentry("log(", OutputCalculations, "logarithm"), border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_log.grid(row=2, column=2)
    button_sqrt = CTkButton(ButtonsForCalculationsFrame, corner_radius=0,text="√",height=40, width=60,command=lambda: appendtoentry("√", OutputCalculations, "sqrt"), border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_sqrt.grid(row=3, column=2)
    button_exponent = CTkButton(ButtonsForCalculationsFrame,corner_radius=0, text="x^2",height=40, width=60, command=lambda: appendtoentry("^2",OutputCalculations, "exponent"), border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_exponent.grid(row=4, column=2)
    #I do this because it's funny
    button_perc = CTkButton(ButtonsForCalculationsFrame,corner_radius=0, text="%",command=lambda: appendtoentry("%",OutputCalculations, "percentage"),height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_perc.grid(row=0, column=3)
    button_7 = CTkButton(ButtonsForCalculationsFrame,corner_radius=0,command=lambda: appendtoentry("7",OutputCalculations, "integer"), text="7",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_7.grid(row=1, column=3)
    button_4 = CTkButton(ButtonsForCalculationsFrame,corner_radius=0,command=lambda: appendtoentry("4",OutputCalculations, "integer"), text="4",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_4.grid(row=2, column=3)
    button_1 = CTkButton(ButtonsForCalculationsFrame,corner_radius=0,command=lambda: appendtoentry("1",OutputCalculations, "integer"), text="1",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_1.grid(row=3, column=3)
    button_0 = CTkButton(ButtonsForCalculationsFrame,corner_radius=0,command=lambda: appendtoentry("0",OutputCalculations, "integer"), text="0",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_0.grid(row=4, column=3)
    #the long slope of redundancy and idiocracy
    button_opb = CTkButton(ButtonsForCalculationsFrame,corner_radius=0, text="(",height=40, width=60,command=lambda: appendtoentry("(", OutputCalculations, "openbracket"), border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_opb.grid(row=0, column=4)
    button_8 = CTkButton(ButtonsForCalculationsFrame,corner_radius=0,command=lambda: appendtoentry("8",OutputCalculations, "integer"), text="8",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_8.grid(row=1, column=4)
    button_5 = CTkButton(ButtonsForCalculationsFrame,corner_radius=0,command=lambda: appendtoentry("5",OutputCalculations, "integer"), text="5",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_5.grid(row=2, column=4)
    button_2 = CTkButton(ButtonsForCalculationsFrame,corner_radius=0,command=lambda: appendtoentry("2",OutputCalculations, "integer"), text="2",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_2.grid(row=3, column=4)
    button_dot = CTkButton(ButtonsForCalculationsFrame,corner_radius=0, text=".",height=40, width=60, command=lambda: appendtoentry(".", OutputCalculations, "integer"), border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_dot.grid(row=4, column=4)

    button_clob = CTkButton(ButtonsForCalculationsFrame,corner_radius=0,command=lambda: appendtoentry(")",OutputCalculations, "bracket"), text=")",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_clob.grid(row=0, column=5)
    button_9 = CTkButton(ButtonsForCalculationsFrame,corner_radius=0,command=lambda: appendtoentry("9",OutputCalculations, "integer"), text="9",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_9.grid(row=1, column=5)
    button_6 = CTkButton(ButtonsForCalculationsFrame,corner_radius=0,command=lambda: appendtoentry("6",OutputCalculations, "integer"), text="6",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_6.grid(row=2, column=5)
    button_3 = CTkButton(ButtonsForCalculationsFrame,corner_radius=0,command=lambda: appendtoentry("3",OutputCalculations, "integer"), text="3",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_3.grid(row=3, column=5)
    button_equal = CTkButton(ButtonsForCalculationsFrame,corner_radius=0, text="=", command=lambda: calculate(OutputCalculations), height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_equal.grid(row=4, column=5)

    button_clearN = CTkButton(ButtonsForCalculationsFrame,corner_radius=0, text="CE", height=40, width=60,command=lambda: clear(OutputCalculations), border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_clearN.grid(row=0, column=6)
    button_div = CTkButton(ButtonsForCalculationsFrame,corner_radius=0, text="÷",height=40, width=60 ,command=lambda: appendtoentry("÷",OutputCalculations, "operation"), border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_div.grid(row=1, column=6)
    button_mult = CTkButton(ButtonsForCalculationsFrame,corner_radius=0, text="x",height=40, width=60,command=lambda: appendtoentry("x",OutputCalculations, "operation"),  border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_mult.grid(row=2, column=6)
    button_min = CTkButton(ButtonsForCalculationsFrame,corner_radius=0, text="-",height=40, width=60,command=lambda: appendtoentry("-",OutputCalculations, "operation"),  border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_min.grid(row=3, column=6)
    button_plus = CTkButton(ButtonsForCalculationsFrame,corner_radius=0, text="+",height=40, width=60,command=lambda: appendtoentry("+",OutputCalculations, "operation"),  border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_plus.grid(row=4, column=6)

 

                
def appendtoentry(value, OutputCalculations, type):
    print(value)
    currentvalue = OutputCalculations.get()
    OutputCalculations.configure(state="normal")
    if currentvalue == "Error":
        OutputCalculations.delete(0, END)

    if type == "integer":
        OutputCalculations.insert(END, str(value))
    elif type == "operation":
        OutputCalculations.insert(END, str(value))
    elif type == "trig":
        OutputCalculations.insert(END, value + "(")
    elif type == "bracket":
        OutputCalculations.insert(END, value)
    elif type == "bracket1":
        OutputCalculations.insert(END, value)
    elif type == "logarithm":
        OutputCalculations.insert(END, value)
    elif type == "sqrt":
        OutputCalculations.insert(END, value+ "(")
    elif type == "pi":
        OutputCalculations.insert(END, value)
        currentvalue = currentvalue.replace("π", "3.14159265359")
        
    elif type == "natlog":
        OutputCalculations.insert(END, value+"(")
    elif type == "exponent":
        OutputCalculations.insert(END, value)
    elif type == "e":
        OutputCalculations.insert(END, value)
    elif type == "openbracket":
        OutputCalculations.insert(END, value)
    elif type == "percentage":
        OutputCalculations.insert(END, value)
    elif type == "factorial":   
        OutputCalculations.insert(END, value)
    

    OutputCalculations.configure(state="readonly")

def clear(OutputCalculations):
    OutputCalculations.configure(state="normal")
    OutputCalculations.delete(0, END)
    OutputCalculations.configure(state="readonly")

def delete(OutputCalculations):
    current_value = OutputCalculations.get()
    
    if current_value == "Error":
        OutputCalculations.configure(state="normal")
        OutputCalculations.delete(0, END)
        OutputCalculations.configure(state="readonly")
    OutputCalculations.configure(state="normal")
    OutputCalculations.delete(len(current_value)-1, END)
    OutputCalculations.configure(state="readonly")

History = False


def calculate(OutputCalculations):
    global EquationStack, ResultsStack, History, HistoryScrollbar
    print("Calculate function called")
    EquationStack = []
    ResultsStack = []

    try:
        expression = OutputCalculations.get()
        EquationStack.append(expression)
        print("Expression:", expression)

        is_degrees = mode_var.get() == "Degrees"

        # Replace symbols
        expression = expression.replace("x", "*")
        expression = expression.replace("÷", "/")
        expression = expression.replace("--", "+")
        expression = expression.replace("%", "/100")

        # For trig functions, replace with math. prefix
        if is_degrees:
            expression = re.sub(r'sin\(([\d\.]+)\)', lambda m: f'math.sin(math.radians({m.group(1)}))', expression)#11/04/2024: Teacher Melvin was not here, so I utilized AI to help debug my RE expressions.
            expression = re.sub(r'cos\(([\d\.]+)\)', lambda m: f'math.cos(math.radians({m.group(1)}))', expression)
            expression = re.sub(r'tan\(([\d\.]+)\)', lambda m: f'math.tan(math.radians({m.group(1)}))', expression)
        else:
            expression = re.sub(r'sin\(([\d\.]+)\)', lambda m: f'math.sin({m.group(1)})', expression)
            expression = re.sub(r'cos\(([\d\.]+)\)', lambda m: f'math.cos({m.group(1)})', expression)
            expression = re.sub(r'tan\(([\d\.]+)\)', lambda m: f'math.tan({m.group(1)})', expression)

        #Factorial
        expression = re.sub(r'(\d+)!', r'math.factorial(\1)', expression)


        # Exponents
        expression = expression.replace("log(", "math.log10(")
        expression = expression.replace("ln(", "math.log(")
        expression = expression.replace("^", "**")
        expression = expression.replace("√(", "math.sqrt(")

        # Replace with numerical constants
        expression = expression.replace("π", "3.141592653589793")
        expression = expression.replace("e", "math.e")

        # Handle multiplication signs and spacing
        expression = expression.replace(")(", ")*(")
        expression = expression.replace(") ", ")*")
        expression = expression.replace(")(", ")*(")
        

        # Insert multiplication where necessary
        expression = re.sub(r'(\d+)([a-zA-Z]+)(\()', r'\1*\2\(', expression) 
        expression = re.sub(r'(?<!\w)(\d)(\()', r'\1*\2', expression)
        expression = re.sub(r'(?<!\w)(\))(\d)', r'\1*\2', expression)
        expression = re.sub(r'(\d)([a-zA-Z]+)', r'\1*\2', expression)

        print("Modified Expression:", expression)

        if expression.strip() == "":
            raise ValueError("Empty expression after modifications")

        result = eval(expression)  # Ensure eval is used SAFELY
        finalresult = round(result, 9)
        
            
        print("Result:", finalresult)
        ResultsStack.append(finalresult)
        OutputCalculations.configure(state="normal")
        OutputCalculations.delete(0, END)
        OutputCalculations.insert(0, str(finalresult))
        OutputCalculations.configure(state="readonly")

    except Exception as e:
        print(f"Error: {e}")
        OutputCalculations.configure(state="normal")
        OutputCalculations.delete(0, END)
        OutputCalculations.insert(0, "Error")
        OutputCalculations.configure(state="readonly")

    for I in EquationStack:
        EquationPop = str(EquationStack.pop())
        print(EquationPop)
        NewEquationArray.append(EquationPop)
        
    for I in ResultsStack:
        ResultsPop = str(ResultsStack.pop())
        print(ResultsPop)
        NewResultsArray.append(ResultsPop)
        
    UpdateHistory(NewEquationArray, History, HistoryScrollbar, NewResultsArray)

 
def set_History(): #sets whether or not its results or equations
    global History, HistoryToggleButton, EquationStack, ResultsStack,NewEquationArray,HistoryScrollbar
    
    if History == True:
        History = not History
        HistoryToggleButton.configure(text="EQUATION HISTORY")
        UpdateHistory(NewEquationArray, History,HistoryScrollbar, NewResultsArray)
        print("Now set to Equation.")
        DeleteButton()
        
    elif History== False:
        History = not History
        HistoryToggleButton.configure(text="RESULTS HISTORY")   
        UpdateHistory(NewEquationArray, History,HistoryScrollbar, NewResultsArray)
        print("Now set to Results")
        DeleteButton()
    

NewEquationArray=[]
NewResultsArray=[]

NewEquationArray[0:100]
NewResultsArray[0:100]


def UpdateHistory(NewEquationArray, History, HistoryScrollbar,NewResultsArray): #Updates the History by pasting everything within the New Equation Array
    global HistoryToggleButton, EquationStack, ResultsStack, EquationButton, ResultsButton
    print(History)
    
    if History == False:
        RowNum = 0
        for I in NewEquationArray:
                EquationButton = CTkButton(HistoryScrollbar, text=I, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000",hover_color="#FFFFFF", corner_radius=0)
                EquationButton.grid(row=RowNum,column=0)
                RowNum = RowNum + 1   
        
    elif History== True:  
        RowNum = 0
        for I in NewResultsArray:
                ResultsButton = CTkButton(HistoryScrollbar, text=I, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000",hover_color="#FFFFFF", corner_radius=0)
                ResultsButton.grid(row=RowNum,column=0)
                RowNum = RowNum + 1 
        
def DeleteButton():
    global EquationButton, ResultsButton
    if History == False:
        print("YOUR")
        for I in NewResultsArray:
            ResultsButton.destroy()
    else:
        print("MOM!")
        for I in NewEquationArray:
            EquationButton.destroy()
        






    


# ////////////////////////////{{HOME PAGE}}
def homepage(page):
    NoteButtonBox = CTkFrame(HomePage, width=160, height=298, fg_color="#FFFFFF", corner_radius=0)
    NoteBoxPadding = CTkFrame(HomePage, width=380, height=298, fg_color="#FFFFFF", corner_radius=0)

    NoteButtonBox.grid_propagate(0)
    NoteBoxPadding.grid_propagate(0)
    

    #THE NOTE BUTTONS SECTION---------------------------------
    for i in range(2):
        NoteButtonBox.grid_columnconfigure(i, weight=1, uniform="col")
        NoteButtonBox.grid_rowconfigure(0, minsize=51)

    NoteButtonBox.grid(row=0, column=0, pady = 20, padx = 15)
    NoteBoxPadding.grid(row=0, column=1, pady = 20, padx = 5) 

    NotesLabel = CTkLabel(NoteButtonBox,height=10, width=5, text="NOTES", anchor=CENTER, fg_color='#194680',text_color='white')

    AddNoteButton = CTkButton(NoteButtonBox, height=10, width=5, text="Add", corner_radius=0, fg_color='#06bd36',hover_color='#227839')
    EditNoteButton = CTkButton(NoteButtonBox, height=10, width=5, text="Edit",corner_radius=0, fg_color='#d41e06',hover_color='#782522')
    

    NotesLabel.grid(row=0,column=0,columnspan=2, sticky='nsew')
    AddNoteButton.grid(row=1,column=0, sticky='ew')
    EditNoteButton.grid(row=1,column=1, sticky='ew')
    
    #NOTE ADD BOX---------------------------------
    
    AddedNotesScrollbar = CTkScrollableFrame(NoteButtonBox, fg_color="#FFFFFF") 
    AddedNotesScrollbar.grid(rowspan=100, columnspan=2, sticky='nsew')
    
    

    #NOTE EDIT BOX---------------------------------
    TitleFont = CTkFont(family="Oswald", size=15, weight='bold')
    EditTitleLabel = CTkLabel(NoteBoxPadding,text="Notes", font=TitleFont)
    EditTitleLabel.grid(row=0,column=0, sticky='nsew')

    EditTextBox = CTkTextbox(NoteBoxPadding, width=380,corner_radius=0,fg_color='#ededed')
    EditTextBox.grid(row=1,column=0, sticky='nsew')

    AddNoteButton.configure(command=lambda: addnotecommand(AddedNotesScrollbar, EditTextBox, EditNoteButton, NoteBoxPadding, EditTitleLabel)) #c
    retrievenotebuttons(AddedNotesScrollbar,EditTextBox, EditNoteButton, NoteBoxPadding, EditTitleLabel)
    
    changelogid = 3.14159 #I made the changelog id pi because it's a unique number, which is great if we're making it into an id because most of the ids are just counting numbers, also making decimals impossible to configure as a proper note id
    Changelog = CTkButton(AddedNotesScrollbar, height=30, width=140, corner_radius=0, text="Changelog", command=lambda: verifyclick(changelogid, EditTextBox, EditNoteButton, NoteBoxPadding, AddedNotesScrollbar, EditTitleLabel))
    Changelog.grid(row=100, columnspan=2, pady=2, sticky='ew') 






#ADD NOTE BUTTON FUNCTIONS
def retrievenotebuttons(AddedNotesScrollbar, EditTextBox, EditNoteButton, NoteBoxPadding, EditTitleLabel):
    cur.execute("SELECT * FROM notes") #this literally just saves the notes
    rows = cur.fetchall()

    cur.execute("TRUNCATE TABLE notes") #This truncates the whole table, and deletes the whole table
    for i, row in enumerate(rows, start=1):
        cur.execute("INSERT INTO notes (noteid, note, notename) VALUES (%s, %s, %s)",  #This basically just reinserts everything from 1 to the constant amount of items in a row
                    (i, row[1], row[2]))
    
    cur.execute("""SELECT noteId, notename FROM Notes ORDER BY noteId""") #This selects everything to be in proper order from 1 to the constant amount of items in a row
    names = []
    nameBtnID = cur.fetchall() 
    for i, (note_id, notename) in enumerate(nameBtnID):
        if notename is None:
            notename = f"Note {note_id}"
        names.append(notename)

    cur.execute("""SELECT noteId, note FROM Notes ORDER BY noteId""") #same again here, but this time for the notes
    oldnotes = []  # a list to hold all the buttons
    noteBtnID = cur.fetchall()
    for i, (note_id, note) in enumerate(noteBtnID):
        notename = names[i]  # get the corresponding notename from the list
        oldnote = CTkButton(AddedNotesScrollbar, height=30, width=140, corner_radius=0, text=notename, command=lambda id=note_id: button_clicked(id, EditTextBox, EditNoteButton, NoteBoxPadding, AddedNotesScrollbar, EditTitleLabel))
        oldnote.grid(row=note_id, columnspan=2, pady=2, sticky='ew') 
        oldnotes.append(oldnote) #puts old notes into the list to track them down ig
    


TitleFont = CTkFont(family="Oswald", size=15, weight='bold')

def verifyclick(button_id, EditTextBox, EditNoteButton, NoteBoxPadding, AddedNotesScrollbar, EditTitleLabel):
    global EDITFLAG
    button_clicked(button_id, EditTextBox, EditNoteButton, NoteBoxPadding, AddedNotesScrollbar, EditTitleLabel)
    button_idEvt(button_id, EditTextBox, EditNoteButton, NoteBoxPadding, AddedNotesScrollbar)
    if button_id == 3.14159 and EDITFLAG == FALSE: 
        EditTitleLabel.configure(font=TitleFont, text="Changelog")
        changelognotes(button_id, EditTextBox, EditNoteButton, NoteBoxPadding, AddedNotesScrollbar) #this is for changelogs
    

def button_clicked(button_id, EditTextBox, EditNoteButton, NoteBoxPadding, AddedNotesScrollbar, EditTitleLabel): #clickity click click
    global EDITFLAG
    EditTitleLabel.configure(font=TitleFont,text="Notes")
    print(f"Button {button_id} clicked") 
    if EDITFLAG == FALSE:
        retrieveNote(button_id, EditTextBox, EditNoteButton, NoteBoxPadding, AddedNotesScrollbar) #this calls on so edit functions may work
        
    
def button_idEvt(button_id, EditTextBox, EditNoteButton, NoteBoxPadding, AddedNotesScrollbar):
    changelognotes(button_id, EditTextBox, EditNoteButton, NoteBoxPadding, AddedNotesScrollbar)


def changelognotes(id, EditTextBox, EditNoteButton, NoteBoxPadding, AddedNotesScrollbar):
    global EDITFLAG
    if id == 3.14159 and EDITFLAG == False:
        cur.execute("""SELECT MAX(version) FROM changelog""")
        version = cur.fetchone()
        EditTextBox.configure(state=NORMAL) #configure so the editbox can be editable
        EditTextBox.delete(1.0, END)
        cur.execute("""SELECT changelog FROM changelog WHERE version = %s""", version)
        notefeedback = cur.fetchone()
        if str(notefeedback[0]) == "None": #basically just checks if given is null, then don't post
            EditTextBox.insert("0.0", ' ')
        else:
            EditTextBox.insert("0.0", str(notefeedback[0]))
        EditTextBox.configure(state=DISABLED)
    else: 
        print("gg")




def addnotecommand(notescrollbar, EditTextBox, EditNoteButton, NoteBoxPadding, EditTitleLabel): 
    global EDITFLAG
    cur.execute("""SELECT noteId FROM Notes """)
    x = cur.fetchall()
    noteIDs = [item[0] for item in x]  # Extract the note IDs from the query result

    if noteIDs:  # Check if the list is not empty
        NewNoteID = max(noteIDs) + 1  # finds max note ID and increment it
    else:
        NewNoteID = 1  # If list is empty, set the NewNoteID to 1

    if NewNoteID < 100 and EDITFLAG == FALSE:
        noteIDs = [item[0] for item in x]  # Extract the note IDs from the query result

        if noteIDs:  # Check if the list is not empty
            NewNoteID = max(noteIDs) + 1  # finds max note ID and increment it
        else:
            NewNoteID = 1  # If list is empty, set the NewNoteID to 1

        cur.execute("""INSERT INTO Notes(noteId) VALUES(%s)""",[NewNoteID])
        conn.commit()

        newnote = CTkButton(notescrollbar, height=30, width=140, text="Note " + str(NewNoteID), corner_radius=0)
        newnote.grid(row=NewNoteID, columnspan=2, pady=2, sticky='ew')
        newnote.configure(command=lambda: button_clicked(NewNoteID, EditTextBox, EditNoteButton, NoteBoxPadding, notescrollbar, EditTitleLabel))
    else:
        cur.execute("""DELETE FROM Notes WHERE noteId>100""")
        conn.commit()
        print("Yes")



def editselect(NoteBoxPadding,EditTextBox, button_id, AddedNotesScrollbar): #ASK ABOUT THE EDITTING BUG BRO PLS // 11/4/2024:
    global EDITFLAG
    EDITFLAG = True
    print(button_id) 
    if EDITFLAG == True and button_id != 3.14159:
        NoteBoxPadding.configure()
        EditTextBox.configure(state=NORMAL)
        saveButton = CTkButton(NoteBoxPadding, text="save",width=5,corner_radius=0,fg_color='#ffb300')
        deleteButton = CTkButton(NoteBoxPadding, text="delete",width=5,corner_radius=0,fg_color='#ff3300')

        saveButton.grid(row=2,column=0, sticky='ew', pady=2)
        deleteButton.grid(row=3,column=0, sticky='ew')

        saveButton.configure(command=lambda: editsave(EditTextBox.get("1.0",END), saveButton, deleteButton, EditTextBox, button_id ))
        deleteButton.configure(command=lambda: editdelete(saveButton, deleteButton, EditTextBox, button_id, AddedNotesScrollbar))


    
    

def editsave(Content, saveButton, deleteButton, EditTextBox, button_id): #SAVE BUTTON FOR EDITTING MODE
    print(button_id)
    cur.execute("""UPDATE notes
    SET note = (%s)
    WHERE noteid = (%s);""",(Content, button_id))
    EditTextBox.configure(state=DISABLED)
    saveButton.grid_forget()
    deleteButton.grid_forget()
    print("debugging worked")
    conn.commit()
    global EDITFLAG
    EDITFLAG = False

def editdelete(saveButton, deleteButton, EditTextBox, button_id, AddedNotesScrollbar):#DELETE BUTTON FOR EDITTING MODE
    cur.execute("""UPDATE notes
    SET note = NULL
    WHERE noteid = (%s);""",(button_id,)) #Updates the notes to set the note to null so bye bye note

    cur.execute("""DELETE FROM notes WHERE noteid = (%s);""",(button_id,))
    EditTextBox.delete(1.0, END)
    EditTextBox.configure(state=DISABLED)
    delete_notes(AddedNotesScrollbar, button_id) #opens function to delete the note 
    
    saveButton.grid_forget() #deletes all edit buttons
    deleteButton.grid_forget()
    print("debugging worked")
    conn.commit()
    global EDITFLAG
    EDITFLAG = False

def delete_notes(AddedNotesScrollbar, button_id):
    for widget in AddedNotesScrollbar.winfo_children():
        if widget.cget("text") == f"Note {button_id}":
            widget.destroy()
    cur.execute("DELETE FROM notes WHERE noteid = (%s);",(button_id,))
    conn.commit()



def retrieveNote(button_id, EditTextBox, EditNoteButton, NoteBoxPadding, AddedNotesScrollbar): #Retrieve note
    global EDITFLAG
    print(str(button_id) + " is the page")
    if EDITFLAG == False and button_id != 3.14159:
        print(str(button_id) + " is the page")
        EditTextBox.configure(state=NORMAL) #configure so the editbox can be editable
        EditTextBox.delete(1.0, END) #basically just deletes the previous entry
        cur.execute("""SELECT note FROM Notes WHERE noteId = (%s)""",[button_id]) #fetches notes from desired button_id
        notefeedback = cur.fetchone()
        if str(notefeedback[0]) == "None": #basically just checks if given is null, then don't post
            EditTextBox.insert("0.0", ' ')
        else:
            EditTextBox.insert("0.0", str(notefeedback[0]))
        EditTextBox.configure(state=DISABLED)
        EditNoteButton.configure(command = lambda button_id=button_id: editselect(NoteBoxPadding, EditTextBox, button_id, AddedNotesScrollbar))
    else:
        EditNoteButton.configure(command = lambda: printcannotretrieve())

def printcannotretrieve():
    print("Cannot retrieve.")





#++++++++++++++++++++++++++++++ {LOGIN FUNCTIONS} ++++++++++++++++++++++++++++++++++++++

#submit function
def RecieveUser(Username, Password, loginaccess, page):
    cur.execute("SELECT * FROM loginpaswd WHERE loginid = %(username)s AND password = %(password)s", {'username': Username.get(), 'password': Password.get()})
    for row in cur.fetchall():
        print(row)
        loginaccess=True
    
    if loginaccess == True:
        admittedAccess(True)
    else:
        print("no go, hombre :(") #MAKE SURE TO ADD ERROR SIGN HERE

    conn.commit()


#LOGIN PAGE
def loginpage(page,loginaccess):
    global LOGIN
    LOGINFONT = CTkFont(family="Oswald", size=30, weight='bold')

    if loginaccess == False and not LOGIN and page != HomePage:
        page.configure(fg_color='#0053A0')
        LOGIN = CTkFrame(page, width=600, height=400, corner_radius=0, fg_color='#FFFFFF')
        LOGIN.pack (expand=True)

        loginlabel = CTkLabel(master=LOGIN, font=LOGINFONT, text="LOGIN")
        loginlabel.grid(row=0,column=0, pady=10)
        Account = CTkEntry(master=LOGIN, width=400, corner_radius=0, placeholder_text="Username")
        Account.grid(row=1, column=0, padx=25, pady=5)

        Password = CTkEntry(master=LOGIN, width=400, corner_radius=0, show="●",placeholder_text="Password")
        Password.grid(row=2, column=0, padx=25, pady=5)

        SubmitLog = CTkButton(master=LOGIN, width=400, corner_radius=0, text="SUBMIT", fg_color='#424242', hover_color='#231F20', command=lambda: RecieveUser(Account, Password,loginaccess, page))
        SubmitLog.grid(row=3, column=0, padx=25, pady=30)
        SubmitLog.configure()
    elif loginaccess == True:
        destroyloginitems(LOGIN)
    else:
        print("it happened dawg")

def destroyloginitems(LOGIN):
    LOGIN.pack_forget()

LoadedFont = CTkFont(family="Oswald", size=20, weight='bold')
def loadedpage(page):
    AccessContent = CTkFrame(page, width=600, height=355, fg_color="#0053A0", corner_radius=0)
    AccessLabel = CTkLabel(AccessContent, font=LoadedFont, text="You now have access! Click on a tab to get started.", text_color='#FFFFFF', justify="center")
    AccessContent.grid_propagate(0)

    AccessContent.grid(pady = 0, padx = 0)
    AccessLabel.place(relx=0.5, rely=0.5, anchor="center")

#++++++++++++++++++++++++++++++ {TAB FUNCTIONS} ++++++++++++++++++++++++++++++++++++++

# Function to handle button clicks
def button_event(page,loginaccess):
    show_page(page,loginaccess)

#To resize and center all buttons
for i in range(6):
    TABFRAME.grid_columnconfigure(i, weight=1, uniform="col")
    TABFRAME.grid_rowconfigure(0, minsize=51)

# buttons
HomeTab = CTkButton(TABFRAME, text="Home", width=20, corner_radius=0 , command=lambda: button_event(HomePage,loginaccess))
HomeTab.grid(row=0, column=0, pady=10, padx=6, sticky="nsew")

TransactionsTab = CTkButton(TABFRAME, text="Transactions", width=20, corner_radius=0, command=lambda: button_event(LoginPage,loginaccess))
TransactionsTab.grid(row=0, column=1, pady=10, padx=6, sticky="nsew")

ClientTab = CTkButton(TABFRAME, text="Donator", width=20, corner_radius=0, command=lambda: button_event(LoginPage,loginaccess))
ClientTab.grid(row=0, column=2, pady=10, padx=6, sticky="nsew")

InventoryTab = CTkButton(TABFRAME, text="Inventory", width=20, corner_radius=0, command=lambda: button_event(LoginPage,loginaccess))
InventoryTab.grid(row=0, column=3, pady=10, padx=6, sticky="nsew")

BudgetTab = CTkButton(TABFRAME, text="Budget", width=20, corner_radius=0, command=lambda: button_event(LoginPage,loginaccess))
BudgetTab.grid(row=0, column=4, pady=10, padx=6, sticky="nsew")

Calculatortab = CTkButton(TABFRAME, text="Calculator", width=20, corner_radius=0, command=lambda: button_event(CalculatorPage,loginaccess))
Calculatortab.grid(row=0, column=5, pady=10, padx=6, sticky="nsew")

def admittedAccess(loginaccess):
    if loginaccess == True:
        destroyloginitems(LOGIN)
        loadedpage(LoginPage)
        TransactionsTab.configure(command=lambda: button_event(TransactionsPage,loginaccess))
        ClientTab.configure(command=lambda: button_event(ClientPage,loginaccess))
        InventoryTab.configure(command=lambda: button_event(InventoryPage,loginaccess))
        BudgetTab.configure(command=lambda: button_event(InventoryPage,loginaccess))
        


# Show the first page by default
show_page(HomePage, loginaccess)

window.mainloop()

#am cooked

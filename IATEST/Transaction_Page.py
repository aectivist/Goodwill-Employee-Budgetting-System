from customtkinter import *
from CTkTable import *
import psycopg2
import random
import tkinter as tk
from tkinter import ttk
from datetime import datetime
        
conn=psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="Saibaba216$", port=5432)
cur = conn.cursor()

#https://github.com/Akascape/CTkTable



window = CTk()
window.title("BUDGET")
window.geometry("600x400") #fml
window.resizable(0,0) #disable resize
set_appearance_mode("light")




#++++++++++++++++++++++++++++++ {PAGES} ++++++++++++++++++++++++++++++++++++++


# Create frames for each page
TABFRAME = CTkFrame(window, height=51, width=600, fg_color="#1E1E1E", corner_radius=0)
TABFRAME.pack(anchor=CENTER, fill=X)


#These are the individual pages, or rather, the frames
TransactionsPage = CTkFrame(window)
TransactionsPage.pack(fill=BOTH, expand=True)




# Create a list to hold all the pages
pages = [TransactionsPage]


# Function to show a page
def show_page(page):
    page.pack(fill=BOTH, expand=True)
    window.update_idletasks()  # Update the UI
    if page == TransactionsPage:
        transactionpage(TransactionsPage)
       


         
#++++++++++++++++++++++++++++++ {PAGE FUNCTIONS} ++++++++++++++++++++++++++++++++++++++
#DO NOT EDIT SPACE, WILL USE SPACE FOR THE OTHER PAGES


#def clientpage(page):
#def assetpage(page):
#def calculator(page):





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
        SearchComboChoices.set("Select")
        SearchComboChoices.grid(row = 3, column=0, padx=10,pady=2)
        SearchComboChoices.configure(state="readonly")
        TransactionsPagePost=1
    else:
        print("Page has already been outputted!")


#REQUIRED DATATYPES _------------------------------------------------------------------- 
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

ConfirmedChoiceForSearch = ""
def TransactionSearch_ComboCallback(choice):
    global ConfirmedChoiceForSearch
    if choice == "Transaction ID":
        ConfirmedChoiceForSearch = "Transaction ID"
    elif choice == "Transaction From":
        ConfirmedChoiceForSearch = "Transaction From"
    elif choice == "Transaction To":
        ConfirmedChoiceForSearch = "Transaction To"
    elif choice == "Date":
        ConfirmedChoiceForSearch = "Date"
    print("Search Combobox works")
    print(choice)
    print(ConfirmedChoiceForSearch)

def TransactionSearch(SearchEntry):
    global Error, ErrorBoolean, viewederror,ConfirmedChoiceForSearch
    columns = ["Transaction ID", "From", "To", "Inventory ID", "Value",  "Name", "Type", "Status", "Branch ID"]

    try:
        query = """
            SELECT 
                transactionTable.TransactionId, 
                transactionTable.TransactorFrom, 
                transactionTable.TransactionTo, 
                transactionTable.TransactionDate, 
                transactionTable.transactionTypeID, 
                Inventory.InventoryName, 
                Inventory.InventoryValue, 
                Inventory.InventoryType, 
                Inventory.BranchId, 
                Inventory.GoodsStatus
            FROM 
                transactionTable
            LEFT JOIN 
                transactionType ON transactionTable.transactionTypeID = transactionType.transactionTypeId
            LEFT JOIN 
                Inventory ON transactionType.InventoryId = Inventory.InventoryId
            WHERE
        """
        params = {}

        if ConfirmedChoiceForSearch == "Transaction ID":
            query += " transactionTable.TransactionId = %(TransID)s;"
            params = {"TransID": SearchEntry.get()}
        elif ConfirmedChoiceForSearch == "Transaction From":
            query += " transactionTable.TransactorFrom = %(TransactorFrom)s;"
            params = {"TransactorFrom": SearchEntry.get()}
        elif ConfirmedChoiceForSearch == "Transaction To":
            query += " transactionTable.TransactionTo = %(TransactionTo)s;"
            params = {"TransactionTo": SearchEntry.get()}
        elif ConfirmedChoiceForSearch == "Date":
            try:
                # Parse the date input to a datetime object
                search_date = datetime.strptime(SearchEntry.get(), "%d/%m/%Y")
                # Convert the datetime object to the desired format (yyyy/mm/dd)
                formatted_date = search_date.strftime("%Y/%m/%d")
                query += " transactionTable.TransactionDate = %(Date)s;"
                params = {"Date": formatted_date}
            except ValueError:
                print("Date invalid")
                if viewederror == 0:
                    print("Please Input Date Entry CORRECTLY.")
                    ErrorBoolean = True
                    Error = CTkLabel(SearchRequestContent, text="Please Input Date Entry CORRECTLY.", text_color="red", height=13)
                    Error.place(x=50, y=3)
                    viewederror = 1  # Avoid repeated error messages
                return  # Exit the function if date is invalid


        # Execute the query
        cur.execute(query, params)

        # Fetch and display results
        rows = cur.fetchall()
        if rows:
            tree = ttk.Treeview(OutputTableScrollbarContent, columns=columns, show="headings", height=10)
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, anchor="center", width=90)

            for row in rows:
                print(row)
                tree.insert("", "end", values=row)

            # Add Scrollbar
            scrollbar = ttk.Scrollbar(OutputTableScrollbarContent, orient="vertical", command=tree.yview)
            x_view_scrollbar = ttk.Scrollbar(OutputTableScrollbarContent, orient="horizontal", command=tree.xview)

            tree.configure(yscroll=scrollbar.set, xscroll=x_view_scrollbar.set)
            tree.grid(row=0, column=0, sticky="nsew")
            scrollbar.grid(row=0, column=1, sticky="ns")
            x_view_scrollbar.grid(row=1, column=0, sticky="ew")

            OutputTableScrollbarContent.grid_rowconfigure(0, weight=1)
            OutputTableScrollbarContent.grid_columnconfigure(0, weight=1)
        else:
            print("No results found.")
            
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        cur.connection.rollback()
        print("Rolling back the transaction due to an error.")
        
    except Exception as e:
        print(f"Unexpected error: {e}")


        




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
            print("ERROR")

        TransAddExist = False
    # Destroy Edit mode widgets if they exist
    if TransEditExist:
        try:
            TransactionIDEdit.destroy()
            Transaction_combobox.destroy()
        except Exception as e:
            print(f"Error destroying Transaction_combobox and TransactionIDEdit: {e}")
        try:
            if ErrorBoolean==True:
                Error.destroy()
                viewederror=0
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
                try:
                    inventorytypebox.place_forget()
                except Exception as e:
                    print("inventorytypebox does not exist")
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

    # Destroy the common input button if it exists
    try:
        Transaction_inputbutton.destroy()
    except NameError:
        pass  # Handle case where button isn't created yet

        
    
   
def addmodeui():
    vieweditemflag = 1
    
    global TransAddExist, TransactionNameBoxFrom, TransactionNameBoxTo, Transaction_inputbutton, Transaction_combobox, sucessful_transaction 
    global DateHolder, GoodsHolder, BranchHolder, TypeHolder, AmountHolder, PartyToHolder, PartyForHolder, StatusHolder, InvTypHolder,TransIDHolder
    DateHolder=""
    GoodsHolder=""
    BranchHolder=""
    TypeHolder="Item"
    AmountHolder = "0"
    StatusHolder = "Bought"
    PartyToHolder=""
    PartyForHolder=""
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
    Transaction_combobox = CTkComboBox(OutputEditContent, values=["Date", "Inventory Name", "Type", "Branch ID"], command=callback, variable=comboVal, height = 25, corner_radius=1, width=110)
    Transaction_combobox.set("Select")
    Transaction_combobox.place(x=5, y = 53)
    Transaction_combobox.configure(state="readonly")
    
    Transaction_inputbutton = CTkButton(OutputEditContent, text="Add", corner_radius=0, font=BTNFont, text_color='#000000', fg_color='#FFFFFF', border_color='#000000', border_width=1,hover_color='#e6e6e6', width=100, height=27,command= lambda: handleaddtrans())
    Transaction_inputbutton.place(x=295, y=82)
    

    TransAddExist = True  # Mark Add mode as active

def editmodeui():
    
    vieweditemflag = 1
    global TransEditExist, TransactionIDEdit, Transaction_combobox, Transaction_inputbutton, sucessful_transaction
    global DateHolder, GoodsIDHolder, BranchHolder, TypeHolder, AmountHolder, PartyToHolder, PartyForHolder, StatusHolder, InvTypHolder,TransIDHolder
    TransIDHolder=""
    DateHolder=""
    GoodsIDHolder=""
    BranchHolder=""
    TypeHolder="Item"
    AmountHolder = "0"
    PartyToHolder=""
    PartyForHolder=""
    StatusHolder ="Bought"
    InvTypHolder="None"

    sucessful_transaction = False

    #All Flags
    global Trans_DateFlag, Trans_GoodsFlag, Trans_TypeFlag, Trans_BranchFlag, Trans_IDFlag, Trans_PartyFlag
    Trans_DateFlag=False
    Trans_GoodsFlag=False
    Trans_TypeFlag=False
    Trans_BranchFlag=False
    Trans_IDFlag = False
    Trans_PartyFlag = False
    
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
    Transaction_combobox = CTkComboBox(OutputEditContent, values=["Date", "Inventory ID", "Type", "Branch ID", "Parties"], command=callback, variable=comboVal, height = 25, corner_radius=1, width=110)
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
    global deletebuttonrequestchecker
    ItemToDelete = TransactionIDDelete.get()
    if ItemToDelete != "":
        print("Item is deleted. Transaction =" + str(ItemToDelete))
        clearcurrentmode()
        
    else:
        print("Please enter correct field properly.")
        
def callback(choice): #COMBO BOX FUNCTIONALITIES
    global enteronce, enteronceforcombo, inventorytypebox, diffvalue, typebox,  DateHolder, GoodsHolder,TransIDHolder, BranchHolder, TypeHolder, AmountHolder,InvTypHolder, typewaschecked
    enteronce = enteronce + 1
    enteronceforcombo = enteronceforcombo + 1

    global ErrorBoolean, Error, viewederror
    try:
            if ErrorBoolean==True:
                Error.destroy()
                viewederror=0
                ErrorBoolean = False
    except Exception as e:
        print(f"Deletion Error not working. Error: {e}" )
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
                
                
            elif choice == "Inventory Name": #for Inventory
                diffvalue = 2
                AddGoodsEntryBox = CTkEntry(OutputEditContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="Inventory Id", width=275, height = 25)
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
                    AddGoodsEntryBox.configure(placeholder_text="Inventory Name")
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
                elif TypeHolder == "Cash": #otherwise, it would only place balance if it is cash (since CASH cannot have any other name other than it being run against the balance)
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
            EditSearchBoxEnter.destroy()
            enteronce = 1
            print (enteronce)
            
        
        if enteronce == 1:
            EditSearchBoxEnter = CTkButton(OutputEditContent, text = "Confirm", corner_radius=0,font=BTNFont, text_color='#000000', fg_color='#FFFFFF', border_color='#000000', border_width=1, hover_color='#e6e6e6', width=100, height = 27, command=lambda: confirmyourchoice(choice, EditSearchBoxEnter))
            EditSearchBoxEnter.place(x=190,y=82)

        if enteronceforcombo>1:
            if diffvalue == 1:
                EditDateEntryBox.destroy()
            elif diffvalue == 2:
                EditGoodsEntryBox.destroy()
                inventorytypebox.destroy()
            elif diffvalue == 3:
                typebox.destroy()
                amtinputEdit.destroy()
                statusbox.destroy()
            elif diffvalue == 4:
                EditBranchEntryBox.destroy()
            elif diffvalue == 5:
                PartyToEntryBox.destroy()
                PartyForEntryBox.destroy()

            enteronceforcombo = 1
            print (enteronceforcombo)

        if enteronceforcombo == 1:
            if choice == "Date": #For DATE
                diffvalue = 1
                EditDateEntryBox = CTkEntry(OutputEditContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="Date of Transaction", width=275, height = 25)
                EditDateEntryBox.place(x=120, y = 53)
                EditDateEntryBox.configure(state="normal")
                EditDateEntryBox.insert(0,DateHolder)
                
                
            elif choice == "Inventory ID": #for GOODS
                diffvalue = 2
                EditGoodsEntryBox = CTkEntry(OutputEditContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="Inventory Id", width=275, height = 25)
                EditGoodsEntryBox.place(x=120, y = 53)
                EditGoodsEntryBox.configure(state="normal")
                EditGoodsEntryBox.insert(0,GoodsIDHolder)
                
                inventorytypeVal = StringVar(value="None")
                inventorytypebox = CTkComboBox(OutputEditContent, values=["None", "Liability","Asset"], command=boolforinvtypcheck, variable=inventorytypeVal, height = 27, corner_radius=1, width=180) #whether none asset or liability 
                inventorytypebox.place(x=5, y = 82)
                inventorytypebox.set(InvTypHolder)
                inventorytypebox.configure(state="readonly")
                
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
        
        
            
        if BranchHolder == "" or DateHolder == "" or GoodsIDHolder == "" or AmountHolder == "" or PartyForHolder == "" or PartyToHolder == "": #if blank is empty, then delete items in it
            if DateHolder ==""and diffvalue == 1:
                EditDateEntryBox.delete(0, END)
                EditDateEntryBox.configure(placeholder_text="Date of Transaction")
            elif GoodsIDHolder ==""and diffvalue == 2:
                EditGoodsEntryBox.delete(0, END)
                EditGoodsEntryBox.configure(placeholder_text="Inventory Id")
            elif TypeHolder == ""and diffvalue == 3:
                amtinputEdit.delete(0, END)
                amtinputEdit.configure(placeholder_text="Amount")
            elif BranchHolder == "" and diffvalue == 4:
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
                inventorytypebox.insert(0, InvTypHolder)
            elif TypeHolder != "" and diffvalue==3:
                typebox.insert(0, TypeHolder)
                amtinputEdit.insert(0, AmountHolder)
                statusbox.insert(0, StatusHolder)
            elif BranchHolder != "" and diffvalue==4: 
                EditBranchEntryBox.insert(0,BranchHolder)
            elif PartyToHolder != "" and diffvalue == 5:
                PartyToEntryBox.insert(0,PartyToHolder)
            elif PartyForHolder != "" and diffvalue == 5:
                PartyForEntryBox.insert(0,PartyForHolder)
            
        
        print ("diffvalue: " + str(diffvalue))


def confirmyourchoice(choice, AddSearchBoxEnter):  # CONFIRMS THE CHOICE
    global DateHolder, GoodsHolder, BranchHolder, TypeChecker, TypeHolder, typebox, AmountHolder, TransIDHolder, PartyForHolder, InvTypHolder, PartyToHolder, Trans_PartyFlag, StatusHolder, StatusChecker
    global Trans_DateFlag, Trans_GoodsFlag, Trans_TypeFlag, Trans_BranchFlag, Trans_IDFlag
    global ErrorBoolean, Error, viewederror, amountedit
    
    if mode == "add":
        if diffvalue == 1:  # DATE ----------
            DateHolder = AddDateEntryBox.get()
            
            try:
                # Try to convert the input to a datetime object using the desired format
                datetime.strptime(AddDateEntryBox.get(), "%d/%m/%Y")  # format: DD-MM-YYYY
                # If no exception is raised, it's a valid date
                Trans_DateFlag = True
                # Now destroy AddSearchBoxEnter only if the date is valid\
                print("Yow!")
                AddDateEntryBox.place_forget()  # Forget the entry box
                AddSearchBoxEnter.destroy()  # Only destroy if the date is valid
                try:
                    Error.destroy()
                except Exception as e:
                    print("Error does not exist")
            except ValueError:
                # If there's a ValueError, date is invalid
                Trans_DateFlag = False
                if viewederror == 0:
                    print("Please Input ALL entries.")
                    ErrorBoolean = True
                    Error = CTkLabel(OutputEditContent, text="Please Input Date Entry CORRECTLY.", text_color="red", height=13)
                    Error.place(x=200, y=3)
                    viewederror = 1  # Avoid repeated error messages
                    
                

        elif diffvalue == 2:  # GOODS ---------
            if TypeChecker == True:
                GoodsHolder = AddGoodsEntryBox.get()
                InvTypHolder = inventorytypebox.get()
            else:
                GoodsHolder = "Balance"
            AddGoodsEntryBox.place_forget()
            try:
                inventorytypebox.place_forget()
            except Exception as e:
                print("inventorytypebox does not exist")
            print(GoodsHolder)
            Trans_GoodsFlag = True
            # AddSearchBoxEnter.destroy() should only be called if other flags are valid, not for Goods alone
            AddSearchBoxEnter.destroy()

        elif diffvalue == 3:  # TYPE ----------
            typebox.place_forget()
            amtinput.place_forget()
            if TypeChecker == True:  # If it's true, then it's an item
                TypeHolder = "Item"
            elif TypeChecker == False:
                TypeHolder = "Cash"
            print(TypeHolder)
            Trans_TypeFlag = True
            try:
                statusbox.place_forget()
            except Exception as e:
                print("Already destroyed.")
            # AddSearchBoxEnter.destroy() should only be called if other flags are valid, not for Type alone
            AddSearchBoxEnter.destroy()

        elif diffvalue == 4:  # BRANCH ------
            BranchHolder = AddBranchEntryBox.get()
            AddBranchEntryBox.place_forget()
            print(BranchHolder)
            Trans_BranchFlag = True
            # AddSearchBoxEnter.destroy() should only be called if other flags are valid, not for Branch alone
            AddSearchBoxEnter.destroy()


        


    elif mode=="edit": #CONFIRM EDIT CHOICE
        global GoodsIDHolder
        EditSearchBoxEnter.destroy()
        if choice == "Date" and EditDateEntryBox.get() != "": #DATE
            DateHolder = EditDateEntryBox.get()
            print (DateHolder)
            Trans_DateFlag = True
            EditDateEntryBox.configure(state="readonly")
            
        elif choice == "Inventory ID" and EditGoodsEntryBox.get() != "": #INV
            GoodsIDHolder = EditGoodsEntryBox.get()
            print (GoodsIDHolder)
            Trans_GoodsFlag = True
            EditGoodsEntryBox.configure(state="readonly")
            
        elif choice == "Branch ID" and EditBranchEntryBox.get() != "": #BRANCH
            BranchHolder = EditBranchEntryBox.get()
            print (BranchHolder)
            Trans_BranchFlag = True
            EditBranchEntryBox.configure(state="readonly")

        elif choice == "Type" and TypeHolder != "": #TYPE
            if TypeChecker == True: #if its true then its an item
                TypeHolder = "Item"
            elif TypeChecker == False:
                TypeHolder = "Cash"
            print (TypeHolder)

            if StatusChecker == 1: #if its 1 then its bought, else its sold or donated
                StatusHolder = "Bought"
            elif StatusChecker == 2:
                StatusHolder = "Sold"
            elif StatusChecker == 3:
                StatusHolder = "Donation"
            print(StatusHolder)
            Trans_TypeFlag = True #checks if confirmed then flag is true
            AmountHolder = amtinputEdit.get()
            amtinputEdit.configure(state="readonly")
            
        elif choice == "Parties": #PARTIES
           if PartyForEntryBox.get != "" and PartyToEntryBox.get != "":
                PartyForHolder = PartyForEntryBox.get() #gets and puts
                print(PartyForHolder)
                PartyToHolder = PartyToEntryBox.get()#gets and puts
                print(PartyToHolder)

                PartyForEntryBox.configure(state="readonly")
                PartyToEntryBox.configure(state="readonly")
                
                Trans_PartyFlag = True



            
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
    print ("Name= " + str(Trans_DateFlag) + ", Goods= " + str(Trans_GoodsFlag) + ", Type= " + str(Trans_TypeFlag) + ", Branch= " + str(Trans_BranchFlag)) 

    if diffvalue>0:
        if (Trans_DateFlag == True and Trans_GoodsFlag== True and Trans_TypeFlag == True and Trans_BranchFlag == True and TransactionNameToFlag == True and TransactionNameForFlag == True and AmountHolder.isnumeric()): #CHECKS IF ALL ARE TRUE AND CORRECTLY INPUTTED!!
        
            
            cur.execute("""SELECT * FROM goodwillBranch WHERE branchId = %(branchId)s""", {'branchId': BranchHolder})
            for row in cur.fetchall():
                print(row)
                if row != "":
                    outputFlag = True
            
            conn.commit()
            
            if outputFlag == True:      
                print("Sucessfully Submitted.")
                print("Transactor From: " + TransactorFromHolder)
                print("Transactor To: " + TransactorToHolder)
                print("Date: " + DateHolder)
                print("Inv Type " + InvTypHolder )
                print("Goods: " + GoodsHolder)
                print("Branch ID: " + BranchHolder) 
                print("Type: " + TypeHolder)
                print("amount of type: " + AmountHolder)
                print("good status: " + StatusHolder)
                
                transactionIDcreator()
                
                TransactionNameBoxTo.place_forget()
                TransactionNameBoxFrom.place_forget()
                Transaction_combobox.place_forget()
                Transaction_inputbutton.place_forget()
                
                AddBranchEntryBox.place_forget()
                AddDateEntryBox.place_forget()
                AddGoodsEntryBox.place_forget()
                try:
                    inventorytypebox.place_forget()
                except Exception as e:
                    print("inventorytypebox does not exist")
                
                typebox.place_forget()
                amtinput.place_forget()
                try:
                    statusbox.place_forget()
                except Exception as e:
                    print("Already destroyed.")
                
                if ErrorBoolean==True:
                    Error.place_forget()
                    viewederror=0
                    ErrorBoolean = False
                    
            elif outputFlag == False and viewederror == 0 and not viewederror > 1:
                print("Please Input ALL entries.")
                ErrorBoolean = True
                Error = CTkLabel(OutputEditContent, text="Please Input ALL entries.", text_color="red", height=13)
                Error.place(x=200, y=3)
                viewederror = 1
            
            
        else: #prints an error
            if viewederror == 0 and not viewederror > 1:
                print("Please Input ALL entries.")
                ErrorBoolean = True
                Error = CTkLabel(OutputEditContent, text="Please Input ALL entries correctly.", text_color="red", height=13)
                Error.place(x=200, y=3)
                viewederror = 1
    else: #prints an error
        if viewederror == 0 and not viewederror > 1:
            print("Please Input ALL entries.")
            ErrorBoolean = True
            Error = CTkLabel(OutputEditContent, text="Please Input ALL entries correctly.", text_color="red", height=13)
            Error.place(x=200, y=3)
            viewederror = 1

def handleedittrans():
    global ErrorBoolean, Error, viewederror, amountedit
    global Trans_DateFlag, Trans_GoodsFlag, Trans_TypeFlag, Trans_BranchFlag, Trans_IDFlag, Trans_PartyFlag
    global sucessful_transaction, Transaction_inputbutton, TrueInventoryIDFlag

    outputFlag = False
    
    # Validate transaction ID first
    if TransactionIDEdit.get():
        Trans_IDFlag = True
        TransIDHolder = TransactionIDEdit.get()
        
        # Check if transaction exists
        cur.execute("""
            SELECT * FROM transactionTable WHERE transactionId = %(TransID)s
        """, {'TransID': TransIDHolder})
        
        if cur.fetchone():
            outputFlag = True
        else:
            if viewederror == 0:
                ErrorBoolean = True
                Error = CTkLabel(OutputEditContent, text="Transaction ID not found", text_color="red", height=13)
                Error.place(x=200, y=3)
                viewederror = 1
                return

    # Validate inputs based on what's being edited
    if diffvalue == 3: # Type validation
        if AmountHolder.isnumeric() and Trans_TypeFlag:
            amountedit = True
        else:
            show_error("Invalid amount")
            return

    if Trans_GoodsFlag and Trans_TypeFlag:
        TrueInventoryIDFlag = True

    if PartyForHolder and PartyToHolder:
        Trans_PartyFlag = True

    # Execute update if we have valid transaction ID and at least one valid field to update
    if outputFlag and Trans_IDFlag and (Trans_DateFlag or TrueInventoryIDFlag or Trans_BranchFlag or Trans_PartyFlag):
        try:
            # Update transaction table
            if Trans_DateFlag:
                cur.execute("""
                    UPDATE transactionTable 
                    SET transactionDate = %(date)s
                    WHERE transactionId = %(TransID)s
                """, {'date': DateHolder, 'TransID': TransIDHolder})

            if Trans_PartyFlag:
                cur.execute("""
                    UPDATE transactionTable
                    SET transactorFrom = %(from)s, transactionTo = %(to)s
                    WHERE transactionId = %(TransID)s
                """, {'from': PartyForHolder, 'to': PartyToHolder, 'TransID': TransIDHolder})

            # Update inventory if type or goods changed
            if TrueInventoryIDFlag:
                cur.execute("""
                    UPDATE Inventory
                    SET InventoryName = %(name)s,
                        InventoryValue = %(value)s,
                        InventoryType = %(type)s,
                        GoodsStatus = %(status)s
                    WHERE InventoryId = (
                        SELECT InventoryId 
                        FROM transactionTable 
                        WHERE transactionId = %(TransID)s
                    )
                """, {
                    'name': GoodsIDHolder,
                    'value': AmountHolder,
                    'type': TypeHolder,
                    'status': StatusHolder,
                    'TransID': TransIDHolder
                })

            if Trans_BranchFlag:
                cur.execute("""
                    UPDATE Inventory
                    SET BranchId = %(branch)s
                    WHERE InventoryId = (
                        SELECT InventoryId 
                        FROM transactionTable 
                        WHERE transactionId = %(TransID)s
                    )
                """, {'branch': BranchHolder, 'TransID': TransIDHolder})

            conn.commit()
            clear_edit_ui()
            show_success_message()

        except Exception as e:
            conn.rollback()
            show_error(f"Database error: {str(e)}")
            return
    else:
        show_error("Please input the correct entries")

def show_error(message):
    global ErrorBoolean, Error, viewederror
    if viewederror == 0:
        ErrorBoolean = True
        Error = CTkLabel(OutputEditContent, text=message, text_color="red", height=13)
        Error.place(x=200, y=3)
        viewederror = 1

def show_success_message():
    global ErrorBoolean, Error, viewederror
    if ErrorBoolean:
        Error.destroy()
        viewederror = 0
        ErrorBoolean = False
    print("Successfully updated transaction")

def clear_edit_ui():
    # Clear all edit UI elements
    try:
        TransactionIDEdit.place_forget()
        Transaction_combobox.destroy()
        Transaction_inputbutton.destroy()
        
        if diffvalue > 0:
            if diffvalue == 1:
                EditDateEntryBox.place_forget()
            elif diffvalue == 2:
                EditGoodsEntryBox.place_forget()
                inventorytypebox.place_forget() 
            elif diffvalue == 3:
                typebox.place_forget()
                amtinputEdit.place_forget()
                statusbox.place_forget()
            elif diffvalue == 4:
                EditBranchEntryBox.place_forget()
            elif diffvalue == 5:
                PartyToEntryBox.place_forget()
                PartyForEntryBox.place_forget()
            EditSearchBoxEnter.place_forget()
    except Exception as e:
        print(f"Error clearing UI: {e}")


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
    ID = [] #trans id
    ITID=[] #inv typ id
    RID = [] #inventory generator

    idCharLimit = 5 #Transaction ID generator
    while idCharLimit >=0: 
        I= get_random_integer(0, 9)
        RandInt = str(I)
        idCharLimit =idCharLimit-1
        ID.append(RandInt)
    TransIDHolder = ''.join(ID)
    print(int(TransIDHolder))

    idCharLimit3 = 5
    while idCharLimit3 >=0: #transtype ID generator
        I= get_random_integer(0, 9)
        RandInt = str(I)
        idCharLimit3 =idCharLimit3-1
        ITID.append(RandInt)
    TransTypeIDHolder = ''.join(ITID)
    print(int(TransTypeIDHolder))


    idCharLimit2=5
    while idCharLimit2 >=0: #Goods ID generator
        N= get_random_integer(0, 9)
        idCharLimit2 =idCharLimit2-1
        RandInt = str(N)
        RID.append(RandInt)
    GoodsIDHolder = ''.join(RID)
    print(int(GoodsIDHolder))
    transactionsql(mode, cur, TransIDHolder,TransTypeIDHolder, PartyForHolder, PartyToHolder, GoodsIDHolder, 
                   GoodsHolder, AmountHolder, InvTypHolder, BranchHolder, StatusHolder)
        

    
def transactionsql(mode, cur, TransIDHolder,TransTypeIDHolder, PartyForHolder, PartyToHolder, GoodsIDHolder, 
                   GoodsHolder, AmountHolder, InvTypHolder, BranchHolder, StatusHolder):
    global TransactorFromHolder, TransactorToHolder
    try:
        if mode == "add":
            
            cur.execute("""
                INSERT INTO transactionTable (transactionId, transactorFrom, transactionTo, transactionDate, transactionType, transactionTypeID) 
                VALUES (%(TransID)s, %(From)s, %(To)s, %(transactionDate)s, %(Typ)s, %(TransTypID)s)
            """, {'TransID': TransIDHolder, 'From': TransactorFromHolder, 'To': TransactorToHolder, 'transactionDate': DateHolder,'Typ':TypeHolder, 'TransTypID': GoodsIDHolder}) #UPDATE TRANSACTION TABLE
            
            if TypeHolder == "Item":    #IF THE TRANSACTION CONTAINS AN ITEM, THEN:
                cur.execute("""
                INSERT INTO Inventory (InventoryId, InventoryName, InventoryValue, InventoryType, BranchId, GoodsStatus) 
                VALUES (%(InvID)s, %(InvName)s, %(Value)s, %(InvTyp)s, %(BranchId)s, %(Status)s)
                """, {'InvID': GoodsIDHolder, 'InvName': GoodsHolder, 'Value': AmountHolder, 
                  'InvTyp': InvTypHolder, 'BranchId': BranchHolder, 'Status': StatusHolder}) #INVENTORY-
                
                cur.execute("""
                    INSERT INTO transactionType (transactionTypeId, balanceID, InventoryId)
                    VALUES (%(transTypeId)s, 0, %(InvID)s)""", {"transTypeId":TransTypeIDHolder,"InvID":GoodsIDHolder}) #TRANSACTION TYPE--
                

            elif TypeHolder == "Cash":     #ELE IF IT CONTAINS CASH< THEN:
                cur.execute("""
                    INSERT INTO balance (balanceid, balanceamount, dateofchange, transactionId) 
                    VALUES (%(GoodsIDHolder)s, %(Amt)s, %(dateofchange)s, %(BranchID)s)
                """, {'GoodsIDHolder': GoodsIDHolder,  'Amt': AmountHolder, 'dateofchange': DateHolder, 'BranchID': BranchHolder})
                
                cur.execute("""
                    INSERT INTO transactionType (transactionTypeId, balanceID, InventoryId)
                    VALUES (%(transTypeId)s,   %(BalID)s), 0""", {"transTypeId":TransTypeIDHolder,"BalID":GoodsIDHolder}) #TRANSACTION TYPE--
        
            
            
                
            conn.commit()
            print("EXECUTED")
        elif mode == "edit":
            print("Edit functionality not yet implemented.")
            # Add edit functionality here
        elif mode == "delete":
            cur.execute("""SELECT InventoryId FROM transactionTable""")
            InvID = cur.fetchone()
            cur.execute("""
                DELETE transactionTable, Inventory
                FROM transactionTable
                INNER JOIN Inventory
                ON transactionTable.InventoryId = Inventory.InventoryId
                WHERE transactionTable.transactionId = %(TransID)s""", {'TransID': TransIDHolder})
            
            cur.execute("""
               DELETE Inventory
                FROM Inventory
                INNER JOIN transactionTable
                ON transactionTable.InventoryId = Inventory.InventoryId
                WHERE transactionTable.transactionId = %(TransID)s;
                        """, {'TransID': TransIDHolder})
            
            conn.commit
            
            

    except Exception as e:
        print(f"An error occurred: {e}")





# Function to handle button clicks
def button_event(page):
    salespage(page)
SalesTab = CTkButton(TABFRAME, text="Sales", width=20)
SalesTab.grid(row=0, column=1, pady=10, padx=10, sticky="nsew")
SalesTab.configure(command=lambda: button_event(TransactionsPage))
# Show the first page by default
show_page(TransactionsPage)    
window.mainloop()


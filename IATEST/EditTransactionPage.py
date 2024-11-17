from customtkinter import *
from CTkTable import *

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
    global TransactionsPagePost, OutputEditContent
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
        OutputEditContent = CTkFrame(OutputPadding, width=410, height=115, fg_color="#FFFFFF", corner_radius=0, border_color='#000000', border_width=1)
        OutputEditContent.grid(row = 0, column = 0)
        LabelTransactionAdd = CTkLabel(OutputEditContent, text="TRANSACTIONS",font = EditFont)
        LabelTransactionAdd.place(x=5, y=1)
        

        OutputTableContent = CTkFrame(OutputPadding, width=410, height=215, fg_color="#a6a6a6", corner_radius=0, border_color='#000000', border_width=1)
        OutputTableContent.grid(row = 1, column = 0) 
        OutputEditContent.grid_propagate(0)
        
        
        OutputTableScrollbarContent = CTkFrame(OutputTableContent, width=410, height=215)
        OutputTableScrollbarContent.pack(fill="both", expand=True)
        
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
        
        #SearchRequestContentItemsg
        
        SearchLabel = CTkLabel(SearchRequestContent, text="TRANSACTIONS", font=EditFont)
        SearchLabel.grid(row=0, column=0, padx = 10, pady = 0,)
        
        SearchEntry = CTkEntry(SearchRequestContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="Search")
        SearchEntry.grid(row=1, column=0, padx = 10, pady = 4,)
        
        SearchButton = CTkButton(SearchRequestContent, text="Search", fg_color='#0053A0', corner_radius=0, text_color='#FFFFFF', border_color='#000000', border_width=1, hover_color='#0051ff')
        SearchButton.grid(row=2,column=0, padx = 10, pady = 1,)

        comboVal = StringVar(value="Select")
        SearchComboChoices = CTkComboBox(SearchRequestContent, values=["Items", "Cash", "Date"], command=callback, variable=comboVal, corner_radius=1)
        SearchComboChoices.set("Select")
        SearchComboChoices.grid(row = 3, column=0, padx=10,pady=2)
        SearchComboChoices.configure(state="readonly")
        TransactionsPagePost=1
    else:
        print("printed!")

viewedqueue = []
vieweditemflag = False


A_vieweditemflag = 0
E_vieweditemflag = 0
D_vieweditemflag = 0

currentmode = ""

TransAddExist = False
TransEditExist = False
TransDeleteExist = False

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
    global TransAddExist, TransEditExist, TransDeleteExist, TransactionNameBoxFrom, TransactionNameBoxTo, TransactionIDEdit, Transaction_inputbutton, TransactionIDDelete, Transaction_combobox

    # Destroy Add mode widgets if they exist
    if TransAddExist:
        TransactionNameBoxFrom.destroy()
        TransactionNameBoxTo.destroy()
        Transaction_combobox.destroy()
        TransAddExist = False

    # Destroy Edit mode widgets if they exist
    if TransEditExist:
        TransactionIDEdit.destroy()
        Transaction_combobox.destroy()
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
    
    global TransAddExist, TransactionNameBoxFrom, TransactionNameBoxTo, Transaction_inputbutton, Transaction_combobox
    DateHolder=""
    GoodsHolder=""
    BranchHolder=""
    TypeHolder="Item"
    AmountHolder = ""
    PartyToHolder=""
    PartyForHolder=""
        
    #All Flags
    Trans_DateFlag=False
    Trans_GoodsFlag=False
    Trans_TypeFlag=False
    Trans_BranchFlag=False
    # Create Add-specific widgets
    TransactionNameBoxFrom = CTkEntry(OutputEditContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="Transaction From", width=190, height=25)
    TransactionNameBoxFrom.place(x=5, y=25)

    TransactionNameBoxTo = CTkEntry(OutputEditContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="Transaction To", width=190, height=25)
    TransactionNameBoxTo.place(x=205, y=25)

    comboVal = StringVar(value="Select")
    Transaction_combobox = CTkComboBox(OutputEditContent, values=["Date", "Inventory ID", "Type", "Branch ID"], command=callback, variable=comboVal, height = 25, corner_radius=1, width=110)
    Transaction_combobox.set("Select")
    Transaction_combobox.place(x=5, y = 53)
    Transaction_combobox.configure(state="readonly")
    
    Transaction_inputbutton = CTkButton(OutputEditContent, text="Add", corner_radius=0, font=BTNFont, text_color='#000000', fg_color='#FFFFFF', border_color='#000000', border_width=1,hover_color='#e6e6e6', width=100, height=27,command=handleaddtrans())
    Transaction_inputbutton.place(x=295, y=82)
    

    TransAddExist = True  # Mark Add mode as active

def editmodeui():
    
    vieweditemflag = 1
    global TransEditExist, TransactionIDEdit, Transaction_combobox, Transaction_inputbutton
    DateHolder=""
    GoodsHolder=""
    BranchHolder=""
    TypeHolder="Item"
    AmountHolder = ""
    PartyToHolder=""
    PartyForHolder=""
        
    #All Flags
    Trans_DateFlag=False
    Trans_GoodsFlag=False
    Trans_TypeFlag=False
    Trans_BranchFlag=False
    # Create Edit-specific widgets
    TransactionIDEdit = CTkEntry(OutputEditContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="Transaction ID", width=390, height=25)
    TransactionIDEdit.place(x=5, y=25)

    comboVal = StringVar(value="Select")
    Transaction_combobox = CTkComboBox(OutputEditContent, values=["Date", "Inventory ID", "Type", "Branch ID"], command=callback, variable=comboVal, height = 25, corner_radius=1, width=110)
    Transaction_combobox.set("Select")
    Transaction_combobox.place(x=5, y = 53)
    Transaction_combobox.configure(state="readonly")

    Transaction_inputbutton = CTkButton(OutputEditContent, text="Edit", corner_radius=0, font=BTNFont, text_color='#000000', fg_color='#FFFFFF', border_color='#000000', border_width=1, hover_color='#e6e6e6', width=100, height=27, command=handleedittrans())
    Transaction_inputbutton.place(x=295, y=82)
    


    TransEditExist = True  # Mark Edit mode as active

def deletemodeui():
    global TransactionIDDelete, Transaction_inputbutton, TransDeleteExist
    TransactionIDDelete = CTkEntry(OutputEditContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="enter Transaction ID to delete", width=390, height = 25)
    TransactionIDDelete.place(x=5,y=25)

    Transaction_inputbutton = CTkButton(OutputEditContent, text = "Delete", command = lambda: DeleteTheItems(TransactionIDDelete, Transaction_inputbutton), corner_radius=0,font=BTNFont, text_color='#000000', fg_color='#FFFFFF', border_color='#000000', border_width=1, hover_color='#e6e6e6', width=100, height = 27)
    Transaction_inputbutton.place (x=295, y = 82)
    TransDeleteExist = True


            
            

def DeleteTheItems(TransactionIDDelete, deleteinputbutton):
    global deletebuttonrequestchecker
    ItemToDelete = TransactionIDDelete.get()
    if ItemToDelete != "":
        print("Item is deleted. Transaction =" + str(ItemToDelete))
        clearcurrentmode()
        
    else:
        print("Please enter correct field properly.")
        



        
        
        

def handleaddtrans():
    print("y")
def handleedittrans():
    print("y")
def callback():
    print("y")





























# Function to handle button clicks
def button_event(page):
    salespage(page)
SalesTab = CTkButton(TABFRAME, text="Sales", width=20)
SalesTab.grid(row=0, column=1, pady=10, padx=10, sticky="nsew")
SalesTab.configure(command=lambda: button_event(TransactionsPage))
# Show the first page by default
show_page(TransactionsPage)    
window.mainloop()


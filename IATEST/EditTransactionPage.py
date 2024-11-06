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
    global TransactionsPagePost, OutputEditContent, addbuttonrequestchecker, editbuttonrequestchecker, deletebuttonrequestchecker
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
        AddButtonRequest = CTkButton(EditsRequestContent, text="ADD",corner_radius=0, command=lambda: outputContentGivenButtons(OutputEditContent, OutputTableContent, 1),font=BTNFont, text_color='#000000', fg_color='#FFFFFF', border_color='#000000', border_width=1, hover_color='#e6e6e6')
        AddButtonRequest.grid(row=1,column=0,padx = 10, pady = 4, sticky='nsew')
        
        EditButtonRequest = CTkButton(EditsRequestContent, text="EDIT",corner_radius=0, command=lambda: outputContentGivenButtons(OutputEditContent, OutputTableContent, 2), font=BTNFont, fg_color='#FFFFFF', text_color='#000000', border_color='#000000', border_width=1, hover_color='#e6e6e6')
        EditButtonRequest.grid(row=2,column=0,padx = 10, pady = 1, sticky='nsew')
        
        DeleteButtonRequest = CTkButton(EditsRequestContent, text="DELETE",  corner_radius=0,command=lambda: outputContentGivenButtons(OutputEditContent, OutputTableContent, 3), font=BTNFont, fg_color='#FFFFFF', text_color='#000000', border_color='#000000', border_width=1, hover_color='#e6e6e6')
        DeleteButtonRequest.grid(row=3,column=0,padx = 10, pady = 2, sticky='nsew')
        
        #SearchRequestContentItemsg
        
        SearchLabel = CTkLabel(SearchRequestContent, text="TRANSACTIONS", font=EditFont)
        SearchLabel.grid(row=0, column=0, padx = 10, pady = 0,)
        
        SearchEntry = CTkEntry(SearchRequestContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="Search")
        SearchEntry.grid(row=1, column=0, padx = 10, pady = 4,)
        
        SearchButton = CTkButton(SearchRequestContent, text="Search", fg_color='#0053A0', corner_radius=0, text_color='#FFFFFF', border_color='#000000', border_width=1, hover_color='#0051ff')
        SearchButton.grid(row=2,column=0, padx = 10, pady = 1,)

        comboVal = StringVar(value="Select")
        
        TransactionsPagePost=1
    else:
        print("printed!")
    
    addbuttonrequestchecker = False
    editbuttonrequestchecker = False
    deletebuttonrequestchecker = False
    
   
def outputContentGivenButtons(OutputEditContent, OutputTableContent, value): 
    global addbuttonrequestchecker, editbuttonrequestchecker, deletebuttonrequestchecker
    if value == 1:
        addbuttonrequestchecker = not addbuttonrequestchecker
        editbuttonrequestchecker = False
        deletebuttonrequestchecker = False
    elif value == 2:
        editbuttonrequestchecker=not editbuttonrequestchecker
        addbuttonrequestchecker = False
        deletebuttonrequestchecker = False
        
    elif value == 3:
        deletebuttonrequestchecker = not deletebuttonrequestchecker 
        editbuttonrequestchecker = False
        addbuttonrequestchecker = False

    searchAddButtonFunction(OutputEditContent)
    searchEditButtonFunction(OutputEditContent,OutputTableContent)
    searchDeleteButtonFunction(OutputEditContent,OutputTableContent)

#EDIT FUNCTION==================================================================================
def searchEditButtonFunction(OutputEditContent,OutputTableContent):
    print("WOW!")
    global diffvalue,EditSearchBoxEnter, PartyForHolder, PartyToHolder, amountedit, enteronceforcombo, comboboxedit, editinputbutton, EditDateFlag, EditGoodsFlag, EditTypeFlag, EditBranchFlag, TransactorFrom, TransactionIDEdit, DateHolder, GoodsHolder, BranchHolder, TypeHolder, TypeChecker, amountholder, typewaschecked, TransactionNameIDFlag, enteronce

    if editbuttonrequestchecker == True: #checks if the button request is true
        TypeChecker = True #whether item or cash
        typewaschecked = False #checks whether or not type in combo box was checked or not

        enteronce = 0
        diffvalue = 0 #to findout which combo is working orn ot
        enteronceforcombo = 0 

        TransactionNameIDFlag = False
        EditDateFlag=False
        EditGoodsFlag=False
        EditTypeFlag=False
        amountedit=False
        EditBranchFlag=False   
        
        
        TransactorFrom = ""
        DateHolder=""
        GoodsHolder=""
        BranchHolder=""
        TypeHolder="Item"
        amountholder = ""
        
        PartyToHolder=""
        PartyForHolder=""
        
        
        TransactionIDEdit = CTkEntry(OutputEditContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="Transaction ID", width=390, height = 25)
        TransactionIDEdit.place(x=5,y=25)
        
        comboVal = StringVar(value="Select")
        comboboxedit = CTkComboBox(OutputEditContent, values=["Date", "Inventory ID", "Type", "Branch ID", "Parties"], command=callbackedit, variable=comboVal, height = 25, corner_radius=1, width=110)
        comboboxedit.set("Select")
        comboboxedit.place(x=5, y = 53)
        comboboxedit.configure(state="readonly")

        editinputbutton = CTkButton(OutputEditContent, text = "Add", command = lambda: EdittingTheItems(), corner_radius=0,font=BTNFont, text_color='#000000', fg_color='#FFFFFF', border_color='#000000', border_width=1, hover_color='#e6e6e6', width=100, height = 27)
        editinputbutton.place (x=295, y = 82)

    elif editbuttonrequestchecker == False:
        TransactionIDEdit.destroy()
        comboboxedit.destroy()
        editinputbutton.destroy()
        if diffvalue == 1:
            EditDateEntryBox.destroy()
            EditSearchBoxEnter.destroy()
        elif diffvalue == 2:
            EditGoodsEntryBox.destroy()
            EditSearchBoxEnter.destroy()
        elif diffvalue == 3:
            typebox.destroy()
            amtinputEdit.destroy()
            EditSearchBoxEnter.destroy()
        elif diffvalue == 4:
            EditBranchEntryBox.destroy()
            EditSearchBoxEnter.destroy()
        elif diffvalue == 5:
            PartyToEntryBox.destroy()
            PartyForEntryBox.destroy()
            EditSearchBoxEnter.destroy()



def callbackedit(choice): #COMBO BOX FUNCTIONALITIES
    global diffvalue, PartyForEntryBox, PartyToEntryBox, enteronceforcombo, EditDateEntryBox, EditGoodsEntryBox, EditBranchEntryBox,typebox, amtinputEdit, DateHolder, GoodsHolder, BranchHolder, TypeHolder, amountholder, PartyForHolder, PartyToHolder,  EditSearchBoxEnter, typewaschecked, enteronce
    
    enteronce = enteronce + 1
    enteronceforcombo = enteronceforcombo + 1
    
    print (enteronce)
    if enteronce > 1:
        EditSearchBoxEnter.destroy()
        enteronce = 1
        print (enteronce)
        
    
    if enteronce == 1:
        EditSearchBoxEnter = CTkButton(OutputEditContent, text = "Confirm", corner_radius=0,font=BTNFont, text_color='#000000', fg_color='#FFFFFF', border_color='#000000', border_width=1, hover_color='#e6e6e6', width=100, height = 27, command=lambda: confirmyourchoiceForEdit(choice, EditSearchBoxEnter))
        EditSearchBoxEnter.place(x=190,y=82)

    if enteronceforcombo>1:
        if diffvalue == 1:
            EditDateEntryBox.destroy()
        elif diffvalue == 2:
            EditGoodsEntryBox.destroy()
        elif diffvalue == 3:
            typebox.destroy()
            amtinputEdit.destroy()
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
            EditGoodsEntryBox.insert(0,GoodsHolder)
            
            
        elif choice == "Type": #for TYPE
            diffvalue = 3
            typewaschecked = True
            comboVal = StringVar(value="Item")
            typebox = CTkComboBox(OutputEditContent, values=["Item", "Cash"], command=boolfortypecheck, variable=comboVal, height = 25, corner_radius=1, width=275)
            typebox.place(x=120, y = 53)
            
            amtinputEdit = CTkEntry(OutputEditContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="Enter Amount", width=120, height = 27)
            amtinputEdit.place(x=5, y = 82)
            amtinputEdit.insert(0, amountholder)

            typebox.set(TypeHolder)
            typebox.configure(state="readonly")
            
        elif choice == "Branch ID": #certain BRANCH
            diffvalue = 4
            EditBranchEntryBox = CTkEntry(OutputEditContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="Branch Id", width=275, height = 25)
            EditBranchEntryBox.place(x=120, y = 53)
            EditBranchEntryBox.insert(0,BranchHolder)
        elif choice == "Parties":
            diffvalue = 5
            PartyForEntryBox = CTkEntry(OutputEditContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="Transaction For", width=132, height = 25)
            PartyForEntryBox.place(x=120, y = 53)
            
            PartyToEntryBox = CTkEntry(OutputEditContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="Transaction To", width=132, height = 25)
            PartyToEntryBox.place(x=260, y = 53)
        
    if typewaschecked == True and choice != "Type":
        amtinputEdit.destroy()
        typewaschecked = False
    
        
    if BranchHolder or DateHolder or GoodsHolder or amountholder or PartyToHolder or PartyForHolder == "":
        if DateHolder ==""and diffvalue == 1:
            EditDateEntryBox.delete(0, END)
            EditDateEntryBox.configure(placeholder_text="Date of Transaction")
        elif GoodsHolder ==""and diffvalue == 2:
            EditGoodsEntryBox.delete(0, END)
            EditGoodsEntryBox.configure(placeholder_text="Inventory Id")
        elif TypeHolder == ""and diffvalue == 3:
            typebox.delete(0, END)
            amtinputEdit.delete(0, END)
            amtinputEdit.configure(placeholder_text="Enter Amount")
        elif BranchHolder == "" and diffvalue == 4:
            EditBranchEntryBox.delete(0, END)
            EditBranchEntryBox.configure(placeholder_text="Branch Id")
        elif PartyToHolder == ""and diffvalue == 5:
            PartyToEntryBox.delete(0, END)
            PartyToEntryBox.configure(placeholder_text="Transaction To")
        elif PartyForHolder == ""and diffvalue == 5:
            PartyForEntryBox.delete(0, END)
            PartyForEntryBox.configure(placeholder_text="Transaction From")
    else:
        if BranchHolder != "" and diffvalue==4:
            EditBranchEntryBox.insert(0,BranchHolder)
        elif DateHolder !="" and diffvalue ==1:
            EditDateEntryBox.insert(0,DateHolder)
        elif GoodsHolder !=""and diffvalue == 2:
            EditGoodsEntryBox.insert(0, GoodsHolder)
        elif TypeHolder != "" and diffvalue==3:
            typebox.insert(0, TypeHolder)
            amtinputEdit.insert(0, amountholder)
        elif PartyToHolder != "" and diffvalue == 5:
            PartyToEntryBox.insert(0,PartyToHolder)
        elif PartyForHolder != "" and diffvalue == 5:
            PartyForEntryBox.insert(0,PartyForHolder)
        
    
    print ("diffvalue: " + str(diffvalue))
    
        
    
    
def confirmyourchoiceForEdit(choice, EditSearchBoxEnter): #CONFIRMS THE CHOICE

    global PartyForHolder, PartyToHolder, DateHolder, GoodsHolder, BranchHolder, TypeChecker, TypeHolder, EditDateFlag, EditGoodsFlag, EditBranchFlag, EditTypeFlag, amountholder
    EditSearchBoxEnter.destroy()
    if choice == "Date" and EditDateEntryBox.get() != "":
        DateHolder = EditDateEntryBox.get()
        print (DateHolder)
        EditDateFlag = True
        EditDateEntryBox.configure(state="readonly")
        
    elif choice == "Inventory ID" and EditGoodsEntryBox.get() != "":
        GoodsHolder = EditGoodsEntryBox.get()
        print (GoodsHolder)
        EditGoodsFlag = True
        EditGoodsEntryBox.configure(state="readonly")
        
    elif choice == "Branch ID" and EditBranchEntryBox.get() != "":
        BranchHolder = EditBranchEntryBox.get()
        print (BranchHolder)
        EditBranchFlag = True
        EditBranchEntryBox.configure(state="readonly")

    elif choice == "Type" and TypeHolder != "":
        if TypeChecker == True:
            TypeHolder = "Item"
        else:
            TypeHolder = "Cash"
        print (TypeHolder)
        EditTypeFlag = True
        amountholder = amtinputEdit.get()
        amtinputEdit.configure(state="readonly")
    elif choice == "Parties" and (PartyToEntryBox and PartyForEntryBox != ""):
        PartyForHolder = PartyForEntryBox.get()
        PartyToHolder = PartyToEntryBox.get()


def EdittingTheItems():
    global addbuttonrequestchecker, amountedit
    TransactorFrom = TransactionIDEdit.get()
    ErrorBoolean=False

    if TransactorFrom != "": #if the transactor to and transactor from is NOT empty, then it'll post as true.
        TransactionNameIDFlag = True
    
    if amountholder.isnumeric() and EditTypeFlag == True:
        amountedit = True

    print ("Date= " + str(EditDateFlag) + ", Inventory= " + str(EditGoodsFlag) + ", Type= " + str(EditTypeFlag) + ", Branch= " + str(EditBranchFlag)) 
    if (EditDateFlag or EditGoodsFlag or EditTypeFlag or EditBranchFlag or amountedit== True) and  TransactionNameIDFlag == True: #CHECKS IF ALL ARE TRUE AND CORRECTLY INPUTTED!!
        print("Sucessfully Submitted.")
        print("TransactionID : " + TransactorFrom)
        print("Date: " + DateHolder)
        print("Goods: " + GoodsHolder)
        print("Branch ID: " + BranchHolder) 
        print("Type: " + TypeHolder)
        print("amount of type: " + amountholder)
        
        TransactionIDEdit.destroy()
        comboboxedit.destroy()
        editinputbutton.destroy()
        
        if diffvalue == 1:
            EditDateEntryBox.destroy()
        elif diffvalue == 2:
            EditGoodsEntryBox.destroy()
        elif diffvalue == 3:
            typebox.destroy()
            amtinputEdit.destroy()
        elif diffvalue == 4:
            EditBranchEntryBox.destroy()
        elif diffvalue == 5:
            PartyToEntryBox.destroy()
            PartyForEntryBox.destroy()

        if ErrorBoolean==True:
            Error.destroy()
        addbuttonrequestchecker = False
        
    else: #prints an error
        print("Please Input an entry.")
        ErrorBoolean = True
        Error = CTkLabel(OutputEditContent, text="Please Input an entry.", text_color="red", height=13)
        Error.place(x=200, y=3)



#ADD FUNCTION =======================================================================
def searchAddButtonFunction(OutputEditContent):
        if addbuttonrequestchecker == True:
            print("but")
        else:
            print("and")
    

         
#DELETE FUNCTION==================================================================================
def searchDeleteButtonFunction(OutputEditContent,OutputTableContent):
        if deletebuttonrequestchecker == True:
            print("gay...")
        else:
            print("him!")

















#++++++++++++++++++++++++++++++ {TAB FUNCTIONS} ++++++++++++++++++++++++++++++++++++++


# Function to handle button clicks
def button_event(page):
    salespage(page)






SalesTab = CTkButton(TABFRAME, text="Sales", width=20)
SalesTab.grid(row=0, column=1, pady=10, padx=10, sticky="nsew")


SalesTab.configure(command=lambda: button_event(TransactionsPage))


# Show the first page by default
show_page(TransactionsPage)


window.mainloop()


#am cooked

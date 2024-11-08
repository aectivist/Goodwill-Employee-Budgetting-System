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
        SearchComboChoices = CTkComboBox(SearchRequestContent, values=["Items", "Cash", "Date"], command=callback, variable=comboVal, corner_radius=1)
        SearchComboChoices.set("Select")
        SearchComboChoices.grid(row = 3, column=0, padx=10,pady=2)
        SearchComboChoices.configure(state="readonly")
        TransactionsPagePost=1
    else:
        print("printed!")
    
    
    
vieweditemaddflag = 0
vieweditemeditflag = 0
vieweditemdeleteflag = 0

viewederror = 0
viewederroredit = 0

ErrorBoolean = False
ErrorBooleanEdit = False

addbuttonrequestchecker = False
editbuttonrequestchecker = False
deletebuttonrequestchecker = False

pastpostforoutput = ""
currentpostforoutput = ""
   
def outputContentGivenButtons(OutputEditContent, OutputTableContent, value): 
    
    global addbuttonrequestchecker, editbuttonrequestchecker, deletebuttonrequestchecker
    global vieweditemaddflag , vieweditemeditflag, vieweditemdeleteflag, pastpostforoutput, currentpostforoutput
    pastpostforoutput = currentpostforoutput
    if value == 1:#Add
        vieweditemaddflag = vieweditemaddflag+1
        addbuttonrequestchecker = not addbuttonrequestchecker
        editbuttonrequestchecker = False
        deletebuttonrequestchecker = False
        searchAddButtonFunction(OutputEditContent, value)
        currentpostforoutput = "ADD"
    elif value == 2: #Edit
        vieweditemeditflag = vieweditemeditflag+1
        editbuttonrequestchecker=not editbuttonrequestchecker
        addbuttonrequestchecker = False
        deletebuttonrequestchecker = False
        searchEditButtonFunction(OutputEditContent,value)
        currentpostforoutput = "EDIT"
    elif value == 3: #Delete
        vieweditemdeleteflag = vieweditemdeleteflag+1
        deletebuttonrequestchecker = not deletebuttonrequestchecker
        editbuttonrequestchecker = False
        addbuttonrequestchecker = False
        searchDeleteButtonFunction(OutputEditContent, value)
        currentpostforoutput = "DELETE"
    print ("ACTIVE:")
    print("edit checker: " + str(editbuttonrequestchecker))
    print("add checker: " + str(addbuttonrequestchecker))
    print("delete checker: " + str(deletebuttonrequestchecker))
    print("value: " + str(value))
    
    
    
def TrueDeleter(value):
    global vieweditemeditflag,ErrorBooleanEdit,ErrorEdit,viewederroredit,vieweditemaddflag, ErrorBoolean, Error , viewederror ,deleteinputbutton,vieweditemdeleteflag
    global pastpostforoutput
    #deletes edit
    
    
    if pastpostforoutput == "EDIT" and (vieweditemaddflag >= 1 or vieweditemdeleteflag >=1):
        vieweditemeditflag =0
        if TransactionIDEdit.winfo_exists():
            TransactionIDEdit.destroy()
        if comboboxedit.winfo_exists():
            comboboxedit.destroy()
        if editinputbutton.winfo_exists():
            editinputbutton.destroy()
        if editdiffvalue == 1:
            EditDateEntryBox.destroy()
            EditSearchBoxEnter.destroy()
        elif editdiffvalue == 2:
            print(str(diffvalue) + " is set")
            EditGoodsEntryBox.destroy()
            EditSearchBoxEnter.destroy()
        elif editdiffvalue == 3:
            typebox.destroy()
            amtinputEdit.destroy()
            EditSearchBoxEnter.destroy()
        elif editdiffvalue == 4:
            EditBranchEntryBox.destroy()
            EditSearchBoxEnter.destroy()
        elif editdiffvalue == 5:
            PartyToEntryBox.destroy()
            PartyForEntryBox.destroy()
            EditSearchBoxEnter.destroy()
        if ErrorBooleanEdit==True or viewederroredit >0:
                ErrorEdit.destroy()
                viewederroredit = 0
                print("error is destroyed" + str(viewederroredit))
    #deletes add 
   
    if pastpostforoutput == "ADD" and (vieweditemeditflag >= 1 or vieweditemdeleteflag >=1):
        vieweditemaddflag = 0
        if TransactionNameBoxFromAdd.winfo_exists():
            TransactionNameBoxFromAdd.destroy()
        if TransactionNameBoxTo.winfo_exists():
            TransactionNameBoxTo.destroy()
        if combobox.winfo_exists():
            combobox.destroy()
        if addinputbutton.winfo_exists():
            addinputbutton.destroy()
        if diffvalue == 1:
            AddDateEntryBox.destroy()
            AddSearchBoxEnter.destroy()
        elif diffvalue == 2:
            AddGoodsEntryBox.destroy()
            AddSearchBoxEnter.destroy()
        elif diffvalue == 3:
            typebox.destroy()
            amtinput.destroy()
            AddSearchBoxEnter.destroy()
        elif diffvalue == 4:
            AddBranchEntryBox.destroy()
            AddSearchBoxEnter.destroy()
        if ErrorBoolean==True or viewederror >0:
            print (viewederror)
            Error.destroy()
            print("error is destroyed" + str(viewederror))
            viewederror = viewederror - 1
            ErrorBoolean = False
    #deletes delete 
    
    if pastpostforoutput == "DELETE" and (vieweditemaddflag >=1 or vieweditemeditflag >=1):
        print("viewed the delete, deleting delete. :" + str(vieweditemdeleteflag))
        vieweditemdeleteflag = 0
        if TransactionIDDelete.winfo_exists():
            TransactionIDDelete.destroy()
            deleteinputbutton.destroy()
        
                
                

#ADD FUNCTION =======================================================================
def searchAddButtonFunction(OutputEditContent, valuereader):
        global diffvalue,AddSearchBoxEnter, vieweditemaddflag, enteronceforcombo, combobox, addinputbutton, InputDateFlag, InputGoodsFlag, InputTypeFlag, InputBranchFlag, TransactorFrom, TransactorTo, TransactionNameBoxFromAdd, TransactionNameBoxTo, DateHolder, GoodsHolder, BranchHolder, TypeHolder, TypeChecker, amountholder, typewaschecked, TransactionNameForFlag, TransactionNameToFlag, enteronce
        print('viewed item add: ' + str(vieweditemaddflag))
        if addbuttonrequestchecker == True and vieweditemaddflag == 1:
            TypeChecker = True #whether item or cash
            typewaschecked = False #checks whether or not type in combo box was checked or not

            enteronce = 0
            diffvalue = 0 #to findout which combo is working orn ot
            enteronceforcombo = 0 

            TransactionNameForFlag = False
            TransactionNameToFlag = False
            InputDateFlag=False
            InputGoodsFlag=False
            InputTypeFlag=False
            InputBranchFlag=False   

            TransactorFrom = ""
            TransactorTo = ""
            DateHolder=""
            GoodsHolder=""
            BranchHolder=""
            TypeHolder="Item"
            amountholder = ""
            
            
            TransactionNameBoxFromAdd = CTkEntry(OutputEditContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="Transaction From", width=190, height = 25)
            TransactionNameBoxFromAdd.place(x=5,y=25)

            TransactionNameBoxTo = CTkEntry(OutputEditContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="Transaction To", width=190, height = 25)
            TransactionNameBoxTo.place(x=205,y=25)
            
            comboVal = StringVar(value="Select")
            combobox = CTkComboBox(OutputEditContent, values=["Date", "Inventory ID", "Type", "Branch ID"], command=callback, variable=comboVal, height = 25, corner_radius=1, width=110)
            combobox.set("Select")
            combobox.place(x=5, y = 53)
            combobox.configure(state="readonly")

            addinputbutton = CTkButton(OutputEditContent, text = "Add", command = lambda: AddingTheItems(), corner_radius=0,font=BTNFont, text_color='#000000', fg_color='#FFFFFF', border_color='#000000', border_width=1, hover_color='#e6e6e6', width=100, height = 27)
            addinputbutton.place (x=295, y = 82)
        elif vieweditemaddflag > 1 or (vieweditemeditflag >= 1 or vieweditemdeleteflag >=1):
            vieweditemaddflag = 0
            if TransactionNameBoxFromAdd.winfo_exists():
                TransactionNameBoxFromAdd.destroy()
            if TransactionNameBoxTo.winfo_exists():
                TransactionNameBoxTo.destroy()
            if combobox.winfo_exists():
                combobox.destroy()
            if addinputbutton.winfo_exists():
                addinputbutton.destroy()
            if diffvalue == 1:
                AddDateEntryBox.destroy()
                AddSearchBoxEnter.destroy()
            elif diffvalue == 2:
                AddGoodsEntryBox.destroy()
                AddSearchBoxEnter.destroy()
            elif diffvalue == 3:
                typebox.destroy()
                amtinput.destroy()
                AddSearchBoxEnter.destroy()
            elif diffvalue == 4:
                AddBranchEntryBox.destroy()
                AddSearchBoxEnter.destroy()
            if ErrorBoolean==True or viewederror >0:
                print (viewederror)
                Error.destroy()
                print("error is destroyed" + str(viewederror))
                viewederror = viewederror - 1
                ErrorBoolean = False
        else:
            TrueDeleter(valuereader)  


def callback(choice): #COMBO BOX FUNCTIONALITIES
    global diffvalue, enteronceforcombo, AddDateEntryBox, AddGoodsEntryBox, AddBranchEntryBox,typebox, amtinput, DateHolder, GoodsHolder, BranchHolder, TypeHolder, amountholder, AddSearchBoxEnter, typewaschecked, enteronce, ErrorBoolean, Error
    
    enteronce = enteronce + 1
    enteronceforcombo = enteronceforcombo + 1
    
    print (enteronce)
    if enteronce > 1:
        AddSearchBoxEnter.destroy()
        enteronce = 1
        print (enteronce)
        

    if enteronce == 1:
        AddSearchBoxEnter = CTkButton(OutputEditContent, text = "Confirm", corner_radius=0,font=BTNFont, text_color='#000000', fg_color='#FFFFFF', border_color='#000000', border_width=1, hover_color='#e6e6e6', width=100, height = 27, command=lambda: confirmyourchoice(choice, AddSearchBoxEnter))
        AddSearchBoxEnter.place(x=190,y=82)

    if enteronceforcombo>1:
        if diffvalue == 1:
            AddDateEntryBox.destroy()
        elif diffvalue == 2:
            AddGoodsEntryBox.destroy()
        elif diffvalue == 3:
            typebox.destroy()
            amtinput.destroy()
        elif diffvalue == 4:
            AddBranchEntryBox.destroy()

        enteronceforcombo = 1
        print (enteronceforcombo)

    if enteronceforcombo == 1:
        if choice == "Date": #For DATE
            diffvalue = 1
            AddDateEntryBox = CTkEntry(OutputEditContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="Date of Transaction", width=275, height = 25)
            AddDateEntryBox.place(x=120, y = 53)
            AddDateEntryBox.configure(state="normal")
            AddDateEntryBox.insert(0,DateHolder)
            
            
        elif choice == "Inventory ID": #for Inventory
            diffvalue = 2
            AddGoodsEntryBox = CTkEntry(OutputEditContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="Inventory Id", width=275, height = 25)
            AddGoodsEntryBox.place(x=120, y = 53)
            AddGoodsEntryBox.configure(state="normal")
            AddGoodsEntryBox.insert(0,GoodsHolder)
            
            
        elif choice == "Type": #for TYPE
            diffvalue = 3
            typewaschecked = True
            comboVal = StringVar(value="Item")
            typebox = CTkComboBox(OutputEditContent, values=["Item", "Cash"], command=boolfortypecheck, variable=comboVal, height = 25, corner_radius=1, width=275)
            typebox.place(x=120, y = 53)
            
            amtinput = CTkEntry(OutputEditContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="Enter Amount", width=120, height = 27)
            amtinput.place(x=5, y = 82)
            amtinput.insert(0, amountholder)

            typebox.set(TypeHolder)
            typebox.configure(state="readonly")
            
        elif choice == "Branch ID": #certain BRANCH
            diffvalue = 4
            AddBranchEntryBox = CTkEntry(OutputEditContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="Branch Id", width=275, height = 25)
            AddBranchEntryBox.place(x=120, y = 53)
            AddBranchEntryBox.insert(0,BranchHolder)

    if typewaschecked == True and choice != "Type":
        amtinput.destroy()
        typewaschecked = False
    
    print ("diffvalue: " + str(diffvalue))
     
    if BranchHolder == "" or DateHolder == "" or GoodsHolder == "" or amountholder == "":
        if DateHolder ==""and diffvalue == 1:
            AddDateEntryBox.delete(0, END)
            AddDateEntryBox.configure(placeholder_text="Date of Transaction")
        elif GoodsHolder ==""and diffvalue == 2:
            AddGoodsEntryBox.delete(0, END)
            AddGoodsEntryBox.configure(placeholder_text="Inventory Id")
        elif TypeHolder == ""and diffvalue == 3:
            typebox.delete(0, END)
            amtinput.delete(0, END)
            amtinput.configure(placeholder_text="Enter Amount")
        elif BranchHolder == "" and diffvalue == 4:
            AddBranchEntryBox.delete(0, END)
            AddBranchEntryBox.configure(placeholder_text="Branch Id")
        
    else:
        if BranchHolder != "" and diffvalue==4:
            AddBranchEntryBox.insert(0,BranchHolder)
        elif DateHolder !="" and diffvalue ==1:
            AddDateEntryBox.insert(0,DateHolder)
        elif GoodsHolder !=""and diffvalue == 2:
            AddGoodsEntryBox.insert(0, GoodsHolder)
        elif TypeHolder != "" and diffvalue==3:
            typebox.insert(0, TypeHolder)
            amtinput.insert(0, amountholder)
        
    
    
def confirmyourchoice(choice, AddSearchBoxEnter): #CONFIRMS THE CHOICE

    global DateHolder, GoodsHolder, BranchHolder, TypeChecker, TypeHolder,InputDateFlag, InputGoodsFlag, InputBranchFlag, InputTypeFlag, typebox, amountholder
    AddSearchBoxEnter.destroy()
    if choice == "Date" and AddDateEntryBox.get() != "":
        DateHolder = AddDateEntryBox.get()
        print (DateHolder)
        InputDateFlag = True
        AddDateEntryBox.configure(state="readonly")
        
    elif choice == "Inventory ID" and AddGoodsEntryBox.get() != "":
        GoodsHolder = AddGoodsEntryBox.get()
        print (GoodsHolder)
        InputGoodsFlag = True
        AddGoodsEntryBox.configure(state="readonly")
        
    elif choice == "Branch ID" and AddBranchEntryBox.get() != "":
        BranchHolder = AddBranchEntryBox.get()
        print (BranchHolder)
        InputBranchFlag = True
        AddBranchEntryBox.configure(state="readonly")

    elif choice == "Type" and TypeHolder != "":
        if TypeChecker == True:
            TypeHolder = "Item"
        else:
            TypeHolder = "Cash"
        print (TypeHolder)
        InputTypeFlag = True
        amountholder = amtinput.get()
        amtinput.configure(state="readonly")
   

def AddingTheItems():
    global addbuttonrequestchecker, ErrorBoolean, Error, viewederror
    TransactorTo =  TransactionNameBoxTo.get()
    TransactorFrom = TransactionNameBoxFromAdd.get()

    if TransactorTo and TransactorFrom != "": #if the transactor to and transactor from is NOT empty, then it'll post as true.
        TransactionNameForFlag = True
        TransactionNameToFlag = True
    print ("Name= " + str(InputDateFlag) + ", Goods= " + str(InputGoodsFlag) + ", Type= " + str(InputTypeFlag) + ", Branch= " + str(InputBranchFlag)) 
    if (InputDateFlag == True and InputGoodsFlag== True and InputTypeFlag == True and InputBranchFlag == True and 
    TransactionNameToFlag == True and TransactionNameForFlag == True and amountholder.isnumeric()): #CHECKS IF ALL ARE TRUE AND CORRECTLY INPUTTED!!
        print("Sucessfully Submitted.")
        print("Transactor From: " + TransactorFrom)
        print("Transactor To: " + TransactorTo)
        print("Date: " + DateHolder)
        print("Goods: " + GoodsHolder)
        print("Branch ID: " + BranchHolder) 
        print("Type: " + TypeHolder)
        print("amount of type: " + amountholder)
        
        TransactionNameBoxTo.destroy()
        TransactionNameBoxFromAdd.destroy()
        combobox.destroy()
        addinputbutton.destroy()
        
        AddBranchEntryBox.destroy()
        AddDateEntryBox.destroy()
        AddGoodsEntryBox.destroy()
        typebox.destroy()
        amtinput.destroy()
 
        if ErrorBoolean==True:
            Error.destroy()
            viewederror=0
            ErrorBoolean = False
            

    else: #prints an error
        if viewederror == 0 and not viewederror > 1:
            print("Please Input ALL entries.")
            ErrorBoolean = True
            Error = CTkLabel(OutputEditContent, text="Please Input ALL entries correctly.", text_color="red", height=13)
            Error.place(x=200, y=3)
            viewederror = 1

        

    
    
#EDIT FUNCTION==================================================================================
def searchEditButtonFunction(OutputEditContent,valuereader):
    global ErrorBooleanEdit, ErrorEdit, editdiffvalue, vieweditemeditflag, editbuttonrequestchecker, EditSearchBoxEnter, PartyForHolder, PartyToHolder, amountedit, enteronceforcombo, comboboxedit, editinputbutton, EditDateFlag, EditGoodsFlag, EditTypeFlag, EditBranchFlag, TransactorFrom, TransactionIDEdit, DateHolder, GoodsHolder, BranchHolder, TypeHolder, TypeChecker, amountholder, typewaschecked, TransactionNameIDFlag, enteronce, ErrorBooleanEdit, ErrorEdit
    print ('viewed edit: '+ str(vieweditemeditflag))
    if editbuttonrequestchecker == True and vieweditemeditflag == 1: #checks if the button request is true
        TypeChecker = True #whether item or cash
        typewaschecked = False #checks whether or not type in combo box was checked or not

        enteronce = 0
        editdiffvalue = 0 #to findout which combo is working orn ot
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

        editinputbutton = CTkButton(OutputEditContent, text = "Edit", command = lambda: EdittingTheItems(), corner_radius=0,font=BTNFont, text_color='#000000', fg_color='#FFFFFF', border_color='#000000', border_width=1, hover_color='#e6e6e6', width=100, height = 27)
        editinputbutton.place (x=295, y = 82)
    elif vieweditemeditflag > 1 or (vieweditemaddflag >= 1 or vieweditemdeleteflag >=1):
        vieweditemeditflag =0
        if TransactionIDEdit.winfo_exists():
            TransactionIDEdit.destroy()
        if comboboxedit.winfo_exists():
            comboboxedit.destroy()
        if editinputbutton.winfo_exists():
            editinputbutton.destroy()
        if editdiffvalue == 1:
            EditDateEntryBox.destroy()
            EditSearchBoxEnter.destroy()
        elif editdiffvalue == 2:
            print(str(diffvalue) + " is set")
            EditGoodsEntryBox.destroy()
            EditSearchBoxEnter.destroy()
        elif editdiffvalue == 3:
            typebox.destroy()
            amtinputEdit.destroy()
            EditSearchBoxEnter.destroy()
        elif editdiffvalue == 4:
            EditBranchEntryBox.destroy()
            EditSearchBoxEnter.destroy()
        elif editdiffvalue == 5:
            PartyToEntryBox.destroy()
            PartyForEntryBox.destroy()
            EditSearchBoxEnter.destroy()
        if ErrorBooleanEdit==True or viewederroredit >0:
                ErrorEdit.destroy()
                viewederroredit = 0
                print("error is destroyed" + str(viewederroredit))
    else:
        TrueDeleter(valuereader)

                    



def callbackedit(choice): #COMBO BOX FUNCTIONALITIES
    global editdiffvalue, PartyForEntryBox, PartyToEntryBox, enteronceforcombo, EditDateEntryBox, EditGoodsEntryBox, EditBranchEntryBox,typebox, amtinputEdit, DateHolder, GoodsHolder, BranchHolder, TypeHolder, amountholder, PartyForHolder, PartyToHolder,  EditSearchBoxEnter, typewaschecked, enteronce
    
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
        if editdiffvalue == 1:
            EditDateEntryBox.destroy()
        elif editdiffvalue == 2:
            EditGoodsEntryBox.destroy()
        elif editdiffvalue == 3:
            typebox.destroy()
            amtinputEdit.destroy()
        elif editdiffvalue == 4:
            EditBranchEntryBox.destroy()
        elif editdiffvalue == 5:
            PartyToEntryBox.destroy()
            PartyForEntryBox.destroy()

        enteronceforcombo = 1
        print (enteronceforcombo)

    if enteronceforcombo == 1:
        if choice == "Date": #For DATE
            editdiffvalue = 1
            EditDateEntryBox = CTkEntry(OutputEditContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="Date of Transaction", width=275, height = 25)
            EditDateEntryBox.place(x=120, y = 53)
            EditDateEntryBox.configure(state="normal")
            EditDateEntryBox.insert(0,DateHolder)
            
            
        elif choice == "Inventory ID": #for GOODS
            editdiffvalue = 2
            EditGoodsEntryBox = CTkEntry(OutputEditContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="Inventory Id", width=275, height = 25)
            EditGoodsEntryBox.place(x=120, y = 53)
            EditGoodsEntryBox.configure(state="normal")
            EditGoodsEntryBox.insert(0,GoodsHolder)
            
            
        elif choice == "Type": #for TYPE
            editdiffvalue = 3
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
            editdiffvalue = 4
            EditBranchEntryBox = CTkEntry(OutputEditContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="Branch Id", width=275, height = 25)
            EditBranchEntryBox.place(x=120, y = 53)
            EditBranchEntryBox.insert(0,BranchHolder)
        elif choice == "Parties":
            editdiffvalue = 5
            PartyForEntryBox = CTkEntry(OutputEditContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="Transaction For", width=132, height = 25)
            PartyForEntryBox.place(x=120, y = 53)
            
            PartyToEntryBox = CTkEntry(OutputEditContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="Transaction To", width=132, height = 25)
            PartyToEntryBox.place(x=260, y = 53)
        
    if typewaschecked == True and choice != "Type":
        amtinputEdit.destroy()
        typewaschecked = False
    
        
    if BranchHolder == "" or DateHolder == "" or GoodsHolder == "" or amountholder == "" or PartyForHolder == "" or PartyToHolder == "":
        if DateHolder ==""and editdiffvalue == 1:
            EditDateEntryBox.delete(0, END)
            EditDateEntryBox.configure(placeholder_text="Date of Transaction")
        elif GoodsHolder ==""and editdiffvalue == 2:
            EditGoodsEntryBox.delete(0, END)
            EditGoodsEntryBox.configure(placeholder_text="Inventory Id")
        elif TypeHolder == ""and editdiffvalue == 3:
            typebox.delete(0, END)
            amtinputEdit.delete(0, END)
            amtinputEdit.configure(placeholder_text="Enter Amount")
        elif BranchHolder == "" and editdiffvalue == 4:
            EditBranchEntryBox.delete(0, END)
            EditBranchEntryBox.configure(placeholder_text="Branch Id")
        elif PartyToHolder == ""and editdiffvalue == 5:
            PartyToEntryBox.delete(0, END)
            PartyToEntryBox.configure(placeholder_text="Transaction To")
        elif PartyForHolder == ""and editdiffvalue == 5:
            PartyForEntryBox.delete(0, END)
            PartyForEntryBox.configure(placeholder_text="Transaction From")
    else:
        if BranchHolder != "" and editdiffvalue==4:
            EditBranchEntryBox.insert(0,BranchHolder)
        elif DateHolder !="" and editdiffvalue ==1:
            EditDateEntryBox.insert(0,DateHolder)
        elif GoodsHolder !=""and editdiffvalue == 2:
            EditGoodsEntryBox.insert(0, GoodsHolder)
        elif TypeHolder != "" and editdiffvalue==3:
            typebox.insert(0, TypeHolder)
            amtinputEdit.insert(0, amountholder)
        elif PartyToHolder != "" and editdiffvalue == 5:
            PartyToEntryBox.insert(0,PartyToHolder)
        elif PartyForHolder != "" and editdiffvalue == 5:
            PartyForEntryBox.insert(0,PartyForHolder)
        
    
    print ("diffvalue: " + str(editdiffvalue))
    
        
    
    
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
    global editbuttonrequestchecker, amountedit, ErrorBooleanEdit, ErrorEdit, viewederroredit
    TransactorFrom = TransactionIDEdit.get()

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
        
        if editdiffvalue == 1:
            EditDateEntryBox.destroy()
        elif editdiffvalue == 2:
            EditGoodsEntryBox.destroy()
        elif editdiffvalue == 3:
            typebox.destroy()
            amtinputEdit.destroy()
        elif editdiffvalue == 4:
            EditBranchEntryBox.destroy()
        elif editdiffvalue == 5:
            PartyToEntryBox.destroy()
            PartyForEntryBox.destroy()

        if ErrorBooleanEdit==True:
            ErrorEdit.destroy()
            viewederroredit=0
            ErrorBooleanEdit = False
        
        
    else: #prints an error
        if viewederroredit == 0 and not viewederroredit > 1:
            print("Please Input an entry.")
            ErrorBooleanEdit = True
            ErrorEdit = CTkLabel(OutputEditContent, text="Please Input an entry.", text_color="red", height=13)
            ErrorEdit.place(x=200, y=3)
            viewederroredit = viewederroredit + 1
            print(viewederroredit)
         
#DELETE FUNCTION==================================================================================
def searchDeleteButtonFunction(OutputEditContent,valuereader):
        global deleteinputbutton, TransactionIDDelete, vieweditemdeleteflag, deleteinputbutton,editbuttonrequestchecker
        print('viewed delete: ' + str(vieweditemdeleteflag))
        if deletebuttonrequestchecker == True and vieweditemdeleteflag == 1:
            TransactionIDDelete = CTkEntry(OutputEditContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="enter Transaction ID to delete", width=390, height = 25)
            TransactionIDDelete.place(x=5,y=25)
        
            deleteinputbutton = CTkButton(OutputEditContent, text = "Delete", command = lambda: DeleteTheItems(TransactionIDDelete, deleteinputbutton), corner_radius=0,font=BTNFont, text_color='#000000', fg_color='#FFFFFF', border_color='#000000', border_width=1, hover_color='#e6e6e6', width=100, height = 27)
            deleteinputbutton.place (x=295, y = 82)
        elif vieweditemdeleteflag > 1 or (vieweditemeditflag >= 1 or vieweditemaddflag >=1):
            print("viewed the delete, deleting delete. :" + str(vieweditemdeleteflag))
            vieweditemdeleteflag = 0
            if TransactionIDDelete.winfo_exists():
                TransactionIDDelete.destroy()
                deleteinputbutton.destroy()
        else:
            TrueDeleter(valuereader)
            
            

def DeleteTheItems(TransactionIDDelete, deleteinputbutton):
    global deletebuttonrequestchecker
    ItemToDelete = TransactionIDDelete.get()
    if ItemToDelete != "":
        print("Item is deleted. Transaction =" + str(ItemToDelete))
        TransactionIDDelete.destroy()
        deleteinputbutton.destroy()
        editbuttonrequestchecker = False
        
    else:
        print("Please enter correct field properly.")
        





#FOR BOOLEAN
def boolfortypecheck(choice):
    global TypeChecker, InputTypeFlag
    if choice == "Item":
        TypeChecker=True
        print("Item")
    elif choice == "Cash":
        TypeChecker=False
        print("Cash")










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

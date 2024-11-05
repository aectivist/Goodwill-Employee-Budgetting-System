from customtkinter import *
import psycopg2
from CTkTable import *
#https://github.com/Akascape/CTkTable


conn=psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="12345", port=5432)




cur = conn.cursor()
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
TransactionsPagePost = 0
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
        

        OutputTableContent = CTkFrame(OutputPadding, width=410, height=215, fg_color="#a6a6a6", corner_radius=0, border_color='#000000', border_width=1)
        OutputTableContent.grid(row = 1, column = 0) 
        OutputEditContent.grid_propagate(0)
        
        
        #Okay for the redundant code part: **only for the table "thats supposed to have meaning"
        OutputTableScrollbarContent = CTkFrame(OutputTableContent, width=410, height=215)
        OutputTableScrollbarContent.pack(fill="both", expand=True)
        
        canvas = CTkCanvas(OutputTableScrollbarContent, width=410, height=215, highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)
        
        scrollbar = CTkScrollableFrame(canvas, width =387)
        scrollbar.grid(rowspan=100, row = 0, column = 0, sticky='nsew')

        EditLabelRequest = CTkLabel(EditsRequestContent, text="EDITS", font=EditFont)
        EditLabelRequest.grid(row=0, column=0, )
        
        AddButtonRequest = CTkButton(EditsRequestContent, text="ADD",corner_radius=0, command=lambda: outputContentGivenButtons(OutputEditContent, OutputTableContent, 1),font=BTNFont, text_color='#000000', fg_color='#FFFFFF', border_color='#000000', border_width=1, hover_color='#e6e6e6')
        AddButtonRequest.grid(row=1,column=0,padx = 10, pady = 5, sticky='nsew')
        
        EditButtonRequest = CTkButton(EditsRequestContent, text="EDIT",corner_radius=0, command=lambda: outputContentGivenButtons(OutputEditContent, OutputTableContent, 2), font=BTNFont, fg_color='#FFFFFF', text_color='#000000', border_color='#000000', border_width=1, hover_color='#e6e6e6')
        EditButtonRequest.grid(row=2,column=0,padx = 10, pady = 5, sticky='nsew')
        
        DeleteButtonRequest = CTkButton(EditsRequestContent, text="DELETE",  corner_radius=0,command=lambda: outputContentGivenButtons(OutputEditContent, OutputTableContent, 3), font=BTNFont, fg_color='#FFFFFF', text_color='#000000', border_color='#000000', border_width=1, hover_color='#e6e6e6')
        DeleteButtonRequest.grid(row=3,column=0,padx = 10, pady = 5, sticky='nsew')
        
        #SearchRequestContentItemsg
        
        SearchLabel = CTkLabel(SearchRequestContent, text="TRANSACTIONS", font=EditFont)
        SearchLabel.grid(row=0, column=0, padx = 10, pady = 5,)
        
        SearchEntry = CTkEntry(SearchRequestContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="Search")
        SearchEntry.grid(row=1, column=0, padx = 10, pady = 5,)
        
        SearchButton = CTkButton(SearchRequestContent, text="Search", fg_color='#0053A0', corner_radius=0, text_color='#FFFFFF', border_color='#000000', border_width=1, hover_color='#0051ff')
        SearchButton.grid(row=2,column=0, padx = 10, pady = 5,)
        TransactionsPagePost=1
    else:
        print("printed!")
        


SearchAddButton = False
SearchEditButton = False
SearchDeleteButton = False
   
def outputContentGivenButtons(OutputEditContent, OutputTableContent, value): 
    global SearchAddBoolean, SearchEditBoolean, SearchDeleteBoolean
    if value == 1:
        SearchAddBoolean = True
        SearchEditBoolean = False
        SearchDeleteBoolean = False
        searchAddButtonFunction(OutputEditContent,OutputTableContent)
    elif value == 2:
        SearchAddBoolean = False
        SearchEditBoolean = True
        SearchDeleteBoolean = False
        searchEditButtonFunction(OutputEditContent,OutputTableContent)
    elif value == 3:
        SearchAddBoolean = False
        SearchEditBoolean = False
        SearchDeleteBoolean = True
        searchDeleteButtonFunction(OutputEditContent,OutputTableContent)

def searchAddButtonFunction(OutputEditContent,OutputTableContent):
        print("WOW!")
        global InputNameFlag, InputGoodsFlag, InputTypeFlag, InputBranchFlag, NameHolder, GoodsHolder, BranchHolder, TypeHolder, TypeChecker

        TypeChecker = True
        InputNameFlag=False
        InputGoodsFlag=False
        InputTypeFlag=False
        InputBranchFlag=False
        NameHolder=str() 
        GoodsHolder=str()
        BranchHolder=str()
        TypeHolder="Item"
        
        LabelTransactionAdd = CTkLabel(OutputEditContent, text="TRANSACTIONS",font = EditFont)
        LabelTransactionAdd.place(x=5, y=1)
        
        SearchButtonAdd = CTkEntry(OutputEditContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="Transaction ID", width=390, height = 25)
        SearchButtonAdd.place(x=5,y=25)
        
        comboVal = StringVar(value="Select")
        combobox = CTkComboBox(OutputEditContent, values=["Name", "Goods", "Type", "Branch"], command=callback, variable=comboVal, height = 25, corner_radius=1, width=110)
        combobox.set("Select")
        combobox.place(x=5, y = 53)
        combobox.configure(state="readonly")

        AddButton = CTkButton(OutputEditContent, text = "Add", command = lambda: AddingTheItems(), corner_radius=0,font=BTNFont, text_color='#000000', fg_color='#FFFFFF', border_color='#000000', border_width=1, hover_color='#e6e6e6', width=100, height = 27)
        AddButton.place (x=295, y = 82)
        
        
        
def searchEditButtonFunction(OutputEditContent,OutputTableContent):
        print("YOU'RE!")
         
def searchDeleteButtonFunction(OutputEditContent,OutputTableContent):
        print("FEIN!")
   
def callback(choice): #COMBO BOX FUNCTIONALITIES
    global AddNameSearchBox, AddGoodsSearchBox, AddBranchSearchBox,typebox, NameHolder, GoodsHolder, BranchHolder, TypeHolder
    
    
    if choice == "Name": #When Name is clicked in combo box
        AddNameSearchBox = CTkEntry(OutputEditContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="Transactor Name", width=275, height = 25)
        AddNameSearchBox.place(x=120, y = 53)
        AddNameSearchBox.insert(0,NameHolder)
        
        
    elif choice == "Goods":
        AddGoodsSearchBox = CTkEntry(OutputEditContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="Transaction Goods", width=275, height = 25)
        AddGoodsSearchBox.place(x=120, y = 53)
        AddGoodsSearchBox.insert(0,GoodsHolder)
        
    elif choice == "Type":
        comboVal = StringVar(value="Item")
        typebox = CTkComboBox(OutputEditContent, values=["Item", "Cash"], command=boolfortypecheck, variable=comboVal, height = 25, corner_radius=1, width=275)
        typebox.place(x=120, y = 53)
        typebox.set(TypeHolder)
        typebox.configure(state="readonly")
        
    elif choice == "Branch":
        AddBranchSearchBox = CTkEntry(OutputEditContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="Existing Branch", width=275, height = 25)
        AddBranchSearchBox.place(x=120, y = 53)
        AddBranchSearchBox.insert(0,BranchHolder)
        
    AddSearchBoxEnter = CTkButton(OutputEditContent, text = "Confirm", corner_radius=0,font=BTNFont, text_color='#000000', fg_color='#FFFFFF', border_color='#000000', border_width=1, hover_color='#e6e6e6', width=100, height = 27, command=lambda: confirmyourchoice(choice, AddSearchBoxEnter))
    AddSearchBoxEnter.place(x=190,y=82)
    
def confirmyourchoice(choice, AddSearchBoxEnter): #CONFIRMS THE CHOICE
    global Item, Cash, NameHolder, GoodsHolder, BranchHolder, TypeChecker, TypeHolder, InputNameFlag, InputGoodsFlag, InputBranchFlag, InputTypeFlag, typebox
    if choice == "Name" and AddNameSearchBox.get() != "":
        NameHolder = AddNameSearchBox.get()
        print (NameHolder)
        InputNameFlag = True
        AddSearchBoxEnter.destroy()
        
    elif choice == "Goods" and AddGoodsSearchBox.get() != "":
        GoodsHolder = AddGoodsSearchBox.get()
        print (GoodsHolder)
        InputGoodsFlag = True
        AddSearchBoxEnter.destroy()
        
    elif choice == "Branch" and AddBranchSearchBox.get() != "":
        BranchHolder = AddBranchSearchBox.get()
        print (BranchHolder)
        InputBranchFlag = True
        AddSearchBoxEnter.destroy()
    elif choice == "Type" and TypeHolder != "":
        if TypeChecker == True:
            TypeHolder = "Item"
        else:
            TypeHolder = "Cash"
        print (TypeHolder)
        InputTypeFlag = True
        AddSearchBoxEnter.destroy()
            
def boolfortypecheck(choice):
    global TypeChecker, InputTypeFlag
    if choice == "Item":
        TypeChecker=True
        print("Item")
    elif choice == "Cash":
        TypeChecker=False
        print("Cash")

def AddingTheItems():
    global InputNameFlag, InputGoodsFlag, InputTypeFlag, InputBranchFlag, NameHolder, GoodsHolder, BranchHolder, TypeHolder
    print ("Name= " + str(InputNameFlag) + ", Goods= " + str(InputGoodsFlag) + ", Type= " + str(InputTypeFlag) + ", Branch= " + str(InputBranchFlag))
    if InputNameFlag and InputGoodsFlag and InputTypeFlag and InputBranchFlag == True:
        print("Sucessfully Submitted.")
        print("Name: " + NameHolder)
        print("Goods: " + GoodsHolder)
        print("Branch: " + BranchHolder) 
        print("Type: " + TypeHolder)
        
        
            
        















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

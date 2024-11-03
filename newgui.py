from customtkinter import *
from pywinstyles import *
import psycopg2
import threading
from CTkTable import *
#https://github.com/Akascape/CTkTable

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
SalesPage = CTkFrame(window, corner_radius=0)
ClientPage = CTkFrame(window, corner_radius=0)
AssetPage = CTkFrame(window, corner_radius=0)
CalculatorPage = CTkFrame(window, corner_radius=0)
LoginPage = CTkFrame(window, corner_radius=0, bg_color='#0053A0')
LoadingPage = CTkFrame(window, corner_radius=0) #implement later

# Create a list to hold all the pages
pages = [HomePage, SalesPage, ClientPage, AssetPage, CalculatorPage]

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
    elif page == SalesPage:
        print(page)
        LoginPage.pack_forget()
        salespage(SalesPage)
        

         
#++++++++++++++++++++++++++++++ {PAGE FUNCTIONS} ++++++++++++++++++++++++++++++++++++++
#DO NOT EDIT SPACE, WILL USE SPACE FOR THE OTHER PAGES


#def clientpage(page):
#def assetpage(page):
#def calculator(page):

TitleFont = CTkFont(family="Oswald", size=15, weight='bold')
EditFont = CTkFont(family="Oswald", size=15, weight='bold')
BTNFont = CTkFont(family="Oswald", size=13)
SalesPagePost = 0
def salespage(page): #TO BE UPDATED
    global SalesPagePost
    if SalesPagePost==0:
        
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
        
        AddButtonRequest = CTkButton(EditsRequestContent, text="ADD",corner_radius=0, font=BTNFont, text_color='#000000', fg_color='#FFFFFF', border_color='#000000', border_width=1, hover_color='#e6e6e6')
        AddButtonRequest.grid(row=1,column=0,padx = 10, pady = 5, sticky='nsew')
        
        EditButtonRequest = CTkButton(EditsRequestContent, text="EDIT",corner_radius=0, font=BTNFont, fg_color='#FFFFFF', text_color='#000000', border_color='#000000', border_width=1, hover_color='#e6e6e6')
        EditButtonRequest.grid(row=2,column=0,padx = 10, pady = 5, sticky='nsew')
        
        DeleteButtonRequest = CTkButton(EditsRequestContent, text="DELETE",  corner_radius=0, font=BTNFont, fg_color='#FFFFFF', text_color='#000000', border_color='#000000', border_width=1, hover_color='#e6e6e6')
        DeleteButtonRequest.grid(row=3,column=0,padx = 10, pady = 5, sticky='nsew')
        
        #SearchRequestContentItemsg
        
        SearchLabel = CTkLabel(SearchRequestContent, text="SALES", font=EditFont)
        SearchLabel.grid(row=0, column=0, padx = 10, pady = 5,)
        
        SearchEntry = CTkEntry(SearchRequestContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="Search")
        SearchEntry.grid(row=1, column=0, padx = 10, pady = 5,)
        
        SearchButton = CTkButton(SearchRequestContent, text="Search", fg_color='#0053A0', corner_radius=0, text_color='#FFFFFF', border_color='#000000', border_width=1, hover_color='#0051ff')
        SearchButton.grid(row=2,column=0, padx = 10, pady = 5,)
        SalesPagePost=1
    else:
        print("printed!")
        
        
        

SearchAddButton = False
SearchEditButton = False
SearchDeleteButton = False
    
def outputContentGivenButtons():   
    print("Hello world!")
    



    


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



def editselect(NoteBoxPadding,EditTextBox, button_id, AddedNotesScrollbar): #ASK ABOUT THE EDITTING BUG BRO PLS
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
for i in range(5):
    TABFRAME.grid_columnconfigure(i, weight=1, uniform="col")
    TABFRAME.grid_rowconfigure(0, minsize=51)

# buttons
HomeTab = CTkButton(TABFRAME, text="Home", width=20, corner_radius=0 , command=lambda: button_event(HomePage,loginaccess))
HomeTab.grid(row=0, column=0, pady=10, padx=6, sticky="nsew")

SalesTab = CTkButton(TABFRAME, text="Sales", width=20, corner_radius=0, command=lambda: button_event(LoginPage,loginaccess))
SalesTab.grid(row=0, column=1, pady=10, padx=6, sticky="nsew")

ClientTab = CTkButton(TABFRAME, text="Client/Donator", width=20, corner_radius=0, command=lambda: button_event(LoginPage,loginaccess))
ClientTab.grid(row=0, column=2, pady=10, padx=6, sticky="nsew")

AssetTab = CTkButton(TABFRAME, text="Assets", width=20, corner_radius=0, command=lambda: button_event(LoginPage,loginaccess))
AssetTab.grid(row=0, column=3, pady=10, padx=6, sticky="nsew")

Calculatortab = CTkButton(TABFRAME, text="Calculator", width=20, corner_radius=0, command=lambda: button_event(LoginPage,loginaccess))
Calculatortab.grid(row=0, column=4, pady=10, padx=6, sticky="nsew")

def admittedAccess(loginaccess):
    
    if loginaccess == True:
        destroyloginitems(LOGIN)
        loadedpage(LoginPage)
        SalesTab.configure(command=lambda: button_event(SalesPage,loginaccess))
        ClientTab.configure(command=lambda: button_event(ClientPage,loginaccess))
        AssetTab.configure(command=lambda: button_event(AssetPage,loginaccess))
        Calculatortab.configure(command=lambda: button_event(CalculatorPage,loginaccess))


# Show the first page by default
show_page(HomePage, loginaccess)

window.mainloop()

#am cooked

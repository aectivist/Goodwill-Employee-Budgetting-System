from customtkinter import *
from pywinstyles import *
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
SalesPage = CTkFrame(window)
SalesPage.pack(fill=BOTH, expand=True)




# Create a list to hold all the pages
pages = [SalesPage]


# Function to show a page
def show_page(page):
    page.pack(fill=BOTH, expand=True)
    window.update_idletasks()  # Update the UI
    if page == SalesPage:
        salespage(SalesPage)
       


         
#++++++++++++++++++++++++++++++ {PAGE FUNCTIONS} ++++++++++++++++++++++++++++++++++++++
#DO NOT EDIT SPACE, WILL USE SPACE FOR THE OTHER PAGES


#def clientpage(page):
#def assetpage(page):
#def calculator(page):




TitleFont = CTkFont(family="Oswald", size=15, weight='bold')
EditFont = CTkFont(family="Oswald", size=15, weight='bold')
BTNFont = CTkFont(family="Oswald", size=13)


def salespage(page):
        #START MASTER
        PageMargin = CTkFrame(page)
        PageMargin.pack(expand=True)
        RequestPadding = CTkFrame(PageMargin, width=215, height=299, fg_color="#dbdbdb", corner_radius=0, border_color='#000000', border_width=1)
        OutputPadding = CTkFrame(PageMargin, width=365, height=300, fg_color="#dbdbdb", corner_radius=0, border_color='#000000', border_width=1)
        RequestPadding.grid_propagate(0)
        OutputPadding.grid_propagate(0)
       
        RequestPadding.grid(row=0, column=0)
        OutputPadding.grid(row=0, column=1)


        #Requested Content
        SearchRequestContent = CTkFrame(RequestPadding, width=400, height=149, fg_color="#FFFFFF", corner_radius=0, border_color='#000000', border_width=1)
        SearchRequestContent.grid_propagate(0)
       
        EditsRequestContent = CTkFrame(RequestPadding, width=400, height=151, fg_color="#FFFFFF", corner_radius=0, border_color='#000000', border_width=1)
        EditsRequestContent.grid_propagate(0)
       
        SearchRequestContent.grid(row=0, column=0)
        EditsRequestContent.grid(row=1, column=0)
       
        #Fixes all Buttons
        for i in range(2):
            EditsRequestContent.grid_columnconfigure(i, weight=1, uniform="column")
            EditsRequestContent.grid_rowconfigure(0, minsize=51)
       
        for i in range(2):
            SearchRequestContent.grid_columnconfigure(i, weight=1, uniform="column")
            SearchRequestContent.grid_rowconfigure(0, minsize=51)
       
       


        #Output Content
        OutputEditContent = CTkFrame(OutputPadding, width=365, height=133, fg_color="#FFFFFF", corner_radius=0, border_color='#000000', border_width=1)
        OutputEditContent.grid_propagate(0)
        OutputTableContent = CTkFrame(OutputPadding, width=365, height=167, fg_color="#a6a6a6", corner_radius=0, border_color='#000000', border_width=1)
        OutputTableContent.grid_propagate(0)
        OutputEditContent.grid(row=0)
        OutputTableContent.grid(row=1)
        for i in range(2):
            OutputEditContent.grid_columnconfigure(i, weight=1, uniform="column")
            OutputEditContent.grid_rowconfigure(0, minsize=51)
       
        #EditRequestContentItems


        EditLabelRequest = CTkLabel(EditsRequestContent, text="EDITS", font=EditFont)
        EditLabelRequest.grid(row=0, column=0, sticky='nsew', pady = 4, padx=10)
       
        AddButtonRequest = CTkButton(EditsRequestContent, text="ADD", height=20, width=5,corner_radius=0, font=BTNFont, text_color='#000000', fg_color='#FFFFFF', border_color='#000000', border_width=1, hover_color='#e6e6e6')
        AddButtonRequest.grid(row=1,column=0, sticky='nsew', pady = 9, padx=20)
       
        EditButtonRequest = CTkButton(EditsRequestContent, text="EDIT", height=20, width=5,corner_radius=0, font=BTNFont, fg_color='#FFFFFF', text_color='#000000', border_color='#000000', border_width=1, hover_color='#e6e6e6')
        EditButtonRequest.grid(row=2,column=0, sticky='nsew', pady = 0, padx=20)
       
        DeleteButtonRequest = CTkButton(EditsRequestContent, text="DELETE", height=20, width=5, corner_radius=0, font=BTNFont, fg_color='#FFFFFF', text_color='#000000', border_color='#000000', border_width=1, hover_color='#e6e6e6')
        DeleteButtonRequest.grid(row=3,column=0, sticky='nsew', pady = 9, padx=20)
       
        #SearchRequestContentItems
       
        SearchLabel = CTkLabel(SearchRequestContent, text="CLIENT/DONATOR", font=EditFont)
        SearchLabel.grid(row=0, column=0, sticky='nsew', pady = 5, padx=10)
       
        SearchEntry = CTkEntry(SearchRequestContent, corner_radius=0, border_color='#000000', border_width=1, placeholder_text="Search")
        SearchEntry.grid(row=1, column=0, sticky='nsew', pady = 5, padx=10)
       
        SearchButton = CTkButton(SearchRequestContent, text="Search", fg_color='#0053A0', corner_radius=0, text_color='#FFFFFF', border_color='#000000', border_width=1, hover_color='#0051ff')
        SearchButton.grid(row=2,column=0, sticky='nsew', pady = 5, padx=20)
       
       
        #OutputScrollbar
       


SearchAddButton = False
SearchEditButton = False
SearchDeleteButton = False
   
def outputContentGivenButtons():  
    print("Hello world!")
   
















#++++++++++++++++++++++++++++++ {TAB FUNCTIONS} ++++++++++++++++++++++++++++++++++++++


# Function to handle button clicks
def button_event(page):
    salespage(page)






SalesTab = CTkButton(TABFRAME, text="Sales", width=20)
SalesTab.grid(row=0, column=1, pady=10, padx=10, sticky="nsew")


SalesTab.configure(command=lambda: button_event(SalesPage))


# Show the first page by default
show_page(SalesPage)


window.mainloop()


#am cooked

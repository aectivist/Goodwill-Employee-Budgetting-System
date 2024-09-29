from customtkinter import *
from pywinstyles import *
import psycopg2
from CTkTable import *
#https://github.com/Akascape/CTkTable
import math




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
    CalculatorMargin = CTkFrame(page)
    CalculatorMargin.pack(expand=True)
    #LEFT BAR
    FormulaSideBar = CTkFrame(CalculatorMargin, width=150, height=320, border_color="#000000", border_width=1)
    FormulaSideBar.grid(row=0,column=0)
    #RIGHT BAR
    CalculatorSide = CTkFrame(CalculatorMargin, width=410, height=320, border_color="#000000", border_width=1)
    CalculatorSide.grid(row=0,column=1)
    CalculatorSide.grid_propagate(0)    
    #RIGHT BAR UI
    OutputCalculations = CTkEntry(CalculatorSide, width=410, height=120, border_color="#000000", border_width=1)
    OutputCalculations.grid(row=0,column=0)

    ButtonsForCalculationsFrame = CTkFrame(CalculatorSide, width=410, height=200, border_color="#000000", border_width=1)
    ButtonsForCalculationsFrame.grid(row=1, column=0)
    for i in range(7):
        ButtonsForCalculationsFrame.grid_columnconfigure(i, weight=1, uniform="column")
        ButtonsForCalculationsFrame.grid_rowconfigure(0, minsize=51)
    ButtonCalculations(ButtonsForCalculationsFrame)

    #CALCULATOR BUTTONS


   













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

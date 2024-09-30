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




OutputCalculatorFont = CTkFont(family="Oswald", size=30, weight='bold')
EditFont = CTkFont(family="Oswald", size=15, weight='bold')


def salespage(page):
    #START MASTER
    CalculatorMargin = CTkFrame(page)
    CalculatorMargin.pack(expand=True)
    #LEFT BAR
    FormulaSideBar = CTkFrame(CalculatorMargin, width=150, height=320, border_color="#000000", border_width=1, fg_color="#FFFFFF")
    FormulaSideBar.grid(row=0,column=0)
    #RIGHT BAR
    CalculatorSide = CTkFrame(CalculatorMargin, width=410, height=320, border_color="#000000", border_width=1)
    CalculatorSide.grid(row=0,column=1)
    CalculatorSide.grid_propagate(0)    
    #RIGHT BAR UI
    OutputCalculations = CTkEntry(CalculatorSide ,font=OutputCalculatorFont, width=410, height=120, border_color="#000000", border_width=1)
    OutputCalculations.grid(row=0,column=0)
    OutputCalculations.configure(state="readonly")


    ButtonsForCalculationsFrame = CTkFrame(CalculatorSide, width=410, height=200, border_color="#000000", border_width=1)
    ButtonsForCalculationsFrame.grid(row=1, column=0)
    ButtonsForCalculationsFrame.grid_propagate(0)
    for i in range(6):
        ButtonsForCalculationsFrame.grid_columnconfigure(i, weight=1, uniform="column")
        ButtonsForCalculationsFrame.grid_rowconfigure(0, minsize=40)
    
    #Welcome to a programmer's worst nightmare LMFAOOOOO
    button1 = CTkButton(ButtonsForCalculationsFrame, text="Rad",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button1.grid(row=0, column=0)
    button2 = CTkButton(ButtonsForCalculationsFrame, text="Inv",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button2.grid(row=1, column=0)
    button3 = CTkButton(ButtonsForCalculationsFrame, text="π",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button3.grid(row=2, column=0)
    button4 = CTkButton(ButtonsForCalculationsFrame, text="e",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button4.grid(row=3, column=0)
    button5 = CTkButton(ButtonsForCalculationsFrame, text="Ans",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button5.grid(row=4, column=0)

    button6 = CTkButton(ButtonsForCalculationsFrame, text="Deg",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button6.grid(row=0, column=1)
    button7 = CTkButton(ButtonsForCalculationsFrame, text="sin",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button7.grid(row=1, column=1)
    button8 = CTkButton(ButtonsForCalculationsFrame, text="cos",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button8.grid(row=2, column=1)
    button9 = CTkButton(ButtonsForCalculationsFrame, text="tan",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button9.grid(row=3, column=1)
    button0 = CTkButton(ButtonsForCalculationsFrame, text="EXP",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button0.grid(row=4, column=1)
    #fun fact, barely most of these can be rewritten in a simple string
    button6 = CTkButton(ButtonsForCalculationsFrame, text="x!",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button6.grid(row=0, column=2)
    button7 = CTkButton(ButtonsForCalculationsFrame, text="ln",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button7.grid(row=1, column=2)
    button8 = CTkButton(ButtonsForCalculationsFrame, text="log",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button8.grid(row=2, column=2)
    button9 = CTkButton(ButtonsForCalculationsFrame, text="√",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button9.grid(row=3, column=2)
    button0 = CTkButton(ButtonsForCalculationsFrame, text="x^2",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button0.grid(row=4, column=2)
    #I do this because it's funny
    button6 = CTkButton(ButtonsForCalculationsFrame, text="%",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button6.grid(row=0, column=3)
    button7 = CTkButton(ButtonsForCalculationsFrame,command=lambda: appendtoentry("7",OutputCalculations, "integer"), text="7",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button7.grid(row=1, column=3)
    button8 = CTkButton(ButtonsForCalculationsFrame,command=lambda: appendtoentry("4",OutputCalculations, "integer"), text="4",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button8.grid(row=2, column=3)
    button9 = CTkButton(ButtonsForCalculationsFrame,command=lambda: appendtoentry("1",OutputCalculations, "integer"), text="1",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button9.grid(row=3, column=3)
    button0 = CTkButton(ButtonsForCalculationsFrame,command=lambda: appendtoentry("0",OutputCalculations, "integer"), text="0",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button0.grid(row=4, column=3)
    #the long slope of redundancy and idiocracy
    button6 = CTkButton(ButtonsForCalculationsFrame, text="(",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button6.grid(row=0, column=4)
    button7 = CTkButton(ButtonsForCalculationsFrame,command=lambda: appendtoentry("8",OutputCalculations, "integer"), text="8",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button7.grid(row=1, column=4)
    button8 = CTkButton(ButtonsForCalculationsFrame,command=lambda: appendtoentry("5",OutputCalculations, "integer"), text="5",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button8.grid(row=2, column=4)
    button9 = CTkButton(ButtonsForCalculationsFrame,command=lambda: appendtoentry("2",OutputCalculations, "integer"), text="2",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button9.grid(row=3, column=4)
    button0 = CTkButton(ButtonsForCalculationsFrame, text=".",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button0.grid(row=4, column=4)

    button6 = CTkButton(ButtonsForCalculationsFrame, text=")",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button6.grid(row=0, column=5)
    button7 = CTkButton(ButtonsForCalculationsFrame,command=lambda: appendtoentry("9",OutputCalculations, "integer"), text="9",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button7.grid(row=1, column=5)
    button8 = CTkButton(ButtonsForCalculationsFrame,command=lambda: appendtoentry("6",OutputCalculations, "integer"), text="6",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button8.grid(row=2, column=5)
    button9 = CTkButton(ButtonsForCalculationsFrame,command=lambda: appendtoentry("3",OutputCalculations, "integer"), text="3",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button9.grid(row=3, column=5)
    button0 = CTkButton(ButtonsForCalculationsFrame, text="=",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button0.grid(row=4, column=5)

    button6 = CTkButton(ButtonsForCalculationsFrame, text="CE", height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button6.grid(row=0, column=6)
    button7 = CTkButton(ButtonsForCalculationsFrame, text="÷",height=40, width=60 ,command=lambda: appendtoentry("÷",OutputCalculations, "operation"), border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button7.grid(row=1, column=6)
    button8 = CTkButton(ButtonsForCalculationsFrame, text="x",height=40, width=60,command=lambda: appendtoentry("x",OutputCalculations, "operation"),  border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button8.grid(row=2, column=6)
    button9 = CTkButton(ButtonsForCalculationsFrame, text="-",height=40, width=60,command=lambda: appendtoentry("-",OutputCalculations, "operation"),  border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button9.grid(row=3, column=6)
    button0 = CTkButton(ButtonsForCalculationsFrame, text="+",height=40, width=60,command=lambda: appendtoentry("+",OutputCalculations, "operation"),  border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button0.grid(row=4, column=6)

 
    
    
#It's morbilations time...

def appendtoentry(value, OutputCalculations, datatype):
    print(value)
    global expression
    if datatype == "integer":
        current_value = OutputCalculations.get()
        OutputCalculations.configure(state="normal")
        OutputCalculations.delete(0, END)
        OutputCalculations.insert(0, current_value + str(value))
        OutputCalculations.configure(state="readonly")

    elif datatype != "integer" :
        current_value = OutputCalculations.get()
        OutputCalculations.configure(state="normal")
        OutputCalculations.delete(0, END)
        OutputCalculations.insert(0, current_value + str(value))
        OutputCalculations.configure(state="readonly")
        

def HolderFunction():
    number = []
    operation = []













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

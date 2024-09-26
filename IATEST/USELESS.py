from customtkinter import *
from pywinstyles import *
import psycopg2
import threading

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



def salespage(page):
    AccessContent = CTkFrame(page, width=600, height=355, fg_color="#0053A0", corner_radius=0)
    AccessLabel = CTkLabel(AccessContent, font=TitleFont, text="You now have access! Click on a tab to get started.", text_color='#FFFFFF', justify="center")
    AccessContent.grid_propagate(0)

    AccessContent.grid(pady = 0, padx = 0)
    AccessLabel.place(relx=0.5, rely=0.5, anchor="center")


    page.grid_propagate(False)  # Disable grid propagation on the SalesPage

    
    









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
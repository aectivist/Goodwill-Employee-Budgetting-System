from customtkinter import *
import psycopg2
import threading
import sys
import os

# Add Program directory to Python path
program_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(program_dir))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Global variables for user tracking
current_user = None
current_employee_id = None

def set_current_user(username, employee_id):
    global current_user, current_employee_id
    current_user = username
    current_employee_id = employee_id

from IATEST.Admin.init_login import init_login_db
from IATEST.Admin.activity_logger import ActivityLogger
from loginpage import LoginPage

# Initialize login database
init_login_db()

# Initialize activity logger
activity_logger = ActivityLogger()
# Imports for pages will be done when needed to avoid circular dependencies
#https://github.com/Akascape/CTkTable

import math
from math import *
import re




def play_sound():
    global soundpath
    global playingbool
    if playingbool == False:
        print("yea")
    else:
        print("nah")

# Database connection - make it accessible to imported modules
conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="12345", port=5432)
conn.autocommit = False  # Ensure transactions are used
cur = conn.cursor()

# Export database objects for other modules
def get_db():
    return conn, cur

loginaccess = False
EDITFLAG = False #FOR EDITTING
window = CTk()
window.title("BUDGET")
window.geometry("600x400") #fml
window.resizable(0,0) #disable resize
set_appearance_mode("light")


#++++++++++++++++++++++++++++++ {PAGES} ++++++++++++++++++++++++++++++++++++++

# Create frames for each page
TABFRAME = CTkFrame(window, height=51, width=600, fg_color="#1E1E1E", corner_radius=0, bg_color='#231F20')
TABFRAME.pack(anchor=CENTER, fill=X)

# Initialize page flags
HomePagePost = 0
ViewedPost = 0  # For Calculator
BudgetPagePost = 0

# These are the individual pages, or rather, the frames
LoadingPage = CTkFrame(window, corner_radius=0) #implement later
HomePage = CTkFrame(window, corner_radius=0)
setattr(HomePage, 'post_flag', 0)
TransactionsPage = CTkFrame(window, corner_radius=0)
DonatorPage = CTkFrame(window, corner_radius=0)  # Changed from ClientPage to DonatorPage
InventoryPage = CTkFrame(window, corner_radius=0)
BudgetPage = CTkFrame(window, corner_radius=0)
CalculatorPage = CTkFrame(window, corner_radius=0)
LoginPageFrame = CTkFrame(window, corner_radius=0, bg_color='#0053A0')

# Create a list to hold all the pages
pages = [HomePage, TransactionsPage, DonatorPage, InventoryPage, BudgetPage, CalculatorPage]  # Updated list with DonatorPage

# Function to show a page
def show_page(page, loginaccess):
    event = threading.Event()
    
    # Page initialization states
    global ViewedPost  # For Calculator
    global HomePagePost, login_handler, current_user, current_employee_id
    HomePagePost = getattr(HomePage, 'post_flag', 0)
    BudgetPagePost = getattr(BudgetPage, 'post_flag', 0)
    
    # Store currently visible page if any
    current_page = None
    for p in pages + [LoginPageFrame]:  # Include login frame in check
        if str(p.winfo_viewable()) == "1":  # Check if page is visible
            current_page = p
            break

    # Get page name for logging
    page_names = {
        HomePage: "Home Page",
        TransactionsPage: "Transactions Page",
        DonatorPage: "Donator Page",
        InventoryPage: "Inventory Page",
        BudgetPage: "Budget Page",
        CalculatorPage: "Calculator Page"
    }
    page_name = page_names.get(page, "Unknown Page")

    # Check if trying to access restricted page without login
    if loginaccess == False and page not in [HomePage, CalculatorPage]:
        # Check if login page exists and is not visible
        login_exists = login_handler is not None
        login_visible = str(LoginPageFrame.winfo_viewable()) == "1"
        
        if not login_visible:
            if current_page:
                current_page.pack_forget()
                window.update_idletasks()
            # If login handler exists, just show the frame without creating new handler
            if login_exists:
                LoginPageFrame.configure(fg_color='#0053A0')
                LoginPageFrame.pack(fill=BOTH, expand=True)
                login_handler.show_login(lambda success: admittedAccess(success))
            else:
                loginpage(LoginPageFrame, loginaccess)
        return  # Exit early to prevent showing other pages
    
    # Hide current page if exists
    if current_page:
        current_page.pack_forget()
        window.update_idletasks()
    
    # Show requested page
    if page == HomePage:
        if not HomePagePost:
            homepage(HomePage)
            HomePage.post_flag = 1
        HomePage.pack(fill=BOTH, expand=True)
    elif page == CalculatorPage:
        if ViewedPost == 0:
            calculatorpage(CalculatorPage)
        CalculatorPage.pack(fill=BOTH, expand=True)
    elif page == BudgetPage:
        if not BudgetPagePost:
            from BudgetPage import budgetpage
            budgetpage(BudgetPage)
            BudgetPage.post_flag = 1
        BudgetPage.pack(fill=BOTH, expand=True)
    elif page == InventoryPage:
        from InventoryPage import I_show_page, init_db as init_inventory_db
        init_inventory_db(conn, cur)  # Initialize database connection
        I_show_page(window, InventoryPage)  # Pass both window and frame
    elif page == DonatorPage:
        from DonatorPage import D_show_page, init_db as init_donator_db
        init_donator_db(conn, cur)  # Initialize database connection
        D_show_page(window, DonatorPage)  # Pass both window and frame
    elif page == TransactionsPage:
        from TransactionPage import T_show_page, init_db as init_transactions_db
        init_transactions_db(conn, cur)  # Initialize database connection
        T_show_page(window, TransactionsPage)  # Pass both window and frame
        
    # Log page access if user is logged in
    if loginaccess and current_user and page not in [LoginPageFrame]:
        activity_logger.log_page_access(
            current_employee_id,
            current_user,
            page_names.get(page, "Unknown Page"),
            f"Accessed {page_names.get(page, 'Unknown Page')}"
        )
    
    print(f"Showing page: {page}")
    window.update_idletasks()  # Update the UI
         
#++++++++++++++++++++++++++++++ {PAGE FUNCTIONS} ++++++++++++++++++++++++++++++++++++++
#DO NOT EDIT SPACE, WILL USE SPACE FOR THE OTHER PAGES


#def clientpage(page):
#def assetpage(page):


# ////////////////////////////{{CALCULATOR PAGE}}
mode_var = StringVar(value="Degrees")  # Default to Degrees
active_color = "#b8d4e0"  # Green for active
inactive_color = "#FFFFFF"  # White for inactive

def set_degrees():
    global mode_var
    mode_var.set("Degrees")
    button_degrees.configure(fg_color=active_color, text_color="#000000")  # Active button
    button_radians.configure(fg_color=inactive_color, text_color="#000000")  # Inactive button
    print("Mode set to Degrees")
    

def set_radians():
    global mode_var
    mode_var.set("Radians")
    button_radians.configure(fg_color=active_color, text_color="#000000")  # Active button
    button_degrees.configure(fg_color=inactive_color, text_color="#000000")  # Inactive button
    print("Mode set to Radians")


OutputCalculatorFont = CTkFont(family="Oswald", size=30, weight='bold')
EditFont = CTkFont(family="Oswald", size=15, weight='bold')

ViewedPost=0

def calculatorpage(page):
    global ViewedPost
    if ViewedPost == 0:
        global button_degrees, button_radians, button_EXP, HistoryToggleButton, HistorySideBar, HistoryScrollbar
        #START MASTER
        CalculatorMargin = CTkFrame(page)
        CalculatorMargin.pack(expand=True)
        #LEFT BAR
        HistorySideBar = CTkFrame(CalculatorMargin, width=150, height=320, border_color="#000000", border_width=1,fg_color="#FFFFFF")
        HistorySideBar.grid(row=0,column=0)
        HistorySideBar.grid_propagate(0)
        HistoryScrollbar = CTkScrollableFrame(HistorySideBar, width=140, height=270, border_width=1, fg_color="#FFFFFF",corner_radius=0)
        HistoryScrollbar.grid(row=1,column=0)
        HistoryToggleButton = CTkButton(HistorySideBar,text="EQUATION HISTORY",command=set_History,height=45, width=160, border_color="#000000", border_width=1,corner_radius=0, fg_color="#FFFFFF",text_color='#000000')
        HistoryToggleButton.grid(row=0,column=0)
        HistoryToggleButton.grid_propagate(0)
        

        #RIGHT BAR
        CalculatorSide = CTkFrame(CalculatorMargin, width=410, height=320, border_color="#000000", border_width=1)
        CalculatorSide.grid(row=0,column=1)
        CalculatorSide.grid_propagate(0)    
        #RIGHT BAR UI
        OutputCalculations = CTkEntry(CalculatorSide ,font=OutputCalculatorFont, width=410, height=120, border_color="#000000", border_width=1,corner_radius=0)
        OutputCalculations.grid(row=0,column=0)
        OutputCalculations.configure(state="readonly")
        
        OutputCalculations.ans = 0
        OutputCalculations.radians = True
        OutputCalculations.trig_input = ""

        OutputCalculations.degrees_button = None
        OutputCalculations.radians_button = None


        ButtonsForCalculationsFrame = CTkFrame(CalculatorSide, width=410, height=200, border_color="#000000", border_width=1,corner_radius=0)
        ButtonsForCalculationsFrame.grid(row=1, column=0)
        ButtonsForCalculationsFrame.grid_propagate(0)
        
        for i in range(6):
            ButtonsForCalculationsFrame.grid_columnconfigure(i, weight=1, uniform="column")
            ButtonsForCalculationsFrame.grid_rowconfigure(0, minsize=40)
        ViewedPost+=1
    else:
        print("Calculator page has been printed!")
    

    
    #Welcome to a programmer's worst nightmare LMFAOOOOO
    button_radians = CTkButton(ButtonsForCalculationsFrame,corner_radius=0, text="Rad",height=40, width=60,command=set_radians, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_radians.grid(row=0, column=0)
    button_EXP = CTkButton(ButtonsForCalculationsFrame, corner_radius=0,text="Play",height=40, width=60,command=play_sound, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_EXP.grid(row=1, column=0)
    button_pi = CTkButton(ButtonsForCalculationsFrame, corner_radius=0,text="π",height=40, width=60,command=lambda: appendtoentry("π", OutputCalculations, "pi"), border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_pi.grid(row=2, column=0)
    button_e = CTkButton(ButtonsForCalculationsFrame,corner_radius=0, text="e",height=40, width=60,command=lambda: appendtoentry("e", OutputCalculations, "e"), border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_e.grid(row=3, column=0)
    button_Ans = CTkButton(ButtonsForCalculationsFrame,corner_radius=0, text="Ans",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_Ans.grid(row=4, column=0)

    button_degrees = CTkButton(ButtonsForCalculationsFrame, corner_radius=0,text="Deg",height=40, width=60,command=set_degrees, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_degrees.grid(row=0, column=1)
    button_sin = CTkButton(ButtonsForCalculationsFrame,corner_radius=0, text="sin", height=40, width=60,command=lambda: appendtoentry("sin", OutputCalculations, "trig"), border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_sin.grid(row=1, column=1)

    button_cos = CTkButton(ButtonsForCalculationsFrame,corner_radius=0, text="cos", height=40, width=60,command=lambda: appendtoentry("cos", OutputCalculations, "trig"), border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_cos.grid(row=2, column=1)

    button_tan = CTkButton(ButtonsForCalculationsFrame,corner_radius=0, text="tan", height=40, width=60,command=lambda: appendtoentry("tan", OutputCalculations, "trig"), border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_tan.grid(row=3, column=1)
    button_del = CTkButton(ButtonsForCalculationsFrame,corner_radius=0, text="del",height=40, width=60,command=lambda: delete(OutputCalculations), border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_del.grid(row=4, column=1)
    #troll
    button6 = CTkButton(ButtonsForCalculationsFrame,corner_radius=0, text="x!",height=40, width=60,command=lambda: appendtoentry("!", OutputCalculations, "factorial"), border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button6.grid(row=0, column=2)
    button_natlog = CTkButton(ButtonsForCalculationsFrame,corner_radius=0, text="ln",height=40, width=60, command=lambda: appendtoentry("ln", OutputCalculations, "natlog"), border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_natlog.grid(row=1, column=2)
    button_log = CTkButton(ButtonsForCalculationsFrame,corner_radius=0, text="log",height=40, width=60,command=lambda: appendtoentry("log(", OutputCalculations, "logarithm"), border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_log.grid(row=2, column=2)
    button_sqrt = CTkButton(ButtonsForCalculationsFrame, corner_radius=0,text="√",height=40, width=60,command=lambda: appendtoentry("√", OutputCalculations, "sqrt"), border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_sqrt.grid(row=3, column=2)
    button_exponent = CTkButton(ButtonsForCalculationsFrame,corner_radius=0, text="x^2",height=40, width=60, command=lambda: appendtoentry("^2",OutputCalculations, "exponent"), border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_exponent.grid(row=4, column=2)
    #I do this because it's funny
    button_perc = CTkButton(ButtonsForCalculationsFrame,corner_radius=0, text="%",command=lambda: appendtoentry("%",OutputCalculations, "percentage"),height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_perc.grid(row=0, column=3)
    button_7 = CTkButton(ButtonsForCalculationsFrame,corner_radius=0,command=lambda: appendtoentry("7",OutputCalculations, "integer"), text="7",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_7.grid(row=1, column=3)
    button_4 = CTkButton(ButtonsForCalculationsFrame,corner_radius=0,command=lambda: appendtoentry("4",OutputCalculations, "integer"), text="4",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_4.grid(row=2, column=3)
    button_1 = CTkButton(ButtonsForCalculationsFrame,corner_radius=0,command=lambda: appendtoentry("1",OutputCalculations, "integer"), text="1",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_1.grid(row=3, column=3)
    button_0 = CTkButton(ButtonsForCalculationsFrame,corner_radius=0,command=lambda: appendtoentry("0",OutputCalculations, "integer"), text="0",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_0.grid(row=4, column=3)
    #the long slope of redundancy and idiocracy
    button_opb = CTkButton(ButtonsForCalculationsFrame,corner_radius=0, text="(",height=40, width=60,command=lambda: appendtoentry("(", OutputCalculations, "openbracket"), border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_opb.grid(row=0, column=4)
    button_8 = CTkButton(ButtonsForCalculationsFrame,corner_radius=0,command=lambda: appendtoentry("8",OutputCalculations, "integer"), text="8",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_8.grid(row=1, column=4)
    button_5 = CTkButton(ButtonsForCalculationsFrame,corner_radius=0,command=lambda: appendtoentry("5",OutputCalculations, "integer"), text="5",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_5.grid(row=2, column=4)
    button_2 = CTkButton(ButtonsForCalculationsFrame,corner_radius=0,command=lambda: appendtoentry("2",OutputCalculations, "integer"), text="2",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_2.grid(row=3, column=4)
    button_dot = CTkButton(ButtonsForCalculationsFrame,corner_radius=0, text=".",height=40, width=60, command=lambda: appendtoentry(".", OutputCalculations, "integer"), border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_dot.grid(row=4, column=4)

    button_clob = CTkButton(ButtonsForCalculationsFrame,corner_radius=0,command=lambda: appendtoentry(")",OutputCalculations, "bracket"), text=")",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_clob.grid(row=0, column=5)
    button_9 = CTkButton(ButtonsForCalculationsFrame,corner_radius=0,command=lambda: appendtoentry("9",OutputCalculations, "integer"), text="9",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_9.grid(row=1, column=5)
    button_6 = CTkButton(ButtonsForCalculationsFrame,corner_radius=0,command=lambda: appendtoentry("6",OutputCalculations, "integer"), text="6",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_6.grid(row=2, column=5)
    button_3 = CTkButton(ButtonsForCalculationsFrame,corner_radius=0,command=lambda: appendtoentry("3",OutputCalculations, "integer"), text="3",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_3.grid(row=3, column=5)
    button_equal = CTkButton(ButtonsForCalculationsFrame,corner_radius=0, text="=", command=lambda: calculate(OutputCalculations), height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_equal.grid(row=4, column=5)

    button_clearN = CTkButton(ButtonsForCalculationsFrame,corner_radius=0, text="CE", height=40, width=60,command=lambda: clear(OutputCalculations), border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_clearN.grid(row=0, column=6)
    button_div = CTkButton(ButtonsForCalculationsFrame,corner_radius=0, text="÷",height=40, width=60 ,command=lambda: appendtoentry("÷",OutputCalculations, "operation"), border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_div.grid(row=1, column=6)
    button_mult = CTkButton(ButtonsForCalculationsFrame,corner_radius=0, text="x",height=40, width=60,command=lambda: appendtoentry("x",OutputCalculations, "operation"),  border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_mult.grid(row=2, column=6)
    button_min = CTkButton(ButtonsForCalculationsFrame,corner_radius=0, text="-",height=40, width=60,command=lambda: appendtoentry("-",OutputCalculations, "operation"),  border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_min.grid(row=3, column=6)
    button_plus = CTkButton(ButtonsForCalculationsFrame,corner_radius=0, text="+",height=40, width=60,command=lambda: appendtoentry("+",OutputCalculations, "operation"),  border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button_plus.grid(row=4, column=6)

 

                
def appendtoentry(value, OutputCalculations, type):
    print(value)
    currentvalue = OutputCalculations.get()
    OutputCalculations.configure(state="normal")
    if currentvalue == "Error":
        OutputCalculations.delete(0, END)

    if type == "integer":
        OutputCalculations.insert(END, str(value))
    elif type == "operation":
        OutputCalculations.insert(END, str(value))
    elif type == "trig":
        OutputCalculations.insert(END, value + "(")
    elif type == "bracket":
        OutputCalculations.insert(END, value)
    elif type == "bracket1":
        OutputCalculations.insert(END, value)
    elif type == "logarithm":
        OutputCalculations.insert(END, value)
    elif type == "sqrt":
        OutputCalculations.insert(END, value+ "(")
    elif type == "pi":
        OutputCalculations.insert(END, value)
        currentvalue = currentvalue.replace("π", "3.14159265359")
        
    elif type == "natlog":
        OutputCalculations.insert(END, value+"(")
    elif type == "exponent":
        OutputCalculations.insert(END, value)
    elif type == "e":
        OutputCalculations.insert(END, value)
    elif type == "openbracket":
        OutputCalculations.insert(END, value)
    elif type == "percentage":
        OutputCalculations.insert(END, value)
    elif type == "factorial":   
        OutputCalculations.insert(END, value)
    

    OutputCalculations.configure(state="readonly")

def clear(OutputCalculations):
    OutputCalculations.configure(state="normal")
    OutputCalculations.delete(0, END)
    OutputCalculations.configure(state="readonly")

def delete(OutputCalculations):
    current_value = OutputCalculations.get()
    
    if current_value == "Error":
        OutputCalculations.configure(state="normal")
        OutputCalculations.delete(0, END)
        OutputCalculations.configure(state="readonly")
    OutputCalculations.configure(state="normal")
    OutputCalculations.delete(len(current_value)-1, END)
    OutputCalculations.configure(state="readonly")

History = False


def calculate(OutputCalculations):
    global EquationStack, ResultsStack, History, HistoryScrollbar
    print("Calculate function called")
    EquationStack = []
    ResultsStack = []

    try:
        expression = OutputCalculations.get()
        EquationStack.append(expression)
        print("Expression:", expression)

        is_degrees = mode_var.get() == "Degrees"

        # Replace symbols
        expression = expression.replace("x", "*")
        expression = expression.replace("÷", "/")
        expression = expression.replace("--", "+")
        expression = expression.replace("%", "/100")

        # For trig functions, replace with math. prefix
        if is_degrees:
            expression = re.sub(r'sin\(([\d\.]+)\)', lambda m: f'math.sin(math.radians({m.group(1)}))', expression)#11/04/2024: Teacher Melvin was not here, so I utilized AI to help debug my RE expressions.
            expression = re.sub(r'cos\(([\d\.]+)\)', lambda m: f'math.cos(math.radians({m.group(1)}))', expression)
            expression = re.sub(r'tan\(([\d\.]+)\)', lambda m: f'math.tan(math.radians({m.group(1)}))', expression)
        else:
            expression = re.sub(r'sin\(([\d\.]+)\)', lambda m: f'math.sin({m.group(1)})', expression)
            expression = re.sub(r'cos\(([\d\.]+)\)', lambda m: f'math.cos({m.group(1)})', expression)
            expression = re.sub(r'tan\(([\d\.]+)\)', lambda m: f'math.tan({m.group(1)})', expression)

        #Factorial
        expression = re.sub(r'(\d+)!', r'math.factorial(\1)', expression)


        # Exponents
        expression = expression.replace("log(", "math.log10(")
        expression = expression.replace("ln(", "math.log(")
        expression = expression.replace("^", "**")
        expression = expression.replace("√(", "math.sqrt(")

        # Replace with numerical constants
        expression = expression.replace("π", "3.141592653589793")
        expression = expression.replace("e", "math.e")

        # Handle multiplication signs and spacing
        expression = expression.replace(")(", ")*(")
        expression = expression.replace(") ", ")*")
        expression = expression.replace(")(", ")*(")
        

        # Insert multiplication where necessary
        expression = re.sub(r'(\d+)([a-zA-Z]+)(\()', r'\1*\2\(', expression) 
        expression = re.sub(r'(?<!\w)(\d)(\()', r'\1*\2', expression)
        expression = re.sub(r'(?<!\w)(\))(\d)', r'\1*\2', expression)
        expression = re.sub(r'(\d)([a-zA-Z]+)', r'\1*\2', expression)

        print("Modified Expression:", expression)

        if expression.strip() == "":
            raise ValueError("Empty expression after modifications")

        result = eval(expression)  # Ensure eval is used SAFELY
        finalresult = round(result, 9)
        
            
        print("Result:", finalresult)
        ResultsStack.append(finalresult)
        OutputCalculations.configure(state="normal")
        OutputCalculations.delete(0, END)
        OutputCalculations.insert(0, str(finalresult))
        OutputCalculations.configure(state="readonly")

    except Exception as e:
        print(f"Error: {e}")
        OutputCalculations.configure(state="normal")
        OutputCalculations.delete(0, END)
        OutputCalculations.insert(0, "Error")
        OutputCalculations.configure(state="readonly")

    for I in EquationStack:
        EquationPop = str(EquationStack.pop())
        print(EquationPop)
        NewEquationArray.append(EquationPop)
        
    for I in ResultsStack:
        ResultsPop = str(ResultsStack.pop())
        print(ResultsPop)
        NewResultsArray.append(ResultsPop)
        
    UpdateHistory(NewEquationArray, History, HistoryScrollbar, NewResultsArray)

 
def set_History(): #sets whether or not its results or equations
    global History, HistoryToggleButton, EquationStack, ResultsStack,NewEquationArray,HistoryScrollbar
    
    if History == True:
        History = not History
        HistoryToggleButton.configure(text="EQUATION HISTORY")
        UpdateHistory(NewEquationArray, History,HistoryScrollbar, NewResultsArray)
        print("Now set to Equation.")
        DeleteButton()
        
    elif History== False:
        History = not History
        HistoryToggleButton.configure(text="RESULTS HISTORY")   
        UpdateHistory(NewEquationArray, History,HistoryScrollbar, NewResultsArray)
        print("Now set to Results")
        DeleteButton()
    

NewEquationArray=[]
NewResultsArray=[]

NewEquationArray[0:100]
NewResultsArray[0:100]


def UpdateHistory(NewEquationArray, History, HistoryScrollbar,NewResultsArray): #Updates the History by pasting everything within the New Equation Array
    global HistoryToggleButton, EquationStack, ResultsStack, EquationButton, ResultsButton
    print(History)
    
    if History == False:
        RowNum = 0
        for I in NewEquationArray:
                EquationButton = CTkButton(HistoryScrollbar, text=I, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000",hover_color="#FFFFFF", corner_radius=0)
                EquationButton.grid(row=RowNum,column=0)
                RowNum = RowNum + 1   
        
    elif History== True:  
        RowNum = 0
        for I in NewResultsArray:
                ResultsButton = CTkButton(HistoryScrollbar, text=I, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000",hover_color="#FFFFFF", corner_radius=0)
                ResultsButton.grid(row=RowNum,column=0)
                RowNum = RowNum + 1 
        
def DeleteButton():
    global EquationButton, ResultsButton
    if History == False:
        print("YOUR")
        for I in NewResultsArray:
            ResultsButton.destroy()
    else:
        print("MOM!")
        for I in NewEquationArray:
            EquationButton.destroy()
        






    


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
    #ADD NOTE BUTTON FUNCTIONS


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

def button_clicked(button_id, EditTextBox, EditNoteButton, NoteBoxPadding, AddedNotesScrollbar, EditTitleLabel): #clickity click click
    global EDITFLAG
    EditTitleLabel.configure(font=TitleFont,text="Notes")
    print(f"Button {button_id} clicked")
    if EDITFLAG == FALSE:
        retrieveNote(button_id, EditTextBox, EditNoteButton, NoteBoxPadding, AddedNotesScrollbar) #this calls on so edit functions may work




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



def editselect(NoteBoxPadding,EditTextBox, button_id, AddedNotesScrollbar): #ASK ABOUT THE EDITTING BUG BRO PLS // 11/4/2024:
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

# Initialize login page handler
login_handler = None

def loginpage(page, loginaccess):
    global login_handler
    if loginaccess == False and page not in [HomePage, CalculatorPage]:
        # Only proceed if login page is not visible
        if str(LoginPageFrame.winfo_viewable()) != "1":
            # Hide current pages first
            for p in [LoginPageFrame] + pages:
                if str(p.winfo_viewable()) == "1":
                    p.pack_forget()
            window.update_idletasks()
            
            # Show login page
            page.configure(fg_color='#0053A0')
            page.pack(fill=BOTH, expand=True)
            
            # Initialize login handler only if it doesn't exist
            if not login_handler:
                login_handler = LoginPage(page, conn, cur)
                login_handler.show_login(lambda success, username=None, employee_id=None:
                    admittedAccess(success, username, employee_id))
#++++++++++++++++++++++++++++++ {TAB FUNCTIONS} ++++++++++++++++++++++++++++++++++++++

# Function to handle button clicks
def button_event(page,loginaccess):
    show_page(page,loginaccess)

#To resize and center all buttons
for i in range(6):
    TABFRAME.grid_columnconfigure(i, weight=1, uniform="col")
    TABFRAME.grid_rowconfigure(0, minsize=51)

# buttons
HomeTab = CTkButton(TABFRAME, text="Home", width=20, corner_radius=0 , command=lambda: button_event(HomePage,loginaccess))
HomeTab.grid(row=0, column=0, pady=10, padx=6, sticky="nsew")

TransactionsTab = CTkButton(TABFRAME, text="Transactions", width=20, corner_radius=0, command=lambda: button_event(TransactionsPage,loginaccess))
TransactionsTab.grid(row=0, column=1, pady=10, padx=6, sticky="nsew")

DonatorTab = CTkButton(TABFRAME, text="Donator", width=20, corner_radius=0, command=lambda: button_event(DonatorPage,loginaccess))
DonatorTab.grid(row=0, column=2, pady=10, padx=6, sticky="nsew")

InventoryTab = CTkButton(TABFRAME, text="Inventory", width=20, corner_radius=0, command=lambda: button_event(InventoryPage,loginaccess))
InventoryTab.grid(row=0, column=3, pady=10, padx=6, sticky="nsew")

BudgetTab = CTkButton(TABFRAME, text="Budget", width=20, corner_radius=0, command=lambda: button_event(BudgetPage,loginaccess))
BudgetTab.grid(row=0, column=4, pady=10, padx=6, sticky="nsew")

Calculatortab = CTkButton(TABFRAME, text="Calculator", width=20, corner_radius=0, command=lambda: button_event(CalculatorPage,loginaccess))
Calculatortab.grid(row=0, column=5, pady=10, padx=6, sticky="nsew")
def admittedAccess(success, username=None, employee_id=None):
    global loginaccess, HomePagePost
    if success:
        loginaccess = True
        
        # Set user info and log successful login
        set_current_user(username or "Unknown", employee_id or "UNKNOWN")
        activity_logger.log_login(
            employee_id,
            username,
            True,
            "User logged in successfully"
        )
        
        # Hide all pages first
        for page in [LoginPageFrame] + pages:
            if str(page.winfo_viewable()) == "1":
                page.pack_forget()
        window.update_idletasks()
        
        # Initialize HomePage if needed
        if not HomePagePost:
            homepage(HomePage)
            HomePage.post_flag = 1
            
        # Create and show success page
        SuccessPage = CTkFrame(window, corner_radius=0, fg_color='#0053A0')
        SuccessPage.pack(fill=BOTH, expand=True)
        
        AccessContainer = CTkFrame(SuccessPage, corner_radius=0, fg_color='transparent')
        AccessContainer.pack(expand=True)
        
        AccessLabel = CTkLabel(
            AccessContainer,
            font=CTkFont(family="Oswald", size=20, weight='bold'),
            text="You now have access!\nClick on a tab to get started.",
            text_color='#FFFFFF',
            justify="center"
        )
        AccessLabel.pack(expand=True)
        
        # Switch to Home page after 2 seconds
        window.after(2000, lambda: [SuccessPage.pack_forget(), show_page(HomePage, True)])
        
        # Enable restricted tabs
        TransactionsTab.configure(command=lambda: button_event(TransactionsPage, loginaccess))
        DonatorTab.configure(command=lambda: button_event(DonatorPage, loginaccess))
        InventoryTab.configure(command=lambda: button_event(InventoryPage, loginaccess))
        BudgetTab.configure(command=lambda: button_event(BudgetPage, loginaccess))
        
    

# Show the first page by default
show_page(HomePage, loginaccess)

window.mainloop()

#am cooked

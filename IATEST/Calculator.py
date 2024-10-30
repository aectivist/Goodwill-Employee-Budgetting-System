from customtkinter import *
from pywinstyles import *
import psycopg2
from CTkTable import *
#https://github.com/Akascape/CTkTable


import math
import re
import pygame
import random
playingbool = False
def get_random_integer(min_value, max_value):
    return random.randint(min_value, max_value)




def songchanger():
    global soundpath
    A=['Serial Experiments Lain Opening.mp3','Cyberpunk Edgerunners.mp3','DanDaDan.mp3','Nirvana.mp3','breakcore.mp3']
    I = get_random_integer(0, len(A)-1)
    soundpath = os.path.join('IATEST\\song', A[I])
    return soundpath
    
pygame.mixer.init()


def play_sound():
    global soundpath
    global playingbool
    if playingbool == False:
        songchanger()
        pygame.mixer.music.load(soundpath)
        pygame.mixer.music.play()
        button_EXP.configure(text="Play")  # Change button text to "Play"
    else:
        pygame.mixer.music.stop()
        button_EXP.configure(text="Stop")  # Change button text to "Stop"
    playingbool = not playingbool

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


def salespage(page):
    global button_degrees, button_radians, button_EXP
    #START MASTER
    CalculatorMargin = CTkFrame(page)
    CalculatorMargin.pack(expand=True)
    #LEFT BAR
    HistorySideBar = CTkFrame(CalculatorMargin, width=150, height=320, border_color="#000000", border_width=1,fg_color="#FFFFFF")
    HistorySideBar.grid(row=0,column=0)
    HistorySideBar.grid_propagate(0)
    HistoryToggleButton = CTkButton(HistorySideBar,text="EQUATION HISTORY", height=45, width=160, border_color="#000000", border_width=1,corner_radius=0, fg_color="#FFFFFF",text_color='#000000')
    HistoryToggleButton.grid(row=0,column=0)
    HistoryToggleButton.grid_propagate(0)
    HistoryScrollBar = CTkScrollableFrame(HistorySideBar, width=140, height=270, border_width=1, fg_color="#FFFFFF",corner_radius=0)
    HistoryScrollBar.grid(row=1,column=0)

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

    # Variable to store the mode
    
    # Radio buttons for Degrees and Radians
    

    
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
    button6 = CTkButton(ButtonsForCalculationsFrame,corner_radius=0, text="x!",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
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
    button6 = CTkButton(ButtonsForCalculationsFrame,corner_radius=0, text="%",command=lambda: appendtoentry("%",OutputCalculations, "percentage"),height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button6.grid(row=0, column=3)
    button7 = CTkButton(ButtonsForCalculationsFrame,corner_radius=0,command=lambda: appendtoentry("7",OutputCalculations, "integer"), text="7",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button7.grid(row=1, column=3)
    button8 = CTkButton(ButtonsForCalculationsFrame,corner_radius=0,command=lambda: appendtoentry("4",OutputCalculations, "integer"), text="4",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button8.grid(row=2, column=3)
    button9 = CTkButton(ButtonsForCalculationsFrame,corner_radius=0,command=lambda: appendtoentry("1",OutputCalculations, "integer"), text="1",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button9.grid(row=3, column=3)
    button0 = CTkButton(ButtonsForCalculationsFrame,corner_radius=0,command=lambda: appendtoentry("0",OutputCalculations, "integer"), text="0",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button0.grid(row=4, column=3)
    #the long slope of redundancy and idiocracy
    button6 = CTkButton(ButtonsForCalculationsFrame,corner_radius=0, text="(",height=40, width=60,command=lambda: appendtoentry("(", OutputCalculations, "openbracket"), border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button6.grid(row=0, column=4)
    button7 = CTkButton(ButtonsForCalculationsFrame,corner_radius=0,command=lambda: appendtoentry("8",OutputCalculations, "integer"), text="8",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button7.grid(row=1, column=4)
    button8 = CTkButton(ButtonsForCalculationsFrame,corner_radius=0,command=lambda: appendtoentry("5",OutputCalculations, "integer"), text="5",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button8.grid(row=2, column=4)
    button9 = CTkButton(ButtonsForCalculationsFrame,corner_radius=0,command=lambda: appendtoentry("2",OutputCalculations, "integer"), text="2",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button9.grid(row=3, column=4)
    button0 = CTkButton(ButtonsForCalculationsFrame,corner_radius=0, text=".",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button0.grid(row=4, column=4)

    button6 = CTkButton(ButtonsForCalculationsFrame,corner_radius=0,command=lambda: appendtoentry(")",OutputCalculations, "bracket"), text=")",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button6.grid(row=0, column=5)
    button7 = CTkButton(ButtonsForCalculationsFrame,corner_radius=0,command=lambda: appendtoentry("9",OutputCalculations, "integer"), text="9",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button7.grid(row=1, column=5)
    button8 = CTkButton(ButtonsForCalculationsFrame,corner_radius=0,command=lambda: appendtoentry("6",OutputCalculations, "integer"), text="6",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button8.grid(row=2, column=5)
    button9 = CTkButton(ButtonsForCalculationsFrame,corner_radius=0,command=lambda: appendtoentry("3",OutputCalculations, "integer"), text="3",height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button9.grid(row=3, column=5)
    button0 = CTkButton(ButtonsForCalculationsFrame,corner_radius=0, text="=", command=lambda: calculate(OutputCalculations), height=40, width=60, border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button0.grid(row=4, column=5)

    button6 = CTkButton(ButtonsForCalculationsFrame,corner_radius=0, text="CE", height=40, width=60,command=lambda: clear(OutputCalculations), border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button6.grid(row=0, column=6)
    button7 = CTkButton(ButtonsForCalculationsFrame,corner_radius=0, text="÷",height=40, width=60 ,command=lambda: appendtoentry("÷",OutputCalculations, "operation"), border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button7.grid(row=1, column=6)
    button8 = CTkButton(ButtonsForCalculationsFrame,corner_radius=0, text="x",height=40, width=60,command=lambda: appendtoentry("x",OutputCalculations, "operation"),  border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button8.grid(row=2, column=6)
    button9 = CTkButton(ButtonsForCalculationsFrame,corner_radius=0, text="-",height=40, width=60,command=lambda: appendtoentry("-",OutputCalculations, "operation"),  border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button9.grid(row=3, column=6)
    button0 = CTkButton(ButtonsForCalculationsFrame,corner_radius=0, text="+",height=40, width=60,command=lambda: appendtoentry("+",OutputCalculations, "operation"),  border_color="#000000", border_width=1, fg_color="#FFFFFF", text_color="#000000")
    button0.grid(row=4, column=6)

 
    
    



    
    

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



def calculate(OutputCalculations):
    print("Calculate function called")

    startchecker = OutputCalculations.get()
    
    try:
        expression = OutputCalculations.get()
        print("Expression:", expression)

        is_degrees = mode_var.get() == "Degrees"


        #replace symbols
        expression = expression.replace("x", "*")
        expression = expression.replace("÷", "/")
        expression = expression.replace("%", "/100")

        
        #for trig
        if is_degrees:
            expression = re.sub(r'sin\(([\d\.]+)\)', lambda m: f'math.sin(math.radians({m.group(1)}))', expression)
            expression = re.sub(r'cos\(([\d\.]+)\)', lambda m: f'math.cos(math.radians({m.group(1)}))', expression)
            expression = re.sub(r'tan\(([\d\.]+)\)', lambda m: f'math.tan(math.radians({m.group(1)}))', expression)
        else:
            expression = re.sub(r'sin\(([\d\.]+)\)', lambda m: f'math.sin(math.degrees({m.group(1)}))', expression)
            expression = re.sub(r'cos\(([\d\.]+)\)', lambda m: f'math.cos(math.degrees({m.group(1)}))', expression)
            expression = re.sub(r'tan\(([\d\.]+)\)', lambda m: f'math.tan(math.degrees({m.group(1)}))', expression)
        
        #exponents
        expression = expression.replace("log(", "math.log10(")
        expression = expression.replace("ln(", "math.log(")
        expression = expression.replace("^", "**")
        expression = expression.replace("√(", "math.sqrt(")

        #replace with nums
        expression = expression.replace("π", "(3.14159265359)")
        expression = expression.replace("e", "(2.71828182846)")

        #bracket
        expression = expression.replace(")(", ")*(")  #)(60+24)
        expression = expression.replace(") ", ")*")  # 6( 
        expression = expression.replace(")(", ")*(")  #2(5)
        
        expression = re.sub(r'(\d+)([a-zA-Z]+)(\()', r'\1*\2\(', expression) #glazin that * in between nums and funcs
        expression = re.sub(r'(?<!\w)(\d)(\()', r'\1*\2', expression)  #glazin that * in between
        expression = re.sub(r'(?<!\w)(\))(\d)', r'\1*\2', expression) #glazin that log() so * aint touched
        
        expression = re.sub(r'(\d)([a-zA-Z]+)', r'\1*\2', expression) #glaze confirmer for 3*math.sin(monkey)

        print("Modified Expression:", expression)
        result = eval(expression)
        if math.isclose(result, 0.5, rel_tol=1e-9):
            finalresult = 0.5
        else:
            finalresult = result

        print("Result:", finalresult)
        
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

#HISTORY
def EquationHistory():
 print("hello world")

    
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

from customtkinter import *
import psycopg2
#https://github.com/Akascape/CTkTable

import math
from math import * #i'd like to complain about this, for some reason it won't load even tho it'scalled so please remember if ever trig or any math func is not working.
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


OutputCalculatorFont = CTkFont(family="Oswald", size=30, weight='bold')
EditFont = CTkFont(family="Oswald", size=15, weight='bold')



def salespage(page):
    


    
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

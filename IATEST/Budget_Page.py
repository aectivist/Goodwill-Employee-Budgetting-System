import customtkinter as Ctk

from customtkinter import *

window = CTk()
window.title("BUDGET")
window.geometry("600x400") #fml
window.resizable(0,0) #disable resize
set_appearance_mode("light")

# Create a frame
frame = CTkFrame(window)
frame.pack(fill="both", expand=1)



window.mainloop()



from customtkinter import *

# First verify pycryptodome is installed correctly
try:
    from cryptography import *
    import os
    print("Crypto imports successful")
except ImportError:
    print("Please install pycryptodome using:")
    print("pip uninstall pycrypto cryptography")
    print("pip install pycryptodome")
    exit(1)

window = CTk()
window.title("BUDGET")
window.geometry("600x400") #fml
window.resizable(0,0) #disable resize
set_appearance_mode("light")


salt = "woah"
print (salt)

simple_key = get_random_bytes(32)
print(simple_key)

window.mainloop()
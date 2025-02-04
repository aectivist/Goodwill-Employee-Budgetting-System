import psycopg2
from customtkinter import (
    CTkFrame, CTkLabel, CTkEntry, CTkButton,
    CTkFont, CENTER, NORMAL, END, DISABLED, BOTH
)

class LoginPage:
    def __init__(self, parent, conn, cur):
        self.parent = parent
        self.conn = conn
        self.cur = cur
        self.login_frame = None
        self.login_font = CTkFont(family="Oswald", size=30, weight='bold')
        self.loaded_font = CTkFont(family="Oswald", size=20, weight='bold')

    def show_login(self, callback):
        # Create main login frame
        self.login_frame = CTkFrame(self.parent, width=600, height=400, corner_radius=0, fg_color='#FFFFFF')
        self.login_frame.pack(expand=True)

        # Login components
        login_label = CTkLabel(master=self.login_frame, font=self.login_font, text="LOGIN")
        login_label.grid(row=0, column=0, pady=10)

        self.username_entry = CTkEntry(master=self.login_frame, width=400, corner_radius=0, placeholder_text="Username")
        self.username_entry.grid(row=1, column=0, padx=25, pady=5)

        self.password_entry = CTkEntry(master=self.login_frame, width=400, corner_radius=0, show="●", placeholder_text="Password")
        self.password_entry.grid(row=2, column=0, padx=25, pady=5)

        submit_button = CTkButton(
            master=self.login_frame,
            width=400,
            corner_radius=0,
            text="SUBMIT",
            fg_color='#424242',
            hover_color='#231F20',
            command=lambda: self.validate_login(callback)
        )
        submit_button.grid(row=3, column=0, padx=25, pady=30)

    def validate_login(self, callback):
        username = self.username_entry.get()
        
        self.cur.execute(
            "SELECT * FROM loginpaswd WHERE loginid = %(username)s AND password = %(password)s",
            {'username': username, 'password': self.password_entry.get()}
        )
        
        login_successful = self.cur.fetchone() is not None
        
        # Log the login attempt
        action_type = 'LOGIN_SUCCESS' if login_successful else 'LOGIN_FAILED'
        self.cur.execute(
            "INSERT INTO user_login_logs (username, action_type) VALUES (%s, %s)",
            (username, action_type)
        )
        
        if login_successful:
            self.login_frame.pack_forget()
            self.show_success()
            callback(True)  # Notify successful login
        else:
            self.show_error()
            callback(False)  # Notify failed login
        
        self.conn.commit()

    def show_success(self):
        success_frame = CTkFrame(self.parent, width=600, height=355, fg_color="#0053A0", corner_radius=0)
        success_label = CTkLabel(
            success_frame,
            font=self.loaded_font,
            text="You now have access! Click on a tab to get started.",
            text_color='#FFFFFF',
            justify="center"
        )
        success_frame.grid_propagate(0)
        success_frame.grid(pady=0, padx=0)
        success_label.place(relx=0.5, rely=0.5, anchor="center")

    def show_error(self):
        # Flash the entries red briefly to indicate error
        original_color = self.username_entry.cget("fg_color")
        self.username_entry.configure(fg_color="#ffcccc")
        self.password_entry.configure(fg_color="#ffcccc")
        
        # Reset color after 1 second
        self.parent.after(1000, lambda: (
            self.username_entry.configure(fg_color=original_color),
            self.password_entry.configure(fg_color=original_color)
        ))
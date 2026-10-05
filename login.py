import customtkinter as ctk
from tkinter import messagebox

from gui import CollegeManager


USERNAME = "admin"
PASSWORD = "1234"


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


def login():
    username = username_entry.get().strip()
    password = password_entry.get()

    if username == USERNAME and password == PASSWORD:

        app.destroy()

        manager = CollegeManager()
        manager.mainloop()

    else:
        messagebox.showerror(
            "Login Failed",
            "Invalid username or password."
        )


app = ctk.CTk()

app.title("College Manager - Login")
app.geometry("450x400")
app.resizable(False, False)


title = ctk.CTkLabel(
    app,
    text="College Manager",
    font=("Arial", 30, "bold")
)
title.pack(pady=(50, 10))


subtitle = ctk.CTkLabel(
    app,
    text="Login to continue",
    font=("Arial", 15)
)
subtitle.pack(pady=(0, 25))


username_entry = ctk.CTkEntry(
    app,
    width=300,
    height=40,
    placeholder_text="Username"
)
username_entry.pack(pady=10)


password_entry = ctk.CTkEntry(
    app,
    width=300,
    height=40,
    placeholder_text="Password",
    show="*"
)
password_entry.pack(pady=10)


login_button = ctk.CTkButton(
    app,
    text="Login",
    width=300,
    height=40,
    command=login
)
login_button.pack(pady=25)


password_entry.bind(
    "<Return>",
    lambda event: login()
)


app.mainloop()
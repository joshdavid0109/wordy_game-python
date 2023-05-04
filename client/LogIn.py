import tkinter as tk
from tkinter import *
from tkinter import messagebox


class Login(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Login")
        self.parent = parent

        tk.Label(self, text="Username").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(self, text="Password").grid(row=1, column=0, padx=10, pady=10)

        self.username_entry = tk.Entry(self)
        self.password_entry = tk.Entry(self, show="*")

        self.username_entry.grid(row=0, column=1, padx=10, pady=10)
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(self, text="Login", command=self.login).grid(row=2, column=1, padx=10, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "admin" and password == "password":
            messagebox.showinfo("Login Successful", "Welcome!")
            self.parent.show_main_menu()
            self.destroy()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")
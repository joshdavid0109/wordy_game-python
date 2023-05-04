import tkinter as tk
from tkinter import messagebox

class MainMenu(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Main Menu")
        self.parent = parent

        tk.Button(self, text="Play Game", command=self.play_game).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(self, text="Button 1").grid(row=1, column=0, padx=10, pady=10)
        tk.Button(self, text="Button 2").grid(row=2, column=0, padx=10, pady=10)
        tk.Button(self, text="Logout", command=self.logout).grid(row=3, column=0, padx=10, pady=10)

    def play_game(self):
        pass

    def logout(self):
        self.parent.show_login_screen()
        self.destroy()
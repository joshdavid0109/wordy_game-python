import tkinter as tk
from tkinter import messagebox
from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk


class LogIn(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        Label = tk.Label(self, text="LogIn")
        Label.place(x=230, y=230)

        Button = tk.Button(self, text="next", font=("Arial", 15), command=lambda: controller.show_frame(MainMenu))
        Button.place(x=400, y=300)


class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        Label = tk.Label(self, text="MainMenu")
        Label.place(x=230, y=230)

        Button = tk.Button(self, text="next", command=lambda: controller.show_frame(Game))
        Button.place(x=650, y=450)


class Game(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Label = tk.Label(self, text="Game")
        Label.place(x=230, y=230)

        Button = tk.Button(self, text="next", command=lambda: controller.show_frame(LogIn))
        Button.place(x=650, y=450)


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        window = tk.Frame(self)
        window.pack()

        window.grid_rowconfigure(0, minsize=400)
        window.grid_columnconfigure(0, minsize=800)

        self.frames = {}
        for F in (LogIn, MainMenu, Game):
            frame = F(window, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LogIn)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()


app = Application()
app.mainloop()

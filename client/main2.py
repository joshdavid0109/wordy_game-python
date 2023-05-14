import random
import threading
import tkinter as tk
import traceback
from tkinter import messagebox
from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk

import Connector
import WordyGame
from Connector import daConnector

Font = ("Comic Sans MS", 15, "bold")

connector = daConnector("localhost", 9999)#should be read sa config
connector.connect()

eo = Connector.getEo()
gameID = None

class LogIn(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, width=250,height=200)

        #border = tk.LabelFrame(self, text='login', bg ='ivory', bd = 2, font=("Arial", 20))
        #border.pack(fill="both", expand="yes", padx = 100, pady = 100)

        userIdLabel = tk.Label(self, text="UserID")
        userIdLabel.place(x=20, y=20)

        userIdTextField = tk.Entry(self, width = 30, bd = 1)
        userIdTextField.place(x=120, y= 20)

        passwordLabel = tk.Label(self, text="Password")
        passwordLabel.place(x=20, y=50)

        passwordTextField = tk.Entry(self, width=30, bd=1)
        passwordTextField.place(x=120, y=50)

        def verify():
            userId = userIdTextField.get()
            password = passwordTextField.get()
            try:
                eo.login(userId, password)
            except Exception as e:
                userIdTextField.delete(0, "end")
                passwordTextField.delete(0, "end")
                messagebox.showwarning("ERROR", str(e.args[0]))
                controller.show_frame(MainMenu)#TODO COMMENT OUT THIS LINE THIS IS FOR THE SAKE OF TESTING LANG !!
                print(e)
            else:
                print("log in OK:) ! welcome "+userId+"! ")
                controller.show_frame(MainMenu)

        logInButton = tk.Button(self, text="ENTER", command=verify)
        #logInButton = tk.Button(self, text="ENTER", command=lambda: controller.show_frame(MainMenu))
        logInButton.place(x=180, y=90)


class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #hindi gumagana kapag 2022-2_9328-fingrp7_others/res/bookCover.jpg lang nilagay ko :( replace with absolute file path nalang
        image = Image.open("C:/Users/ADMIN/PycharmProjects/2022-2_9328-fingrp7_others/res/bookCover.jpg")
        photo = ImageTk.PhotoImage(image)

        background = tk.Label(self, image=photo)
        background.image = photo
        background.place(relx=0, rely=0, relwidth=1, relheight=1)

        #wordyLabel = tk.Label(self, text="WORDY", bg='green')
        wordyLabel = tk.Label(self, text="WORDY")
        #TODO HOW TO ACTUALLY CENTER THIS FKN LABEL
        print(self.winfo_width())
        print(self.winfo_height())
        print(parent.winfo_width())
        print(parent.winfo_height())
        print(self.winfo_width())
        print(self.winfo_screenwidth())
        print(self.winfo_screenheight())
        wordyLabel.place(x=170,y=50,anchor="center")
        #wordyLabel.configure(anchor="center")

        def playGameButton():
            try:
                threading.Thread(target=playGame).start()
                threading.Thread(target=open_countdown).start()
            except Exception as e:
                traceback.print_exc()
                print(str(e.args[0]))


        def play_game():
            print("exec a")
            eo.playGame(69)

        def playGame():
            try:
                print("exec a")
                randomnum = random.randint(1000, 9999)
                print(randomnum)
                gameID = eo.playGame(randomnum)
                print("GAME ID: ",gameID)
                print(eo.getTimer("g"))
            except Exception as e:
                traceback.print_exc()
                print(e)
                warningMsg(e)

        def open_countdown():
            try:
                print("exec b")
                new = Toplevel(self)
                new.geometry("750x250")
                new.title("MATCH")

                print(eo.getTimer("g"))
                # this always 0 ^ :(
            except Exception as e:
                traceback.print_exc()
                print(e)
                warningMsg(e)

            # Create a Label in New
            #todo retrieve timer from server, countdowm, countdown will close after finishing timer, and will either go to main menu or game
            #Label(new, text="Hey, Howdy?", font=('Helvetica 17 bold')).pack(pady=30)

        #playGameBTN = tk.Button(self, text="PLAY GAME", command=lambda: controller.show_frame(Game), font=Font)
        playGameBTN = tk.Button(self, text="PLAY GAME", command=playGameButton, font=Font)
        playGameBTN.place(x=170, y=150, anchor='center')


class Game(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Label = tk.Label(self, text="Game")
        Label.place(x=230, y=230)

        Button = tk.Button(self, text="next", command=lambda: controller.show_frame(LogIn))
        #Button = tk.Button(self, text="next", command=open_countdown)
        Button.place(x=230, y=300)


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        window = tk.Frame(self)
        window.pack()
        window.pack_propagate(0)

        Font_tuple = ("Comic Sans MS", 20, "bold")

        self.resizable(False, False)
        #self.wm_attributes("-transparentcolor", 'green')

        window.grid_rowconfigure(0, minsize=350)
        window.grid_columnconfigure(0, minsize=350)

        self.frames = {}
        for F in (LogIn, MainMenu, Game):
            frame = F(window, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LogIn)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()

def warningMsg(exception):
    messagebox.showwarning("ERROR", str(exception.args[0]))


app = Application()
app.mainloop()

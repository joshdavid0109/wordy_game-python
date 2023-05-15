import random
import threading
import time
import tkinter as tk
import traceback
from tkinter import messagebox
from tkinter import *
from tkinter.ttk import *

from concurrent.futures import ThreadPoolExecutor

from PIL import Image, ImageTk

import Connector
import WordyGame
from Connector import daConnector

Font = ("Comic Sans MS", 15, "bold")

connector = daConnector("localhost", 9999)  # should be read sa config
connector.connect()

eo = Connector.eo
gameID = None
userID = None
timer_value = None
roundNum = 0
winsNum = 0


def setGameID(num):
    global gameID
    gameID = num


class LogIn(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, width=250, height=200)

        # border = tk.LabelFrame(self, text='login', bg ='ivory', bd = 2, font=("Arial", 20))
        # border.pack(fill="both", expand="yes", padx = 100, pady = 100)

        userIdLabel = tk.Label(self, text="UserID")
        userIdLabel.place(x=20, y=20)

        userIdTextField = tk.Entry(self, width=30, bd=1)
        userIdTextField.place(x=120, y=20)

        passwordLabel = tk.Label(self, text="Password")
        passwordLabel.place(x=20, y=50)

        passwordTextField = tk.Entry(self, width=30, bd=1)
        passwordTextField.place(x=120, y=50)

        def verify():
            global userID
            userId = userIdTextField.get()
            password = passwordTextField.get()
            try:
                eo.login(userId, password)
            except Exception as e:
                print(e)
                traceback.print_exc()
                userID = userId  # TODO COMMENT OUT THIS LINE THIS IS FOR THE SAKE OF TESTING LANG !!
                userIdTextField.delete(0, "end")
                passwordTextField.delete(0, "end")
                messagebox.showwarning("ERROR", str(e.args[0]))
                print(userID)
                controller.show_frame(MainMenu)  # TODO COMMENT OUT THIS LINE THIS IS FOR THE SAKE OF TESTING LANG !!
                controller.frames[Game].focus_set()
            else:
                print("log in OK:) ! welcome " + str(userId) + "! ")
                global userID
                userID = userId
                controller.show_frame(MainMenu)
                controller.frames[Game].focus_set()

        logInButton = tk.Button(self, text="ENTER", command=verify)
        # logInButton = tk.Button(self, text="ENTER", command=lambda: controller.show_frame(MainMenu))
        logInButton.place(x=180, y=90)


class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # hindi gumagana kapag 2022-2_9328-fingrp7_others/res/bookCover.jpg lang nilagay ko :( replace with absolute file path nalang
        image = Image.open("C:/Users/ADMIN/PycharmProjects/2022-2_9328-fingrp7_others/res/bookCover.jpg")
        photo = ImageTk.PhotoImage(image)

        background = tk.Label(self, image=photo)
        background.image = photo
        background.place(relx=0, rely=0, relwidth=1, relheight=1)

        # wordyLabel = tk.Label(self, text="WORDY", bg='green')
        wordyLabel = tk.Label(self, text="WORDY")
        wordyLabel.place(x=170, y=50, anchor="center")

        # wordyLabel.configure(anchor="center")

        def playGameButton():
            try:
                threading.Thread(target=playGame).start()
                threading.Thread(target=open_countdown).start()
            except Exception as e:
                traceback.print_exc()
                print(str(e.args[0]))

        def playGame():
            try:
                print("exec a")
                global userID, gameID
                print("USER ID: ", userID)
                gameID = eo.playGame(int(userID))
                print(eo.getTimer("g"))
            except Exception as e:
                traceback.print_exc()
                print(e)
                warningMsg(e)
            else:
                # put code ng game here
                print("INGAME")
                setGameID(gameID)
                print("GAME ID: ", gameID)
                controller.show_frame(Game)
                controller.frames[Game].focus_set()

        def open_countdown():
            try:
                print("exec b")
                new = Toplevel(self)
                new.geometry("350x150")
                new.title("MATCH")

                # WAIT MUNA <1 SECOND KASI 0 MAKUKUHA NA ANO NUN TIMER PAG FIRST TYM HEHEH
                time.sleep(0.1)

                timerStart = eo.getTimer("g")

                def close_window():
                    new.destroy()

                print(timerStart)
                timer = threading.Timer(timerStart, close_window)
                timer.start()

            except Exception as e:
                traceback.print_exc()
                print(e)
                warningMsg(e)

        # playGameBTN = tk.Button(self, text="PLAY GAME", command=lambda: controller.show_frame(Game), font=Font)
        playGameBTN = tk.Button(self, text="PLAY GAME", command=playGameButton, font=Font)
        playGameBTN.place(x=170, y=150, anchor='center')


class Game(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global gameID

        self.textWordy = tk.Label(self, fg="#333333", justify="center", text="", font=Font)
        self.textWordy.place(x=130, y=280)

        self.pack()
        self.focus_set()
        self.bind("<Key>", self.handle_key)
        self.focus_set()
        self.stack = []

        # INDIVIDUAL LETTERS
        self.letter1 = tk.Label(self, fg="#333333", justify="center", text="1")
        self.letter2 = tk.Label(self, fg="#333333", justify="center", text="2")
        self.letter3 = tk.Label(self, fg="#333333", justify="center", text="3")
        self.letter4 = tk.Label(self, fg="#333333", justify="center", text="4")
        self.letter5 = tk.Label(self, fg="#333333", justify="center", text="5")
        self.letter6 = tk.Label(self, fg="#333333", justify="center", text="6")
        self.letter7 = tk.Label(self, fg="#333333", justify="center", text="7")
        self.letter8 = tk.Label(self, fg="#333333", justify="center", text="8")
        self.letter9 = tk.Label(self, fg="#333333", justify="center", text="9")
        self.letter10 = tk.Label(self, fg="#333333", justify="center", text="10")
        self.letter11 = tk.Label(self, fg="#333333", justify="center", text="11")
        self.letter12 = tk.Label(self, fg="#333333", justify="center", text="12")
        self.letter13 = tk.Label(self, fg="#333333", justify="center", text="13")
        self.letter14 = tk.Label(self, fg="#333333", justify="center", text="14")
        self.letter15 = tk.Label(self, fg="#333333", justify="center", text="15")
        self.letter16 = tk.Label(self, fg="#333333", justify="center", text="16")
        self.letter17 = tk.Label(self, fg="#333333", justify="center", text="17")
        self.letter1.place(x=120, y=70, width=30, height=30)
        self.letter2.place(x=160, y=70, width=30, height=30)
        self.letter3.place(x=200, y=70, width=30, height=30)
        self.letter4.place(x=240, y=70, width=30, height=30)
        self.letter5.place(x=280, y=70, width=30, height=30)
        self.letter6.place(x=120, y=120, width=30, height=30)
        self.letter7.place(x=160, y=120, width=30, height=30)
        self.letter8.place(x=200, y=120, width=30, height=30)
        self.letter9.place(x=240, y=120, width=30, height=30)
        self.letter10.place(x=280, y=120, width=30, height=30)
        self.letter11.place(x=120, y=170, width=30, height=30)
        self.letter12.place(x=160, y=170, width=30, height=30)
        self.letter13.place(x=200, y=170, width=30, height=30)
        self.letter14.place(x=240, y=170, width=30, height=30)
        self.letter15.place(x=280, y=170, width=30, height=30)
        self.letter16.place(x=120, y=220, width=30, height=30)
        self.letter17.place(x=160, y=220, width=30, height=30)

        # OTHER LABELS N STUFF
        self.roundLabel = tk.Label(self, fg="#333333", justify="left", text="ROUND: ")
        self.roundLabel.place(x=10, y=110, width=70, height=25)
        self.roundNum = tk.Label(self, fg="#333333", justify="left", text="0")
        self.roundNum.place(x=70, y=110, width=30, height=25)

        self.winsLabel = tk.Label(self, fg="#333333", justify="left", text="WINS: ")
        self.winsLabel.place(x=10, y=150, width=70, height=25)
        self.winsNum = tk.Label(self, fg="#333333", justify="left", text="0")
        self.winsNum.place(x=70, y=150, width=30, height=25)

        self.timerLabel = tk.Label(self, fg="#333333", justify="center", text="10")
        self.timerLabel.place(x=20, y=260, width=70, height=25)

        self.gameIDLabel = tk.Label(self, fg="#333333", justify="left", text=str(gameID))
        self.gameIDLabel.place(x=10, y=10, width=70, height=25)

        # self.wordTextField = tk.Entry(self, width=25, bd=1)
        # self.wordTextField.place(x=130, y=280)

        self.readyBTN = tk.Button(self, text="READY", command=self.ready)  # test lang, will change
        self.readyBTN.place(x=30, y=300)

        self.roundNum = 0

        self.letters = []

        self.availableLetters = []

    def handle_key(self, event):
        # print(self.letters)
        # print(self.availableLetters)
        if event.keysym == "Return":
            try:
                entered_word = self.textWordy.cget("text")
                print("WORD SENT  : ", entered_word)
                self.textWordy.config(text="")
                self.availableLetters = self.letters.copy()
                eo.checkWord(entered_word, int(gameID), int(userID))
            except Exception as e:
                print(str(e.args[0]))
            else:
                print("word is OK:)")
        elif event.keysym == "BackSpace":
            current_text = self.textWordy.cget("text")
            if current_text:
                last_letter = current_text[-1]
                self.textWordy.config(text=current_text[:-1])
                self.stack.append(last_letter)
                self.availableLetters.append(last_letter)
        else:
            pressed_letter = event.char.lower()
            if pressed_letter in self.availableLetters:
                current_text = self.textWordy.cget("text")
                self.textWordy.config(text=current_text + pressed_letter)
                self.availableLetters.remove(pressed_letter)
        self.textWordy.after(1, self.textWordy.update())

    def update_label_texts(self, char_array):
        label_texts = [getattr(self, f"letter{i}") for i in range(1, 18)]
        for i in range(len(char_array)):
            label_texts[i].configure(text=char_array[i])

    def ready(self):
        print("READY BUTTON CLICKED")
        self.readyBTN.config(state="disabled")

        print("USER ID: ", userID)
        print("GAME ID: ", gameID)

        print(eo.ready(int(userID), int(gameID)))

        self.timer()
        # result = lambda: eo.check_winner(gameID)
        # executor_service.submit(result)

        round_counter = lambda: self.addRound()

    def roundTimer(self):
        roundTimer = eo.getTimer("round")
        print("rount timer has started")
        print("ROUND TMR START AT" + str(roundTimer))

        for i in range(roundTimer):
            print("Timer: " + str(roundTimer - i))
            time.sleep(1)

        print("The round is over!")
        self.readyBTN.config(state="normal")

    def timer(self):
        print("PRE ROUND COUNTDOWN STARTED")
        global gameID, timer_value
        self.letters = list(eo.requestLetters(int(gameID)))
        timer_value = eo.getTimer("r")
        self.timerLabel.config(text=str(timer_value))

        print("PRE ROUND COUNTDOWN VALUE START: ", str(timer_value))
        print("LETTERS THIS ROUND: " + str(self.letters))

        while timer_value > 0:
            time.sleep(0.1)#not sure if necessary, 0 kasi una nareretrieve na value
            print("READY COUNTER: " + str(timer_value))
            timer_value = eo.getTimer("r")
            time.sleep(1)

        print("ready timer finish")
        self.update_label_texts(self.letters)
        self.availableLetters = self.letters.copy()
        self.roundTimer()

        # else:
        # timer_object = threading.Timer(timer_value, self.timer)
        # timer_object.start()

    def addRound(self):
        self.roundNum += 1
        self.roundNum.config(text=str(self.roundNum))

    # test
    print(gameID)

    def updTimer(self):
        print()


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        window = tk.Frame(self)
        window.pack()
        window.pack_propagate(0)

        Font_tuple = ("Comic Sans MS", 20, "bold")

        self.resizable(False, False)
        # self.wm_attributes("-transparentcolor", 'green')

        window.grid_rowconfigure(0, minsize=350)
        window.grid_columnconfigure(0, minsize=350)

        self.frames = {}
        for F in (LogIn, MainMenu, Game):
            frame = F(window, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # self.show_frame(Game)
        self.show_frame(LogIn)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()


def warningMsg(exception):
    messagebox.showwarning("ERROR", str(exception.args[0]))


app = Application()
app.mainloop()

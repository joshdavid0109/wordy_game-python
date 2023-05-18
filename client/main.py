import random
import threading
import time
import tkinter as tk
import traceback
from tkinter import messagebox
from tkinter import *
from tkinter.ttk import *

from concurrent.futures import ThreadPoolExecutor

import Connector
import WordyGame
from Connector import daConnector

Font = ("Comic Sans MS", 15, "bold")
FontLetters = ("Courier", 13, "bold")
FontLetterz = ("Helvetica", 12, "bold")

# connector = daConnector("192.168.219.133", 9999)  # should be read sa config
connector = daConnector("localhost", 9999)  # should be read sa config
connector.connect()

eo = Connector.eo
gameID = 0
userID = None
roundNum = 0
winsNum = 0

timer_lock = threading.Lock()


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
                # userID = userId  # TODO COMMENT OUT THIS LINE THIS IS FOR THE SAKE OF TESTING LANG !!
                userIdTextField.delete(0, "end")
                passwordTextField.delete(0, "end")
                messagebox.showwarning("ERROR", str(e.args[0]))
                print(userID)
                # controller.show_frame(MainMenu)  # TODO COMMENT OUT THIS LINE THIS IS FOR THE SAKE OF TESTING LANG !!
                # controller.frames[Game].focus_set()
            else:
                print("log in OK:) ! welcome " + str(userId) + "! ")
                global userID
                userID = userId
                controller.show_frame(MainMenu)
                controller.frames[Game].focus_set()

        logInButton = tk.Button(self, text="ENTER", command=verify)
        logInButton.place(x=180, y=90)


class MainMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.shutdown_flag = threading.Event() #pang shut down ng thread kung nagstart na yung timer.starrt
        # wordyLabel = tk.Label(self, text="WORDY", bg='green')
        self.wordyLabel = tk.Label(self, text="WORDY", font=("Impact", 56))
        self.wordyLabel.place(x=170, y=50, anchor="center")

        # wordyLabel.configure(anchor="center")

        # play game button is clicked, run two threads
        def playGameButton():
            try:
                playGameThread = threading.Thread(target=playGame)
                openCountdownThread = threading.Thread(target=open_countdown)

                playGameThread.start()
                openCountdownThread.start()

                self.threads = [playGameThread, openCountdownThread]

            except Exception as e:
                traceback.print_exc()
                print(str(e.args[0]))

        def close_countdown_thread():
            self.shutdown_flag.set()

        def playGame():
            try:
                global userID, gameID
                print("USER ID: ", userID)
                gameID = eo.playGame(int(userID))
                print("GAME ID: " + str(gameID))
            except Exception as e:
                traceback.print_exc()
                print(e)
                print("returning to main menu...")
                warningMsg(e)
            else:
                # put code ng game here
                if gameID != 0:
                    setGameID(gameID)
                    controller.show_frame(Game)
                    controller.frames[Game].focus_set()
                else:
                    messagebox.showwarning("sad :(", "no other players have joined the game\nreturning to menu")

        def open_countdown():
            try:
                self.playGameBTN.config(state="disabled")
                print("exec b")
                new = Toplevel(self)
                new.geometry("350x150")
                new.title("MATCH")

                # WAIT MUNA <1 SECOND KASI 0 MAKUKUHA NA ANO NUN TIMER PAG FIRST TYM HEHEH
                time.sleep(0.2)
                print("GID" + str(gameID))
                timerStart = eo.getTimer(int(gameID), "g")

                def close_window():
                    self.playGameBTN.config(state="normal")
                    print("window closed")
                    new.destroy()

                def countToZero(count):
                    timer_label.config(text=str(count - 1))  # for some reason delayed yung first countdown kaya -1
                    if count > 0:
                        new.after(1000, lambda: countToZero(count - 1))
                    else:
                        close_window()

                timer_label = Label(new, text=str(timerStart), font=("Arial", 54, "bold"))
                timer_label.pack()

                new.after(1000, lambda: countToZero(timerStart))

                print(timerStart)
                timer = threading.Timer(timerStart, close_countdown_thread)
                timer.start()

            except Exception as e:
                traceback.print_exc()
                print(e)
                warningMsg(e)

        def showTopP():
            print("top p")

        def showTopW():
            print("top w")

        self.playGameBTN = tk.Button(self, text="PLAY GAME", command=playGameButton, font=("Helvetica", 20))
        self.playGameBTN.place(x=170, y=190, anchor='center')

        self.topPlayersBTN = tk.Button(self, text="TOP PLAYERS", command=showTopP, font=("Helvetica", 10))
        self.topPlayersBTN.place(x=10, y=270, anchor='w')

        self.topWordsBTN = tk.Button(self, text="TOP WORDS", command=showTopW, font=("Helvetica", 10))
        self.topWordsBTN.place(x=10, y=310, anchor='w')


class Game(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        global gameID
        self.textWordy = tk.Label(self, fg="#333333", justify="center", text="", font=Font)
        self.textWordy.place(x=130, y=280)

        self.readyTimer = 10

        self.initLetters()
        self.fixLettersPlace()
        self.initLabels()
        self.pack()
        self.focus_set()
        self.bind("<Key>", self.handle_key)
        self.focus_set()
        self.stack = []

        self.roundNum = 0
        self.numberOfWins = 0

        self.letters = []  # ALL letters per round
        self.availableLetters = []  # temporary char array to place mga hindi pa nagamit ni user na letters

        # threading.Thread(target=self.checkRounds).start()

    def checkRounds(self):
        if gameID != 0 or not None:
            print("ROUND:" + str(self.roundNum) + " OF GAME: " + str(gameID))
            self.roundNum = eo.getRound(gameID)
            self.roundNumLab.config(text=str(self.roundNum))

    def updateWinsNum(self):
        self.winsNum.config(text=str(self.numberOfWins))

    # code executed when ready button is clicked ^^
    def readyBtnClicked(self):
        self.roundNum = eo.getRound(gameID)
        print("STARTING - ROUND: " + str(self.roundNum) + " OF GAME: " + str(gameID))
        self.readyBTN.config(state="disabled")
        eo.ready(int(userID), int(gameID))

        timer_thread = threading.Thread(target=self.timer)
        timer_thread.start()

    # before round, after ready btn is clicked
    def timer(self):
        print("PRE ROUND COUNTDOWN STARTED")
        global gameID
        self.letters = list(eo.requestLetters(int(gameID)))

        def update_timer_label():
            print("THREAD TIMER START")
            print(int(eo.getTimer(int(gameID), "r")))
            time.sleep(1)
            self.readyTimer = eo.getTimer(int(gameID), "r")
            print(self.readyTimer)
            while self.readyTimer > 0:
                print("NAGTRUE")
                self.readyTimer = eo.getTimer(int(gameID), "r")
                print("READY TIMER: "+str(self.readyTimer))
                self.timerLabel.config(text=str(self.readyTimer))
                time.sleep(1)

            print("nagtapos na")
            self.readyTimer = 10
            self.timerLabel.config(text=str(self.readyTimer))
            self.afterReadyTimer()
            return

        update_timer_label()

    def afterReadyTimer(self):
        print("READY TIMER FINISH, ROUND START NA")
        self.checkRounds()
        self.roundTimer()
        self.update_label_texts(self.letters)
        self.availableLetters = self.letters.copy()

    # the 10 second round timer yung sa round itself
    def roundTimer(self):

        def after():
            print("ROUND IS OVER!!")
            self.initLetters()
            self.checkRounds()
            time.sleep(3)
            print("WINNER OF THE ROUND: " + str(eo.checkWinner(gameID)))

            # TRUE IF WIN
            print(str(userID) == str(eo.checkWinner(gameID)))

            if str(eo.checkWinner(int(gameID))) == str(userID):
                self.numberOfWins += 1
                print("YOU WON THE ROUND, WINS: " + str(self.numberOfWins))
                self.updateWinsNum()

            if str(eo.checkWinner(int(gameID))) == str("Game Over"):
                print("GAME OVER!")
                if str(eo.checkMatchStatus(int(gameID))) == str(userID):
                    print("YOU WON THE GAME")
                    print("\n\n")
                else:
                    print("YOU LOST, THE WINNER IS: " + str(eo.checkMatchStatus(int(gameID))))
                    print("\n\n")

            print()
            match_status = str(eo.checkMatchStatus(int(gameID)))
            print(match_status + " << this is match status")

            if str(eo.checkMatchStatus(int(gameID))) != "" and str(eo.checkMatchStatus(int(gameID))) != "ready":
                messagebox.showinfo("WORDY", "GAME OVER! ")
                self.controller.show_frame(MainMenu)
                self.controller.frames[MainMenu].focus_set()

            print("PRESS READY!!")
            self.readyBTN.config(state="normal")

        self.readyBTN.config(state="disabled")
        # eo.getTimer(gameID, "round")
        # time.sleep(0.1)
        roundTimer = eo.getTimer(int(gameID), "round")
        print()
        print("ROUND TIMER START AT: " + str(roundTimer))

        timer = threading.Timer(roundTimer, after)
        timer.start()

    def handle_key(self, event):
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

    # update letters in gui with random letters given by the server
    def update_label_texts(self, char_array):
        label_texts = [getattr(self, f"letter{i}") for i in range(1, 18)]
        for i in range(len(char_array)):
            label_texts[i].configure(text=char_array[i].upper())

    def initLetters(self):
        self.letter1 = tk.Label(self, fg="#333333", justify="center", text="1", font=FontLetters)
        self.letter2 = tk.Label(self, fg="#333333", justify="center", text="2", font=FontLetters)
        self.letter3 = tk.Label(self, fg="#333333", justify="center", text="3", font=FontLetters)
        self.letter4 = tk.Label(self, fg="#333333", justify="center", text="4", font=FontLetters)
        self.letter5 = tk.Label(self, fg="#333333", justify="center", text="5", font=FontLetters)
        self.letter6 = tk.Label(self, fg="#333333", justify="center", text="6", font=FontLetters)
        self.letter7 = tk.Label(self, fg="#333333", justify="center", text="7", font=FontLetters)
        self.letter8 = tk.Label(self, fg="#333333", justify="center", text="8", font=FontLetters)
        self.letter9 = tk.Label(self, fg="#333333", justify="center", text="9", font=FontLetters)
        self.letter10 = tk.Label(self, fg="#333333", justify="center", text="10", font=FontLetters)
        self.letter11 = tk.Label(self, fg="#333333", justify="center", text="11", font=FontLetters)
        self.letter12 = tk.Label(self, fg="#333333", justify="center", text="12", font=FontLetters)
        self.letter13 = tk.Label(self, fg="#333333", justify="center", text="13", font=FontLetters)
        self.letter14 = tk.Label(self, fg="#333333", justify="center", text="14", font=FontLetters)
        self.letter15 = tk.Label(self, fg="#333333", justify="center", text="15", font=FontLetters)
        self.letter16 = tk.Label(self, fg="#333333", justify="center", text="16", font=FontLetters)
        self.letter17 = tk.Label(self, fg="#333333", justify="center", text="17", font=FontLetters)

    def fixLettersPlace(self):
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

    def initLabels(self):
        self.roundLabel = tk.Label(self, fg="#333333", justify="left", text="ROUND: ")
        self.roundLabel.place(x=10, y=110, width=70, height=25)
        self.roundNumLab = tk.Label(self, fg="#333333", justify="left", text="0")
        self.roundNumLab.place(x=70, y=110, width=30, height=25)
        self.winsLabel = tk.Label(self, fg="#333333", justify="left", text="WINS: ")
        self.winsLabel.place(x=10, y=150, width=70, height=25)
        self.winsNum = tk.Label(self, fg="#333333", justify="left", text="0")
        self.winsNum.place(x=70, y=150, width=30, height=25)
        self.timerLabel = tk.Label(self, fg="#333333", justify="center", text="10")
        self.timerLabel.place(x=20, y=260, width=70, height=25)
        self.gameIDLabel = tk.Label(self, fg="#333333", justify="left", text=str(gameID))
        self.gameIDLabel.place(x=10, y=10, width=70, height=25)
        self.readyBTN = tk.Button(self, text="READY", command=self.readyBtnClicked)  # test lang, will change
        self.readyBTN.place(x=30, y=300)


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        window = tk.Frame(self)
        window.pack()
        window.pack_propagate(False)

        Font_tuple = ("Comic Sans MS", 20, "bold")

        self.resizable(False, False)
        # self.wm_attributes("-transparentcolor", 'green')

        window.grid_rowconfigure(0, minsize=350)
        window.grid_columnconfigure(0, minsize=350)

        self.frames = {}
        for F in (LogIn, MainMenu, Game):
            frame = F(window, self)
            self.frames[F] = frame
            self.title("WORDY - GROUP 7 :D")
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

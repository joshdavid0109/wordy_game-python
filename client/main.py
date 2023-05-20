import random
import threading
import time as t
import time
import tkinter as tk
import traceback
import sched
from tkinter import messagebox, ttk
from tkinter import *
from tkinter.ttk import *

from concurrent.futures import ThreadPoolExecutor

import omniORB
from omniORB import CORBA

import Connector
import WordyGame
from Connector import daConnector
import WordyGame_idl

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
roundLetters = []
global check
global a

timer_lock = threading.Lock()


def getCon():
    global connector, eo
    connector = daConnector("localhost", 9999)  # should be read sa config
    connector.connect()
    eo = Connector.eo

def setGameID(num):
    global gameID
    gameID = num

    def __str__(self):
        return f"Rank: {self.rank}, Username: {self.username}, Wins: {self.wins}"

    def getRank(self):
        return self.rank

    def getUName(self):
        return self.username

    def getWins(self):
        return self.wins


class TopWord:
    def __init__(self, username, word):
        self.username = username
        self.word = word

    def __str__(self):
        return f"Player Name: {self.username}, Word: {self.word}"

    def getUserName(self):
        return self.username

    def getWord(self):
        return self.word


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
            username = userIdTextField.get()
            password = passwordTextField.get()
            try:
                getCon()
                eo.login(username, password)
            except WordyGame.InvalidCredentials as e:
                messagebox.showwarning("ERROR", str(e.args[0]))
                return
            except WordyGame.UserAlreadyLoggedIn as e:
                messagebox.showwarning("ERROR", str(e.args[0]))
                return
            except WordyGame.InvalidPassword as e:
                messagebox.showwarning("ERROR", str(e.args[0]))
                return
            except Exception as e:
                messagebox.showwarning("ERROR", "SERVER IS UNAVAILABLE, \nERROR CODE: " + str(e.args[0]))
                return
            else:
                print("YOU HAVE LOGGED IN AS: "+username+"\nUSER ID: "+str(eo.getPlayerID(username)))
                global userID
                userID = eo.getPlayerID(username)
                controller.show_frame(MainMenu)
                controller.frames[Game].focus_set()
            finally:
                userIdTextField.delete(0, "end")
                passwordTextField.delete(0, "end")

        logInButton = tk.Button(self, text="ENTER", command=verify)
        logInButton.place(x=180, y=90)


class MainMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.shutdown_flag = threading.Event()  # pang shut down ng thread kung nagstart na yung timer.starrt
        # wordyLabel = tk.Label(self, text="WORDY", bg='green')
        self.wordyLabel = tk.Label(self, text="WORDY", font=("Impact", 56))
        self.wordyLabel.place(x=170, y=50, anchor="center")
        self.topPlayersList = []

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
                userID = eo.getPlayerID(str(userID))
                print("USER ID: ", userID)
                gameID = eo.playGame((userID))
                print("GAME ID: " + str(gameID))
            except Exception as e:
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
                time.sleep(0.5)
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
            topPlayerList = eo.getTopPlayers()
            self.topPlayersList = []

            for player in topPlayerList:
                playerAsString = str(player)
                rs = playerAsString.index("rank=") + len("rank=")
                re = playerAsString.index(",", rs)
                rank = int(playerAsString[rs:re])
                us = playerAsString.index("username='") + len("username='")
                ue = playerAsString.index("'", us)
                username = playerAsString[us:ue]
                ws = playerAsString.index("wins=") + len("wins=")
                we = playerAsString.index(")", ws)
                wins = int(playerAsString[ws:we])
                top = WordyGame.TopPlayer(rank, username, wins)
                print(top)
                self.topPlayersList.append(top)

            top_players_window = tk.Toplevel()
            top_players_window.title("TOP PLAYERS")

            treeview = ttk.Treeview(top_players_window, columns=("Rank", "Username", "Wins"))
            treeview.pack()
            treeview.heading("#0", text="RANK")
            treeview.heading("#1", text="USERNAME")
            treeview.heading("#2", text="WINS")

            for player in self.topPlayersList:
                rank = player.rank
                username = player.username
                wins = player.wins
                treeview.insert("", "end", text=str(rank), values=(username, wins))

        def showTopW():
            print("top w")
            longestWords = eo.getLongestWords()
            self.longestWords = []

            for word in longestWords:
                wordAsString = str(word)
                us = wordAsString.index("username='") + len("username='")
                ue = wordAsString.index("'", us)
                username = wordAsString[us:ue]
                ws = wordAsString.index("word=") + len("word=")
                we = wordAsString.index(")", ws)
                wins = str(wordAsString[ws:we])
                top = TopWord(username, wins)
                print(top)
                self.longestWords.append(top)

            longest_words_window = tk.Toplevel()
            longest_words_window.title("LONGEST WORDS")

            treeview = ttk.Treeview(longest_words_window, columns=("Username", "Wins"))
            treeview.pack()
            treeview.heading("#0", text="USERNAME")
            treeview.heading("#1", text="WORDS")

            for word in self.longestWords:
                username = word.username
                word = word.word
                treeview.insert("", "end", text=str(username), values=(word))

        self.playGameBTN = tk.Button(self, text="PLAY GAME", command=playGameButton, font=("Helvetica", 20))
        self.playGameBTN.place(x=170, y=190, anchor='center')

        self.topPlayersBTN = tk.Button(self, text="TOP PLAYERS", command=showTopP, font=("Helvetica", 10))
        self.topPlayersBTN.place(x=10, y=270, anchor='w')

        self.topWordsBTN = tk.Button(self, text="TOP WORDS", command=showTopW, font=("Helvetica", 10))
        self.topWordsBTN.place(x=10, y=310, anchor='w')


class Game(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

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

        self.controller = controller
        global gameID
        self.timerLabel = None
        self.textWordy = tk.Label(self, fg="#333333", justify="center", text="", font=Font)
        self.textWordy.place(x=130, y=280)

        self.readyTimer = 10

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

    def run(self):
        global win
        global check

        if gameID != 0:
            check = False
            while not check:
                # print("this is running in the background")
                win = eo.checkMatchStatus(gameID)
                if win != "" and win != "ready":
                    check = True
                    self.roundNumLab.config(text="0")
                    self.winsLabel.config(text="0")
                    self.roundTimerLabel.config(text="0")
                    messagebox.showinfo("WORDY", "GAME OVER! ")
                    self.controller.show_frame(MainMenu)
                    self.controller.frames[MainMenu].focus_set()

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
        global gameID, roundLetters

        print("THREAD TIMER START")
        print(int(eo.getTimer(int(gameID), "r")))
        time.sleep(1)

        class reqLetters(threading.Thread):
            def __init__(self, thread_name, thread_ID, letters, game):
                threading.Thread.__init__(self)
                global roundLetters
                roundLetters = letters
                self.thread_name = thread_name
                self.thread_ID = thread_ID
                self.game = game

            def run(self):
                global roundLetters
                roundLetters = list(eo.requestLetters(int(gameID)))
                # print("SHOULD BE")
                # print(roundLetters)
                # self.game.update_label_texts(roundLetters)

        class timerThread(threading.Thread):
            def __init__(self, thread_name, thread_ID, timerLabel):
                threading.Thread.__init__(self)
                self.timerLabel = timerLabel
                self.thread_name = thread_name
                self.thread_ID = thread_ID

                # helper function to execute timer countdown // check tester.py

            def run(self):
                global a
                a = False
                # global roundLetters
                # roundLetters = list(eo.requestLetters(int(gameID)))
                while not a:
                    timez = eo.getTimer(gameID, "r")
                    print(timez)
                    self.timerLabel.config(text=str(timez))
                    t.sleep(1)
                    timez -= 1
                    if timez < 0:
                        a = True

        thread1 = timerThread("timer", 1000, self.timerLabel)

        thread2 = reqLetters("reqLetters", 2, self.letters, self)
        thread2.start()
        thread1.start()

        thread1.join()

        print("updating table")
        print(roundLetters)
        print("x x")

        self.letters = roundLetters
        # self.update_label_texts(roundLetters)
        self.availableLetters = roundLetters
        self.readyTimer = 10
        self.timerLabel.config(text=str(self.readyTimer))
        self.afterReadyTimer()
        threading.Thread(target=self.run()).start()
        threading.Thread(target=self.afterReadyTimer()).start()
        # self.afterReadyTimer()
        return

    def afterReadyTimer(self):
        print("READY TIMER FINISH, ROUND START NA")
        self.checkRounds()
        self.roundTimer()
        global roundLetters
        roundLetters = list(eo.requestLetters(int(gameID)))
        self.update_label_texts(roundLetters)
        self.availableLetters = roundLetters.copy()

    # the 10 second round timer yung sa round itself
    def roundTimer(self):

        def roundCountDown():
            self.update_label_texts(roundLetters)
            rc = False
            # print("this is running in the background1")
            while not rc:
                timezz = eo.getTimer(gameID, "round")
                print(timezz)
                self.roundTimerLabel.config(text=str(timezz))
                t.sleep(1)
                timezz -= 1
                if timezz < 0:
                    rc = True
                    after()

        def after():
            print("ROUND IS OVER!!")
            self.checkRounds()
            self.update_label_texts_to_default()
            time.sleep(3)
            winnerID = str(eo.checkWinner(gameID))
            print("WINNER OF THE ROUND: " + winnerID)

            # TRUE IF WIN
            print(str(userID) == str(winnerID))

            if winnerID == str(userID):
                self.numberOfWins += 1
                print("YOU WON THE ROUND, WINS: " + str(self.numberOfWins))
                self.updateWinsNum()

            if winnerID == str("Game Over"):
                print("GAME OVER!")
                if str(eo.checkMatchStatus(int(gameID))) == str(userID):
                    print("YOU WON THE GAME")
                    print("\n\n")
                else:
                    print("YOU LOST, THE WINNER IS: " + str(eo.checkMatchStatus(int(gameID))))
                    print("\n\n")

            print()
            global roundLetters
            roundLetters = []
            match_status = str(eo.checkMatchStatus(int(gameID)))
            print(match_status + " << this is match status")
            self.readyBTN.config(state="normal")

            global a
            if a or check:
                return

            print("PRESS READY!!")

        self.readyBTN.config(state="disabled")
        # eo.getTimer(gameID, "round")
        # time.sleep(0.1)
        roundTimer = eo.getTimer(int(gameID), "round")
        print()
        global a

        print("ROUND TIMER START AT: " + str(roundTimer))

        if roundTimer != 10:
            threading.Thread(target=roundCountDown()).start()

    def handle_key(self, event):
        if event.keysym == "Return":
            try:
                entered_word = self.textWordy.cget("text")
                print("WORD SENT  : ", entered_word)
                self.textWordy.config(text="")
                self.availableLetters = roundLetters.copy()
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
        self.availableLetters = roundLetters.copy()
        self.textWordy.after(1, self.textWordy.update())

    # update letters in gui with random letters given by the server
    def update_label_texts(self, char_array):
        print("UPDATING GUI TEXT WITH: " + str(char_array))
        label_texts = [getattr(self, f"letter{i}") for i in range(1, 18)]
        for i in range(len(char_array)):
            label_texts[i].configure(text=char_array[i].upper())

    def update_label_texts_to_default(self):
        label_texts = [getattr(self, f"letter{i}") for i in range(1, 18)]
        for i in range(17):
            label_texts[i].configure(text=str(i))

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
        self.roundTimerLabel = tk.Label(self, fg="#333333", justify="center", text="10")
        self.roundTimerLabel.place(x=200, y=10, width=70, height=50)
        self.gameIDLabel = tk.Label(self, fg="#333333", justify="left", text=10)
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

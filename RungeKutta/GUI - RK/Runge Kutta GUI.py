import ctypes
from tkinter import *


class RungeKuttaGUI:
    def __init__(self, master):
        # Window design
        self.master = master
        master.title("Runge Kutta 4th Order")
        master.config(bg="#4F5251")
        master.geometry("1200x600")
        master.resizable(width=FALSE, height=FALSE)
        master.wm_iconbitmap(default='RK4logon.ico')

        titletext = Label(master, text="Runge Kutta 4th Order",
                          bg="#4F5251", fg="white", font="time 20 bold")
        titletext.pack(side='top')

        myappid = 'Isa-Carlos.RungeKutta.RK4.1-1'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        self.button_close = Button(master, text='Close', bg='black', fg="white", command=master.quit)
        self.button_close.pack()


root = Tk()
rk = RungeKuttaGUI(root)
root.mainloop()

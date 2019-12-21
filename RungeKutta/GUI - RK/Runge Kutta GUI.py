import ctypes
from tkinter import *
from RungeKutta.FirstOrderODE.RK4 import *
import numpy as np
from math import *


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

        label_equation = Label(master, text='Enter Equation')
        label_equation.pack()

        self.equation = StringVar()
        self.equation.set('2*t -3*y + 1')
        equantion_entry = Entry(master, width=12, textvariable=self.equation)
        equantion_entry.pack()

        self.label_parameters = Label(master, text='Parameters')
        self.label_parameters.pack()

        # ti parameter
        self.label_ti = Label(master, text='ti:')
        self.label_ti.pack(side='left')
        self.ti = DoubleVar()
        self.ti.set('1.0')
        self.entry_ti = Entry(master, width=6, textvariable=self.ti)
        self.entry_ti.pack(side='left')

        # yi parameter
        self.label_yi = Label(master, text='yi:')
        self.label_yi.pack(side='left')
        self.yi = DoubleVar()
        self.yi.set('5.0')
        self.entry_yi = Entry(master, width=6, textvariable=self.yi)
        self.entry_yi.pack(side='left')

        # done parameter
        self.label_done = Label(master, text='done:')
        self.label_done.pack(side='left')
        self.done = DoubleVar()
        self.done.set('1.5')
        self.entry_done = Entry(master, width=6, textvariable=self.done)
        self.entry_done.pack(side='left')

        # h parameter
        self.label_h = Label(master, text='h:')
        self.label_h.pack(side='left')
        self.h = DoubleVar()
        self.h.set('0.1')
        self.entry_h = Entry(master, width=6, textvariable=self.h)
        self.entry_h.pack(side='left')

        # computed
        compute = Button(master, text=' equals', command=self.solve, relief='flat')
        compute.pack(side='left')

        self.computed = DoubleVar()
        self.label_computed = Label(master, textvariable=self.computed, width=20)
        self.label_computed.pack(side='left')

        self.button_close = Button(master, text='Close', bg='black', fg="white", command=master.quit)
        self.button_close.pack()

    def f(self, t, y):
        # ODE = (self.equation.get())
        ODEtemp = 2 * t - 3 * y + 1 #While developing a correct form for entry equation
        return ODEtemp

    def solve(self):
        self.rk4 = RK4(self.f)
        computed = self.rk4.solve(np.double(self.ti.get()), np.double(self.yi.get()), np.double(self.done.get()),
                                  np.double(self.h.get()))
        self.computed.set(computed)

root = Tk()
rk = RungeKuttaGUI(root)
root.mainloop()

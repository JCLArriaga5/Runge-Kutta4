import ctypes
# noinspection PyCompatibility
from tkinter import *
import matplotlib
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from RungeKutta.FirstOrderODE.RK4 import *
import numpy as np


class RungeKuttaGUI:
    def __init__(self, master):
        # Window design
        self.master = master
        self.fig = Figure(figsize=(5, 4), dpi=100, facecolor='#4F5251')
        self.rk4 = RK4(self.f)
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

        titleODE = Label(master, text="Ordinary differential equations of the first order",
                         bg="#4F5251", fg="white", font="time 12 bold")
        titleODE.place(x=60, y=40)

        label_equation = Label(master, text='Enter equation: dy/dt =', bg='#689E8C')
        label_equation.place(x=60, y=80, width=140, height=30)

        self.equation = StringVar()
        self.equation.set('2*t -3*y + 1')
        equantion_entry = Entry(master, width=12, textvariable=self.equation)
        equantion_entry.place(x=200, y=80, width=100, height=30)

        self.label_parameters = Label(master, text='Parameters', bg='#476B5F')
        self.label_parameters.place(x=110, y=120, width=100, height=30)

        # ti parameter
        self.label_ti = Label(master, text='ti:', bg='#689E8C')
        self.label_ti.place(x=60, y=160, width=30, height=20)
        self.ti = DoubleVar()
        self.ti.set('1.0')
        self.entry_ti = Entry(master, width=7, textvariable=self.ti)
        self.entry_ti.place(x=90, y=160, width=40, height=20)

        # yi parameter
        self.label_yi = Label(master, text='yi:', bg='#689E8C')
        self.label_yi.place(x=130, y=160, width=30, height=20)
        self.yi = DoubleVar()
        self.yi.set('5.0')
        self.entry_yi = Entry(master, width=7, textvariable=self.yi)
        self.entry_yi.place(x=160, y=160, width=40, height=20)

        # done parameter
        self.label_done = Label(master, text='done:', bg='#689E8C')
        self.label_done.place(x=200, y=160, width=30, height=20)
        self.done = DoubleVar()
        self.done.set('1.5')
        self.entry_done = Entry(master, width=7, textvariable=self.done)
        self.entry_done.place(x=230, y=160, width=40, height=20)

        # h parameter
        self.label_h = Label(master, text='h:', bg='#689E8C')
        self.label_h.place(x=270, y=160, width=30, height=20)
        self.h = DoubleVar()
        self.h.set('0.1')
        self.entry_h = Entry(master, width=7, textvariable=self.h)
        self.entry_h.place(x=300, y=160, width=40, height=20)

        # computed
        compute = Button(master, text='Compute', command=self.solve, relief='flat', bg='#989E9C')
        compute.place(x=110, y=190, width=80, height=30)

        self.computed = DoubleVar()
        self.label_computed = Label(master, textvariable=self.computed, width=20)
        self.label_computed.place(x=190, y=190, width=150, height=30)

        # Graph
        graph_label = Label(master, text='Graph the function with respect to time',
                            bg="#4F5251", fg="white", font="time 12 bold")
        graph_label.place(x=800, y=40)
        graph_button = Button(master, text='Graph Function', command=self.graph, relief='flat', bg='#989E9C')
        graph_button.place(x=800, y=80, width=200, height=20)


        self.button_close = Button(master, text='Close', bg='#E1EBE7', fg="black", command=master.quit())
        self.button_close.place(x=1000, y=500, width=80, height=30)

    # noinspection PyUnusedLocal
    def f(self, t, y):
        """

                    @param t: Variable needed for the function imported from RK4
                    @param y: Variable needed for the function imported from RK4
                    """
        ODE = eval(self.equation.get())
        return ODE

    def solve(self):
        computed = self.rk4.solve(np.double(self.ti.get()), np.double(self.yi.get()), np.double(self.done.get()),
                                  np.double(self.h.get()))
        self.computed.set(computed)

    def graph(self):
        # Show in IDE
        self.rk4.graph('r--', label="Function y")
        # Show in GUI
        ts, ys = self.rk4.graphvalues()
        ax = self.fig.add_subplot(111)
        ax.set_title("Graph of the function")
        ax.plot(ts, ys, 'r--')
        ax.legend("y")
        ax.grid()
        ax.set_xlabel("$ t $")
        ax.set_ylabel("$ y(t) $")


        canvas = FigureCanvasTkAgg(self.fig, self.master)
        canvas.draw()
        canvas.get_tk_widget().place(x=600, y=120)



root = Tk()
rk = RungeKuttaGUI(root)
root.mainloop()

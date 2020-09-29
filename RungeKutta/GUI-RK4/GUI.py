#!/usr/bin/python3
#-*- coding: utf-8 -*-

from __future__ import division
import ctypes
import sys
import os

if eval(sys.version[0]) < 3: # For check python version
    raise ValueError('GUI Code requires Python3 or higher')
else:
    from tkinter import *

abspath = os.getcwd()
dirpath = abspath.replace('/RungeKutta/GUI-RK4', '/')
sys.path.append(dirpath)
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.figure import Figure
from RungeKutta.RK4 import *
import numpy as np


class RungeKuttaGUI:
    def __init__(self, master):
        # Window design
        self.master = master
        gui_bg = "#4F5251"

        master.title("Runge Kutta 4th Order")
        master.config(bg=gui_bg)
        master.geometry("1200x600")
        master.resizable(width=FALSE, height=FALSE)
        # Detect OS for icon
        self.OS = sys.platform
        if self.OS == 'linux' or 'darwin':
            icon = PhotoImage(file=abspath + '/images/RK4-logo.png')
            master.tk.call('wm', 'iconphoto', master._w, icon)
        if self.OS == 'win32':
            # icon = PhotoImage(file='images/RK4-logo.png')
            # master.tk.call('wm', 'iconphoto', master._w, icon)

            master.wm_iconbitmap(default=abspath + '/images/RK4-logo.ico') # For Windows system show icon
            myappid = 'Isa-Carlos.RungeKutta.RK4.1-1'  # arbitrary string
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        # Initialize graph parameters
        self.fig = Figure(figsize=(5, 4), dpi=100, facecolor=gui_bg)
        self.fig.clf()
        self.ax = self.fig.add_subplot(111, facecolor=gui_bg)
        self.canvas = FigureCanvasTkAgg(self.fig, self.master)
        self.canvas.draw()

        # Initialize Runge-Kutta firstorder ode
        self.rk4 = firstorder(self.f)
        self.ts = 0
        self.ys = 0

        titletext = Label(master, text="Runge Kutta 4th Order",
                          bg=gui_bg, fg="white", font="time 20 bold")
        titletext.pack(side='top')

        titleODE = Label(master, text="Ordinary differential equations of the first order",
                         bg=gui_bg, fg="white", font="time 12 bold").place(x=60, y=40)

        label_equation = Label(master, text='Enter equation: dy/dt =', bg='#689E8C').place(x=110, y=80, width=180, height=40)

        self.equation = StringVar()
        self.equation.set('2*t -3*y + 1')
        equantion_entry = Entry(master, width=12, textvariable=self.equation).place(x=290, y=80, width=150, height=40)

        self.label_parameters = Label(master, text='Parameters', bg='#476B5F').place(x=225, y=130, width=100, height=40)

        # ti parameter
        self.label_ti = Label(master, text='ti:', bg='#689E8C').place(x=110, y=170, width=40, height=25)
        self.ti = DoubleVar()
        self.ti.set('1.0')
        self.entry_ti = Entry(master, width=7, textvariable=self.ti).place(x=150, y=170, width=40, height=25)

        # yi parameter
        self.label_yi = Label(master, text='yi:', bg='#689E8C').place(x=190, y=170, width=40, height=25)
        self.yi = DoubleVar()
        self.yi.set('5.0')
        self.entry_yi = Entry(master, width=7, textvariable=self.yi).place(x=220, y=170, width=40, height=25)

        # done parameter
        self.label_done = Label(master, text='done:', bg='#689E8C').place(x=260, y=170, width=40, height=25)
        self.done = DoubleVar()
        self.done.set('1.5')
        self.entry_done = Entry(master, width=7, textvariable=self.done).place(x=300, y=170, width=40, height=25)

        # h parameter
        self.label_h = Label(master, text='h:', bg='#689E8C').place(x=340, y=170, width=40, height=25)
        self.h = DoubleVar()
        self.h.set('0.1')
        self.entry_h = Entry(master, width=7, textvariable=self.h).place(x=380, y=170, width=40, height=25)

        # computed
        compute = Button(master, text='Compute', command=self.solve, relief='raised', bg='#989E9C').place(x=180, y=200, width=80, height=30)

        self.computed = DoubleVar()
        self.label_computed = Label(master, textvariable=self.computed, width=20).place(x=260, y=200, width=150, height=30)

        # Graph
        graph_label = Label(master, text='Graph the solution with respect to variable t',
                            bg="#4F5251", fg="white", font="time 12 bold").place(x=700, y=40)
        graph_button = Button(master, text='Graph Function', command=self.graph, relief='raised', bg='#989E9C').place(x=800, y=80, width=200, height=20)

        self.button_close = Button(master, text='Close', bg='#E1EBE7', fg="black", command=self.exit).place(x=1100, y=500, width=80, height=30)

    # noinspection PyUnusedLocal
    def f(self, t, y):
        """
        Function to declare the function to solve in the RK4 library format.

        Parameters
        ----------
        t : Variable needed for the function imported from RK4.
        y : Variable needed for the function imported from RK4.

        Return
        ------
        ODE : Evaluation of the function entered in the GUI to be solved.
        """

        ODE = eval(self.equation.get())
        return ODE

    def solve(self):
        """
        To use the -solve- function of RK4 and solve the equation that was entered in the GUI
        """

        self.ax.clear()
        computed = self.rk4.solve(np.double(self.ti.get()), np.double(self.yi.get()), np.double(self.done.get()),
                                  np.double(self.h.get()))
        self.computed.set(computed)

    def graph(self):
        """
        To use the -graph- function of RK4 and display the graph solution
        """
        # Show in GUI
        # Obtain values of solution
        self.ts, self.ys = self.rk4.graphvalues()
        self.ax.clear()
        self.ax.set_title(r'Solution graph of $\frac{dy}{dt}$= %s' % self.equation.get())
        self.ax.plot(self.ts, self.ys, 'r')
        self.ax.legend('y')
        self.ax.grid()
        self.ax.set_xlabel("$ t $")
        self.ax.set_ylabel("$ y(t) $")

        self.canvas.draw()
        self.canvas.get_tk_widget().place(x=600, y=120)

        # Clear values for next solutions
        self.rk4.clearvalues()

    def exit(self):
        """
        Finish the GUI
        """

        self.master.quit()
        sys.exit()

def main():
    root = Tk()
    rk = RungeKuttaGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()

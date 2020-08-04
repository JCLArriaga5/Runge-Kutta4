#!/usr/bin/python3
#-*- coding: utf-8 -*-

from __future__ import division
import ctypes
import sys
import os

if eval(sys.version[0]) < 3: # For Python 2
    print('Error: Code requires Python3 or higher')
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

        master.title("Runge Kutta 4th Order")
        master.config(bg="#4F5251")
        master.geometry("1200x600-600-300")
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
        self.fig = Figure(figsize=(5, 4), dpi=100, facecolor='#4F5251')
        self.fig.clf()
        self.ax = self.fig.add_subplot(111, facecolor='#4F5251')
        self.canvas = FigureCanvasTkAgg(self.fig, self.master)
        self.canvas.draw()

        # Initialize Runge-Kutta firstorder ode
        self.rk4 = firstorder(self.f)
        self.ts = 0
        self.ys = 0

        titletext = Label(master, text="Runge Kutta 4th Order",
                          bg="#4F5251", fg="white", font="time 20 bold")
        titletext.pack(side='top')

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
        compute = Button(master, text='Compute', command=self.solve, relief='raised', bg='#989E9C')
        compute.place(x=110, y=190, width=80, height=30)

        self.computed = DoubleVar()
        self.label_computed = Label(master, textvariable=self.computed, width=20)
        self.label_computed.place(x=190, y=190, width=150, height=30)

        # Graph
        graph_label = Label(master, text='Graph the solution with respect to variable t',
                            bg="#4F5251", fg="white", font="time 12 bold")
        graph_label.place(x=700, y=40)
        graph_button = Button(master, text='Graph Function', command=self.graph, relief='raised', bg='#989E9C')
        graph_button.place(x=800, y=80, width=200, height=20)

        self.button_close = Button(master, text='Close', bg='#E1EBE7', fg="black", command=self.exit)
        self.button_close.place(x=1100, y=500, width=80, height=30)

    # noinspection PyUnusedLocal
    def f(self, t, y):
        """

            @param t: Variable needed for the function imported from RK4
            @param y: Variable needed for the function imported from RK4
        """
        ODE = eval(self.equation.get())
        return ODE

    def solve(self):
        self.ax.clear()
        computed = self.rk4.solve(np.double(self.ti.get()), np.double(self.yi.get()), np.double(self.done.get()),
                                  np.double(self.h.get()))
        self.computed.set(computed)

    def graph(self):
            # Show in GUI
        # Obtain values of solution
        self.ts, self.ys = self.rk4.graphvalues()
        self.ax.clear()
        self.ax.set_title(r'Solution graph of $\frac{dy}{dt}$= %s' % self.equation.get())
        self.ax.plot(self.ts, self.ys, 'r--')
        self.ax.legend('y')
        self.ax.grid()
        self.ax.set_xlabel("$ t $")
        self.ax.set_ylabel("$ y(t) $")

        self.canvas.draw()
        self.canvas.get_tk_widget().place(x=600, y=120)

        self.ts, self.ys = self.rk4.clearvalues()

    def exit(self):
        self.master.quit()
        sys.exit()

if eval(sys.version[0]) < 3: # For Python 2
    pass
else:
    root = Tk()
    rk = RungeKuttaGUI(root)
    root.mainloop()

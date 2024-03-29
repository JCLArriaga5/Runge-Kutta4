# !/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import division
import ctypes
import sys
import os

if eval(sys.version[0]) < 3: # For check python version
    raise ValueError('GUI code requires python3 or higher')
else:
    from tkinter import *
    from tkinter import messagebox
sys.path.append("..")

from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.figure import Figure
import matplotlib.image as mpimg
from rk4 import firstorder
import numpy as np
from math import sqrt, sin, cos, tan, pi, e, tau

class GUI:
    def __init__(self, master):
        # Window design
        self.master = master
        self.master.title("Runge Kutta 4th Order")
        self.master.config(bg='#4F5251')
        self.master.resizable(width=False, height=False)
        self.master.geometry("1200x600+80+80")

        # Detect OS for icon
        self.OS = sys.platform
        if self.OS == 'linux' or 'darwin':
            self.master.tk.call('wm', 'iconphoto', master._w,
                                PhotoImage(file='images/RK4-logo.png'))
        if self.OS == 'win32':
            self.master.tk.call('wm', 'iconphoto', master._w,
                                PhotoImage(file='images/RK4-logo.png'))
            self.master.iconbitmap('images/RK4-logo.ico')

        # Initialize graph parameters
        self.fig = Figure(figsize=(7, 4), dpi=110, facecolor='#4F5251')
        self.fig.clf()
        self.ax = self.fig.add_subplot(111, facecolor='#4F5251')
        self.canvas = FigureCanvasTkAgg(self.fig, master)
        self.canvas.get_tk_widget().place(x=450, y=100)
        self.canvas.draw()

        titletext = Label(master, text="Runge Kutta 4th Order",
                          bg='#4F5251', fg="white", font="time 20 bold")
        titletext.pack(side='top')

        titleODE = Label(master, text="Ordinary differential equations of the first order",
                         bg='#4F5251', fg="white", font="time 12 bold").place(x=90, y=40)

        label_equation = Label(master, text='Enter equation: dy/dt =',
                               bg='#689E8C').place(x=110, y=80, width=180, height=40)

        self.ts = self.ys = []
        self.eqn = StringVar()
        self.eqn.set('2 * t - 3 * y + 1')
        eqn_entry = Entry(self.master, width=12, justify='center',
                                textvariable=self.eqn).place(x=290, y=80, width=150, height=40)

        self.label_parameters = Label(self.master, text='Parameters',
                                      bg='#476B5F').place(x=225, y=130, width=100, height=40)

        # ti parameter
        self.label_ti = Label(self.master, text='ti :',
                              bg='#689E8C').place(x=110, y=170, width=40, height=25)
        self.ti = DoubleVar()
        self.ti.set('1.0')
        entry_ti = Entry(self.master, width=7, justify='center',
                              textvariable=self.ti).place(x=150, y=170, width=40, height=25)

        # yi parameter
        self.label_yi = Label(self.master, text='yi :',
                              bg='#689E8C').place(x=190, y=170, width=40, height=25)
        self.yi = DoubleVar()
        self.yi.set('5.0')
        entry_yi = Entry(self.master, width=7, justify='center',
                              textvariable=self.yi).place(x=220, y=170, width=40, height=25)

        # t parameter
        self.label_t = Label(self.master, text='t :',
                             bg='#689E8C').place(x=260, y=170, width=40, height=25)
        self.t = DoubleVar()
        self.t.set('1.5')
        entry_t = Entry(self.master, width=7, justify='center',
                             textvariable=self.t).place(x=300, y=170, width=40, height=25)

        # h parameter
        self.label_h = Label(self.master, text='h :',
                             bg='#689E8C').place(x=340, y=170, width=40, height=25)
        self.h = DoubleVar()
        self.h.set('0.01')
        entry_h = Entry(self.master, width=7, justify='center',
                             textvariable=self.h).place(x=380, y=170, width=40, height=25)

        # computed
        compute = Button(self.master, text='Compute', command=self.solve, relief='raised', bd=4,
                         bg='#989E9C').place(x=180, y=200, width=80, height=30)

        self.computed = DoubleVar()
        self.label_computed = Label(self.master, textvariable=self.computed,
                                    width=20).place(x=260, y=200, width=150, height=30)

        # Graph
        graph_button = Button(self.master, text='Graph', command=self.graph,
                              relief='raised', bd=4, bg='#989E9C').place(x=770, y=80, width=200, height=20)

        self.button_close = Button(self.master, text='Close', bg='#E1EBE7', fg="black",
                                   command=self.exit).place(x=1100, y=550, width=80, height=30)


    def solve(self):
        """
        To use the -solve- function of RK4 and solve the equation that was
        entered in the GUI
        """

        # Initialize Runge-Kutta firstorder ode
        methd = firstorder(self.eqn.get())
        r = methd.solve(np.double(self.ti.get()), np.double(self.yi.get()),
                        np.double(self.t.get()), np.double(self.h.get()))
        # Obtain values of solution
        self.ts, self.ys = methd.get_vals()
        self.computed.set(r)

    def graph(self):
        """
        Graph values of each iteration of method
        """

        if len(self.ts) == 0 or len(self.ts) == 0:
            # raise ValueError('You need to press computed first')
            messagebox.showerror('Error', 'You need to press computed first')
        else:
            self.ax.clear()
            self.ax.set_title('Solution graph')
            self.ax.scatter(self.ts[len(self.ts) - 1], self.ys[len(self.ys) - 1],
                            facecolor='k',
                            label=r'$ y({}) = {:.4f}$'.format(self.t.get(), self.ys[len(self.ys) - 1]))
            self.ax.set_xlabel("$ t $")
            self.ax.set_ylabel("$ y(t) $", rotation='horizontal', fontsize='large')
            self.ax.plot(self.ts, self.ys, '--r', label='Solution curve')
            self.ax.legend()
            self.ax.grid()

            self.canvas.draw()
            self.ts.clear()
            self.ys.clear()

    def exit(self):
        """
        Finish the GUI
        """

        self.master.quit()
        sys.exit()

def main():
    root = Tk()
    rk = GUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()

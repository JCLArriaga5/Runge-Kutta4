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
    import tkinter.scrolledtext as st

sys.path.append("..")

from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from rk4 import RK4

class GUI:
    def __init__(self, master: Tk):
        # Window design
        self.master = master
        self.master.title("Runge Kutta 4th Order")
        self.master.config(bg='#4F5251')
        self.master.resizable(width=False, height=False)
        self.master.geometry("1200x600+80+80")

        self.OS = sys.platform
        try:
            if self.OS in ['linux', 'darwin']:
                self.master.tk.call('wm', 'iconphoto', master._w,
                                    PhotoImage(file='images/RK4-logo.png'))
            elif self.OS == 'win32':
                self.master.tk.call('wm', 'iconphoto', master._w,
                                    PhotoImage(file='images/RK4-logo.png'))
                self.master.iconbitmap('images/RK4-logo.ico')
        except Exception:
            pass

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

        Label(master, text="Ordinary differential equations / N-Order systems",
              bg='#4F5251', fg="white", font="time 12 bold").place(x=90, y=40)

        Label(master, text='Equations (one per line):',
              bg='#689E8C').place(x=110, y=80, width=180, height=25)

        self.ts: list = []
        self.ys: list = []
        
        self.eqn_text = st.ScrolledText(self.master, width=20, height=4)
        self.eqn_text.place(x=110, y=110, width=180, height=60)
        self.eqn_text.insert(INSERT, "2 * t - 3 * y[0] + 1")

        self.label_parameters = Label(self.master, text='Parameters',
                                      bg='#476B5F').place(x=110, y=180, width=310, height=30)

        # ti parameter
        Label(self.master, text='ti :', bg='#689E8C').place(x=110, y=220, width=40, height=25)
        self.ti = DoubleVar()
        self.ti.set(1.0)
        Entry(self.master, width=7, justify='center', textvariable=self.ti).place(x=150, y=220, width=50, height=25)

        # yi parameter
        Label(self.master, text='yi(s) :', bg='#689E8C').place(x=210, y=220, width=50, height=25)
        self.yi_str = StringVar()
        self.yi_str.set("5.0")
        Entry(self.master, width=12, justify='center', textvariable=self.yi_str).place(x=260, y=220, width=80, height=25)

        # t parameter
        Label(self.master, text='t :', bg='#689E8C').place(x=110, y=250, width=40, height=25)
        self.t = DoubleVar()
        self.t.set(1.5)
        Entry(self.master, width=7, justify='center', textvariable=self.t).place(x=150, y=250, width=50, height=25)

        # h parameter
        Label(self.master, text='h :', bg='#689E8C').place(x=210, y=250, width=40, height=25)
        self.h = DoubleVar()
        self.h.set(0.01)
        Entry(self.master, width=7, justify='center', textvariable=self.h).place(x=250, y=250, width=50, height=25)

        # computed
        Button(self.master, text='Compute', command=self.solve, relief='raised', bd=4,
               bg='#989E9C').place(x=110, y=290, width=80, height=30)

        self.computed = StringVar()
        Label(self.master, textvariable=self.computed, anchor='w',
              width=20).place(x=200, y=290, width=220, height=30)

        # Graph
        Button(self.master, text='Graph', command=self.graph,
               relief='raised', bd=4, bg='#989E9C').place(x=770, y=80, width=200, height=20)

        Button(self.master, text='Close', bg='#E1EBE7', fg="black",
               command=self.exit).place(x=1100, y=550, width=80, height=30)


    def solve(self) -> None:
        try:
            eqns_raw = self.eqn_text.get("1.0", END).strip().split('\n')
            eqns = [eq.strip() for eq in eqns_raw if eq.strip() != '']
            
            if not eqns:
                messagebox.showerror('Error', 'Please enter at least one equation.')
                return

            yi_vals = [float(v.strip()) for v in self.yi_str.get().split(',')]

            if len(yi_vals) != len(eqns):
                messagebox.showerror('Error', f'Number of equations ({len(eqns)}) does not match number of initial conditions ({len(yi_vals)}).')
                return

            methd = RK4(eqns)
            r = methd.solve(np.double(self.ti.get()), yi_vals,
                            np.double(self.t.get()), np.double(self.h.get()))
            
            self.ts, self.ys = methd.get_vals()
            
            res_str = ", ".join([f"{val:.4f}" for val in r])
            self.computed.set(res_str)
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def graph(self) -> None:
        if len(self.ts) == 0 or len(self.ys) == 0:
            messagebox.showerror('Error', 'You need to press compute first')
        else:
            self.ax.clear()
            self.ax.set_title('Solution graph', color='white')
            self.ax.tick_params(colors='white')
            
            ys_array = np.array(self.ys)
            
            for i in range(ys_array.shape[1]):
                label_y = r'$y_{}({}) = {:.4f}$'.format(i, self.t.get(), ys_array[-1, i])
                self.ax.scatter(self.ts[-1], ys_array[-1, i], label=label_y, zorder=5)
                self.ax.plot(self.ts, ys_array[:, i], '--', label=f'Solution y_{i}')
                
            self.ax.set_xlabel("$ t $", color='white')
            self.ax.set_ylabel("$ y(t) $", rotation='vertical', fontsize='large', color='white')
            
            legend = self.ax.legend(facecolor='#4F5251', edgecolor='white')
            for text in legend.get_texts():
                text.set_color("white")
                
            self.ax.grid(color='gray', linestyle=':', linewidth=0.5)

            self.canvas.draw()

    def exit(self) -> None:
        self.master.quit()
        sys.exit()

def main():
    root = Tk()
    app = GUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()

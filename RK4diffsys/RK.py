from __future__ import division
import numpy as np
import matplotlib.pyplot as plt


class RK(object):
    def __init__(self, function1, function2):
        self.f = function1
        self.g = function2
        self.ts = []
        self.us = []
        self.vs = []

    def solve(self, ti, ui, vi, done, h):
        st = np.arange(ti, done, h)

        for _ in st:
            K1 = self.f(vi)
            m1 = self.g(vi, ui, ti)

            K2 = self.f(vi + m1 * h / 2)
            m2 = self.g(vi + m1 * h / 2, ui + K1 * h / 2, ti + h / 2)

            K3 = self.f(vi + m2 * h / 2)
            m3 = self.g(vi + m2 * h / 2, ui + K2 * h / 2, ti * h / 2)

            K4 = self.f(vi + m3 * h)
            m4 = self.g(vi + m3 * h, ui + K3 * h, ti + h)

            ui += (h / 6) * (K1 + 2 * K2 + 2 * K3 + K4)
            self.us.append(ui)

            vi += (h / 6) * (m1 + 2 * m2 + 2 * m3 + m4)
            self.vs.append(vi)

            ti += h
            self.ts.append(ti)
        return ui, vi

    def graph(self, *args, **kwargs):
        plt.title("Graph of functions")
        plt.plot(self.ts, self.us, *args, **kwargs)
        plt.plot(self.ts, self.vs, *args, **kwargs)
        plt.legend()
        plt.grid()
        plt.xlabel("$ t $")
        plt.ylabel("$ u:v $")

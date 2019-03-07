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


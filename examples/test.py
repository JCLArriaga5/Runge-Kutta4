# -*- coding: utf-8 -*-

import sys
import os

abspath = os.getcwd()
if sys.platform == 'linux' or 'darwin':
    dirpath = abspath.replace('/examples', '/')
if sys.platform == 'win32':
    dirpath = abspath.replace('\\examples', '\\')
sys.path.append(dirpath)

from RungeKutta.RK4 import *
from math import e

def main():
    # For 1st Order ODE
    def f(t, y):
        return 2 * t - 3 * y + 1

    # For 2nd Order ODE
    def f1(v):
        return v

    def g(v, u, t):
        return 4 * v + 6 * e ** (3 * t) - 3 * e ** (-t)

    r = firstorder(f)
    ti = 1
    yi = 5
    done = 1.5
    h = 0.1
    resultado = r.solve(ti, yi, done, h)
    print('ODE first order solution: 2 * t - 3 * y + 1')
    print("dy/dt =", resultado)
    print('Close window...')
    r.graph('r--', label="Function y")

    r2 = secondorder(f1, g)
    u_i = 1
    v_i = -1
    t_i = 0

    resultadosuv = r2.solve(t_i, u_i, v_i, done, h)
    print('ODE second order solution: 4 * v + 6 * e ** (3 * t) - 3 * e ** (-t)')
    print("u =", resultadosuv[0])
    print("v =", resultadosuv[1])
    print('Close window...')
    r2.graph()

if __name__ == '__main__':
    main()

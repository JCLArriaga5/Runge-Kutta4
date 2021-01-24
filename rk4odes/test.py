# -*- coding: utf-8 -*-

from rk4 import *
from math import e

def main():
    # For 1st Order ODE
    def f(t, y):
        return 2 * t - 3 * y + 1

    y = firstorder(f)
    ti = 1.0
    yi = 5.0
    t = 1.5
    h = 0.01
    r = y.solve(ti, yi, t, h)
    print('ODE first order solution: y\' = 2t - 3y + 1')
    print('y({}) = {}'.format(t, r))
    print('Close window...')
    y.graph('r--', label="Function y")

    # For 2nd Order ODE
    def g(u):
        return u

    def f(t, y, u):
        return - t * u - y

    rk = secondorder(f, g)
    ti = 0.0
    yi = 1.0
    ui = 2.0
    t = 0.2

    y, u = rk.solve(ti, yi, ui, t, h)
    print('ODE second order solution: y\'\' + ty\' + y = 0')
    print('y({}) = {}'.format(t, y))
    print('y\'({}) = {}'.format(t, u))
    print('Close window...')
    rk.graph()

if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-

from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
import ast
import re
import numexpr

def str2def(eqn):
    """
    Make function <string> to <def> for format in RK4 iterations.

    Example
    -------
    >>> fcn = '2 * t - 3 * y + 1'
    >>> fcn = str2def(fcn)
    >>> type(fcn)
    function
    >>>
    """

    if type(eqn) is not str:
        raise ValueError('Input must be string' )

    def f(t, y):
        """
        To evaluate equation with varibles (t, y).
        """

        chk = list(eqn)
        for idx in range(len(chk)):
            if chk[idx] == 't':
                chk[idx] = '% s' % t

            elif chk[idx] == 'y':
                chk[idx] = '% s' % y

        return numexpr.evaluate(''.join([w for w in chk]))

    return f

class firstorder:
    """
    Implementation of the Runge Kutta 4th method, to obtain the value
    of a first order differential equation given its initial conditions.
    -->  y' = f(t, y),   y(t0) = y0

    ...

    Attributes
    ----------
    function : def
        function of the differential equation to solve def f(t, y)

    Methods
    -------
    solve(ti, yi, t, h):
        Solve the ODE using RK4 and its initial values.

    graph(*args, **kwargs):
        Solution graph of each iteration.

    graphvalues():
        Return (t, y) values of each iteration.

    Example
    -------
    >>> from RungeKutta.RK4 import firstorder
    >>> def f(t, y):
    ...     return 2 * t - 3 * y + 1
    >>> y = firstorder(f)
    >>> ti = 1
    >>> yi = 5
    >>> t = 1.5
    >>> h = 0.01
    >>> r = y.solve(ti, yi, t, h)
    >>> print("dy/dt =", r)
    >>> y.graph('r--', label = "Function y")

    """

    def __init__(self, fcn):
        """
        Constructor

        Parameters
        ----------
        fcn : Function to solve f(t, y)
        """

        self.ts = []
        self.ys = []
        if not callable(fcn) and type(fcn) is str:
            self.f = str2def(fcn)
        elif callable(fcn):
            self.f = fcn
        else:
            raise ValueError("fcn is not <def> or <str>")

    @staticmethod
    def rk4(f, ti, yi, t, h):
        """
        Runge-Kutta 4th Order Method for first order ODE

        Parameters
        ----------
        f : def
            function of the differential equation to solve def f(t, y)
        ti : Value of the initial t
        yi : Value of the initial y
        t : Value that you want to evaluate in the equation
        h : Integration step

        Return
        ------
        yi : list
            List of "y" values of each iteration
        ti : list
            List of "t" values of each iteration
        """

        for _ in np.arange(ti, t, h):
            k1 = f(ti, yi)
            k2 = f(ti + h / 2, yi + k1 * h / 2)
            k3 = f(ti + h / 2, yi + k2 * h / 2)
            k4 = f(ti + h, yi + k3 * h)

            yi += (h / 6) * (k1 + 2 * (k2 + k3) + k4)
            ti += h

            yield yi, ti

    def solve(self, ti, yi, t, h=0.001):
        """
        Solution of the first-order ordinary differential equation

        Parameters
        ----------
        ti : Value of the initial t
        yi : Value of the initial y
        t : Value that you want to evaluate in the equation
        h : Integration step

        Return
        ------
        y : Value of "y" for "t" desired
        """

        self.empty_vals()

        vals = list(firstorder.rk4(self.f, ti, yi, t, h))
        self.ys = [vals[i][0] for i in range(len(vals))]
        self.ts = [vals[i][1] for i in range(len(vals))]

        return self.ys[len(self.ys) - 1]

    def graph(self, *args, **kwargs):
        """
        Solution Graph with values obtained from each iteration.
        """

        if len(self.ts) == 0 or len(self.ys) == 0:
            raise ValueError('Need to solve first')

        plt.title("Solution graph")
        plt.plot(self.ts, self.ys, *args, **kwargs)
        plt.scatter(self.ts[len(self.ts) - 1], self.ys[len(self.ys) - 1],
                    facecolor='k', s=50,
                    label='y({})={}'.format(round(self.ts[len(self.ts) - 1], 4),
                    self.ys[len(self.ys) - 1]))
        plt.xlabel("$ t $")
        plt.ylabel("$ y(t) $")
        plt.legend()
        plt.grid()
        plt.show()

    def get_vals(self):
        """
        Obtain the solution values of each iteration.
        """

        return self.ts, self.ys

    def empty_vals(self):
        """
        Clear all values of each iteration.
        """

        self.ts = []
        self.ys = []

class secondorder:
    """
    Implementation of the Runge Kutta 4th method, to obtain the value of a 2nd
    order differential equation, given its initial conditions, obtain its graph.

    Second Order ODE's in form:
    --> y'' = f(t, y, y'), y(t0) = y0, y'(t0) = u0

    It can be expressed as an initial value problem for a system of first-order
    differential equations. If  y' = u, the second-order differential equation
    becomes in the system:
    y' = u
    u' = f(t, y, u)

    ...

    Attributes
    ----------
    function1 : def
        Function that depends to t, y, u, def f(t, y, u)
    function2 : def
        Function that depends to u, def g(u)

    Methods
    -------
    def solve:
        Solve the second-order differential equation using RK4
    def graph:
        Solution Graph with values obtained from each iteration.

    Example
    -------
    y'' + ty' + y = 0, y(0) = 1, y'(0) = 2
    First leave in terms of y' = u:
        y' = u
        u' + tu + y = 0
        u' = - tu - y

    >>> from RungeKutta.RK4 import secondorder
    >>> def g(u):
    ...     return u
    >>> def f(t, y, u):
    ...     return - t * u - y
    >>> rk = secondorder(f, g)
    >>> ti = 0.0
    >>> yi = 1.0
    >>> ui = 2.0
    >>> t = 0.2
    >>> h = 0.01
    >>> y, u = rk.solve(ti, yi, ui, t, h)
    >>> print('The values of y({}) = {} and y\'({}) = {}'.format(t, y, t, u))

    """

    def __init__(self, fcn1, fcn2):
        """
        Constructor

        Parameters
        ----------
        fcn1 : Function that depends to t, y, u, def f(t, y, u)
        fcn2 : Function that depends to u, def g(u)

        """

        self.f = fcn1
        self.g = fcn2
        self.ts = []
        self.ys = []
        self.us = []

    def solve(self, ti, yi, ui, t, h=0.001):
        """
        Solution of the second-order ordinary differential equation

        Parameters
        ----------
        ti : Value of the initial t
        yi : Value of the initial y
        ui : Value of the initial y'
        t : Value that you want to evaluate in the diff system
        h : Integration step

        Returns
        -------
        yi : Value of y for the t desired
        ui : Value of y' for the t desired
        """

        for _ in np.arange(ti, t, h):
            m1 = self.g(ui)
            k1 = self.f(ti, yi, ui)

            m2 = self.g(ui + k1 * h / 2)
            k2 = self.f(ti + h / 2, yi + m1 * h / 2, ui + k1 * h / 2)

            m3 = self.g(ui + k2 * h / 2)
            k3 = self.f(ti + h / 2, yi + m2 * h / 2, ui + k2 * h / 2)

            m4 = self.g(ui + k3 * h)
            k4 = self.f(ti + h, yi + m3 * h, ui + k3 * h)

            yi += (h / 6) * (m1 + 2 * (m2 + m3) + m4)
            self.ys.append(yi)

            ui += (h / 6) * (k1 + 2 * (k2 + k3) + k4)
            self.us.append(ui)

            ti += h
            self.ts.append(ti)

        return yi, ui

    def graph(self, *args, **kwargs):
        """
        Solution Graph with values obtained from each iteration.
        """

        plt.title("Graph of functions")
        plt.plot(self.ts, self.ys, label="$y(t)$", *args, **kwargs)
        plt.plot(self.ts, self.us, label="$y'(t)$", *args, **kwargs)
        plt.legend()
        plt.grid()
        plt.xlabel("$ t $")
        plt.ylabel("$ y \quad | \quad y'$")
        plt.show()

if __name__ == "__main__":
    y = firstorder('2 * t - 3 * y + 1')

    ti = 1.0
    yi = 5.0
    t = 1.5
    h = 0.01
    r = y.solve(ti, yi, t, h)
    print("y({}) = {}".format(t, r))
    y.graph('r--', label="Solution curve")

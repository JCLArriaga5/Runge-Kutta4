# -*- coding: utf-8 -*-

# José Carlos López Arriaga & Ana Isabel Gutiérrez Chávez
#
# Implementation of the Runge Kutta method of fourth order, a small module was implemented to solve ordinary
# differential equations of the first order, the purposes are educational and learning by the authors.

import sys
import os
abspath = os.getcwd()
dirpath = abspath.replace('/RungeKutta/GUI-RK4', '/')
sys.path.append(dirpath)
import numpy as np
import math

np.set_printoptions(suppress=True)

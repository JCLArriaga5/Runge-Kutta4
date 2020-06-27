<p align="center"><img src="images/logo/RK4-logo.png" height="150"></p>

## Runge-Kutta4

[![License](https://img.shields.io/badge/License-MIT-green.svg)](../master/LICENSE)

Fourth-order Runge Kutta method to solve ordinary differential equations (ODE's) given the initial conditions of the equation, to obtain the solution. The implementation can resolve first and second order ODEs.

To solve the second order ODE's can be decomposed into a system of differential equations, as shown below.
- y = u
- du/dx = v
- dv/dx = y"

## Installation
```sh
$ python -m pip install git+https://github.com/JCLArriaga5/Runge-Kutta4.git
```
## GUI for first-order ODE's
To run the GUI if you clone the repository, use the following commands
```sh
:~/Runge-Kutta4$ cd RungeKutta/GUI-RK4/
:~/Runge-Kutta4/RungeKutta/GUI-RK4$ python RungeKutta_GUI.py
```
The following window will open.

<p align="center"><img src="images/GUI-preview.png" height=""></p>

To see the default example, first click on `compute`. To see the solution graph press on the `Graph function` button, so that it is shown as in the following image.

<p align="center"><img src="images/GUI-run.png" height=""></p>

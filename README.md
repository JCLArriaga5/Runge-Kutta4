<p align="center"><img src="images/logo/RK4-logo.png" height="150"></p>

## Runge-Kutta4

[![License](https://img.shields.io/badge/License-MIT-green.svg)](../master/LICENSE) ![size](https://img.shields.io/github/repo-size/JCLArriaga5/Runge-Kutta4)

Fourth-order Runge Kutta method to solve ordinary differential equations (ODE's) given the initial conditions of the equation, to obtain the solution. The implementation can resolve first and second order ODEs.

To solve the second order ODE's can be decomposed into a system of differential equations, as shown below.
<p align="left"><img src="images/example_convert_2ode.png" height="110"></p>

## Use the repository
<!-- ```sh
$ python -m pip install git+https://github.com/JCLArriaga5/Runge-Kutta4.git
``` -->
Clone repository
```sh
$ git clone https://github.com/JCLArriaga5/Runge-Kutta4.git
```
Enter the path where the repository was cloned and install the dependencies with the following command:
```sh
pip install -r requirements.txt
```
First check if you have [tkinter](https://docs.python.org/3.6/library/tkinter.html) installed, the GUI needs tkinter to run, use the following command to install tkinter:
```sh
sudo apt-get install python3-tk
```

## Examples
For examples of how to use the functions see this [file](../master/rk4odes/test.py), run the test:
```sh
:~/Runge-Kutta4$ cd rk4odes/
:~/Runge-Kutta4/rk4odes$ python test.py
```

## GUI for first-order ODE's
<span style="color:red">Note: GUI needs Python 3 or higher</span>

To run the GUI use the following commands inside the path where the repository was cloned
```sh
:~/Runge-Kutta4$ cd rk4odes/GUI/
:~/Runge-Kutta4/rk4odes/GUI$ python GUI.py
```
The following window will open.
<p align="center"><img src="images/GUI-preview.png" height=""></p>

To see the default example, first click on `compute`. To see the solution graph press on the `Graph` button, so that it is shown as in the following image.

<p align="center"><img src="images/Runge_Kutta_4th_Order_Window.gif" height=""></p>

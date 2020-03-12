from RungeKutta.FirstOrderODE.RK4 import *
from RungeKutta.SecondOrderODE.RK import *
from math import e


# For 1st Order ODE
def f(t, y):
    return 2 * t - 3 * y + 1


r = RK4(f)
ti = 1
yi = 5
done = 1.5
h = 0.1
resultado = r.solve(ti, yi, done, h)
print("dy/dt =", resultado)
r.graph('r--', label="Function y")


# For 2nd Order ODE
def f1(v):
    return v


def g(v, u, t):
    return 4 * v + 6 * e ** (3 * t) - 3 * e ** (-t)


r2 = RK(f1, g)
u_i = 1
v_i = -1
t_i = 0
sh = 0.1
end = 1.5

resultadosuv = r2.solve(t_i, u_i, v_i, end, sh)
print("u =", resultadosuv[0])
print("v =", resultadosuv[1])
r2.graph()

import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from typing import Union, List, Tuple, Callable

class RK4:
    """
    Implementation of the Runge Kutta 4th method, to obtain the value
    of a N-order differential equation given its initial conditions.
    -->  y' = f(t, y),   y(t0) = y0

    ...

    Attributes
    ----------
    f : Callable
        Compiled function of the differential equation system def f(t, y) -> np.ndarray
    """

    def __init__(self, eqns: Union[str, List[str]]):
        """
        Constructor

        Parameters
        ----------
        eqns : Union[str, List[str]]
            Function(s) to solve f(t, y). Can be a single string or a list of strings.
        """
        self.ts: List[float] = []
        self.ys: List[np.ndarray] = []
        
        if isinstance(eqns, str):
            eqns = [eqns]

        self.num_eqns = len(eqns)
        
        t_sym = sp.Symbol('t')
        
        import re
        y_syms = [sp.Symbol(f'y_{i}') for i in range(self.num_eqns)]
        
        exprs = []
        for original_eqn in eqns:
            # Reemplazamos la notación y[i] por y_i para Sympy
            eqn = re.sub(r'y\[(\d+)\]', r'y_\1', original_eqn)
            if self.num_eqns == 1 and 'y_0' not in eqn and 'y' in eqn:
                eqn = re.sub(r'\by\b', 'y_0', eqn)
            
            try:
                # sympify compila de forma segura expresiones matemáticas
                expr = sp.sympify(eqn, evaluate=False)
            except Exception as e:
                raise ValueError(f"Error de sintaxis en '{original_eqn}'. Revisa paréntesis y operadores. Detalle: {e}")
            
            # Validar que no haya símbolos extraños (letras que no sean t ni las y definidas)
            allowed_syms = {'t'} | {f'y_{i}' for i in range(self.num_eqns)}
            free_syms = {str(s) for s in expr.free_symbols}
            
            invalid_syms = free_syms - allowed_syms
            if invalid_syms:
                # Formatear el error para que sea claro para el usuario
                invalid_str = ', '.join(invalid_syms).replace('y_', 'y[') + (']' if 'y_' in str(invalid_syms) else '')
                raise ValueError(
                    f"Símbolos desconocidos en '{original_eqn}': {invalid_str}\n"
                    f"Solo se permiten 't' y variables de estado hasta y[{self.num_eqns - 1}]."
                )
                
            exprs.append(expr)
            
        self._lambda_f = sp.lambdify((t_sym, *y_syms), exprs, "numpy")

    def f(self, t: float, y: np.ndarray) -> np.ndarray:
        """
        Evaluates the differential equation system.
        """
        return np.array(self._lambda_f(t, *y))

    @staticmethod
    def rk4(f: Callable[[float, np.ndarray], np.ndarray], ti: float, yi: np.ndarray, t: float, h: float):
        """
        Runge-Kutta 4th Order Method for N-order ODE

        Parameters
        ----------
        f : Callable
            function of the differential equation to solve def f(t, y) -> np.ndarray
        ti : float
            Value of the initial t
        yi : np.ndarray
            Value of the initial y (vector)
        t : float
            Value that you want to evaluate in the equation
        h : float
            Integration step

        Yields
        ------
        yi : np.ndarray
            Value of "y" of each iteration
        ti : float
            Value of "t" of each iteration
        """
        for _ in np.arange(ti, t, h):
            k1 = f(ti, yi)
            k2 = f(ti + h / 2, yi + k1 * h / 2)
            k3 = f(ti + h / 2, yi + k2 * h / 2)
            k4 = f(ti + h, yi + k3 * h)

            yi = yi + (h / 6) * (k1 + 2 * (k2 + k3) + k4)
            ti += h

            yield yi, ti

    def solve(self, ti: float, yi: Union[float, List[float], np.ndarray], t: float, h: float = 0.001) -> np.ndarray:
        """
        Solution of the ordinary differential equation

        Parameters
        ----------
        ti : float
            Value of the initial t
        yi : Union[float, List[float], np.ndarray]
            Value of the initial y
        t : float
            Value that you want to evaluate in the equation
        h : float
            Integration step

        Returns
        -------
        y : np.ndarray
            Value of "y" vector for "t" desired
        """
        self.empty_vals()
        
        if not isinstance(yi, np.ndarray):
            if isinstance(yi, (list, tuple)):
                yi = np.array(yi, dtype=float)
            else:
                yi = np.array([yi], dtype=float)

        self.ts = [ti]
        self.ys = [yi.copy()]
        
        for y_val, t_val in RK4.rk4(self.f, ti, yi, t, h):
            self.ts.append(t_val)
            self.ys.append(y_val.copy())

        return self.ys[-1]

    def graph(self, *args, **kwargs) -> None:
        """
        Solution Graph with values obtained from each iteration.
        """
        if len(self.ts) == 0 or len(self.ys) == 0:
            raise ValueError('Need to solve first')

        ys_array = np.array(self.ys)
        plt.title("Solution graph")
        
        for i in range(ys_array.shape[1]):
            plt.plot(self.ts, ys_array[:, i], label=f"$y_{i}(t)$", *args, **kwargs)
            plt.scatter(self.ts[-1], ys_array[-1, i],
                        facecolor='k', s=50,
                        label=f'$y_{i}({round(self.ts[-1], 4)})={ys_array[-1, i]:.4f}$')
            
        plt.xlabel("$ t $")
        plt.ylabel("$ y(t) $")
        plt.legend()
        plt.grid()
        plt.show()

    def get_vals(self) -> Tuple[List[float], List[np.ndarray]]:
        """
        Obtain the solution values of each iteration.
        """
        return self.ts, self.ys

    def empty_vals(self) -> None:
        """
        Clear all values of each iteration.
        """
        self.ts = []
        self.ys = []

if __name__ == "__main__":
    # Test 1st order
    print("Testing 1st order...")
    rk = RK4('2 * t - 3 * y + 1')
    res = rk.solve(1.0, 5.0, 1.5, 0.01)
    print("y(1.5) =", res)
    
    # Test 2nd order (y'' = -y) => y0' = y1, y1' = -y0
    print("Testing 2nd order (Harmonic Oscillator)...")
    rk2 = RK4(['y[1]', '-y[0]'])
    res2 = rk2.solve(0.0, [0.0, 1.0], np.pi/2, 0.01)
    print("y(pi/2) =", res2)

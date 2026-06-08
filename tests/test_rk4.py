import unittest
import numpy as np
import sys
import os

# Añadimos el directorio raíz al path para que Python encuentre rk4odes
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rk4odes.rk4 import RK4

class TestRK4(unittest.TestCase):

    def test_first_order_ode(self):
        """Prueba un sistema de 1er orden: y' = 2*t - 3*y + 1"""
        rk = RK4('2 * t - 3 * y + 1')
        res = rk.solve(ti=1.0, yi=5.0, t=1.5, h=0.01)
        
        # El resultado esperado (calculado previamente o analítico) para h=0.01
        expected = 2.05321624
        self.assertAlmostEqual(res[0], expected, places=4, msg="El cálculo del RK4 falló para la ODE de 1er orden")

    def test_second_order_ode(self):
        """Prueba un sistema de 2do orden (Oscilador Armónico): y'' = -y => y0' = y1, y1' = -y0"""
        rk = RK4(['y[1]', '-y[0]'])
        # y(0) = 0, y'(0) = 1. Analíticamente y(t) = sin(t), y'(t) = cos(t)
        res = rk.solve(ti=0.0, yi=[0.0, 1.0], t=1.0, h=0.01)
        
        # Para t=1.0, sin(1.0) ≈ 0.84147, cos(1.0) ≈ 0.54030
        self.assertAlmostEqual(res[0], np.sin(1.0), places=4, msg="El valor de y0 (posición) falló")
        self.assertAlmostEqual(res[1], np.cos(1.0), places=4, msg="El valor de y1 (velocidad) falló")

    def test_syntax_validation(self):
        """Verifica que se levante un ValueError si la sintaxis matemática es incorrecta"""
        with self.assertRaises(ValueError) as context:
            rk = RK4('2 t - 3 * y') # Falta el operador * entre 2 y t
            
        self.assertTrue("Error de sintaxis" in str(context.exception))

    def test_invalid_symbols(self):
        """Verifica que símbolos que no sean 't' o variables de estado conocidas levanten ValueError"""
        with self.assertRaises(ValueError) as context:
            rk = RK4('a * t + y') # 'a' es un símbolo desconocido
            
        self.assertTrue("Símbolos desconocidos" in str(context.exception))
        self.assertTrue("a" in str(context.exception))

if __name__ == '__main__':
    unittest.main()

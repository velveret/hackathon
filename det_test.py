from sympy.interactive.printing import init_printing
init_printing(use_unicode=False, wrap_line=False, no_global=True)
from sympy.matrices import *
import sympy as sp

A = Matrix([[1,0,3], [0,1,-2], [-5,2,5]])
print A
print A.det(), "\n\n"

x = sp.Symbol('x')
y = sp.Symbol('y')
B = Matrix([[sp.sin(x),sp.cos(y),sp.sin(x-y)], [0,5*sp.sin(2*x),-2+sp.sin(x+y)], [-5,sp.sin(-5x+4),5]])
print B
print B.inv()
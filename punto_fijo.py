import numpy as np


def f(x):
    return x**2-2*x-3


def g(x):
    return (2*x+3)**(0.5)


def gprima(x):
    h = 1e-5  # Pequeño valor para la derivada numérica
    return (g(x + h) - g(x)) / h


x0, eps1, eps2, k = 4, 0.0001, 0.0001, 0
max_iter = 100

x1 = g(x0)

# Imprimir encabezados de la tabla
print("=" * 70)
print(f"{'Iter':<6} {'x0':<12} {'x1':<12} {'|x1-x0|':<12} {'|f(x1)|':<12}")
print("=" * 70)

if np.abs(gprima(x0)) >= 1:
    print('La función g(x) no es contractiva en el punto x0')
    exit()

while np.abs(x1-x0) > eps1 and k < max_iter:
    print(f"{k:<6} {x0:<12.8f} {x1:<12.8f} {
          np.abs(x1-x0):<12.8f} {np.abs(f(x1)):<12.8f}")
    k = k+1
    x0 = x1
    x1 = g(x0)

print("=" * 70)

if k >= max_iter:
    print(f'No convergió después de {max_iter} iteraciones')
else:
    print('la solución es: ', x1)
    print('verificación f(x1) =', f(x1))

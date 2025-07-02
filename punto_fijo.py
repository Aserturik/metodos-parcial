import numpy as np

# Definir la función de iteración para punto fijo: x = g(x)


def g(x):
    return np.exp(np.tan(x))


def f(x):
    return np.log(x) - np.tan(x)


def punto_fijo(x0, tolerancia=1e-4, max_iter=50):
    print("MÉTODO DEL PUNTO FIJO PARA f(x) = ln(x) - tan(x)")
    print("=" * 55)
    print(f"Punto inicial: x0 = {x0}")
    print(f"{'k':<3} {'x':<12} {'f(x)':<12}")
    print("-" * 30)
    x = x0
    for k in range(max_iter):
        fx = f(x)
        print(f"{k:<3} {x:<12.6f} {fx:<12.6f}")
        if abs(fx) < tolerancia:
            print(f"\nConvergió en {k} iteraciones")
            print(f"Raíz aproximada: x = {x:.8f}")
            print(f"Verificación: f({x:.6f}) = {fx:.2e}")
            print("=" * 55)
            return x
        x = g(x)
    print(f"No convergió en {max_iter} iteraciones")
    print("=" * 55)
    return None


if __name__ == "__main__":
    x0 = 4.090
    punto_fijo(x0)

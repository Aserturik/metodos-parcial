import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use('Agg')

# Función y su derivada
def f(x):
    """Función f(x) = ln(x) - tan(x)"""
    return np.log(x) - np.tan(x)

def df(x):
    """Derivada f'(x) = 1/x - sec²(x)"""
    return 1/x - (1/np.cos(x))**2

def newton_raphson(x0, tolerancia=0.0001, max_iter=50):
    """
    Método de Newton-Raphson simplificado
    
    Args:
        x0: punto inicial
        tolerancia: precisión deseada
        max_iter: máximo de iteraciones
    
    Returns:
        x: raíz encontrada (o None si no converge)
    """
    print(f"\nPunto inicial: x0 = {x0}")
    print(f"{'k':<3} {'x':<12} {'f(x)':<12}")
    print("-" * 30)
    
    x = x0
    for k in range(max_iter):
        fx = f(x)
        print(f"{k:<3} {x:<12.6f} {fx:<12.6f}")
        
        # Verificar convergencia
        if abs(fx) < tolerancia:
            print(f"\nConvergió en {k} iteraciones")
            print(f"Raíz: x = {x:.8f}")
            print(f"Verificación: f({x:.6f}) = {fx:.2e}")
            return x
        
        # Calcular siguiente punto
        dfx = df(x)
        x = x - fx/dfx
    
    print(f"No convergió en {max_iter} iteraciones")
    return None

# Encontrar raíces con diferentes puntos iniciales
print("MÉTODO DE NEWTON-RAPHSON PARA f(x) = ln(x) - tan(x)")
print("=" * 55)

puntos_iniciales = [3.5, 4.5]
raices = []

for x0 in puntos_iniciales:
    raiz = newton_raphson(x0)
    if raiz is not None:
        # Evitar raíces duplicadas
        es_nueva = True
        for r in raices:
            if abs(raiz - r) < 0.01:
                es_nueva = False
                print("(Raíz duplicada)")
                break
        if es_nueva:
            raices.append(raiz)

# Resumen final
print("\n" + "=" * 55)
print("RAÍCES ENCONTRADAS:")
print("=" * 55)
for i, raiz in enumerate(raices):
    print(f"Raíz {i+1}: x = {raiz:.8f}, f(x) = {f(raiz):.2e}")

# Gráfica simple
x = np.linspace(0.5, 12, 1000)
y = []

# Evaluar función evitando problemas en singularidades
for xi in x:
    try:
        yi = f(xi)
        if abs(yi) < 100:  # Evitar valores muy grandes cerca de singularidades
            y.append(yi)
        else:
            y.append(np.nan)
    except:
        y.append(np.nan)

plt.figure(figsize=(10, 6))
plt.plot(x, y, 'b-', linewidth=2, label='f(x) = ln(x) - tan(x)')
plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
plt.grid(True, alpha=0.3)

# Marcar las raíces encontradas
colores = ['red', 'green', 'orange', 'purple']
for i, raiz in enumerate(raices):
    color = colores[i % len(colores)]
    plt.plot(raiz, 0, 'o', markersize=8, color=color, 
             label=f'Raíz {i+1}: x={raiz:.4f}')

plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('Método de Newton-Raphson: f(x) = ln(x) - tan(x)')
plt.legend()
plt.ylim(-5, 5)
plt.xlim(0.5, 12)

plt.tight_layout()
plt.savefig('metodo_newton_grafica.png', dpi=150, bbox_inches='tight')
print(f"\nGráfica guardada como: metodo_newton_grafica.png")
print(f"Se encontraron {len(raices)} raíces distintas")

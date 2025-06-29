import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Usar backend no interactivo antes de importar pyplot


def f(x):
    return 2*x**2 - x - 5


def df(x):
    return 4*x - 1


def newton_raphson(x0_inicial, eps1=0.0001, eps2=0.0001, max_iter=100, mostrar_tabla=True):
    """
    Implementa el método de Newton-Raphson para encontrar una raíz

    Args:
        x0_inicial: punto inicial
        eps1: tolerancia para |x1-x0|
        eps2: tolerancia para |f(x1)|
        max_iter: máximo número de iteraciones
        mostrar_tabla: si mostrar la tabla de iteraciones

    Returns:
        tuple: (raíz encontrada, número de iteraciones, convergió)
    """
    x0, k = x0_inicial, 0

    # Verificar división por cero antes del primer cálculo
    if np.abs(df(x0)) < 1e-15:
        print(f"Error: la derivada es cero en x0 = {x0}, "
              f"no se puede iniciar el método")
        return None, 0, False

    x1 = x0 - (f(x0)/df(x0))

    if mostrar_tabla:
        # Imprimir encabezados de la tabla
        print("=" * 70)
        print(f"{'Iter':<6} {'x0':<12} {'x1':<12} {
              '|x1-x0|':<12} {'|f(x1)|':<12}")
        print("=" * 70)

    while np.abs(x1-x0) > eps1 and np.abs(f(x1)) > eps2 and k < max_iter:
        if mostrar_tabla:
            print(f"{k:<6} {x0:<12.8f} {x1:<12.8f} {np.abs(x1-x0):<12.8f} "
                  f"{np.abs(f(x1)):<12.8f}")
        k = k+1
        x0 = x1
        if np.abs(df(x0)) < 1e-15:
            if mostrar_tabla:
                print(f"Error: la derivada es cero en x = {
                      x0}, no se puede continuar")
            return None, k, False
        x1 = x0 - (f(x0)/df(x0))

    if mostrar_tabla:
        print("=" * 70)

    if k >= max_iter:
        if mostrar_tabla:
            print(f'No convergió después de {
                  max_iter} iteraciones desde x0 = {x0_inicial}')
        return None, k, False
    else:
        return x1, k, True


# Definir múltiples puntos iniciales para encontrar diferentes raíces
puntos_iniciales = [-1, 2]
raices_encontradas = []

print("BÚSQUEDA DE MÚLTIPLES RAÍCES CON EL MÉTODO DE NEWTON-RAPHSON")
print("=" * 80)

for i, x0 in enumerate(puntos_iniciales):
    print(f"\nPUNTO INICIAL {i+1}: x0 = {x0}")
    print("-" * 50)

    raiz, iteraciones, convergio = newton_raphson(x0, mostrar_tabla=True)

    if convergio:
        print(f'La solución es: x = {raiz:.10f}')
        print(f'Verificación: f(x) = {f(raiz):.2e}')
        print(f'Iteraciones: {iteraciones}')

        # Verificar si esta raíz ya fue encontrada (evitar duplicados)
        es_nueva = True
        for raiz_existente in raices_encontradas:
            if np.abs(raiz - raiz_existente) < 1e-3:  # Tolerancia más amplia para duplicados
                es_nueva = False
                break

        if es_nueva:
            raices_encontradas.append(raiz)
            print("*** NUEVA RAÍZ ENCONTRADA ***")
        else:
            print("(Raíz ya encontrada anteriormente)")
    else:
        print(f"No convergió, después de {iteraciones} iteraciones")

print(f"\n" + "=" * 80)
print("RESUMEN DE RAÍCES ENCONTRADAS:")
print("=" * 80)
for i, raiz in enumerate(raices_encontradas):
    print(f"Raíz {i+1}: x = {raiz:.10f}, f(x) = {f(raiz):.2e}")


# Generar la gráfica con todas las raíces encontradas
x = np.linspace(-3, 4, 400)
y = f(x)
plt.figure(figsize=(12, 8))
plt.plot(x, y, color='blue', linewidth=2, label='f(x) = 2x² - x - 5')
plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
plt.axvline(x=0, color='black', linestyle='-', alpha=0.3)

# Plotear todas las raíces encontradas
colores = ['red', 'green', 'orange', 'purple', 'brown']
for i, raiz in enumerate(raices_encontradas):
    color = colores[i % len(colores)]
    plt.plot(raiz, f(raiz), 'o', markersize=10, color=color,
             label=f'Raíz {i+1}: x = {raiz:.6f}')
    # Línea vertical desde la raíz hasta el eje x
    plt.axvline(x=raiz, color=color, linestyle='--', alpha=0.5)

# Mostrar los puntos iniciales en la gráfica
for i, x0 in enumerate(puntos_iniciales):
    plt.plot(x0, f(x0), 's', markersize=8, color='gray', alpha=0.7)

plt.grid(True, alpha=0.3)
plt.xlabel('x', fontsize=12)
plt.ylabel('f(x)', fontsize=12)
plt.title('Método de Newton-Raphson - Múltiples Raíces', fontsize=14)
plt.legend()

# Agregar texto con información
textstr = f'Raíces encontradas: {
    len(raices_encontradas)}\nPuntos iniciales probados: {len(puntos_iniciales)}'
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
plt.text(0.02, 0.98, textstr, transform=plt.gca().transAxes, fontsize=10,
         verticalalignment='top', bbox=props)

plt.tight_layout()
plt.savefig('metodo_newton_grafica.png', dpi=300, bbox_inches='tight')
print('\nGráfica guardada como: metodo_newton_grafica.png')
print(f'La gráfica muestra {len(raices_encontradas)} raíces encontradas usando {
      len(puntos_iniciales)} puntos iniciales')

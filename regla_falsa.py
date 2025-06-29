# Metodo de la regla falsa

import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Usar backend no interactivo antes de importar pyplot


def f(x):
    return 2*x**2 - x - 5


def regla_falsa(xi, xd, eps1=0.0001, eps2=0.0001, max_iter=100,
                mostrar_tabla=True):
    """
    Implementa el método de la regla falsa para encontrar una raíz

    Args:
        xi: límite izquierdo del intervalo
        xd: límite derecho del intervalo
        eps1: tolerancia para el cambio en la raíz
        eps2: tolerancia para |f(xm)|
        max_iter: máximo número de iteraciones
        mostrar_tabla: si mostrar la tabla de iteraciones

    Returns:
        tuple: (raíz encontrada, número de iteraciones, convergió)
    """
    k = 0

    # Verificar que f(xi) y f(xd) tienen signos opuestos
    lados_opuestos = f(xi) * f(xd) < 0

    if not lados_opuestos:
        print(f"Error: f({xi}) * f({xd}) no es menor que cero, "
              "los puntos no están al lado de una raíz.")
        return None, 0, False

    # Calcular el primer punto medio
    xm_anterior = xi  # Para calcular el error en la primera iteración
    xm = xi - ((xd - xi) / (f(xd) - f(xi)) * f(xi))

    if mostrar_tabla:
        # Imprimir encabezados de la tabla
        print("=" * 80)
        print(f"{'Iter':<6} {'xi':<12} {'xd':<12} {'xm':<12} "
              f"{'|xm-xm_ant|':<12} {'|f(xm)|':<12}")
        print("=" * 80)

    while k < max_iter:
        if mostrar_tabla:
            error_xm = np.abs(xm - xm_anterior) if k > 0 else float('inf')
            print(f"{k:<6} {xi:<12.8f} {xd:<12.8f} {xm:<12.8f} "
                  f"{error_xm:<12.8f} {np.abs(f(xm)):<12.8f}")

        # Verificar criterios de convergencia
        if k > 0 and np.abs(xm - xm_anterior) <= eps1 and np.abs(f(xm)) <= eps2:
            if mostrar_tabla:
                print("=" * 80)
            return xm, k, True

        # Actualizar el intervalo según el signo de f(xi) * f(xm)
        if f(xi) * f(xm) > 0:
            xi = xm  # La raíz está entre xm y xd
        else:
            xd = xm  # La raíz está entre xi y xm

        # Actualizar para la siguiente iteración
        k += 1
        xm_anterior = xm

        # Verificar división por cero
        if np.abs(f(xd) - f(xi)) < 1e-15:
            if mostrar_tabla:
                print("Error: f(xd) - f(xi) es muy pequeño, no se puede continuar")
            return None, k, False

        xm = xi - ((xd - xi) / (f(xd) - f(xi)) * f(xi))

    if mostrar_tabla:
        print("=" * 80)
        print(f'No convergió después de {max_iter} iteraciones')

    return None, k, False


# Código principal para ejecutar el método
if __name__ == "__main__":
    # Definir intervalos para encontrar diferentes raíces
    intervalos = [(-3, 0), (1, 3)]
    raices_encontradas = []

    print("BÚSQUEDA DE RAÍCES CON EL MÉTODO DE LA REGLA FALSA")
    print("=" * 80)

    for i, (xi, xd) in enumerate(intervalos):
        print(f"\nINTERVALO {i+1}: [{xi}, {xd}]")
        print("-" * 50)

        raiz, iteraciones, convergio = regla_falsa(xi, xd, mostrar_tabla=True)

        if convergio:
            print(f'La solución es: x = {raiz:.10f}')
            print(f'Verificación: f(x) = {f(raiz):.2e}')
            print(f'Iteraciones: {iteraciones}')

            # Verificar si esta raíz ya fue encontrada (evitar duplicados)
            es_nueva = True
            for raiz_existente in raices_encontradas:
                if np.abs(raiz - raiz_existente) < 1e-3:
                    es_nueva = False
                    break

            if es_nueva:
                raices_encontradas.append(raiz)
                print("*** NUEVA RAÍZ ENCONTRADA ***")
            else:
                print("(Raíz ya encontrada anteriormente)")
        else:
            print(f"No convergió después de {iteraciones} iteraciones")

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

    # Mostrar los intervalos usados en la gráfica
    for i, (xi, xd) in enumerate(intervalos):
        plt.axvspan(xi, xd, alpha=0.1, color='gray',
                    label=f'Intervalo {i+1}: [{xi}, {xd}]' if i < 2 else "")

    plt.grid(True, alpha=0.3)
    plt.xlabel('x', fontsize=12)
    plt.ylabel('f(x)', fontsize=12)
    plt.title('Método de la Regla Falsa - Múltiples Raíces', fontsize=14)
    plt.legend()

    # Agregar texto con información
    textstr = f'Raíces encontradas: {len(raices_encontradas)}\nIntervalos probados: {
        len(intervalos)}'
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    plt.text(0.02, 0.98, textstr, transform=plt.gca().transAxes, fontsize=10,
             verticalalignment='top', bbox=props)

    plt.tight_layout()
    plt.savefig('regla_falsa_grafica.png', dpi=300, bbox_inches='tight')
    print('\nGráfica guardada como: regla_falsa_grafica.png')
    print(f'La gráfica muestra {len(raices_encontradas)} raíces encontradas usando {
          len(intervalos)} intervalos')

"""
Ejercicio 4: Cálculo del volumen molar de gases usando la ecuación de Redlich-Kwong
================================================================================

Este programa calcula el volumen molar de diferentes gases (He, H2, O2) utilizando
la ecuación de estado de Redlich-Kwong y el método numérico de la regla falsa.

Ecuación de Redlich-Kwong:
[P + a/(T^0.5 * V * (V + b))] * (V - b) = RT

Donde:
- P: Presión (atm)
- V: Volumen molar (L/mol)
- T: Temperatura (K)
- R: Constante universal de los gases (atm·L/mol·K)
- a, b: Constantes específicas del gas

Autor: [Nombre del estudiante]
Fecha: [Fecha]
"""

import numpy as np

# Constantes del problema
P = 50          # Presión en atm
T = 373.15      # Temperatura en K (100 °C)
R = 0.08205     # Constante universal de los gases en atm·L/mol·K
eps = 0.0001    # Tolerancia para convergencia
max_iter = 100  # Máximo número de iteraciones permitidas

# Propiedades críticas de los gases: [Pc (atm), Tc (K)]
gases = {
    'He': [2.26, 5.26],     # Helio
    'H2': [12.80, 33.30],   # Hidrógeno
    'O2': [49.70, 154.40]   # Oxígeno
}


def calcular_constantes_redlich_kwong(Pc, Tc):
    """
    Calcula las constantes a y b de la ecuación de Redlich-Kwong.

    Parámetros:
        Pc (float): Presión crítica del gas en atm
        Tc (float): Temperatura crítica del gas en K

    Retorna:
        tuple: (a, b) donde:
            a (float): Constante 'a' de Redlich-Kwong
            b (float): Constante 'b' de Redlich-Kwong
            En caso de error, retorna (None, None)

    Fórmulas:
        a = 0.4278 * (R² * Tc^2.5) / Pc
        b = 0.0867 * (R * Tc) / Pc
    """
    try:
        Tc_2_5 = np.power(Tc, 2.5)
        a = 0.4278 * (R**2 * Tc_2_5) / Pc
        b = 0.0867 * (R * Tc) / Pc
        return a, b
    except OverflowError:
        print("ERROR: Desbordamiento en el cálculo de constantes a y b")
        return None, None


def ecuacion_redlich_kwong(v, P, T, a, b):
    """
    Evalúa la ecuación de Redlich-Kwong reordenada para encontrar raíces.

    Ecuación original: [P + a/(T^0.5 * V * (V + b))] * (V - b) = RT
    Forma reordenada: [P + a/(T^0.5 * V * (V + b))] * (V - b) - RT = 0

    Parámetros:
        v (float): Volumen molar en L/mol
        P (float): Presión en atm
        T (float): Temperatura en K
        a (float): Constante 'a' de Redlich-Kwong
        b (float): Constante 'b' de Redlich-Kwong

    Retorna:
        float: Valor de la función evaluada en v
               Retorna np.inf si hay errores numéricos
    """
    try:
        # Verificar que el volumen sea físicamente válido
        if v <= b or v <= 0:
            return np.inf

        # Calcular términos de la ecuación
        termino_presion = P * (v - b)
        termino_atraccion = (a / (np.sqrt(T) * v * (v + b))) * (v - b)
        termino_gas_ideal = R * T

        resultado = termino_presion + termino_atraccion - termino_gas_ideal
        return resultado

    except (OverflowError, ZeroDivisionError):
        return np.inf


def metodo_regla_falsa(gas_nombre, Pc, Tc, mostrar_iteraciones=True):
    """
    Resuelve la ecuación de Redlich-Kwong usando el método de la regla falsa.

    Parámetros:
        gas_nombre (str): Nombre del gas para identificación
        Pc (float): Presión crítica en atm
        Tc (float): Temperatura crítica en K
        mostrar_iteraciones (bool): Si mostrar la tabla de iteraciones

    Retorna:
        float: Volumen molar en L/mol
               None si no converge o hay errores
    """
    # Calcular constantes de Redlich-Kwong
    a, b = calcular_constantes_redlich_kwong(Pc, Tc)
    if a is None or b is None:
        print(f"ERROR: No se pudieron calcular las constantes para {
              gas_nombre}")
        return None

    # Estimación inicial del volumen usando gas ideal
    v_ideal = R * T / P

    # Definir intervalo inicial [vi, vd] que asegure v > b
    vi = max(b * 1.1, 0.1 * v_ideal)  # Límite inferior
    vd = max(b * 1.1, 5.0 * v_ideal)  # Límite superior

    # Evaluar función en los extremos del intervalo
    fi = ecuacion_redlich_kwong(vi, P, T, a, b)
    fd = ecuacion_redlich_kwong(vd, P, T, a, b)

    # Inicializar variables del método
    fm = 1.0  # Valor inicial diferente de cero
    k = 0     # Contador de iteraciones

    if mostrar_iteraciones:
        print(f"\nGas: {gas_nombre} (Pc = {Pc} atm, Tc = {Tc} K)")
        print(f"Constantes: a = {a:.5f}, b = {b:.5f}")
        print(f"Intervalo inicial: [{vi:.6f}, {vd:.6f}]")
        print("\nTabla de iteraciones:")
        print(f"|{'Iter':^4}|{'Volumen (L/mol)':^15}|{'|f(V)|':^12}|")
        print("-" * 35)

    # Algoritmo de regla falsa
    while abs(fm) > eps and k < max_iter:
        k += 1

        # Verificar que no haya división por cero
        denominador = fd - fi
        if denominador == 0:
            print("ERROR: División por cero en el método de regla falsa")
            return None

        # Calcular nuevo punto usando regla falsa
        vm = (vi * fd - vd * fi) / denominador
        fm = ecuacion_redlich_kwong(vm, P, T, a, b)

        # Verificar valores válidos
        if np.isnan(fm) or np.isinf(fm):
            print("ERROR: Valor no válido (NaN o infinito) en la evaluación")
            return None

        if mostrar_iteraciones:
            print(f"|{k:^4}|{vm:^15.6f}|{abs(fm):^12.4e}|")

        # Actualizar intervalo según el signo de fm
        if fd * fm > 0:
            vd = vm
            fd = fm
        else:
            vi = vm
            fi = fm

    # Verificar convergencia
    if k >= max_iter:
        print(f"ADVERTENCIA: No se alcanzó convergencia para {gas_nombre} "
              f"en {max_iter} iteraciones")
        return None

    if mostrar_iteraciones:
        print(f"\nResultado: Volumen molar para {gas_nombre} = {vm:.6f} L/mol")
        print(f"Convergencia alcanzada en {k} iteraciones")

    return vm


def main():
    """
    Función principal que ejecuta el cálculo para todos los gases.
    """
    print("CÁLCULO DEL VOLUMEN MOLAR USANDO LA ECUACIÓN DE REDLICH-KWONG")
    print("=" * 65)
    print(f"Condiciones: P = {P} atm, T = {T} K ({T-273.15:.1f}°C)")
    print(f"Método numérico: Regla falsa")
    print(f"Tolerancia: {eps}")
    print("=" * 65)

    resultados = {}

    # Procesar cada gas
    for gas_nombre, (Pc, Tc) in gases.items():
        volumen = metodo_regla_falsa(gas_nombre, Pc, Tc)
        resultados[gas_nombre] = volumen

    # Mostrar resumen final
    print("\n" + "=" * 65)
    print("RESUMEN DE RESULTADOS")
    print("=" * 65)
    print(f"{'Gas':<8} {'Pc (atm)':<10} {'Tc (K)':<10} {'V (L/mol)':<12}")
    print("-" * 45)

    for gas_nombre, (Pc, Tc) in gases.items():
        volumen = resultados[gas_nombre]
        if volumen is not None:
            print(f"{gas_nombre:<8} {Pc:<10.2f} {Tc:<10.2f} {volumen:<12.6f}")
        else:
            print(f"{gas_nombre:<8} {Pc:<10.2f} {Tc:<10.2f} {'ERROR':<12}")

    print("=" * 65)


# Ejecutar programa principal
if __name__ == "__main__":
    main()

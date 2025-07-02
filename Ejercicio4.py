import numpy as np

# Constantes generales
P = 50  # Presión en atm
T = 373.15  # Temperatura en K (100 °C)
R = 0.08205  # Constante de gases
eps = 0.0001  # Tolerancia
max_iter = 100  # Máximo de iteraciones permitidas

# Datos por gas: nombre: [Pc, Tc]
gases = {
    'He': [2.26, 5.26],
    'H2': [12.80, 33.30],
    'O2': [49.70, 154.40]
}

# Función para calcular a y b con control de valores pequeños
def calcular_a_b(Pc, Tc):
    try:
        Tc_2_5 = np.power(Tc, 2.5)
        a = 0.4278 * (R**2 * Tc_2_5) / Pc
        b = 0.0867 * (R * Tc) / Pc
        return a, b
    except OverflowError:
        print("Error en cálculo de a y b por overflow")
        return None, None

# Función de Redlich-Kwong reordenada para encontrar la raíz
def redlich_kwong_func(v, P, T, a, b):
    try:
        # Reordenada: [P + a/(T^0.5 * V * (V + b))] * (V - b) - RT = 0
        if v <= b or v <= 0: 
            return np.inf
        
        term1 = P * (v - b)
        term2 = (a / (np.sqrt(T) * v * (v + b))) * (v - b)
        result = term1 + term2 - R * T
        
        return result
    except (OverflowError, ZeroDivisionError):
        return np.inf

def regla_falsa(gas, Pc, Tc):
    a, b = calcular_a_b(Pc, Tc)
    if a is None or b is None:
        print(f"No se pudo calcular a y b para {gas}")
        return None
    
    v_ideal = R * T / P
    vi = max(b * 1.1, 0.1 * v_ideal)  # Límite inferior
    vd = max(b * 1.1, 5.0 * v_ideal)  # Límite superior
    
    fi = redlich_kwong_func(vi, P, T, a, b)
    fd = redlich_kwong_func(vd, P, T, a, b)
    fm = 1
    k = 0
    
    print(f"\nGas: {gas} (Pc={Pc} atm, Tc={Tc} K)")
    print(f"a = {a:.5f}, b = {b:.5f}")
    print(f"|{'k':^3}|{'V':^10}|{'f(V)':^10}|")
    print("-" * 30)
    
    while abs(fm) > eps and k < max_iter:
        k += 1
        
        denominator = fd - fi
        if denominator == 0:
            print("División por cero en la regla falsa. Detener.")
            return None
        
        vm = (vi * fd - vd * fi) / denominator
        fm = redlich_kwong_func(vm, P, T, a, b)
        
        if np.isnan(fm) or np.isinf(fm):
            print("Valor no válido (NaN o inf) en f(V). Detener.")
            return None
        
        print(f"|{k:^3}|{vm:^10.6f}|{abs(fm):^10.4e}|")
        
        # Actualizar intervalos según el método de regla falsa
        if fd * fm > 0:
            vd = vm
            fd = fm
        else:
            vi = vm
            fi = fm
    
    if k >= max_iter:
        print(f"No convergió para {gas} en {max_iter} iteraciones")
        return None
    
    print(f"Volumen molar para {gas}: V ≈ {vm:.6f} L/mol")
    return vm

# Ejecutar para todos los gases
resultados = {}
for gas, (Pc, Tc) in gases.items():
    V = regla_falsa(gas, Pc, Tc)
    resultados[gas] = V

# Resumen final
print("\nResumen de resultados finales:")
print(f"{'Gas':<5} {'V (L/mol)':>12}")
print("-" * 20)
for gas, V in resultados.items():
    if V:
        print(f"{gas:<5} {V:>12.6f}")
    else:
        print(f"{gas:<5} {'Error':>12}")
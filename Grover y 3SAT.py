"""
Comparación entre búsqueda clásica exhaustiva y el algoritmo de Grover
sobre instancias del problema 3-SAT.

Nota: la solución se obtiene primero por fuerza bruta únicamente para
poder construir el oráculo de forma didáctica. Esto no forma parte del
algoritmo de Grover en sí; un oráculo genérico de 3-SAT que verifique
la fórmula en superposición requeriría una construcción más elaborada.
"""

import math, numpy as np, matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def generate_3sat(n, seed=42):
    rng = np.random.default_rng(seed)
    return [list(zip(rng.choice(n,3,replace=False).tolist(),
                     rng.choice([-1,1],3).tolist())) for _ in range(n+2)]


def eval_3sat(bits, clauses):
    return all(any((bits[v]==1 and s==1) or (bits[v]==0 and s==-1)
                   for v,s in clause) for clause in clauses)


# Se obtiene una asignación satisfactoria por fuerza bruta únicamente para
# construir un oráculo didáctico. No forma parte del algoritmo de Grover.
def grover_demo(n, clauses):
    sol = next(([(i>>j)&1 for j in range(n)] for i in range(2**n)
               if eval_3sat([(i>>j)&1 for j in range(n)], clauses)), None)
    if sol is None:
        return None

    iters = max(1, round(math.pi/4 * math.sqrt(2**n)))
    qc = QuantumCircuit(n, n)
    qc.h(range(n))

    for _ in range(iters):
        for i,b in enumerate(sol):
            if b==0: qc.x(i)
        qc.h(n-1); qc.mcx(list(range(n-1)), n-1); qc.h(n-1)
        for i,b in enumerate(sol):
            if b==0: qc.x(i)

        qc.h(range(n)); qc.x(range(n))
        qc.h(n-1); qc.mcx(list(range(n-1)), n-1); qc.h(n-1)
        qc.x(range(n)); qc.h(range(n))

    qc.measure(range(n), range(n))
    sim = AerSimulator()
    result = sim.run(qc, shots=1024).result()
    counts = result.get_counts()
    print(counts)

    return iters


ns = range(3, 8)  # n ≥ 3 porque trabajamos con instancias de 3-SAT
classic, quantum, hybrid = [], [], []

for n in ns:
    classic.append(2**n)  # complejidad teórica clásica: búsqueda O(2^n)
    clauses = generate_3sat(n)
    iters = grover_demo(n, clauses)
    quantum.append(np.nan if iters is None else iters)
    # Cota del mejor algoritmo híbrido conocido: O(1.153^n).
    # No se calcula ejecutando el algoritmo, se grafica como referencia teórica.
    hybrid.append(1.153 ** n)

plt.figure(figsize=(8, 5))
plt.plot(list(ns), classic, 'o-', color='#e74c3c', label='Clásico  O(2ⁿ)', linewidth=2)
plt.plot(list(ns), quantum, 's--', color='#2980b9', label='Grover  O(2^(n/2))', linewidth=2)
plt.plot(list(ns), hybrid, '^:', color='#27ae60', label='Schöning + amplitud (Ambainis) O(1.153ⁿ)', linewidth=2)
plt.yscale('log')  # Escala logarítmica para ver crecimiento exponencial como líneas
plt.xlabel('Variables (n)', fontsize=12)
plt.ylabel('Consultas en escala logarítmica', fontsize=12)
plt.title('Grover vs. búsqueda clásica en 3-SAT', fontsize=13)
plt.legend(fontsize=11); plt.grid(alpha=0.3); plt.tight_layout()
plt.savefig('grover_vs_clasico.png', dpi=150)
plt.show()
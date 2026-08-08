# Grover vs. búsqueda clásica en 3-SAT

## Trabajo final del curso de Introducción a la Computación Cuántica de SADIO 2026.

Implementación en Qiskit que compara el algoritmo de Grover con la búsqueda clásica exhaustiva sobre instancias del problema 3-SAT, contrastando ambos enfoques con la cota teórica del mejor algoritmo híbrido conocido (Schöning combinado con amplificación de amplitud, Ambainis 2004). 

## Tabla de contenidos

- [Contexto](#contexto)
- [Motivación teórica](#motivación-teórica)
- [Qué hace el código](#qué-hace-el-código)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Salida esperada](#salida-esperada)
- [Limitaciones](#limitaciones)
- [Referencias](#referencias)

## Contexto

Este código forma parte de un informe para el cual leí diversas fuentes sobre la relación entre las clases de complejidad P, NP y BQP, que analiza si la computación cuántica puede resolver eficientemente problemas para los cuales solo se conocen algoritmos clásicos de tiempo exponencial. En particular, se examina por qué el algoritmo de Grover, a pesar de ofrecer una aceleración cuadrática, no alcanza para resolver eficientemente problemas NP-completos.

## Motivación teórica

Grover resuelve el problema de búsqueda no estructurada en O(√N) consultas, en contraste con O(N) del mejor algoritmo clásico. Aplicado ingenuamente sobre un espacio de 2ⁿ posibles soluciones (como ocurre al atacar un problema NP con fuerza bruta), esto se traduce en O(2^(n/2)) operaciones. Si bien esta cantidad es menor que 2ⁿ, sigue siendo una función exponencial en n: la aceleración cuadrática no vuelve polinomial al problema.

Además, comparado con el mejor algoritmo clásico conocido para 3-SAT (y no con la fuerza bruta), Grover aplicado de forma directa pierde: el algoritmo de Schöning (1999), refinado como PPSZ, resuelve 3-SAT en tiempo O(1.308ⁿ), mejor que el O(1.414ⁿ) ≈ O(2^(n/2)) de Grover ingenuo. La verdadera ventaja cuántica aparece al combinar la técnica de amplificación de amplitud (Brassard, Høyer, Mosca & Tapp, 2000) con el algoritmo de Schöning, en lugar de aplicarla sobre la búsqueda por fuerza bruta: este enfoque híbrido, propuesto por Ambainis (2004), reduce el tiempo a O(1.153ⁿ).

Este repositorio implementa y grafica esas tres magnitudes para instancias reales de 3-SAT, con el objetivo de ilustrar empíricamente esta relación.

## Qué hace el código

Para cada tamaño de instancia n (de 3 a 7 variables):

1. Genera una instancia aleatoria de 3-SAT con n+2 cláusulas.
2. Encuentra una asignación satisfactoria por fuerza bruta (únicamente para poder construir el oráculo de forma didáctica; esto no forma parte del algoritmo de Grover en sí).
3. Construye un circuito cuántico que implementa Grover: aplica O(π/4 · √(2ⁿ)) iteraciones de inversión de fase (oráculo) e inversión alrededor de la media (difusor).
4. Simula el circuito con `AerSimulator` (1024 shots) e imprime la distribución de resultados medidos.
5. Registra el número de iteraciones de Grover y lo compara contra:
   - la búsqueda clásica exhaustiva, O(2ⁿ)
   - la cota teórica del algoritmo híbrido de Schöning + amplificación de amplitud (Ambainis, 2004), O(1.153ⁿ)

Al final se genera un gráfico en escala logarítmica (`grover_vs_clasico.png`) con las tres curvas superpuestas.

## Requisitos

- Python 3.9+
- qiskit
- qiskit-aer
- matplotlib
- numpy

## Instalación

```bash
pip install qiskit qiskit-aer matplotlib numpy
```

Alternativamente, se puede correr directamente en [Google Colab](https://colab.research.google.com) instalando las dependencias en la primera celda con `!pip install qiskit qiskit-aer`.

## Uso

```bash
python grover_3sat.py
```

El script imprime en consola la distribución de mediciones (`counts`) para cada tamaño n, y al finalizar guarda y muestra el gráfico comparativo.

## Salida esperada

Para cada n, la salida en consola muestra un estado dominante con alta probabilidad sobre los 1024 shots (por ejemplo, para n=5: `{'01000': 1023, ...}`), confirmando que Grover encuentra la solución marcada con probabilidad cercana al 100%.

El gráfico final muestra tres curvas en escala logarítmica, en orden decreciente: búsqueda clásica exhaustiva (más costosa), Grover (intermedia), y la cota híbrida de Schöning + amplitud (la más eficiente de las tres), ilustrando que ninguna deja de ser exponencial, aunque con distintas tasas de crecimiento.

## Limitaciones

- Se usa una única instancia aleatoria por tamaño n (semilla fija = 42), no un promedio sobre múltiples instancias. Un análisis estadísticamente más robusto promediaría los resultados sobre varias instancias por tamaño.
- El oráculo se construye conociendo de antemano la solución (obtenida por fuerza bruta), como simplificación didáctica. Un oráculo genérico de 3-SAT que verifique la fórmula en superposición requiere una construcción más elaborada.
- El conteo de iteraciones representa el número de consultas al oráculo, no el costo total del algoritmo: la construcción del oráculo en sí tiene un costo que no se refleja en el gráfico.
- La curva del algoritmo híbrido (Ambainis, 2004) se grafica como referencia teórica, no como resultado de una ejecución real del algoritmo.

## Referencias

- Grover, L. K. (1996). *A fast quantum mechanical algorithm for database search.* Proceedings of the 28th Annual ACM Symposium on Theory of Computing, 1-2.
- Schöning, U. (1999). *A probabilistic algorithm for k-SAT and constraint satisfaction problems.* Proceedings of the 40th Annual Symposium on Foundations of Computer Science, 410-414.
- Brassard, G., Høyer, P., Mosca, M., & Tapp, A. (2000). *Quantum Amplitude Amplification and Estimation.*
- Ambainis, A. (2004). *Quantum search algorithms.*

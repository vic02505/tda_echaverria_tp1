import random
import time
import math
import statistics
import matplotlib.pyplot as plt
import csv

# ==============================
# ALGORITMO PRINCIPAL (DP)
# ==============================

def min_palindromos(S):
    n = len(S)

    pal = [[False] * n for _ in range(n)]

    for i in range(n):
        pal[i][i] = True

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1

            if S[i] == S[j]:
                if length == 2 or pal[i + 1][j - 1]:
                    pal[i][j] = True

    dp = [0] * n

    for i in range(n):
        if pal[0][i]:
            dp[i] = 1
        else:
            dp[i] = float('inf')
            for j in range(1, i + 1):
                if pal[j][i]:
                    dp[i] = min(dp[i], dp[j - 1] + 1)

    return dp[n - 1]


# ==============================
# GENERADOR DE DATOS
# ==============================

def generar_string(n, seed=42):
    random.seed(seed + n)
    letras = "ABC"
    return "".join(random.choice(letras) for _ in range(n))


# ==============================
# MEDICIÓN
# ==============================

def medir_tiempo_promedio(S, repeticiones=10, warmup=2):
    tiempos = []

    # Warm-up (no se mide)
    for _ in range(warmup):
        min_palindromos(S)

    # Mediciones reales
    for _ in range(repeticiones):
        inicio = time.perf_counter()
        min_palindromos(S)
        fin = time.perf_counter()

        tiempos.append(fin - inicio)

    promedio = statistics.mean(tiempos)
    desvio = statistics.stdev(tiempos) if len(tiempos) > 1 else 0

    return promedio, desvio


# ==============================
# EXPERIMENTO COMPLETO
# ==============================

def correr_experimento(tamanios, repeticiones=10):
    resultados = []

    for n in tamanios:
        S = generar_string(n)

        promedio, desvio = medir_tiempo_promedio(S, repeticiones)

        resultado = min_palindromos(S)

        print(f"n={n:4d} | resultado={resultado:3d} | tiempo_prom={promedio:.6f}s | std={desvio:.6f}")

        resultados.append({
            "n": n,
            "resultado": resultado,
            "tiempo_promedio": promedio,
            "desvio_std": desvio
        })

    return resultados


# ==============================
# AJUSTE TEÓRICO
# ==============================

def ajuste_cuadratico(resultados):
    xs = [r["n"]**2 for r in resultados]
    ys = [r["tiempo_promedio"] for r in resultados]

    # Ajuste c = sum(x*y) / sum(x^2)
    numerador = sum(x*y for x, y in zip(xs, ys))
    denominador = sum(x*x for x in xs)

    c = numerador / denominador if denominador != 0 else 0

    return [c * x for x in xs]


# ==============================
# EXPORTAR CSV
# ==============================

def guardar_csv(resultados, filename="resultados.csv"):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["n", "resultado", "tiempo_promedio", "desvio_std"])

        for r in resultados:
            writer.writerow([r["n"], r["resultado"], r["tiempo_promedio"], r["desvio_std"]])


# ==============================
# GRAFICAR
# ==============================

def graficar(resultados, tiempos_teoricos):
    tamanios = [r["n"] for r in resultados]
    tiempos = [r["tiempo_promedio"] for r in resultados]
    desvios = [r["desvio_std"] for r in resultados]

    plt.figure()

    # Curva experimental
    plt.errorbar(tamanios, tiempos, yerr=desvios, marker='o', label="Medición (promedio ± std)")

    # Curva teórica
    plt.plot(tamanios, tiempos_teoricos, linestyle='--', label="Ajuste O(n^2)")

    plt.xlabel("Tamaño de entrada (n)")
    plt.ylabel("Tiempo (segundos)")
    plt.title("Análisis empírico de complejidad")

    plt.legend()
    plt.grid()

    plt.savefig("grafico_tiempos.png")
    plt.show()


# ==============================
# MAIN
# ==============================

def main():
    tamanios = [10, 50, 100, 200, 400, 800]

    resultados = correr_experimento(tamanios, repeticiones=10)

    tiempos_teoricos = ajuste_cuadratico(resultados)

    guardar_csv(resultados)

    graficar(resultados, tiempos_teoricos)


if __name__ == "__main__":
    main()
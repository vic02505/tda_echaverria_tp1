import csv
import random
import statistics
import time
import matplotlib.pyplot as plt

from palindromo import min_palindromos


def generar_string(n, seed=42):
    random.seed(seed + n)
    letras = "ABC"
    return "".join(random.choice(letras) for _ in range(n))


def medir_tiempo_promedio(S, repeticiones=10, warmup=2):
    tiempos = []

    for _ in range(warmup):
        min_palindromos(S)

    for _ in range(repeticiones):
        inicio = time.perf_counter()
        min_palindromos(S)
        fin = time.perf_counter()

        tiempos.append(fin - inicio)

    promedio = statistics.mean(tiempos)
    desvio = statistics.stdev(tiempos) if len(tiempos) > 1 else 0

    return promedio, desvio


def correr_experimento(tamanios, repeticiones=10):
    resultados = []

    for n in tamanios:
        S = generar_string(n)

        promedio, desvio = medir_tiempo_promedio(S, repeticiones)

        resultado = min_palindromos(S)

        print(
            f"n={n:4d} | resultado={resultado:3d} | "
            f"tiempo_prom={promedio:.6f}s | std={desvio:.6f}"
        )

        resultados.append({
            "n": n,
            "resultado": resultado,
            "tiempo_promedio": promedio,
            "desvio_std": desvio,
        })

    return resultados


def ajuste_cuadratico(resultados):
    xs = [r["n"] ** 2 for r in resultados]
    ys = [r["tiempo_promedio"] for r in resultados]

    numerador = sum(x * y for x, y in zip(xs, ys))
    denominador = sum(x * x for x in xs)

    c = numerador / denominador if denominador != 0 else 0

    return [c * x for x in xs]


def guardar_csv(resultados, filename="resultados.csv"):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["n", "resultado", "tiempo_promedio", "desvio_std"])

        for r in resultados:
            writer.writerow(
                [r["n"], r["resultado"], r["tiempo_promedio"], r["desvio_std"]]
            )


def graficar(resultados, tiempos_teoricos, filename="grafico_tiempos.png"):
    tamanios = [r["n"] for r in resultados]
    tiempos = [r["tiempo_promedio"] for r in resultados]
    desvios = [r["desvio_std"] for r in resultados]

    plt.figure()

    plt.errorbar(
        tamanios,
        tiempos,
        yerr=desvios,
        marker="o",
        label="Medicion (promedio +- std)",
    )

    plt.plot(tamanios, tiempos_teoricos, linestyle="--", label="Ajuste O(n^2)")

    plt.xlabel("Tamano de entrada (n)")
    plt.ylabel("Tiempo (segundos)")
    plt.title("Analisis empirico de complejidad")

    plt.legend()
    plt.grid()

    plt.savefig(filename)
    plt.show()


def main():
    tamanios = [10, 50, 100, 200, 400, 800]

    resultados = correr_experimento(tamanios, repeticiones=10)

    tiempos_teoricos = ajuste_cuadratico(resultados)

    guardar_csv(resultados)

    graficar(resultados, tiempos_teoricos)


if __name__ == "__main__":
    main()

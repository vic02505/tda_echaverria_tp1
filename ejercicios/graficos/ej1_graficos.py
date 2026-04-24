import csv
from pathlib import Path
import subprocess
import sys

try:
    import matplotlib.pyplot as plt
except ImportError:  # pragma: no cover
    plt = None


DEFAULT_SIZES = [100, 500, 1000, 5000, 10000, 50000]


def parse_sizes(argv):
    if not argv:
        return DEFAULT_SIZES
    return [int(x) for x in argv]


def run_ej1(size, root_dir):
    script = root_dir / "ejercicios" / "ej-dyc" / "monedas.py"
    command = [sys.executable, str(script), str(size)]
    completed = subprocess.run(
        command,
        cwd=root_dir,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        mensaje = completed.stdout.strip() or completed.stderr.strip()
        raise RuntimeError(f"Error ejecutando monedas.py con n={size}: {mensaje}")

    tiempo = None
    pesadas = None
    for line in completed.stdout.splitlines():
        if line.startswith("Tiempo:"):
            tiempo = float(line.split(":", 1)[1].strip().split()[0])
        elif line.startswith("Pesadas:"):
            pesadas = int(line.split(":", 1)[1].strip())

    if tiempo is None or pesadas is None:
        raise RuntimeError(
            "Salida inesperada de monedas.py. Se esperaba 'Tiempo:' y 'Pesadas:'."
        )

    return tiempo, pesadas


def escala_lineal(valores, sizes):
    if not valores:
        return []
    if sizes[-1] == 0:
        return [0 for _ in sizes]
    factor = valores[-1] / sizes[-1] if valores[-1] != 0 else 0
    return [factor * n for n in sizes]


def guardar_csv(path_csv, sizes, tiempos, pesadas):
    with path_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["n", "tiempo_s", "pesadas"])
        for n, t, p in zip(sizes, tiempos, pesadas):
            writer.writerow([n, f"{t:.6f}", p])


def guardar_tabla_tex(path_tex, sizes, tiempos, pesadas):
    lineas = [
        "\\begin{table}[h]",
        "    \\centering",
        "    \\begin{tabular}{r r r}",
        "    \\hline",
        "    $n$ & Tiempo (s) & Pesadas \\\\",
        "    \\hline",
    ]
    for n, t, p in zip(sizes, tiempos, pesadas):
        lineas.append(f"    {n} & {t:.6f} & {p} \\\\")
    lineas += [
        "    \\hline",
        "    \\end{tabular}",
        "    \\caption{Resultados experimentales del ejercicio 1.}",
        "    \\label{tab:ej1-resultados}",
        "\\end{table}",
        "",
    ]
    path_tex.write_text("\n".join(lineas), encoding="utf-8")


def graficar_series(path_png, sizes, medidos, teoricos, ylabel, titulo):
    if plt is None:
        raise RuntimeError("matplotlib no esta instalado.")

    plt.figure(figsize=(7, 4))
    plt.plot(sizes, medidos, marker="o", label="Medido")
    plt.plot(sizes, teoricos, linestyle="--", label="Curva teorica O(n)")
    plt.xlabel("n")
    plt.ylabel(ylabel)
    plt.title(titulo)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(path_png, dpi=150)
    plt.close()


def main(argv):
    sizes = parse_sizes(argv)
    root_dir = Path(__file__).resolve().parents[2]

    tiempos = []
    pesadas = []
    for n in sizes:
        tiempo, pesada = run_ej1(n, root_dir)
        tiempos.append(tiempo)
        pesadas.append(pesada)

    out_dir = root_dir / "ejercicios" / "graficos" / "out"
    out_dir.mkdir(parents=True, exist_ok=True)

    report_dir = root_dir / "informe"
    img_dir = report_dir / "img"
    resultados_dir = report_dir / "resultados"
    img_dir.mkdir(parents=True, exist_ok=True)
    resultados_dir.mkdir(parents=True, exist_ok=True)

    guardar_csv(out_dir / "ej1_resultados.csv", sizes, tiempos, pesadas)
    guardar_tabla_tex(resultados_dir / "resultados_ej1.tex", sizes, tiempos, pesadas)

    tiempos_teo = escala_lineal(tiempos, sizes)
    pesadas_teo = escala_lineal(pesadas, sizes)

    graficar_series(
        img_dir / "ej1_tiempos.png",
        sizes,
        tiempos,
        tiempos_teo,
        "Tiempo (s)",
        "Ejercicio 1 - Tiempo vs n",
    )
    graficar_series(
        img_dir / "ej1_pesadas.png",
        sizes,
        pesadas,
        pesadas_teo,
        "Pesadas",
        "Ejercicio 1 - Pesadas vs n",
    )

    print("Listo: CSV, tabla .tex y graficos generados.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
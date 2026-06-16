
from pathlib import Path
import sys
import time


def encontrar_moneda_falsa_dyc(monedas, inicio, fin, contador):
    # caso 1 sola moneda
    if fin == inicio:
        contador[0] += 1
        return monedas[inicio]

    # caso 2 monedas seguidas
    if fin - inicio == 1:
        contador[0] += 1
        return monedas[inicio] if monedas[inicio] <= monedas[fin] else monedas[fin]

    medio = (inicio + fin) // 2
    prom_izq = sum(monedas[inicio : medio ]) / (medio - inicio)
    prom_der = sum(monedas[medio : fin ]) / (fin - medio )
    contador[0] += 1

    if prom_izq < prom_der:
        return encontrar_moneda_falsa_dyc(monedas, inicio, medio, contador)
    return encontrar_moneda_falsa_dyc(monedas, medio, fin, contador)


def encontrar_moneda_falsa(monedas):
    if not monedas:
        return None, 0

    contador = [0]
    resultado = encontrar_moneda_falsa_dyc(monedas, 0, len(monedas) - 1, contador)
    return resultado, contador[0]


def leer_monedas(archivo):
    contenido = Path(archivo).read_text(encoding="utf-8").strip()
    if not contenido:
        return []

    partes = contenido.replace("\n", ",").split(",")
    return [int(p.strip()) for p in partes if p.strip() != ""]


def main(argv):
    if len(argv) < 1:
        print("Error! Ejemplo de uso: python3 ejercicios/ej-dyc/monedas.py 100")
        return 1

    nombre = argv[0]
    if not nombre.endswith(".txt"):
        nombre = f"{nombre}.txt"

    base_dir = Path(__file__).resolve().parent
    ruta_archivo = base_dir / "inputs" / nombre

    if not ruta_archivo.exists():
        print(f"No existe el archivo de entrada: {ruta_archivo}")
        return 1

    monedas = leer_monedas(ruta_archivo)
    inicio = time.time()
    moneda_falsa, pesadas = encontrar_moneda_falsa(monedas)
    fin = time.time()

    print(f"Moneda falsa: {moneda_falsa}")
    print(f"Pesadas: {pesadas}")
    print(f"Tiempo: {fin - inicio:.8f} s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
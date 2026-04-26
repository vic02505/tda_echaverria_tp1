from lectura_escritura_de_archivos import obtener_laberinto_desde_archivo
from laberinto import encontrar_camino_bt
import sys
import time


def main():
    if len(sys.argv) != 2:
        print("Error: parametros incorrectos. La ejecucion debe ser en formato:")
        print("python3 ejercicios/ej-backtracking/laberinto_informe.py <archivo_input>")
        sys.exit(1)

    archivo_input_str = sys.argv[1]
    laberinto = obtener_laberinto_desde_archivo(archivo_input_str)

    t1 = time.perf_counter()
    _resultado = encontrar_camino_bt(laberinto)
    t2 = time.perf_counter()

    print(t2 - t1)


if __name__ == "__main__":
    main()

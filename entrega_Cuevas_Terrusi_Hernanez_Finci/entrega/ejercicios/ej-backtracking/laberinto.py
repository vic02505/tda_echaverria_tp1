from lectura_escritura_de_archivos import obtener_laberinto_desde_archivo
import sys
import time


DIRECCIONES = (
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0),
)

def obtener_inicio(laberinto):
    if not laberinto:
        return None, None

    for fila in range(len(laberinto)):
        for columna in range(len(laberinto[0])):
            if laberinto[fila][columna] == "E":
                return fila, columna

    return None, None


def posicion_valida(laberinto, fila, columna, visitados):
    return (
        fila >= 0
        and columna >= 0
        and fila < len(laberinto)
        and columna < len(laberinto[0])
        and laberinto[fila][columna] != "X"
        and (fila, columna) not in visitados
    )


def avanzar(laberinto, fila, columna, resultado, visitados):
    if not posicion_valida(laberinto, fila, columna, visitados):
        return False

    resultado.append((fila, columna))
    visitados.add((fila, columna))

    if laberinto[fila][columna] == "S":
        return True

    for desplazamiento_fila, desplazamiento_columna in DIRECCIONES:
        nueva_fila = fila + desplazamiento_fila
        nueva_columna = columna + desplazamiento_columna

        if avanzar(laberinto, nueva_fila, nueva_columna, resultado, visitados):
            return True

    resultado.pop()
    return False


def encontrar_camino_bt(laberinto):
    fila_inicial, columna_inicial = obtener_inicio(laberinto)

    if fila_inicial is None or columna_inicial is None:
        return []

    resultado = []
    visitados = set()

    encontro_salida = avanzar(
        laberinto,
        fila_inicial,
        columna_inicial,
        resultado,
        visitados
    )

    if encontro_salida:
        return resultado

    return []


def main():
    if len(sys.argv) != 2:
        print("Error: parametros incorrectos. La ejecucion debe ser en formato:")
        print("python3 ejercicios/ej-backtracking/laberinto.py <archivo_input>")
        sys.exit(1)

    archivo_input_str = sys.argv[1]

    laberinto = obtener_laberinto_desde_archivo(archivo_input_str)
    t1 = time.time()
    resultado = encontrar_camino_bt(laberinto)
    t2 = time.time()
    print(resultado)
    print(t2 - t1)


if __name__ == "__main__":
    main()
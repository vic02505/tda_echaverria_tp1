from lectura_escritura_de_archivos import obtener_laberinto_desde_archivo, guardar_resultado
import sys
import time

def obtener_inicio(laberinto):
    for fila in range(0,len(laberinto)):
        for columna in range(0,len(laberinto[0])):
            if laberinto[fila][columna]== "E":
                return (fila,columna)
    return (None,None)

def avanzar(laberinto,fila,columna,resultado,visitados):
    if (fila < 0 or columna < 0 or fila >= len(laberinto) or columna >= len(laberinto[0])
        or laberinto[fila][columna] == "X" or (fila,columna) in visitados):
        return resultado
    
    resultado.append((fila,columna))
    visitados.append((fila,columna))
    
    derecha = avanzar(laberinto,fila,columna+1,resultado,visitados)

    fila_derecha, columna_derecha = derecha[len(derecha)-1]
    
    if(laberinto[fila_derecha][columna_derecha] == "S"):
        return derecha
    
    izquierda = avanzar(laberinto,fila,columna-1,resultado,visitados)
    
    fila_izquierda, columna_izquierda = izquierda[len(izquierda)-1]
    
    if(laberinto[fila_izquierda][columna_izquierda] == "S"):
        return izquierda
    
    abajo = avanzar(laberinto,fila+1,columna,resultado,visitados)
    
    fila_abajo, columna_abajo = abajo[len(abajo)-1]
    
    if(laberinto[fila_abajo][columna_abajo] == "S"):
        return abajo

    arriba = avanzar(laberinto,fila-1,columna,resultado,visitados)
    fila_arriba, columna_arriba = arriba[len(arriba)-1]

    if(laberinto[fila_arriba][columna_arriba] == "S"):
        return arriba
    
    resultado.pop()
    return resultado


def encontrar_camino_bt(laberinto):
    fila_inicial, columna_inicial = obtener_inicio(laberinto)

    if fila_inicial == None or columna_inicial == None:
        return []
    
    return avanzar(laberinto,fila_inicial,columna_inicial,[],[])


def main():
    if(len(sys.argv) != 3):
        print("Error: parametros incorrectos. La ejecucion debe ser en formato:")
        print("python3 ejercicios/ejercicio_3/ejercicio_3.py <archivo_input> <archivo_output>")
        sys.exit(1)

    archivo_input_str = sys.argv[1]
    archivo_output_str = sys.argv[2]
    laberinto = obtener_laberinto_desde_archivo(archivo_input_str)
    t1 = time.time()
    resultado = encontrar_camino_bt(laberinto)
    t2 = time.time()
    print(t2 - t1)
    guardar_resultado(resultado,archivo_output_str)

main()

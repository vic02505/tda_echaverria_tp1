def obtener_inicio(laberinto):
    for fila in range(0,len(laberinto)):
        for columna in range(0,len(laberinto[0])):
            if laberinto[fila][columna]== "E":
                return (fila,columna)
    return (None,None)

def avanzar(laberinto,fila,columna,resultado):
    if (fila < 0 or columna < 0 or fila >= len(laberinto) or columna >= len(laberinto[0])
        or laberinto[fila][columna] == "X" or (fila,columna) in resultado):
        return resultado
    
    resultado.append((fila,columna))
    derecha = avanzar(laberinto,fila,columna+1,resultado)

    fila_derecha, columna_derecha = derecha[len(derecha)-1]
    
    if(laberinto[fila_derecha][columna_derecha] == "S"):
        return derecha
    
    izquierda = avanzar(laberinto,fila,columna-1,resultado)
    
    fila_izquierda, columna_izquierda = izquierda[len(izquierda)-1]
    
    if(laberinto[fila_izquierda][columna_izquierda] == "S"):
        return izquierda
    
    abajo = avanzar(laberinto,fila+1,columna,resultado)
    
    fila_abajo, columna_abajo = abajo[len(abajo)-1]
    
    if(laberinto[fila_abajo][columna_abajo] == "S"):
        return abajo

    arriba = avanzar(laberinto,fila-1,columna,resultado)
    fila_arriba, columna_arriba = arriba[len(arriba)-1]

    if(laberinto[fila_arriba][columna_arriba] == "S"):
        return arriba
    
    resultado.pop()
    return resultado


def encontrar_camino_bt(laberinto):
    fila_inicial, columna_inicial = obtener_inicio(laberinto)

    if fila_inicial == None or columna_inicial == None:
        return []
    
    return avanzar(laberinto,fila_inicial,columna_inicial,[])

laberinto = [
    ["X","X","X","X","X","X","X","X"],
    ["X"," "," "," "," ","X"," ","S"],
    ["X"," ","X","X","X","X"," ","X"],
    ["X"," "," "," ","X","X"," ","X"],
    ["X"," ","X"," "," "," "," ","X"],
    ["X","E","X","X","X","X","X","X"]
]

resultado = encontrar_camino_bt(laberinto)
print(resultado)

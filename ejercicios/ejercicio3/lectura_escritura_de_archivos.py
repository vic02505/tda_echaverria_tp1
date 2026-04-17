def obtener_laberinto_desde_archivo(archivo_str):
    laberinto = []

    with open(archivo_str, "r") as archivo:
        for linea in archivo:
            fila = []
            linea = linea.strip() 

            if not linea:
                continue

            for caracter in linea:
                fila.append(caracter)
            
            laberinto.append(fila)
    
    return laberinto

def guardar_resultado(resultado,archivo_str):
    with open(archivo_str, "w") as archivo:
        archivo.write(str(resultado))
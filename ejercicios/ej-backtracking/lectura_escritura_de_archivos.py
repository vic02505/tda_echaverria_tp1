import os


def _resolver_ruta_laberinto(archivo_str):
    if os.path.isfile(archivo_str):
        return archivo_str

    base_dir = os.path.dirname(__file__)
    ruta_relativa = os.path.join(base_dir, archivo_str)
    if os.path.isfile(ruta_relativa):
        return ruta_relativa

    ruta_set_datos = os.path.join(base_dir, "set_de_datos", archivo_str)
    if os.path.isfile(ruta_set_datos):
        return ruta_set_datos

    raise FileNotFoundError(f"No se encontro el laberinto: {archivo_str}")


def obtener_laberinto_desde_archivo(archivo_str):
    laberinto = []
    ruta = _resolver_ruta_laberinto(archivo_str)

    with open(ruta, "r") as archivo:
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
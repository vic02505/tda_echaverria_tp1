def encontrar_moneda_falsa_dyc(monedas, inicio, fin, contador):
    if inicio >= fin:
        return monedas[inicio]

    if fin - inicio == 1:
        contador[0] += 1
        return monedas[inicio] if monedas[inicio] <= monedas[fin] else monedas[fin]

    medio = (inicio + fin) // 2

    contador[0] += 1
    if monedas[medio] != monedas[medio + 1]:
        return monedas[medio] if monedas[medio] < monedas[medio + 1] else monedas[medio + 1]

    izquierdo = encontrar_moneda_falsa_dyc(monedas, inicio, medio, contador)
    derecho = encontrar_moneda_falsa_dyc(monedas, medio + 1, fin, contador)

    contador[0] += 1
    return izquierdo if izquierdo <= derecho else derecho

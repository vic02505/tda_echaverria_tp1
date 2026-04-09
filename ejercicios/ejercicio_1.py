
def encontrar_moneda_falsa_dyc(monedas, inicio, fin):
    if inicio >= fin:
        return monedas[inicio]

    if fin - inicio == 1:
        return min(monedas[inicio], monedas[fin])

    medio = (inicio + fin) // 2

    if monedas[medio] != monedas[medio+1]:
        return min(monedas[medio], monedas[medio+1])

    izquierdo = encontrar_moneda_falsa_dyc(monedas, inicio, medio)
    derecho = encontrar_moneda_falsa_dyc(monedas, medio+1, fin)

    return min(izquierdo, derecho)

def encontrar_moneda_falsa(monedas):
    if not monedas or len(monedas) == 0:
        return None

    return encontrar_moneda_falsa_dyc(monedas, 0, len(monedas) - 1)
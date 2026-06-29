
def paolo():
    n = int(input("INGRESE EL NUMERO DE VERTICES "))
    cost = [[0 for _ in range(n)] for _ in range(n)]
    dist = [0 for _ in range(n)]
    sol = [0 for _ in range(n)]
    a = 1
    print("INGRESE EL CUADRO DE COSTOS (INGRESE 0,0 PARA TERMINAR)")
    print()
    while True:
        a, b = map(int, input("EL EJE ").split())
        if a == 0 and b == 0:
            break
        cost[a][b] = int(input("COSTO DEL EJE "))
    for i in range(n):
        for j in range(n):
            if cost[i][j] == 0:
                cost[i][j] = 15000
    for i in range(n):
        for j in range(i):
            cost[i][j] = cost[j][i]
    v = int(input("INGRESE EL VERTICE DE SALIDA "))
    for i in range(n):
        dist[i] = cost[v][i]
        sol[i] = 0
    paolo_sub(n, cost, dist, sol, v)
    print("SALIDA", "LLEGADA", "DISTANCIA")
    for i in range(n):
        if dist[i] < 15000:
            print(v, i, dist[i])
    res = input("OTRA VEZ? (SI/NO) ")
    if res == "NO":
        return
    for i in range(n):
        sol[i] = 0
        dist[i] = 0
    paolo()

def paolo_sub(n, cost, dist, sol, v):
    sol[v] = 1
    dist[v] = 0
    for i in range(n - 1):
        u = 15000
        for j in range(n):
            if dist[j] <= u and sol[j] == 0:
                u = j
        sol[u] = 1
        for j in range(n):
            if dist[j] >= (dist[u] + cost[u][j]):
                dist[j] = dist[u] + cost[u][j]

if __name__ == "__main__":
    paolo()
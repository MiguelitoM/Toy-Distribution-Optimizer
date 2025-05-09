from pulp import *
import sys

def main():
    prob = LpProblem("P3", LpMaximize)

    # ler input
    data = sys.stdin.readlines()
    n, m, t = map(int, data[0].split())
    fabricas = []
    for i in range(1,n+1):
        _, pais, stock = map(int, data[i].split())
        fabricas.append([pais - 1, stock, []]) # [pais, stock, criancas]

    paises = []
    for i in range(n+1,n+m+1):
        line = list(map(int, data[i].split()))
        paises.append([line[1], line[2], []]) # [max exportacoes, min criancas felizes, fabricas]

    criancas_por_pais = [set() for _ in range(m)]
    criancas = []
    entregas = {}
    for i in range(n+m+1,n+m+t+1):
        line = [int(x) - 1 for x in data[i].split()]
        pais = line[1]
        c = i - n - m - 1
        criancas_por_pais[pais].add(c)
        criancas.append([pais, set()]) # [pais, fabricas]
        pedidos = line[2:]
        for pedido in pedidos:
            # entregas[c,f] = 1 if child c uses factory f, else 0
            if fabricas[pedido][1] <= 0:
                continue
            criancas[c][1].add(pedido)
            entregas[c,pedido] = LpVariable(f"e_{c}_{pedido}", 0, 1, LpBinary)
            fabricas[pedido][2].append(c)

#fabricas = [f for f in fabricas if f[1] > 0 and len(f[2]) > 0]

    for c in range(t):
        # Only factories in criancas[c][1] are allowed and each child only has 1 toy
        prob += lpSum(entregas[c,f] for f in criancas[c][1]) <= 1

    # Stock constraints: sum of entregas[c,f] over c <= stock of factory f
    for f in range(n):
        num_criancas = len(fabricas[f][2])
        if fabricas[f][1] <= 0 or num_criancas == 0:
            continue
        pais = fabricas[f][0]
        paises[pais][2].append(f)
        if num_criancas > fabricas[f][1]: # se numero de criancas <= stock   
            prob += lpSum(entregas[c,f] for c in fabricas[f][2]) <= fabricas[f][1]

    # Max export constraints for each country p
    for p in range(m):
        if len(criancas_por_pais[p]) < paises[p][1]:
            return -1
        # sum of entregas[c,f] where factory f is in p and child c in a different country
        export_sum = 0
        for f in paises[p][2]:
            for c in fabricas[f][2]:
                if criancas[c][0] != p:  # child in a different country
                    export_sum += entregas[c,f]
        prob += export_sum <= paises[p][0]

        # Min happy children constraints for each country p
        # sum of crianca_feliz[c] where child c is in p
        prob += lpSum(entregas[c, f] for c in criancas_por_pais[p] for f in criancas[c][1]) >= paises[p][1]

    # Objective: maximize sum of all happy children
    prob += lpSum(entregas[c, f] for c in range(t) for f in criancas[c][1])

    # Solve
    status = prob.solve(GLPK(msg=0))

    # Check feasibility
    if LpStatus[status] == "Optimal":
        result = value(prob.objective)
        return result
    else:
        return -1

print(main())
"""
Red de fibra óptica entre sedes universitarias de Medellín.
Árbol de expansión mínima (AEM) con Prim y Kruskal.

IMPORTANTE: las distancias (km) son ESTIMACIONES por vía. Reemplácenlas por
las medidas con Google Maps (ruta en carro) antes de entregar.
"""
import heapq

NODOS = [
    "Luis Amigó",        # 0
    "U. de Antioquia",   # 1
    "U. Nacional",       # 2
    "UPB",               # 3
    "U. de Medellín",    # 4
    "EAFIT",             # 5
    "Politécnico JIC",   # 6
    "ITM Robledo",       # 7
]

# (origen, destino, costo en km)
ARISTAS = [
    (0, 1, 3.5), (0, 2, 6.5), (0, 3, 6.5), (0, 7, 6.0),
    (1, 2, 4.5), (1, 3, 4.5), (1, 5, 7.5), (1, 4, 7.0), (1, 7, 4.5),
    (2, 3, 4.0), (2, 7, 2.5), (2, 4, 8.0),
    (3, 4, 4.0), (3, 5, 8.0), (3, 7, 3.5),
    (4, 5, 6.5), (4, 6, 7.0),
    (5, 6, 3.0),
]


def kruskal(n, aristas):
    padre = list(range(n))

    def buscar(x):
        while padre[x] != x:
            padre[x] = padre[padre[x]]
            x = padre[x]
        return x

    elegidas = []
    for u, v, w in sorted(aristas, key=lambda a: a[2]):
        ru, rv = buscar(u), buscar(v)
        if ru != rv:          # no forma ciclo
            padre[ru] = rv
            elegidas.append((u, v, w))
            print(f"  Kruskal acepta ({NODOS[u]} - {NODOS[v]}) = {w}")
        else:
            print(f"  Kruskal rechaza ({NODOS[u]} - {NODOS[v]}) = {w} (ciclo)")
    return elegidas


def prim(n, aristas, inicio=0):
    ady = {i: [] for i in range(n)}
    for u, v, w in aristas:
        ady[u].append((w, u, v))
        ady[v].append((w, v, u))
    visitados = {inicio}
    cola = list(ady[inicio])
    heapq.heapify(cola)
    elegidas = []
    while cola and len(visitados) < n:
        w, u, v = heapq.heappop(cola)
        if v in visitados:
            continue
        visitados.add(v)
        elegidas.append((u, v, w))
        print(f"  Prim agrega ({NODOS[u]} - {NODOS[v]}) = {w}")
        for e in ady[v]:
            if e[2] not in visitados:
                heapq.heappush(cola, e)
    return elegidas


if __name__ == "__main__":
    n = len(NODOS)
    print("== Kruskal ==")
    k = kruskal(n, ARISTAS)
    print("\n== Prim (inicio: Luis Amigó) ==")
    p = prim(n, ARISTAS)

    ck = sum(w for _, _, w in k)
    cp = sum(w for _, _, w in p)
    print(f"\nCosto Kruskal: {ck} km | Costo Prim: {cp} km")
    print("Aristas del AEM:", len(k), "(debe ser n-1 =", n - 1, ")")
    assert abs(ck - cp) < 1e-9, "Prim y Kruskal deben dar el mismo costo"

    # Verificación independiente con networkx (si está instalado)
    try:
        import networkx as nx
        G = nx.Graph()
        G.add_weighted_edges_from(ARISTAS)
        T = nx.minimum_spanning_tree(G)
        print("Costo networkx:", T.size(weight="weight"))
        assert abs(T.size(weight="weight") - ck) < 1e-9
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
            pos = nx.spring_layout(G, seed=3)
            etiquetas = {i: NODOS[i] for i in range(n)}
            nx.draw_networkx(G, pos, labels=etiquetas, node_color="#dbeafe",
                             edge_color="#cbd5e1", font_size=8)
            nx.draw_networkx_edges(T, pos, edge_color="#dc2626", width=2.5)
            nx.draw_networkx_edge_labels(
                G, pos, {(u, v): w for u, v, w in ARISTAS}, font_size=7)
            plt.axis("off")
            plt.savefig("grafo_aem.png", dpi=200, bbox_inches="tight")
            print("Figura guardada: grafo_aem.png")
        except ImportError:
            pass
    except ImportError:
        print("networkx no instalado (pip install networkx matplotlib)")

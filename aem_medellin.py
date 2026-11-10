"""
Red de fibra óptica entre sedes universitarias de Medellín.
Árbol de expansión mínima (AEM) con Prim y Kruskal.

Distancias (km) medidas por el equipo en Google Maps: modo carro, ruta de
menos kilómetros, siempre del vértice menor al mayor.
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
    (0, 1, 3.2), (0, 2, 1.4), (0, 3, 2.1), (0, 7, 2.1),
    (1, 2, 1.8), (1, 3, 3.8), (1, 4, 7.2), (1, 5, 10.4), (1, 7, 3.5),
    (2, 3, 4.1), (2, 4, 7.5), (2, 7, 3.7),
    (3, 4, 3.1), (3, 5, 8.5), (3, 7, 5.9),
    (4, 5, 6.9), (4, 6, 6.6),
    (5, 6, 2.0),
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

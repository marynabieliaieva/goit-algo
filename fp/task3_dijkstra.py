"""Завдання 3. Алгоритм Дейкстри з бінарною купою (heapq)."""

import heapq


class Graph:
    """Зважений неорієнтований граф у вигляді списку суміжності."""

    def __init__(self):
        self.adj = {}

    def add_edge(self, u, v, weight):
        if weight < 0:
            raise ValueError("Алгоритм Дейкстри не працює з від'ємними вагами")
        self.adj.setdefault(u, []).append((v, weight))
        self.adj.setdefault(v, []).append((u, weight))

    def vertices(self):
        return list(self.adj)


def dijkstra(graph, start):
    """Повертає (distances, previous): найкоротші відстані від start до всіх вершин
    і словник попередників для відновлення шляхів."""
    distances = {v: float("inf") for v in graph.vertices()}
    previous = {v: None for v in graph.vertices()}
    distances[start] = 0

    heap = [(0, start)]  # бінарна купа: (відстань, вершина)
    visited = set()

    while heap:
        dist, u = heapq.heappop(heap)  # вершина з найменшою відстанню за O(log n)
        if u in visited:
            continue  # застарілий запис у купі
        visited.add(u)

        for v, weight in graph.adj[u]:
            new_dist = dist + weight
            if new_dist < distances[v]:
                distances[v] = new_dist
                previous[v] = u
                heapq.heappush(heap, (new_dist, v))

    return distances, previous


def build_path(previous, target):
    path = []
    while target is not None:
        path.append(target)
        target = previous[target]
    return path[::-1]


if __name__ == "__main__":
    g = Graph()
    edges = [
        ("A", "B", 4), ("A", "C", 2), ("B", "C", 5), ("B", "D", 10),
        ("C", "E", 3), ("E", "D", 4), ("D", "F", 11), ("E", "F", 9),
    ]
    for u, v, w in edges:
        g.add_edge(u, v, w)

    start = "A"
    dist, prev = dijkstra(g, start)
    print(f"Найкоротші шляхи від вершини {start}:")
    for vertex in sorted(dist):
        path = " -> ".join(build_path(prev, vertex))
        print(f"  {vertex}: відстань {dist[vertex]:>3}   шлях: {path}")

    assert dist == {"A": 0, "B": 4, "C": 2, "D": 9, "E": 5, "F": 14}
    print("Перевірку пройдено.")

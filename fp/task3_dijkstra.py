"""Task 3. Dijkstra's algorithm with a binary heap (heapq)."""

import heapq


class Graph:
    """Weighted undirected graph stored as an adjacency list."""

    def __init__(self):
        self.adj = {}

    def add_edge(self, u, v, weight):
        if weight < 0:
            raise ValueError("Dijkstra's algorithm does not support negative weights")
        self.adj.setdefault(u, []).append((v, weight))
        self.adj.setdefault(v, []).append((u, weight))

    def vertices(self):
        return list(self.adj)


def dijkstra(graph, start):
    """Return (distances, previous): shortest distances from `start` to every vertex
    and a predecessor map used to rebuild the paths."""
    distances = {v: float("inf") for v in graph.vertices()}
    previous = {v: None for v in graph.vertices()}
    distances[start] = 0

    heap = [(0, start)]  # binary heap of (distance, vertex)
    visited = set()

    while heap:
        dist, u = heapq.heappop(heap)  # vertex with the smallest distance in O(log n)
        if u in visited:
            continue  # stale heap entry
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
    print(f"Shortest paths from vertex {start}:")
    for vertex in sorted(dist):
        path = " -> ".join(build_path(prev, vertex))
        print(f"  {vertex}: distance {dist[vertex]:>3}   path: {path}")

    assert dist == {"A": 0, "B": 4, "C": 2, "D": 9, "E": 5, "F": 14}
    print("Check passed.")

import heapq
from functools import lru_cache

class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, u, v, weight):
        self.graph.setdefault(u, []).append((v, weight))
        self.graph.setdefault(v, []).append((u, weight))

    def dijkstra(self, start):
        distances = {node: float('inf') for node in self.graph}
        previous = {node: None for node in self.graph}

        distances[start] = 0
        pq = [(0, start)]

        while pq:
            current_distance, current = heapq.heappop(pq)

            if current_distance > distances[current]:
                continue

            for neighbor, weight in self.graph[current]:
                distance = current_distance + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current
                    heapq.heappush(pq, (distance, neighbor))

        return distances, previous

    def shortest_path(self, start, end):
        distances, previous = self.dijkstra(start)

        if distances[end] == float('inf'):
            return None, float('inf')

        path = []
        current = end

        while current is not None:
            path.append(current)
            current = previous[current]

        path.reverse()

        return path, distances[end]


def build_graph():
    g = Graph()

    edges = [
        ('A', 'B', 4),
        ('A', 'C', 2),
        ('B', 'C', 1),
        ('B', 'D', 5),
        ('C', 'D', 8),
        ('C', 'E', 10),
        ('D', 'E', 2),
        ('D', 'F', 6),
        ('E', 'F', 3)
    ]

    for u, v, w in edges:
        g.add_edge(u, v, w)

    return g


def main():
    graph = build_graph()

    start = input("Enter starting node: ").upper()
    end = input("Enter destination node: ").upper()

    if start not in graph.graph or end not in graph.graph:
        print("Invalid node!")
        return

    path, distance = graph.shortest_path(start, end)

    if path is None:
        print("No path exists.")
    else:
        print("\nShortest Path:")
        print(" -> ".join(path))
        print(f"Total Cost: {distance}")


if __name__ == "__main__":
    main()
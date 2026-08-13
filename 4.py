import heapq

def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0

    priority_queue = [(0, start)]
    previous = {node: None for node in graph}

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances, previous


def shortest_path(previous, start, target):
    path = []
    current = target

    while current is not None:
        path.append(current)
        current = previous[current]

    path.reverse()

    if path[0] != start:
        return []

    return path


graph = {
    'A': [('B', 4), ('C', 2)],
    'B': [('A', 4), ('C', 1), ('D', 5)],
    'C': [('A', 2), ('B', 1), ('D', 8), ('E', 10)],
    'D': [('B', 5), ('C', 8), ('E', 2), ('F', 6)],
    'E': [('C', 10), ('D', 2), ('F', 3)],
    'F': [('D', 6), ('E', 3)]
}

start = 'A'
target = 'F'

distances, previous = dijkstra(graph, start)
path = shortest_path(previous, start, target)

print("Shortest distances:")
for node, distance in distances.items():
    print(f"{start} → {node} = {distance}")

print("\nShortest Path:")
print(" → ".join(path))

print("\nShortest Distance:", distances[target])
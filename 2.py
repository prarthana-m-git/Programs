import heapq


class Graph:
    def __init__(self):
        self.graph = {}

    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = []

    def add_edge(self, u, v, weight):
        self.add_node(u)
        self.add_node(v)

        self.graph[u].append((v, weight))
        self.graph[v].append((u, weight))

    def display_graph(self):
        print("\n========== GRAPH ==========")

        for node, connections in self.graph.items():
            print(f"{node} -> ", end="")

            for neighbor, weight in connections:
                print(f"{neighbor}({weight}) ", end="")

            print()

    def dijkstra(self, start):
        distances = {
            node: float("inf")
            for node in self.graph
        }

        previous = {
            node: None
            for node in self.graph
        }

        distances[start] = 0

        priority_queue = [(0, start)]

        while priority_queue:

            current_distance, current_node = heapq.heappop(
                priority_queue
            )

            if current_distance > distances[current_node]:
                continue

            for neighbor, weight in self.graph[current_node]:

                new_distance = (
                    current_distance + weight
                )

                if new_distance < distances[neighbor]:

                    distances[neighbor] = new_distance
                    previous[neighbor] = current_node

                    heapq.heappush(
                        priority_queue,
                        (new_distance, neighbor)
                    )

        return distances, previous

    def get_path(self, previous, start, destination):

        path = []
        current = destination

        while current is not None:
            path.append(current)
            current = previous[current]

        path.reverse()

        if path[0] != start:
            return []

        return path

    def shortest_path(self, start, destination):

        distances, previous = self.dijkstra(start)

        if distances[destination] == float("inf"):
            return [], float("inf")

        path = self.get_path(
            previous,
            start,
            destination
        )

        return path, distances[destination]

    def display_all_distances(self, start):

        distances, _ = self.dijkstra(start)

        print(
            f"\nShortest distances from {start}:"
        )

        for node, distance in distances.items():

            if distance == float("inf"):
                print(f"{node} : Unreachable")
            else:
                print(f"{node} : {distance}")


def create_graph():

    graph = Graph()

    roads = [

        ("A", "B", 4),
        ("A", "C", 2),

        ("B", "C", 1),
        ("B", "D", 5),

        ("C", "D", 8),
        ("C", "E", 10),

        ("D", "E", 2),
        ("D", "F", 6),

        ("E", "F", 3),

        ("F", "G", 4),
        ("E", "G", 7),

        ("G", "H", 2),
        ("F", "H", 8)
    ]

    for u, v, weight in roads:
        graph.add_edge(u, v, weight)

    return graph


def display_route(path, graph):

    print("\n========== ROUTE ==========")

    total = 0

    for i in range(len(path) - 1):

        current = path[i]
        next_node = path[i + 1]

        weight = None

        for neighbor, cost in graph.graph[current]:

            if neighbor == next_node:
                weight = cost
                break

        total += weight

        print(
            f"{current} --({weight})--> {next_node}"
        )

    print("----------------------------")
    print(f"Total cost : {total}")


def main():

    graph = create_graph()

    while True:

        print("\n")
        print("================================")
        print("     SMART ROUTE FINDER")
        print("================================")
        print("1. Display Graph")
        print("2. Find Shortest Path")
        print("3. Show All Shortest Distances")
        print("4. Add New Road")
        print("5. Exit")
        print("================================")

        choice = input(
            "Enter your choice: "
        ).strip()

        if choice == "1":

            graph.display_graph()

        elif choice == "2":

            start = input(
                "Enter starting node: "
            ).upper().strip()

            destination = input(
                "Enter destination node: "
            ).upper().strip()

            if (
                start not in graph.graph
                or destination not in graph.graph
            ):
                print("\n❌ Invalid node!")

                continue

            path, distance = graph.shortest_path(
                start,
                destination
            )

            if not path:

                print(
                    "\n❌ No route exists!"
                )

            else:

                print(
                    f"\nShortest path: "
                    f"{' -> '.join(path)}"
                )

                print(
                    f"Minimum cost: {distance}"
                )

                display_route(
                    path,
                    graph
                )

        elif choice == "3":

            start = input(
                "Enter starting node: "
            ).upper().strip()

            if start not in graph.graph:

                print("\n❌ Invalid node!")

                continue

            graph.display_all_distances(start)

        elif choice == "4":

            u = input(
                "Enter first node: "
            ).upper().strip()

            v = input(
                "Enter second node: "
            ).upper().strip()

            try:

                weight = float(
                    input(
                        "Enter road cost: "
                    )
                )

                if weight <= 0:

                    print(
                        "\n❌ Cost must be positive!"
                    )

                    continue

                graph.add_edge(
                    u,
                    v,
                    weight
                )

                print(
                    "\n✅ New road added!"
                )

            except ValueError:

                print(
                    "\n❌ Enter a valid number!"
                )

        elif choice == "5":

            print(
                "\nProgram terminated. Goodbye!"
            )

            break

        else:

            print(
                "\n❌ Invalid choice!"
            )


if __name__ == "__main__":
    main()
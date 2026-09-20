import heapq


def dijkstra(graph, source, destination):
    distances = {
        node: float("inf")
        for node in graph
    }

    previous = {
        node: None
        for node in graph
    }

    distances[source] = 0

    priority_queue = [(0, source)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(
            priority_queue
        )

        if current_distance > distances[current_node]:
            continue

        if current_node == destination:
            break

        for neighbor, latency in graph[current_node]:
            new_distance = current_distance + latency

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current_node

                heapq.heappush(
                    priority_queue,
                    (new_distance, neighbor)
                )

    # No route exists
    if distances[destination] == float("inf"):
        return None

    # Reconstruct path
    path = []
    current = destination

    while current is not None:
        path.append(current)
        current = previous[current]

    path.reverse()

    return {
        "total_latency": distances[destination],
        "path": path,
    }
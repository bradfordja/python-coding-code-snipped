# Weighted Path / Dijkstra
## Question: Find shortest distance in a weighted graph.
import heapq
from collections import defaultdict

def dijkstra(edges, start, end):
    graph = defaultdict(list)

    for source, target, weight in edges:
        graph[source].append((target, weight))
        graph[target].append((source, weight))

    min_heap = [(0, start)]
    visited = set()

    while min_heap:
        current_distance, node = heapq.heappop(min_heap)

        if node in visited:
            continue

        if node == end:
            return current_distance

        visited.add(node)

        for neighbor, weight in graph[node]:
            if neighbor not in visited:
                heapq.heappush(
                    min_heap,
                    (current_distance + weight, neighbor)
                )

    return -1

print(dijkstra([("A", "B", 1), ("B", "C", 2), ("A", "C", 4)], "A", "C"))  # Output: 3

## Interview note: Use BFS for unweighted graphs; use Dijkstra for weighted graphs.
### Complexity: O((V + E) log V)
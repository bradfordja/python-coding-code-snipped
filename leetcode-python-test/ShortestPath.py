# Shortest Path

## Question: 
## Given nodes and edges, return the shortest path from first node to last node.

from collections import defaultdict, deque

def shortest_path(str_arr):
    node_count = int(str_arr[0])
    nodes = str_arr[1:node_count + 1]
    edges = str_arr[node_count + 1:]

    graph = defaultdict(list)

    for edge in edges:
        start, end = edge.split("-")
        graph[start].append(end)
        graph[end].append(start)

    start_node = nodes[0]
    end_node = nodes[-1]

    queue = deque([(start_node, [start_node])])
    visited = {start_node}

    while queue:
        current, path = queue.popleft()

        if current == end_node:
            return "-".join(path)

        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return -1

print(shortest_path(["4", "A", "B", "C", "D", "A-B", "B-C", "C-D"]))  # Output: "A-B-C-D"
print(shortest_path(["4", "A", "B", "C", "D", "A-B", "B-D"]))  # Output: "A-B-D"
print(shortest_path(["4", "A", "B", "C", "D", "A-B", "C-D"]))  # Output: -1

## Interview note: 
### BFS gives shortest path in an unweighted graph.
### Complexity: O(V + E)
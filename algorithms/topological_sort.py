from collections import deque

def topo_sort(graph, vertices):
    indegree = {v: 0 for v in vertices}
    queue = deque()
    topo_order = []

    # count incoming edges
    for u in vertices:
        for nei, _ in graph[u]:
            indegree[nei] += 1
    
    # find all vertices with indegree 0
    for v in indegree:
        if indegree[v] == 0:
            queue.append(v)
    
    while queue:
        node = queue.popleft()
        topo_order.append(node)

        for nei, _ in graph[node]:
            indegree[nei] -= 1

            if indegree[nei] == 0:
                queue.append(nei)

    if len(topo_order) != len(vertices):
        raise ValueError("Graph contains a cycle")

    return topo_order


vertices = ["A", "B", "C", "D", "E", "F", "G"]
graph = {
    "A": [("C", 2), ("D", 4)],
    "B": [("D", 1), ("E", 3)],
    "C": [("F", 5)],
    "D": [("F", 2), ("G", 6)],
    "E": [("G", 1)],
    "F": [("G", 2)],
    "G": []
}

print(topo_sort(graph, vertices))

vertices = ["F", "C", "A", "E", "B", "D"]

graph = {
    "F": [],
    "C": [("B", 2)],
    "A": [("E", 1), ("C", 3)],
    "E": [("D", 4)],
    "B": [("D", 2)],
    "D": []
}

print(topo_sort(graph, vertices))

vertices = ["A", "B", "C", "D", "E"]
graph = {
    "A": [("B", 1)],
    "B": [("C", 1)],
    "C": [("B", 1)],
    "D": [("E", 1)],
    "E": []
}

# print(topo_sort(graph, vertices))
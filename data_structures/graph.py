from collections import deque
import heapq

from algorithms.topological_sort import topo_sort

class Graph:

    def __init__(self, vertices, edges, directed=True):
        self.vertices = vertices
        self.edges = edges
        self.directed = directed
        self.adj = {v: [] for v in vertices}

        for u, v, w in self.edges:
            if u not in self.adj or v not in self.adj:
                raise ValueError(f"invalid edge: ({u}, {v})")
            
            self.adj[u].append((v, w))
        
            if not self.directed:
                self.adj[v].append((u, w))
    
    def __str__(self):
        return str(self.adj)  

    # Time: extract min dist: O(VlogV) + push a new shorter edge: O(ElogV) = O((V+E)logV) For a connected graph, E >= V-1 so O(ElogV)
    def dijkstra(self, start):
        """Single source shortest path, negative edges are not allowed."""

        if start not in self.vertices:
            raise ValueError("invalid starting vertex")
        
        dist = {v: float('inf') for v in self.vertices}
        dist[start] = 0

        minHeap = [(0, start)]

        while minHeap:
            d1, n1 = heapq.heappop(minHeap)

            if d1 > dist[n1]:
                continue

            for n2, w2 in self.adj[n1]:
                if d1 + w2 < dist[n2]:
                    dist[n2] = d1 + w2
                    heapq.heappush(minHeap, (dist[n2], n2))

        return dist
    
    # Time: O(VE) For a connected graph, E >= V-1 so O(E^2)
    def bellman_ford(self, start):
        """Single source shortest path, negative edges allowed."""

        if start not in self.vertices:
            raise ValueError("invalid starting vertex")
        
        dist = {v: float('inf') for v in self.vertices}
        dist[start] = 0

        # A shortest path without cycles can contain at most V-1 edges
        # Each complete pass can propagate shortest-path information one edge farther along a path, so V-1 passes are sufficient
        for _ in range(len(self.vertices) - 1):
            for u, v, w in self.edges:
                if dist[u] != float('inf') and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                
                if not self.directed:
                    if dist[v] != float('inf') and dist[v] + w < dist[u]:
                        dist[u] = dist[v] + w
        
        # Final loop checking for negative weight cycles
        updated = False
        for u, v, w in self.edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                updated = True
                
            if not self.directed:
                if dist[v] != float('inf') and dist[v] + w < dist[u]:
                    updated = True
            
        if updated:
            raise ValueError("Negative weight cycle detected")

        return dist

    def floyd_warshall(self):
        """All pairs shortest path."""
        D = {v: {u: float('inf') for u in self.vertices} for v in self.vertices}

        # D[i][j] = min ditance from vertex i to j either direct or through intermediate vertex k
        # D[i][j]=min(D[i][j], D[i][k]+D[k][j])

        for v in self.vertices:
            D[v][v] = 0
        
        # intialize direct neighbors
        for v in self.vertices:
            for nei, w in self.adj[v]:
                D[v][nei] = min(D[v][nei], w) # safely pick min in case of multiple edges

        for k in self.vertices: # intermediate vertex
            for i in self.vertices: # start vertex
                for j in self.vertices: # end vertex
                    if D[i][k] != float('inf') and D[k][j] != float('inf'):
                        D[i][j] = min(D[i][j], D[i][k] + D[k][j])

        for v in self.vertices:
            if D[v][v] < 0: # negative cycle detected
                raise ValueError("Negative weight cycle detected")
            
        return D
    
    def bfs_shortest_path(self, start, end):
        """Gives the shortest path from a start node to end node all edge weights are ingored and considered to be 1."""
        if start not in self.vertices or end not in self.vertices:
            raise ValueError("invalid vertex")
        
        dist = {v: float('inf') for v in self.vertices}
        dist[start] = 0

        queue = deque([start])
        parent = {start: None}

        while queue:
            node = queue.popleft()

            for nei, _ in self.adj[node]: # ignore weights
                if dist[nei] == float('inf'): # haven't visited this neighbor yet
                    queue.append(nei)
                    dist[nei] = dist[node] + 1
                    parent[nei] = node
            
        if dist[end] == float('inf'):
            raise ValueError(f"End vertex: {end}, is unreachable")

        # reconstruct the path bfs took
        path = []
        curr = end
        while curr is not None:
            path.append(curr)
            curr = parent[curr]
        
        path.reverse()
        return path, dist[end]
        
    def dfs_path(self, start, end):
        """finds a path and returns its number of edges may not be the minimum."""
        if start not in self.vertices or end not in self.vertices:
            raise ValueError("invalid vertex")

        visited = set()
        path = []

        def explore(node):
            visited.add(node)
            path.append(node)

            if node == end:
                return True
            
            # recursively try each unvisited neighbor and propagate True when the destination is found.
            for nei, _ in self.adj[node]:
                if nei not in visited:
                    if explore(nei):
                        return True

            # backtrack
            path.pop()
            
            return False
    
        if explore(start):
            return path, len(path) - 1
        else:
            raise ValueError("No valid path")

    def dfs_shortest_path(self, start, end):
        """finds the shorest path and returns its number of edges"""
        if start not in self.vertices or end not in self.vertices:
            raise ValueError("invalid vertex")

        visited = set()
        path = []
        best_path = None

        def explore(node):
            nonlocal best_path

            visited.add(node)
            path.append(node)

            if node == end:
                if best_path is None or len(path) < len(best_path):
                    best_path = path[:]
            
            # recursively try each unvisited neighbor and propagate True when the destination is found.
            for nei, _ in self.adj[node]:
                if nei not in visited:
                    explore(nei)

            # backtrack
            path.pop()
            visited.remove(node)

        explore(start)

        if best_path:
            return best_path, len(best_path) - 1
        else:
            raise ValueError("No valid path")  

    def dag_shortest_path(self, start, end):
        """Finds shortest path in a DAG."""
        if start not in self.vertices or end not in self.vertices:
            raise ValueError("invalid vertex")
        
        sorted_vertices = topo_sort(self.adj, self.vertices)
        parent = {v: None for v in self.vertices}

        dist = {v: float('inf') for v in self.vertices}
        dist[start] = 0

        for u in sorted_vertices:
            for v, w in self.adj[u]:
                if dist[u] != float('inf') and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    parent[v] = u

        if dist[end] == float('inf'):
            raise ValueError("No valid path")
        
        path = []
        curr = end
        while curr is not None:
            path.append(curr)
            curr = parent[curr]
        
        path.reverse()
        return path, dist[end]


g = Graph(
    [0, 1, 2, 3, 4],
    [
        (0, 1, 4),
        (0, 2, 8),
        (2, 1, 3),
        (2, 3, 2),
        (3, 4, 10),
        (4, 1, 6)
    ],
    directed=False
)

print(g.bellman_ford(0))
print(g.dijkstra(0))
print(g.floyd_warshall()[0][4])

g2 = Graph(
    [0, 1, 2],
    [(0, 1, 4), (0, 2, 5), (1, 2, -3)],
    directed=True
)

print(g2.bellman_ford(0))
# print(g2.dijkstra(0))
print(g2.floyd_warshall()[0][1])

g3 = Graph(
    [0, 1, 2, 3],
    [
        (0, 1, 2),
        (1, 2, 3),
        (2, 1, -5),
        (2, 3, 4)
    ],
    directed=True
)

# print(g3.bellman_ford(0))
# # print(g3.dijkstra(0)) # gets stuck in endless negative weight cycle
# print(g3.floyd_warshall())

g4 = Graph(
    [0, 1, 2, 3, 4],
    [
        (0, 1, 1),
        (0, 2, 1),
        (1, 3, 1),
        (2, 3, 1),
        (3, 4, 1)
    ],
    directed=True
)

print(g4.bfs_shortest_path(0, 4))

g5 = Graph(
    [0, 1, 2, 3],
    [
        (0, 1, 1),
        (1, 2, 1),
        (2, 3, 1),
        (0, 3, 1)
    ],
    directed=True
)

print(g5.bfs_shortest_path(0, 3))

g6 = Graph(
    [0, 1, 2, 3],
    [(0, 1, 1), (2, 3, 1)],
    directed=True
)

# print(g6.bfs_shortest_path(0, 3))

g7 = Graph(
    [0, 1, 2],
    [(0, 1, 1), (1, 2, 1)],
    directed=True
)

print(g7.bfs_shortest_path(1, 1))

g8 = Graph(
    ["A", "B", "C", "D"],
    [
        ("A", "B", 1),
        ("B", "C", 1),
        ("A", "D", 1)
    ],
    directed=False
)

print(g8.bfs_shortest_path("C", "D"))

g9 = Graph(
    ["A", "B", "C", "D", "E"],
    [
        ("A", "B", 1),
        ("A", "C", 1),
        ("B", "D", 1),
        ("C", "E", 1),
        ("E", "D", 1)
    ],
    directed=True
)

print(g9.dfs_path("A", "D"))
print(g9.dfs_shortest_path("A", "D"))

g10 = Graph(
    ["A", "B", "C", "D", "E", "F"],
    [
        ("A", "B", 1),
        ("B", "C", 1),
        ("C", "D", 1),
        ("D", "E", 1),
        ("E", "F", 1),
        ("A", "F", 1)
    ],
    directed=True
)

print(g10.dfs_path("A", "F"))
print(g10.dfs_shortest_path("A", "F"))

g11 = Graph(
    ["A", "B", "C", "D", "E"],
    [
        ("A", "B", 4),
        ("A", "C", 2),
        ("C", "B", -1),
        ("B", "D", 3),
        ("C", "D", 5),
        ("D", "E", -2)
    ],
    directed=True
)

print(g11.dag_shortest_path("A", "E"))

g12 = Graph(
    ["A", "B", "C", "D", "E"],
    [
        ("A", "B", 10),
        ("A", "C", 1),
        ("B", "D", 1),
        ("C", "E", 1),
        ("E", "D", 1)
    ],
    directed=True
)

print(g12.dag_shortest_path("A", "D"))

g13 = Graph(
    ["A", "B", "C", "D"],
    [
        ("A", "B", 2),
        ("A", "C", 5),
        ("C", "B", -10),
        ("B", "D", 3),
        ("C", "D", 1)
    ],
    directed=True
)

print(g13.dag_shortest_path("A", "D"))
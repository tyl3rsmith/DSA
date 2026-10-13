import heapq

class WeightedGraph:

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


    


g = WeightedGraph(
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

g2 = WeightedGraph(
    [0, 1, 2],
    [(0, 1, 4), (0, 2, 5), (1, 2, -3)],
    directed=True
)

print(g2.bellman_ford(0))
# print(g2.dijkstra(0))
print(g2.floyd_warshall()[0][1])

g3 = WeightedGraph(
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
print(g3.floyd_warshall())
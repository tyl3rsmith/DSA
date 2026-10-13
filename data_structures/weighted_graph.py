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

    # Time: O((V+E)logV)
    def dijkstra(self, start):
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
    
    def bellman_ford(self, start):
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

g2 = WeightedGraph(
    [0, 1, 2],
    [(0, 1, 4), (0, 2, 5), (1, 2, -3)],
    directed=True
)

print(g2.bellman_ford(0))
print(g2.dijkstra(0))

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

print(g3.bellman_ford(0))
# print(g3.dijkstra(0)) # gets stuck in endless negative weight cycele
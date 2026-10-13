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

g = WeightedGraph([0, 1, 2, 3, 4], [(0, 1, 4), (0, 2, 8), (2, 1, 3), (2, 3, 2), (3, 4, 10), (4, 1, 6)], False)
print(g.dijkstra(0))


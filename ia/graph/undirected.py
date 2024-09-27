from .history import AlgorithmHistory
from .algorithm import TraversalAlgorithm, TraversalResult


class UndirectedGraph:
    """
    Undirected graph class
    """

    def __init__(self):
        self.graph = {}
        self.weights = {}

    # Getters / Setters

    def add_edge(self, start: int, end: int, weight: int = 1) -> None:
        """
        Add an edge to the graph
        """
        if start not in self.graph:
            self.graph[start] = []
        if end not in self.graph:
            self.graph[end] = []
        self.graph[start].append(end)
        self.graph[end].append(start)
        self.weights[(start, end)] = weight
        self.weights[(end, start)] = weight

    def remove_edge(self, start: int, end: int) -> None:
        """
        Remove an edge from the graph
        """
        self.graph[start].remove(end)
        self.graph[end].remove(start)
        del self.weights[(start, end)]
        del self.weights[(end, start)]

    def remove_vertex(self, start: int) -> None:
        """
        Remove a vertex from the graph
        """
        del self.graph[start]
        for u in self.graph:
            if start in self.graph[u]:
                self.graph[u].remove(start)
                del self.weights[(u, start)]
                del self.weights[(start, u)]

    def get_vertices(self) -> list[int]:
        """
        Get the vertices of the graph
        """
        return list(self.graph.keys())

    def get_weights(self) -> dict[tuple[int, int], int]:
        """
        Get the weights of the graph
        """
        return self.weights

    def get_edges(self) -> list[tuple[int, int]]:
        """
        Get the edges of the graph
        """
        edges = []
        for start in self.graph:
            for end in self.graph[start]:
                if (end, start) not in edges:
                    edges.append((start, end))
        return edges

    def get_neighbors(self, start: int) -> list[int]:
        """
        Get the neighbors of a vertex
        """
        return self.graph[start]

    def get_degree(self, start: int) -> int:
        """
        Get the degree of a vertex
        """
        return len(self.graph[start])

    def get_adjacency_matrix(self) -> list[list[int]]:
        """
        Get the adjacency matrix of the graph
        """
        vertices = self.get_vertices()
        n = len(vertices)
        matrix = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if vertices[i] in self.graph[vertices[j]]:
                    matrix[i][j] = 1
        return matrix

    def get_adjacency_list(self) -> dict[int, list[int]]:
        """
        Get the adjacency list of the graph
        """
        return self.graph

    def get_incidence_matrix(self) -> list[list[int]]:
        """
        Get the incidence matrix of the graph
        """
        vertices = self.get_vertices()
        edges = self.get_edges()
        n = len(vertices)
        m = len(edges)
        matrix = [[0 for _ in range(m)] for _ in range(n)]
        for i in range(n):
            for j in range(m):
                if vertices[i] in edges[j]:
                    matrix[i][j] = 1
        return matrix

    def get_incidence_list(self) -> dict[int, list[int]]:
        """
        Get the incidence list of the graph
        """
        edges = self.get_edges()
        return {i: edges[i] for i in range(len(edges))}

    # Algorithms
    # TODO: Take weights into account

    def dfs(
        self, start: int, end: int, visited: dict[int, bool] = {}
    ) -> TraversalResult:
        """
        Depth-first search
        """
        history = AlgorithmHistory()
        generated = [start]
        inspected = []
        visited[start] = True
        stack = [start]
        history.add_step({"generated": generated.copy(), "inspected": inspected.copy()})
        while stack:
            current = stack.pop()
            if current == end:
                inspected.append(current)
                history.add_step(
                    {"generated": generated.copy(), "inspected": inspected.copy()}
                )
                break
            for neighbor in self.graph[current]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    generated.append(neighbor)
                    stack.append(neighbor)
            inspected.append(current)
            history.add_step(
                {"generated": generated.copy(), "inspected": inspected.copy()}
            )
        return TraversalResult(history, visited, list(inspected), 0)

    def bfs(
        self, start: int, end: int, visited: dict[int, bool] = {}
    ) -> TraversalResult:
        """
        Breadth-first search
        """
        history = AlgorithmHistory()
        generated = [start]
        inspected = []
        visited[start] = True
        queue = [start]
        history.add_step({"generated": generated.copy(), "inspected": inspected.copy()})
        while queue:
            current = queue.pop(0)
            if current == end:
                inspected.append(current)
                history.add_step(
                    {"generated": generated.copy(), "inspected": inspected.copy()}
                )
                break
            for neighbor in self.graph[current]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    generated.append(neighbor)
                    queue.append(neighbor)
            inspected.append(current)
            history.add_step(
                {"generated": generated.copy(), "inspected": inspected.copy()}
            )
        return TraversalResult(history, visited, list(inspected), 0)

    def traverse(
        self, *, start: int, end: int, algorithm: TraversalAlgorithm
    ) -> TraversalResult:
        """
        Traverse the graph
        """
        visited = {v: False for v in self.get_vertices()}
        if algorithm == "dfs":
            return self.dfs(start, end, visited)
        elif algorithm == "bfs":
            return self.bfs(start, end, visited)
        raise TypeError(f"Invalid algorithm {algorithm}")

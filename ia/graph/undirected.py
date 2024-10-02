"""Undirected graph module.

Contains the UndirectedGraph class.

"""

from .algorithm import (
    TraversalAlgorithm,
    TraversalResult,
    graph_path_cost,
    graph_path_from_predecessors,
)
from .history import AlgorithmHistory


class UndirectedGraph:
    """Undirected graph class."""

    def __init__(self):
        """Initialize the graph."""
        self.adjacency = {}
        self.weights = {}

    # Getters / Setters

    def add_edge(self, start: int, end: int, *, weight: int = 1) -> None:
        """Add an edge to the graph."""
        if start not in self.adjacency:
            self.adjacency[start] = []
        if end not in self.adjacency:
            self.adjacency[end] = []
        self.adjacency[start].append(end)
        self.adjacency[end].append(start)
        self.weights[(start, end)] = weight
        self.weights[(end, start)] = weight

    def remove_edge(self, start: int, end: int) -> None:
        """Remove an edge from the graph."""
        self.adjacency[start].remove(end)
        self.adjacency[end].remove(start)
        del self.weights[(start, end)]
        del self.weights[(end, start)]

    def remove_vertex(self, start: int) -> None:
        """Remove a vertex from the graph."""
        del self.adjacency[start]
        for u in self.adjacency:
            if start in self.adjacency[u]:
                self.adjacency[u].remove(start)
                del self.weights[(u, start)]
                del self.weights[(start, u)]

    def vertices(self) -> list[int]:
        """Get the vertices of the graph."""
        return list(self.adjacency.keys())

    def weights(self) -> dict[tuple[int, int], int]:
        """Get the weights of the graph."""
        return self.weights

    def edges(self) -> list[tuple[int, int]]:
        """Get the edges of the graph."""
        edges = []
        for start in self.adjacency:
            for end in self.adjacency[start]:
                if (end, start) not in edges:
                    edges.append((start, end))
        return edges

    def neighbors(self, start: int) -> list[int]:
        """Get the neighbors of a vertex."""
        return self.adjacency[start]

    def degree(self, start: int) -> int:
        """Get the degree of a vertex."""
        return len(self.adjacency[start])

    def adjacency_matrix(self) -> list[list[int]]:
        """Get the adjacency matrix of the graph."""
        vertices = self.get_vertices()
        n = len(vertices)
        matrix = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if vertices[i] in self.adjacency[vertices[j]]:
                    matrix[i][j] = 1
        return matrix

    def adjacency_list(self) -> dict[int, list[int]]:
        """Get the adjacency list of the graph."""
        return self.adjacency

    def incidence_matrix(self) -> list[list[int]]:
        """Get the incidence matrix of the graph."""
        vertices = self.get_vertices()
        edges = self.edges()
        n = len(vertices)
        m = len(edges)
        matrix = [[0 for _ in range(m)] for _ in range(n)]
        for i in range(n):
            for j in range(m):
                if vertices[i] in edges[j]:
                    matrix[i][j] = 1
        return matrix

    def incidence_list(self) -> dict[int, list[int]]:
        """Get the incidence list of the graph."""
        edges = self.edges()
        return {i: edges[i] for i in range(len(edges))}

    # Algorithms
    # TODO: Take weights into account

    def dfs(
        self, *, start: int, end: int, visited: dict[int, bool] = None
    ) -> TraversalResult:
        """Depth-first search."""
        if visited is None:
            visited = {}
        history = AlgorithmHistory()
        generated = [start]
        inspected = []
        visited[start] = True
        stack = [start]
        predecessors = {start: None}
        history.add_step(generated=generated, inspected=inspected)
        while stack:
            current = stack.pop()
            if current == end:
                inspected.append(current)
                history.add_step(generated=generated, inspected=inspected)
                break
            for neighbor in self.adjacency[current]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    generated.append(neighbor)
                    stack.append(neighbor)
                    predecessors[neighbor] = current
            inspected.append(current)
            history.add_step(generated=generated, inspected=inspected)
        if end not in predecessors:
            return TraversalResult(history, visited, [], -1)
        path = graph_path_from_predecessors(predecessors, end)
        return TraversalResult(
            history, visited, path, graph_path_cost(path, self.weights)
        )

    def bfs(
        self, *, start: int, end: int, visited: dict[int, bool] = None
    ) -> TraversalResult:
        """Breadth-first search."""
        if visited is None:
            visited = {}
        history = AlgorithmHistory()
        generated = [start]
        inspected = []
        visited[start] = True
        queue = [start]
        predecessors = {start: None}
        history.add_step(generated=generated, inspected=inspected)
        while queue:
            current = queue.pop(0)
            if current == end:
                inspected.append(current)
                history.add_step(generated=generated, inspected=inspected)
                break
            for neighbor in self.adjacency[current]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    generated.append(neighbor)
                    queue.append(neighbor)
                    predecessors[neighbor] = current
            inspected.append(current)
            history.add_step(generated=generated, inspected=inspected)
        if end not in predecessors:
            return TraversalResult(history, visited, [], -1)
        path = graph_path_from_predecessors(predecessors, end)
        return TraversalResult(
            history, visited, path, graph_path_cost(path, self.weights)
        )

    def traverse(
        self, *, start: int, end: int, algorithm: TraversalAlgorithm
    ) -> TraversalResult:
        """Traverse the graph."""
        visited = {v: False for v in self.vertices()}
        if algorithm == "dfs":
            return self.dfs(start=start, end=end, visited=visited)
        elif algorithm == "bfs":
            return self.bfs(start=start, end=end, visited=visited)
        raise TypeError(f"Invalid algorithm {algorithm}")

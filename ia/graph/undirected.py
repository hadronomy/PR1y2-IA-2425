"""Undirected graph module.

Contains the UndirectedGraph class.

"""

from ia.tree.node import Node

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

    def dfs(self, *, start: int, end: int) -> TraversalResult:
        """Depth-first search."""
        history = AlgorithmHistory()
        tree_root = Node(start, id=start)
        generated = [tree_root.id]
        inspected = []
        stack = [tree_root]
        history.add_step(generated=generated, inspected=inspected)
        current = None
        while stack:
            current = stack.pop()
            if current.id == end:
                inspected.append(current.id)
                history.add_step(generated=generated, inspected=inspected)
                break
            new_generated = [
                neighbor
                for neighbor in self.adjacency[current.id]
                if neighbor not in [ancestor.id for ancestor in current.ancestors]
                and neighbor is not current
            ]
            generated.extend(new_generated)
            stack.extend(
                [
                    Node(successor, parent=current, id=successor)
                    for successor in reversed(new_generated)
                ]
            )
            inspected.append(current.id)
            history.add_step(generated=generated, inspected=inspected)
        if current.id != end:
            return TraversalResult(history, [], -1, tree=tree_root)
        path = [ancestor.id for ancestor in current.node_path]
        return TraversalResult(
            history, path, graph_path_cost(path, self.weights), tree=tree_root
        )

    def bfs(self, *, start: int, end: int) -> TraversalResult:
        """Breadth-first search."""
        history = AlgorithmHistory()
        tree_root = Node(start, id=start)
        generated = [tree_root.id]
        inspected = []
        stack = [tree_root]
        history.add_step(generated=generated, inspected=inspected)
        current = None
        while stack:
            current = stack.pop(0)
            if current.id == end:
                inspected.append(current.id)
                history.add_step(generated=generated, inspected=inspected)
                break
            new_generated = [
                neighbor
                for neighbor in self.adjacency[current.id]
                if neighbor not in [ancestor.id for ancestor in current.ancestors]
                and neighbor is not current
            ]
            generated.extend(new_generated)
            stack.extend(
                [
                    Node(successor, parent=current, id=successor)
                    for successor in new_generated
                ]
            )
            inspected.append(current.id)
            history.add_step(generated=generated, inspected=inspected)
        if current.id != end:
            return TraversalResult(history, [], -1, tree=tree_root)
        path = [ancestor.id for ancestor in current.node_path]
        return TraversalResult(
            history, path, graph_path_cost(path, self.weights), tree=tree_root
        )

    def traverse(
        self, *, start: int, end: int, algorithm: TraversalAlgorithm
    ) -> TraversalResult:
        """Traverse the graph."""
        if algorithm == "dfs":
            return self.dfs(start=start, end=end)
        elif algorithm == "bfs":
            return self.bfs(start=start, end=end)
        raise TypeError(f"Invalid algorithm {algorithm}")

    def to_networkx(self):
        """Convert the graph to a NetworkX graph."""
        import networkx as nx

        graph = nx.Graph()
        for start in self.adjacency:
            for end in self.adjacency[start]:
                graph.add_node(start, label=start)
                graph.add_node(end, label=end)
                graph.add_edge(start, end, weight=self.weights[(start, end)])
        return graph

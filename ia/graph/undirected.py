"""Undirected graph module.

Contains the UndirectedGraph class.

"""

from collections.abc import Callable

from ia.algorithm import (
    AlgorithmHistory,
    TraversalResult,
    UninformedTraversalAlgorithm,
    graph_path_cost,
)
from ia.tree.node import Node


class UndirectedGraph:
    """Undirected graph class."""

    def __init__(self):
        """Initialize the graph."""
        self.__adjacency = {}
        self.__weights = {}

    # Getters / Setters

    @property
    def adjacency(self) -> dict[int, list[int]]:
        """Get the adjacency list of the graph."""
        return self.__adjacency

    @property
    def weights(self) -> dict[tuple[int, int], int]:
        """Get the weights of the graph."""
        return self.__weights

    @property
    def adjacency_matrix(self) -> list[list[int]]:
        """Get the adjacency matrix of the graph."""
        vertices = self.vertices
        n = len(vertices)
        matrix = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if vertices[i] in self.__adjacency[vertices[j]]:
                    matrix[i][j] = 1
        return matrix

    @property
    def adjacency_list(self) -> dict[int, list[int]]:
        """Get the adjacency list of the graph."""
        return self.__adjacency

    @property
    def vertices(self) -> list[int]:
        """Get the vertices of the graph."""
        return list(self.__adjacency.keys())

    @property
    def edges(self) -> list[tuple[int, int]]:
        """Get the edges of the graph."""
        edges = []
        for start in self.__adjacency:
            for end in self.__adjacency[start]:
                if (end, start) not in edges:
                    edges.append((start, end))
        return edges

    @property
    def neighbors(self, vertex: int) -> list[int]:
        """Get the neighbors of a vertex."""
        return self.__adjacency[vertex]

    @property
    def degree(self, vertex: int) -> int:
        """Get the degree of a vertex."""
        return len(self.__adjacency[vertex])

    @property
    def incidence_matrix(self) -> list[list[int]]:
        """Get the incidence matrix of the graph."""
        vertices = self.vertices
        edges = self.edges
        n = len(vertices)
        m = len(edges)
        matrix = [[0 for _ in range(m)] for _ in range(n)]
        for i in range(n):
            for j in range(m):
                if vertices[i] in edges[j]:
                    matrix[i][j] = 1
        return matrix

    @property
    def incidence_list(self) -> dict[int, list[int]]:
        """Get the incidence list of the graph."""
        edges = self.edges
        return {i: edges[i] for i in range(len(edges))}

    def add_edge(self, start: int, end: int, *, weight: int = 1) -> None:
        """Add an edge to the graph."""
        if start not in self.__adjacency:
            self.__adjacency[start] = []
        if end not in self.__adjacency:
            self.__adjacency[end] = []
        self.__adjacency[start].append(end)
        self.__adjacency[end].append(start)
        self.__weights[(start, end)] = weight
        self.__weights[(end, start)] = weight

    def remove_edge(self, start: int, end: int) -> None:
        """Remove an edge from the graph."""
        self.__adjacency[start].remove(end)
        self.__adjacency[end].remove(start)
        del self.__weights[(start, end)]
        del self.__weights[(end, start)]

    def remove_vertex(self, vertex: int) -> None:
        """Remove a vertex from the graph."""
        del self.__adjacency[vertex]
        for u in self.__adjacency:
            if vertex in self.__adjacency[u]:
                self.__adjacency[u].remove(vertex)
                del self.__weights[(u, vertex)]
                del self.__weights[(vertex, u)]

    def dfs(
        self,
        *,
        start: int,
        end: int,
        sort_generated: Callable[[list[int]], list[int]] = None,
    ) -> TraversalResult:
        """Depth-first search."""
        if sort_generated is None:

            def sort_generated(_generated):
                return reversed(_generated)

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
                    for successor in sort_generated(new_generated)
                ]
            )
            inspected.append(current.id)
            history.add_step(generated=generated, inspected=inspected)
        if current.id != end:
            return TraversalResult(history, [], -1, tree=tree_root)
        path = current.node_path
        return TraversalResult(
            history,
            path=current.node_path,
            cost=graph_path_cost(path, self.weights),
            tree=tree_root,
        )

    def bfs(
        self,
        *,
        start: int,
        end: int,
        sort_generated: Callable[[list[int]], list[int]] = None,
    ) -> TraversalResult:
        """Breadth-first search."""
        if sort_generated is None:

            def sort_generated(_generated):
                return _generated

        history = AlgorithmHistory()
        tree_root = Node(start, id=start)
        generated = [tree_root.id]
        inspected = []
        queue = [tree_root]
        history.add_step(generated=generated, inspected=inspected)
        current = None
        while queue:
            current = queue.pop(0)
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
            queue.extend(
                [
                    Node(successor, parent=current, id=successor)
                    for successor in sort_generated(new_generated)
                ]
            )
            inspected.append(current.id)
            history.add_step(generated=generated, inspected=inspected)
        if current.id != end:
            return TraversalResult(history, [], -1, tree=tree_root)
        path = current.node_path
        return TraversalResult(
            history,
            path=current.node_path,
            cost=graph_path_cost(path, self.weights),
            tree=tree_root,
        )

    def traverse(
        self, *, start: int, end: int, algorithm: UninformedTraversalAlgorithm
    ) -> TraversalResult:
        """Traverse the graph."""
        if algorithm == "dfs":
            return self.dfs(start=start, end=end)
        elif algorithm == "bfs":
            return self.bfs(start=start, end=end)
        raise TypeError(f"Invalid algorithm {algorithm}")

    def to_networkx(self):
        """Convert the graph to a NetworkX graph."""
        import networkx as nx  # type: ignore

        graph = nx.Graph()
        for start in self.adjacency:
            for end in self.adjacency[start]:
                graph.add_node(start, label=start)
                graph.add_node(end, label=end)
                graph.add_edge(start, end, weight=self.weights[(start, end)])
        return graph

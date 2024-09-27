from enum import Enum

from .history import AlgorithmHistory


class TraversalAlgorithm(str, Enum):
    """
    Traversal algorithm class
    """

    dfs = "dfs"
    bfs = "bfs"


class TraversalResult:
    """
    Traversal result class.
    Contains the path, visited nodes, cost and
    the algorithm history
    """

    def __init__(
        self,
        history: AlgorithmHistory,
        visited: dict[int, bool],
        path: list[int],
        cost: int,
    ):
        self.history = history
        self.visited = visited
        self.path = path
        self.cost = cost

    def __str__(self) -> str:
        return f"Path: {self.path}, Cost: {self.cost}, Visited: {self.visited_nodes}"

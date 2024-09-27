"""Graph traversal algorithms related classes and functions."""

from enum import Enum


from .history import AlgorithmHistory


class TraversalAlgorithm(str, Enum):
    """Traversal algorithm class."""

    dfs = "dfs"
    bfs = "bfs"


class TraversalResult:
    """Traversal result class.

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
        """Initialize the result.

        Args:
            history (AlgorithmHistory): The history of the algorithm
            visited (dict[int, bool]): The visited nodes
            path (list[int]): The resulting path
            cost (int): The cost of the

        """
        self.history = history
        self.visited = visited
        self.path = path
        self.cost = cost

    def __str__(self) -> str:
        """Return the result as a string."""
        return f"Path: {self.path}, Cost: {self.cost}, Visited: {self.visited}"


def graph_path_cost(path: list[int], weights: dict[tuple[int, int], int]) -> int:
    """Calculate the cost from a path using the weights of the graph."""
    cost = 0
    for i in range(1, len(path)):
        cost += weights[(path[i - 1], path[i])]
    return cost


def graph_path_from_predecessors(predecessors: dict[int, int], end: int) -> list[int]:
    """Get the path from the predecessors."""
    path = []
    current = end
    while current is not None:
        path.insert(0, current)
        current = predecessors[current]
    return path

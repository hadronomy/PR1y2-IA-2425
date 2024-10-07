"""Graph traversal algorithms related classes and functions."""

from copy import deepcopy
from enum import Enum

from ia.tree.node import Node


class TraversalAlgorithm(str, Enum):
    """Traversal algorithm class."""

    dfs = "dfs"
    bfs = "bfs"


class AlgorithmHistory:
    """Algorithm history class."""

    def __init__(self):
        """Initialize the history."""
        self.history = []

    def add_step(self, **kargs) -> None:
        """Add a step to the history."""
        self.history.append(deepcopy(kargs))

    def get_history(self) -> list[dict]:
        """Get the history."""
        return self.history

    def __str__(self) -> str:
        """Return the history as a string."""
        return str(self.history)

    def __iter__(self):
        """Iterate over the history."""
        return iter(self.history)


class TraversalResult:
    """Traversal result class.

    Contains the path, visited nodes, cost and
    the algorithm history
    """

    def __init__(
        self,
        history: AlgorithmHistory,
        path: list[int],
        cost: int,
        tree: Node | None = None,
    ):
        """Initialize the result.

        Parameters
        ----------
        history: AlgorithmHistory
                The history of the algorithm
        visited: dict[int, bool]
                The visited nodes
        path: list[int]
                The resulting path
        cost: int
                The cost of the path

        """
        self.history = history
        self.path = path
        self.cost = cost
        self.tree = tree

    def __str__(self) -> str:
        """Return the result as a string."""
        return f"Path: {self.path}, Cost: {self.cost}"


def graph_path_cost(path: list[int], weights: dict[tuple[int, int], int]) -> int:
    """Calculate the cost from a path using the weights of the graph."""
    cost = 0
    for i in range(1, len(path)):
        cost += weights[(path[i - 1], path[i])]
    return cost

from enum import Enum


class TraversalAlgorithm(str, Enum):
    """
    Traversal algorithm class
    """

    dfs = "dfs"
    bfs = "bfs"

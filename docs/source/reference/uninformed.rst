.. _uninformed:

============================
Uninformed Search Algorithms
============================

.. currentmodule:: ia.graph.undirected

The uninformed search algorithms are a set of algorithms that do not use any domain-specific knowledge to find the solution.
These algorithms are used when the search space is not known or when the search space is too large to explore exhaustively.

The following algorithms are implemented in this project:

- **Breadth-First Search (BFS)**: Explores the search space level by level.

.. autosummary::
  :toctree: generated/

  UndirectedGraph.bfs

- **Depth-First Search (DFS)**: Explores the search space by going as deep as possible.

.. autosummary::
  :toctree: generated/

  UndirectedGraph.dfs

And their implementation is limited to the context of an :mod:`UndirectedGraph`.


UndirectedGraph
~~~~~~~~~~~~~~~

The algorithms are implemented in the context of 
an :mod:`UndirectedGraph` class that represents an undirected graph.

.. autosummary::
  :toctree: generated/

  UndirectedGraph


Node
~~~~

Under the hood, the algorithms use a :class:`Node` class to represent the
search tree.

.. currentmodule:: ia.tree.node

.. autosummary::
  :toctree: generated/

  Node

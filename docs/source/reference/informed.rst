.. _informed:

==========================
Informed Search Algorithms
==========================

.. currentmodule:: ia.maze.maze

The informed search algorithms are a set of algorithms that use domain-specific knowledge to find the solution.
These algorithms are used when the search space is known and when the search space is small enough to explore exhaustively.

The following algorithms are implemented in this project:

- **A\* Search**: Explores the search space by using a heuristic function to estimate the cost of reaching the goal.

.. autosummary::
  :toctree: generated/

  Maze.a_star


And their implementation is limited to the context of a :mod:`Maze`.

Maze
~~~~

The algorithms are implemented in the context of
a :mod:`Maze` class that represents a maze.

.. autosummary::
  :toctree: generated/

  Maze

MazeTile
~~~~~~~~

Maze uses a :class:`MazeTile` class to represent the
tiles of the maze.

.. autosummary::
  :toctree: generated/

  MazeTile

Matrix
~~~~~~

Maze inherits from a :class:`Matrix` class that represents
a matrix and implements all the necessary operations.

.. currentmodule:: ia.maze.matrix

.. autosummary::
  :toctree: generated/

  Matrix

Node
~~~~

Under the hood, the algorithms use a :class:`Node` class to represent the
search tree.

.. currentmodule:: ia.tree.node

.. autosummary::
  :toctree: generated/

  Node

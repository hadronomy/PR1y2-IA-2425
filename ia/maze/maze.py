"""Maze data structure."""

import heapq
from enum import Enum
from typing import TypeVar

from ia.maze.matrix import Matrix, MatrixPosition
from ia.maze.utils import ALPHABET, number_to_representation
from ia.tree.node import Node


class MazeTile(str, Enum):
    """Maze tile class."""

    WALL = "wall"
    EMPTY = "empty"
    START = "start"
    GOAL = "goal"


MAZE_PRINT_STYLES = {
    MazeTile.WALL: "██",
    MazeTile.EMPTY: "  ",
    MazeTile.START: "SS",
    MazeTile.GOAL: "GG",
}


class Maze(Matrix):
    """Maze data structure."""

    def __init__(
        self,
        *,
        rows: int,
        cols: int,
        start: MatrixPosition = None,
        goal: MatrixPosition = None,
    ) -> None:
        super().__init__(rows=rows, cols=cols, default=MazeTile.WALL)
        self.__start = start
        self.__goal = goal

    @property
    def start(self) -> MatrixPosition:
        """Get the start position."""
        return self.__start

    @start.setter
    def start(self, value: MatrixPosition) -> None:
        """Set the start position."""
        self.__start = value

    @property
    def goal(self) -> MatrixPosition:
        """Get the goal position."""
        return self.__goal

    @goal.setter
    def goal(self, value: MatrixPosition) -> None:
        """Set the goal position."""
        self.__goal = value

    def print(self) -> str:
        """Print the maze as a string."""
        top_border = "".join(
            f"{number_to_representation(i, ALPHABET):2}" for i in range(self.cols)
        )
        top_border = top_border + "\n   " + "╭" + "─" * self.cols * 2 + "╮"
        bottom_border = "╰" + "─" * self.cols * 2 + "╯"
        maze_rows = "\n".join(
            f"{i:2} │" + "".join(MAZE_PRINT_STYLES[cell] for cell in row) + "│"
            for i, row in enumerate(self)
        )
        return f"    {top_border}\n{maze_rows}\n   {bottom_border}"

    def a_star(
        self, start: MatrixPosition = None, goal: MatrixPosition = None
    ) -> list[MatrixPosition] | None:
        """Find the shortest path between the start and goal positions using the A* algorithm."""  # noqa: E501
        if start is None:
            start = self.start
        if goal is None:
            goal = self.goal
        open_set = []
        heapq.heappush(
            open_set,
            (
                0,
                Node(
                    name=start,
                    parent=None,
                    position=start,
                    compare_by="f_score",
                    g_score=0,
                    f_score=manhattan_distance(start, goal),
                ),
            ),
        )
        came_from = {}
        g_score = {start: 0}
        f_score = {start: manhattan_distance(start, goal)}

        while open_set:
            current_node = heapq.heappop(open_set)[1]
            current = current_node.position

            if current == goal:
                return current_node.node_path

            for neighbor in self.neighbors(current.row, current.col).values():
                tentative_g_score = (
                    g_score[current] + 1
                )  # Assuming cost to move to a neighbor is 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + manhattan_distance(
                        neighbor, goal
                    )
                    heapq.heappush(
                        open_set,
                        (
                            f_score[neighbor],
                            Node(
                                name=neighbor,
                                parent=current_node,
                                compare_by="f_score",
                                position=neighbor,
                                g_score=tentative_g_score,
                                f_score=f_score[neighbor],
                            ),
                        ),
                    )

        return None

    def __str__(self) -> str:
        """Return the maze as a string."""
        return self.print()


def manhattan_distance(start: MatrixPosition, goal: MatrixPosition) -> int:
    """Calculate the Manhattan distance between two positions."""
    return abs(start.row - goal.row) + abs(start.col - goal.col)


TContent = TypeVar("TContent", bound=MazeTile)

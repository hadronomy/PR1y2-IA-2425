"""Maze data structure."""

from enum import Enum
from typing import TypeVar

from ia.maze.matrix import Matrix, MatrixPosition
from ia.maze.utils import ALPHABET, number_to_representation


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

    def __str__(self) -> str:
        """Return the maze as a string."""
        return self.print()


TContent = TypeVar("TContent", bound=MazeTile)

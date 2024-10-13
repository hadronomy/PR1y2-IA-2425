"""Maze data structure."""

import heapq
from collections.abc import Callable
from typing import TypeVar

from ia.maze import euristics
from ia.maze.constants import (
    DEFAULT_MAZE_MAPPINGS,
    MAZE_PRINT_STYLES,
    NUMBERS,
)
from ia.maze.matrix import Matrix, MatrixPosition
from ia.maze.tile import MazeTile
from ia.maze.utils import number_to_representation
from ia.tree.node import Node


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
        if self.start is not None:
            self[self.start] = MazeTile.WALL
            self[value] = MazeTile.START
        self.__start = value

    @property
    def goal(self) -> MatrixPosition:
        """Get the goal position."""
        return self.__goal

    @goal.setter
    def goal(self, value: MatrixPosition) -> None:
        """Set the goal position."""
        if self.goal is not None:
            self[self.goal] = MazeTile.WALL
            self[value] = MazeTile.GOAL
        self.__goal = value

    def print(self, path: list[MatrixPosition] = None, style: str = "detailed") -> str:
        """Print the maze as a string with an optional path and style.

        Parameters
        ----------
            path : (list[MatrixPosition])
                The path to highlight in the maze.
            style : (str)
                The style to use for printing the maze.
                Options are "detailed" and "simple".

        Returns
        -------
            (str)
                The maze as a string.
        """
        top_border = "".join(
            f"{number_to_representation(i, NUMBERS):2}" for i in range(self.cols)
        )
        top_border = " " + top_border + "\n   " + "╭" + "─" * (self.cols * 2 + 1) + "╮"
        bottom_border = "╰" + "─" * (self.cols * 2 + 1) + "╯"

        path_set = set(path) if path else set()

        if style == "detailed":

            def get_tile_style(cell, position):
                if (
                    position in path_set
                    and not cell == MazeTile.START
                    and not cell == MazeTile.GOAL
                ):
                    return MAZE_PRINT_STYLES["path"]
                return MAZE_PRINT_STYLES[cell]

            maze_rows = "\n".join(
                f"{i:2} │ "
                + " ".join(
                    get_tile_style(cell, MatrixPosition(i, j))
                    for j, cell in enumerate(row)
                )
                + " │"
                for i, row in enumerate(self)
            )
        elif style == "simple":
            tile_numbers = {v: k for k, v in DEFAULT_MAZE_MAPPINGS.items()}

            maze_rows = "\n".join(
                f"{i:2} │ "
                + " ".join(
                    "*"
                    if MatrixPosition(i, j) in path_set
                    and not cell == MazeTile.START
                    and not cell == MazeTile.GOAL
                    else tile_numbers[cell]
                    for j, cell in enumerate(row)
                )
                + " │"
                for i, row in enumerate(self)
            )
        else:
            raise ValueError(f"Unknown style: {style}")

        return f"    {top_border}\n{maze_rows}\n   {bottom_border}"

    def a_star(
        self,
        start: MatrixPosition | None = None,
        goal: MatrixPosition | None = None,
        euristic_func: Callable[[MatrixPosition, MatrixPosition], int] | None = None,
        g_score_func: Callable[[MatrixPosition, MatrixPosition], int] | None = None,
        tiles_to_ignore: list[MazeTile] | None = None,
    ) -> list[MatrixPosition] | None:
        """Find the shortest path between the start and goal positions using the A* algorithm.

        Parameters
        ----------
            start : (MatrixPosition)
                The start position.
            goal : (MatrixPosition)
                The goal position.
            euristic_func : (Callable[[MatrixPosition, MatrixPosition], int])
                The euristic function to use.
            g_score_func : (Callable[[MatrixPosition, MatrixPosition], int])
                The g score function to use.
            tiles_to_ignore : (list[MazeTile])
                The tiles to ignore.

        Returns
        -------
            (list[MatrixPosition]) | None
                The path from the start to the goal.
                If no path is found, None is returned.
        """  # noqa: E501
        if start is None:
            start = self.start
        if goal is None:
            goal = self.goal
        if euristic_func is None:
            euristic_func = euristics.manhattan_distance
        if g_score_func is None:
            g_score_func = euristics.greater_diagonal_g_score
        if tiles_to_ignore is None:
            tiles_to_ignore = [MazeTile.WALL]

        open_set = []
        heapq.heappush(
            open_set,
            Node(
                name=start,
                parent=None,
                position=start,
                compare_by="f_score",
                g_score=0,
                f_score=euristic_func(start, goal),
                h_score=euristic_func(start, goal),
            ),
        )
        came_from = {}
        g_score = {start: 0}
        f_score = {start: euristic_func(start, goal)}

        while open_set:
            current_node = heapq.heappop(open_set)
            current = current_node.position

            if current == goal:
                return current_node.node_path

            for neighbor in self.neighbors(current.row, current.col).values():
                if self[neighbor] in tiles_to_ignore:
                    continue
                tentative_g_score = g_score[current] + g_score_func(current, neighbor)
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    h_score = euristic_func(neighbor, goal)
                    f_score[neighbor] = tentative_g_score + h_score
                    heapq.heappush(
                        open_set,
                        Node(
                            name=neighbor,
                            parent=current_node,
                            compare_by="f_score",
                            position=neighbor,
                            g_score=tentative_g_score,
                            f_score=f_score[neighbor],
                            h_score=h_score,
                        ),
                    )

        return None

    def plot(
        self,
        path: list[Node] | None = None,
        title: str | None = None,
        subtitle: str | None = None,
        file_path: str | None = None,
    ) -> None:
        """Plot the maze with an optional path."""
        try:
            import matplotlib.pyplot as plt
        except ImportError as e:
            raise ImportError("Matplotlib is required to plot the maze.") from e

        if not title:
            title = "Maze"
        if not subtitle:
            subtitle = "by @hadronomy"

        fig, ax = plt.subplots(
            figsize=(self.cols, self.rows), dpi=300 if file_path else 100
        )
        fig.suptitle(title, fontsize=20)
        fig.text(0.5, 0.90, subtitle, ha="center", fontsize=10)
        ax.imshow(
            [[0 if cell == MazeTile.WALL else 1 for cell in row] for row in self],
            cmap="gray",
            origin="upper",
        )
        ax.set_xticks(range(self.cols))
        ax.set_yticks(range(self.rows))
        ax.set_xticks([x - 0.5 for x in range(1, self.cols)], minor=True)
        ax.set_yticks([y - 0.5 for y in range(1, self.rows)], minor=True)
        ax.grid(which="minor", color="black", linestyle="-", linewidth=1.5)
        ax.tick_params(which="minor", size=0)

        if path:
            for i in range(len(path) - 1):
                current_node = path[i]
                next_node = path[i + 1]
                dx = next_node.position.col - current_node.position.col
                dy = next_node.position.row - current_node.position.row
                ax.arrow(
                    current_node.position.col,
                    current_node.position.row,
                    dx,
                    dy,
                    head_width=0.1,
                    head_length=0.1,
                    fc="cornflowerblue",
                    ec="cornflowerblue",
                )

        for i, row in enumerate(self):
            for j, cell in enumerate(row):
                margin = 0.1
                left = j - 0.5 + margin
                right = j + 0.5 - margin
                bottom = i - 0.5 + margin
                top = i + 0.5 - margin
                if cell == MazeTile.START:
                    ax.text(
                        j,
                        i,
                        "S",
                        ha="center",
                        va="center",
                        color="black",
                        fontsize=20,
                        fontweight="bold",
                        fontstyle="italic",
                    )
                elif cell == MazeTile.GOAL:
                    ax.text(
                        j,
                        i,
                        "E",
                        ha="center",
                        va="center",
                        color="black",
                        fontsize=20,
                        fontweight="bold",
                        fontstyle="italic",
                    )
                for node in path:
                    if node.position.row == i and node.position.col == j:
                        ax.text(
                            left,
                            top,
                            f"{node.g_score}",
                            ha="left",
                            va="bottom",
                            color="limegreen",
                            fontsize=10,
                            fontweight="bold",
                            fontstyle="italic",
                        )
                        ax.text(
                            left,
                            bottom,
                            f"{node.f_score}",
                            ha="left",
                            va="top",
                            color="red",
                            fontsize=10,
                            fontweight="bold",
                            fontstyle="italic",
                        )
                        ax.text(
                            right,
                            top,
                            f"{node.h_score}",
                            ha="right",
                            va="bottom",
                            color="cornflowerblue",
                            fontsize=10,
                            fontweight="bold",
                            fontstyle="italic",
                        )
        if not file_path:
            plt.show()
            return
        plt.savefig(file_path)

    def __str__(self) -> str:
        """Return the maze as a string."""
        return self.print()


TContent = TypeVar("TContent", bound=MazeTile)

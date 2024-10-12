"""Parser for maze files."""

from ia.maze.constants import DEFAULT_MAZE_MAPPINGS
from ia.maze.matrix import MatrixPosition
from ia.maze.maze import Maze, MazeTile


def parse(input_text: str, mappings: dict[str, MazeTile] | None = None) -> Maze:
    """Parse a maze from a string."""
    if mappings is None:
        mappings = DEFAULT_MAZE_MAPPINGS
    lines = input_text.strip().split("\n")
    rows = int(lines[0])
    cols = int(lines[1])
    lines = [line.split() for line in lines[2:]]
    maze = Maze(rows=rows, cols=cols)
    if len(lines) != rows:
        raise ValueError("Invalid maze dimensions.")
    for i, line in enumerate(lines):
        if len(line) != cols:
            raise ValueError("Invalid maze dimensions.")
        for j, char in enumerate(line):
            if char == "3":
                if maze.start is not None:
                    raise ValueError("Multiple start positions.")
                maze.start = MatrixPosition(row=i, col=j)
            if char == "4":
                if maze.goal is not None:
                    raise ValueError("Multiple goal positions.")
                maze.goal = MatrixPosition(row=i, col=j)
            if char not in mappings:
                raise ValueError(f"Invalid character '{char}' in maze.")
            maze[i, j] = mappings[char]
    if maze.start == maze.goal:
        raise ValueError("Start and goal positions are the same.")
    if maze.rows != rows or maze.cols != cols:
        raise ValueError("Invalid maze dimensions.")
    return maze

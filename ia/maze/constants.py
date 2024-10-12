"""Constants for the maze module."""

from ia.maze.tile import MazeTile

ALPHABET = [chr(letter) for letter in range(65, 91)]
NUMBERS = [str(number) for number in range(0, 10)]

MAZE_PRINT_STYLES = {
    MazeTile.WALL: "█",
    MazeTile.EMPTY: " ",
    MazeTile.START: "S",
    MazeTile.GOAL: "G",
    "path": "*",
}

DEFAULT_MAZE_MAPPINGS = {
    "0": MazeTile.EMPTY,
    "1": MazeTile.WALL,
    "3": MazeTile.START,
    "4": MazeTile.GOAL,
}

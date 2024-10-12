"""Maze tile module."""

from enum import Enum


class MazeTile(str, Enum):
    """Maze tile class."""

    WALL = "wall"
    EMPTY = "empty"
    START = "start"
    GOAL = "goal"

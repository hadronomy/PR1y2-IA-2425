"""Informed search command."""

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from ia.maze.matrix import MatrixPosition
from ia.maze.parser import parse as parse_maze


def informed(
    input_path: Annotated[
        Path,
        typer.Argument(
            help="The path to the file containing the graph.",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            resolve_path=True,
        ),
    ],
    start: Annotated[
        tuple[int, int] | None,
        typer.Option(
            "--start",
            "-s",
            help="The start node.",
        ),
    ] = None,
    goal: Annotated[
        tuple[int, int] | None,
        typer.Option(
            "--goal",
            "-g",
            help="The goal node.",
        ),
    ] = None,
    pretty: Annotated[
        bool | None,
        typer.Option(
            help="Use the simple maze representation.",
        ),
    ] = None,
):
    """Traverse a maze using an informed search algorithm."""
    console = Console()
    maze = None
    with open(input_path) as input_file:
        maze = parse_maze(input_file.read())
        if maze is None:
            console.print("\nFailed to parse the maze.", style="red bold")
            raise typer.Exit(1)
    if start is not None:
        maze.start = MatrixPosition(start[0], start[1])
    if goal is not None:
        maze.goal = MatrixPosition(goal[0], goal[1])
    print_style = "detailed" if pretty else "simple"
    console.print(maze.print(style=print_style))
    result = maze.a_star()
    if result is None:
        console.print("\nNo path found.", style="red bold")
        raise typer.Exit(1)
    console.print("\nPath found:", style="green bold")
    for node in result:
        console.print(node)
    console.print(
        maze.print(
            path=[node.position for node in result],
            style=print_style,
        )
    )
    raise typer.Exit(1)

"""Informed search command."""

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

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
    if pretty:
        console.print(maze)
    else:
        console.print(maze.print_simple())
    result = maze.a_star()
    if result is None:
        console.print("\nNo path found.", style="red bold")
        raise typer.Exit(1)
    console.print("\nPath found:", style="green bold")
    for node in result:
        console.print(node)
    raise typer.Exit(1)

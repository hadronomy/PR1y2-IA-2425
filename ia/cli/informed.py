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
    output_path: Annotated[
        Path | None,
        typer.Option(
            "--output",
            "-o",
            help="The path to the output file.",
            writable=True,
            resolve_path=True,
            dir_okay=True,
        ),
    ] = None,
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
    plot: Annotated[
        bool | None,
        typer.Option(
            help="Plot the maze.",
        ),
    ] = None,
    no_header: Annotated[
        bool | None,
        typer.Option(
            "--no-header",
            help="Do not print the header.",
        ),
    ] = None,
):
    """Traverse a maze using an informed search algorithm."""
    console = Console()

    if no_header and not plot:
        console.print("No header and no plot selected.", style="red bold")
        raise typer.Exit(1)

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
    result_path = maze.a_star()
    if result_path is None:
        console.print("\nNo path found.", style="red bold")
        raise typer.Exit(1)
    console.print("\nPath found:", style="green bold")
    for node in result_path:
        console.print(node)
    position_path = [node.position for node in result_path]
    console.print(
        maze.print(
            path=position_path,
            style=print_style,
        )
    )
    file_name = input_path.stem
    plot_file_name = file_name + "_result.png"
    if output_path and not output_path.exists():
        output_path.mkdir(parents=True, exist_ok=True)
    plot_output_path = output_path / plot_file_name if output_path else None
    maze.plot(
        path=result_path,
        title=file_name,
        file_path=plot_output_path,
        headerless=no_header,
    ) if plot else None

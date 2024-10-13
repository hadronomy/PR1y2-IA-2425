"""Informed search command."""

from pathlib import Path
from typing import Annotated, Literal

import typer
from rich.console import Console
from rich.text import Text

from ia.cli.utils import wrap_text
from ia.maze import Maze
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

    result = maze.a_star()

    input_file_name = input_path.stem
    output_file_name = input_file_name + "-out.txt"
    output_text_file_path = output_path / output_file_name if output_path else None  # noqa: E501
    output_text_file = (
        open(output_text_file_path, "w") if output_text_file_path else None
    )  # noqa: E501
    console = Console(file=output_text_file)
    print_result(console, maze, print_style, result)

    plot_file_name = input_file_name + "_result.png"
    if output_path and not output_path.exists():
        output_path.mkdir(parents=True, exist_ok=True)
    plot_output_path = output_path / plot_file_name if output_path else None
    maze.plot(
        path=result.path,
        title=input_file_name,
        file_path=plot_output_path,
        headerless=no_header,
    ) if plot else None


def print_result(
    console: Console,
    maze: Maze,
    print_style: Literal["simple"] | Literal["detailed"],
    result,
):
    """
    Print the result of the maze traversal.

    Parameters
    ----------
        console: Console
            The console to print the result
        maze: Maze
            The maze
        print_style: str
            The style to print the maze
        result: TraversalResult
            The result of the traversal
    """  # noqa: E501
    if result.path is None:
        console.print("\nNo path found.", style="red bold")
    else:
        console.print("\nPath found:", style="green bold")

    position_path = [node.position for node in result.path] if result.path else None
    console.print(
        maze.print(
            path=position_path,
            style=print_style,
        )
    )

    width = 35
    divider = Text("-" * width, style="grey30")
    for i, step in enumerate(result.history):
        console.print(divider)
        console.print(Text(f"Iteration {i + 1}", style="red bold"))
        console.print(
            wrap_text(
                f"Generated nodes: {", ".join(str(i) for i in step["generated"])}",
                width,
            )
        )
        console.print(
            wrap_text(
                f"Inspected nodes: {", ".join(str(i) for i in step["inspected"])}",
                width,
            )
        )
    console.print(divider)
    if position_path:
        console.print(
            Text("Path:", style="bold"),
            wrap_text(
                f"{" -> ".join(str(i) for i in position_path)}",
                width - 5,
            ),
        )
    else:
        console.print(Text("Path:", style="bold"), "-")
    console.print(divider)
    console.print(Text("Cost:", style="bold"), f"{result.cost if result.path else -1}")
    console.print(divider)

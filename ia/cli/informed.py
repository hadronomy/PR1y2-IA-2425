"""Informed search command."""

import math
import time
from pathlib import Path
from typing import Annotated, Literal

import typer
from rich.console import Console
from rich.text import Text

from ia.algorithm import TraversalResult
from ia.cli.utils import wrap_text
from ia.maze import Maze
from ia.maze.euristics import Euristic
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
            help="The path to the output directory.",
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
    euristic: Annotated[
        Euristic,
        typer.Option(
            "--euristic",
            "-e",
            help="The euristic function to use.",
        ),
    ] = Euristic.MANHATTAN,
    suffix: Annotated[
        str | None,
        typer.Option(
            help="The suffix for the output file.",
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

    start_time = time.time()
    result = maze.a_star(euristic_func=euristic.to_function())
    end_time = time.time()
    execution_time = end_time - start_time

    if output_path and not output_path.exists():
        output_path.mkdir(parents=True, exist_ok=True)

    input_file_name = input_path.stem
    output_file_name = (
        input_file_name + "_out.txt"
        if not suffix
        else input_file_name + "_out_" + suffix + ".txt"
    )  # noqa: E501
    output_text_file_path = output_path / output_file_name if output_path else None  # noqa: E501
    output_text_file = (
        open(output_text_file_path, "w") if output_text_file_path else None
    )  # noqa: E501

    console = Console(file=output_text_file)
    console.print("Algorithm: A*", style="blue bold")
    console.print(f"Euristic: {euristic.value}", style="blue bold")
    console.print(f"Execution time: {execution_time:.4f} seconds", style="blue bold")

    print_result(console, input_file_name, maze, print_style, result)

    plot_file_name = (
        input_file_name + "_plot.png"
        if not suffix
        else input_file_name + "_plot_" + suffix + ".png"
    )  # noqa: E501
    plot_output_path = output_path / plot_file_name if output_path else None
    maze.plot(
        path=result.path,
        title=input_file_name,
        file_path=plot_output_path,
        headerless=no_header,
    ) if plot else None


def print_result(
    console: Console,
    input_file_name: str,
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

    print_table(console, input_file_name, maze, result)

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
        console.print(
            wrap_text(
                f"Current path: {" -> ".join(str(i) for i in step["path"])}",
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


def print_table(
    console: Console, input_file_name: str, maze: Maze, result: TraversalResult
):
    """
    Print a table summarizing the maze traversal results.

    Parameters
    ----------
        console: Console
            The console to print the table.
        input_file_name: str
            The name of the input file.
        maze: Maze
            The maze object.
        result: TraversalResult
            The result of the traversal.
    """
    from tabulate import tabulate

    data = (
        [
            (
                "Instance",
                "n",
                "m",
                "S",
                "E",
                "Path",
                "Cost",
                "Nº Nodes generated",
                "Nº Nodes inspected",
            ),
            (
                input_file_name,
                maze.rows,
                maze.cols,
                maze.start,
                maze.goal,
                " -> ".join(
                    str(node) for node in [node.position for node in result.path]
                )
                if result.path
                else "-",
                result.cost if result.path else -1,
                len(result.history[-1]["generated"]),
                len(result.history[-1]["inspected"]),
            ),
        ],
    )
    table_str = tabulate(
        data[0],
        headers="firstrow",
        tablefmt="fancy_grid",
        maxcolwidths=30,
        maxheadercolwidths=math.inf,
    )
    console.print(table_str, crop=False, overflow="ignore")

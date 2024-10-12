"""Uninformed search command."""

import sys
from pathlib import Path
from typing import Annotated, TextIO

import typer
from rich.console import Console
from rich.text import Text

from ia.cli.utils import wrap_text
from ia.graph.algorithm import TraversalAlgorithm, TraversalResult
from ia.graph.parser.parser import parse_and_transform
from ia.graph.undirected import UndirectedGraph
from ia.tree.utils import print_tree


def uninformed(
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
    algorithm: Annotated[
        TraversalAlgorithm,
        typer.Option(
            help="Traversal algorithm to use.",
        ),
    ],
    start: Annotated[
        int,
        typer.Option(
            "--start",
            "-s",
            help="The starting vertex.",
        ),
    ],
    end: Annotated[
        int,
        typer.Option(
            "--end",
            "-e",
            help="The ending vertex.",
        ),
    ],
    output_path: Annotated[
        Path | None,
        typer.Option(
            "--output",
            "-o",
            help="The path to the file to write the output to.",
            writable=True,
            resolve_path=True,
        ),
    ] = None,
    preview: Annotated[
        bool | None,
        typer.Option(
            "--preview",
            "-p",
            help="Render the generated tree.",
        ),
    ] = None,
    force: Annotated[
        bool | None,
        typer.Option(
            "--force",
            "-f",
            help="Force the execution of the command.",
        ),
    ] = None,
):
    """Traverse the graph using the specified algorithm."""
    console = Console()
    graph = None
    with open(input_path) as input_file:
        graph = parse_and_transform(input_file.read())
        if graph is None:
            console.print("\nFailed to parse the graph.", style="red bold")
            raise typer.Exit(1)
    output_stream = sys.stdout if output_path is None else open(output_path, "w")

    if start not in graph.vertices:
        console.print(f"\nStart vertex {start} not in the graph.", style="red bold")
        if force:
            console.print(
                "Cannot force execution with invalid start node.", style="yellow bold"
            )
        raise typer.Exit(1)
    if end not in graph.vertices:
        console.print(f"\nEnd vertex {end} not in the graph.", style="red bold")
        if not force:
            raise typer.Exit(1)
        console.print("Forcing execution with invalid end node.", style="yellow bold")

    result = graph.traverse(start=start, end=end, algorithm=algorithm)
    print_result(graph, start, end, algorithm, result, file=output_stream)
    if preview:
        print_tree(result.tree)


def print_result(
    graph: UndirectedGraph,
    start: int,
    end: int,
    algorithm: TraversalAlgorithm,
    result: TraversalResult,
    file: TextIO = sys.stdout,
):
    """Print the result of the traversal."""
    console = Console(file=file)
    width = 35
    divider = Text("-" * width, style="grey30")
    console.print(divider)
    console.print(f"Number of nodes: {len(graph.vertices)}", style="green bold")
    console.print(f"Number of edges: {len(graph.edges)}", style="green bold")
    console.print(f"Origin vertex: {start}", style="blue bold")
    console.print(f"Destination vertex: {end}", style="yellow bold")
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
    console.print(
        Text("Path:", style="bold"),
        wrap_text(
            f"{" -> ".join(str(i) for i in result.path)}",
            width - 5,
        ),
    )
    console.print(divider)
    console.print(Text("Cost:", style="bold"), f"{result.cost}")
    console.print(divider)

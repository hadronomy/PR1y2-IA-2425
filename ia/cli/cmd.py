"""cmd module.

Contains the different commands available.
"""

from pathlib import Path
from textwrap import wrap
from typing import Annotated, Optional

import typer

from ia import __version__
from ia.graph import UndirectedGraph
from ia.graph.algorithm import TraversalAlgorithm
from ia.parser.graph.undirected import parse_and_transform


def run():
    """Configure and execute the CLI."""
    app = typer.Typer(pretty_exceptions_show_locals=False)
    app.command()(main)
    app(prog_name="ia")


def version_callback(value: bool):
    """Print the version."""
    if value:
        print(f"ia version {__version__}")
        raise typer.Exit()


def wrap_text(text, width):
    """Wrap text to a specified width.

    Parameters
    ----------
        text: str
            The text to wrap.
        width: str
            The width to wrap the text to.

    Returns
    -------
        str: The wrapped text.

    """
    return "\n".join(wrap(text, width=width))


def print_result(
    graph: UndirectedGraph, start: int, end: int, algorithm: TraversalAlgorithm
):
    """Print the result of the traversal."""
    width = 30
    divider = "-" * width
    print(divider)
    print(f"Number of nodes: {len(graph.vertices())}")
    print(f"Number of edges: {len(graph.edges())}")
    print(f"Origin vertex: {1}")
    print(f"Destination vertex: {4}")
    result = graph.traverse(start=start, end=end, algorithm=algorithm)
    for i, step in enumerate(result.history):
        print(divider)
        print(f"Iteration {i + 1}")
        print(
            wrap_text(
                f"Generated nodes: {", ".join(str(i) for i in step["generated"])}",
                width,
            )
        )
        print(
            wrap_text(
                f"Inspected nodes: {", ".join(str(i) for i in step["inspected"])}",
                width,
            )
        )
    print(divider)
    print(
        wrap_text(
            f"Path: {" -> ".join(str(i) for i in result.path)}",
            width - 3,
        )
    )
    print(divider)
    print(f"Cost: {result.cost}")
    print(divider)


def main(
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
        Optional[Path],
        typer.Option(
            "--output",
            "-o",
            help="The path to the file to write the output to.",
            writable=True,
            resolve_path=True,
        ),
    ] = None,
    version: Annotated[
        Optional[bool],
        typer.Option(
            "--version",
            "-v",
            callback=version_callback,
            help="Print the program version.",
        ),
    ] = None,
):
    """Traverse the graph using the specified algorithm."""
    with open(input_path) as input_file:
        graph = parse_and_transform(input_file.read())
        if output_path is not None:
            with open(output_path, "w") as output_file:
                raise NotImplementedError("Not implemented yet.")
                graph = parse_and_transform(output_file.read())
                return
    print_result(graph, start, end, algorithm)

"""cmd module.

Contains the different commands available.
"""

from textwrap import wrap
from typing import Annotated, Optional

import typer

from ia import __version__
from ia.graph import UndirectedGraph
from ia.graph.algorithm import TraversalAlgorithm


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


def main(
    algorithm: Annotated[
        TraversalAlgorithm,
        typer.Option(
            help="Traversal algorithm to use.",
        ),
    ],
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
    graph = UndirectedGraph()
    graph.add_edge(1, 2)
    graph.add_edge(2, 3, weight=10)
    graph.add_edge(3, 4, weight=5)
    graph.add_edge(4, 1, weight=3)
    start = 2
    end = 4
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

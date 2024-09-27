"""cmd module.

Contains the different commands available.
"""

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


def main(
    algorithm: Annotated[TraversalAlgorithm, typer.Option()],
    version: Annotated[
        Optional[bool], typer.Option("--version", "-v", callback=version_callback)
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
    divider = "-" * 30
    print(divider)
    print(f"Number of nodes: {len(graph.vertices())}")
    print(f"Number of edges: {len(graph.edges())}")
    print(f"Origin vertex: {1}")
    print(f"Destination vertex: {4}")
    result = graph.traverse(start=start, end=end, algorithm=algorithm)
    for i, step in enumerate(result.history):
        print(divider)
        print(f"Iteration {i + 1}")
        print(f"Generated nodes: {", ".join(str(i) for i in step["generated"])}")
        print(f"Inspected nodes: {", ".join(str(i) for i in step["inspected"])}")
    print(divider)
    print(f"Path: {" -> ".join(str(i) for i in result.path)}")
    print(divider)
    print(f"Cost: {result.cost}")
    print(divider)

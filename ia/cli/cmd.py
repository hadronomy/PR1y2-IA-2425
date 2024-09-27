from importlib.metadata import version

from typing import Annotated, Optional
import typer

from ia.graph import UndirectedGraph
from ia.graph.algorithm import TraversalAlgorithm


def run():
    """
    Configure and execute the CLI.
    """
    app = typer.Typer(pretty_exceptions_show_locals=False)
    app.command()(main)
    app(prog_name="ia")


def version_callback(value: bool):
    """
    Print the version.
    """
    if value:
        print(f"ia version {version('ia')}")
        raise typer.Exit()


def main(
    algorithm: Annotated[TraversalAlgorithm, typer.Option()],
    version: Annotated[
        Optional[bool], typer.Option("--version", "-v", callback=version_callback)
    ] = None,
):
    """
    Traverse the graph using the specified algorithm.
    """
    graph = UndirectedGraph()
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(3, 4)
    graph.add_edge(4, 1)
    start = 1
    end = 4
    divider = "-" * 30
    print(divider)
    print(f"Number of nodes: {len(graph.get_vertices())}")
    print(f"Number of edges: {len(graph.get_edges())}")
    print(f"Origin vertex: {1}")
    print(f"Destination vertex: {4}")
    for i, step in enumerate(graph.traverse(start=start, end=end, algorithm=algorithm)):
        print(divider)
        print(f"Iteration {i + 1}")
        print(f"Generated nodes: {", ".join(str(i) for i in step["generated"])}")
        print(f"Inspected nodes: {", ".join(str(i) for i in step["inspected"])}")
    print(divider)

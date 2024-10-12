"""cmd module.

Contains the different commands available.
"""

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from ia import __version__
from ia.cli.informed import informed
from ia.cli.uninformed import uninformed
from ia.graph.parser import parse_and_transform


def run():
    """Configure and execute the CLI."""
    app = typer.Typer(pretty_exceptions_show_locals=False)
    app.command("uninformed")(uninformed)
    app.command("informed")(informed)
    # This callback is needed to force typer to use
    # subcommands even when there is only one command.
    app.callback()(callback)

    try:
        import matplotlib.pyplot as plt  # type: ignore # noqa: F401
        import networkx as nx  # type: ignore # noqa: F401

        app.command("preview")(preview)
    except ImportError:
        pass
    app(prog_name="ia")


def version_callback(value: bool):
    """Print the version."""
    if value:
        print(f"ia version {__version__}")
        raise typer.Exit()


def callback(
    version: Annotated[
        bool | None,
        typer.Option(
            "--version",
            "-v",
            callback=version_callback,
            help="Print the program version.",
            is_eager=True,
        ),
    ] = None,
):
    """Cli app callback."""
    pass


def preview(
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
):
    """Render a graph preview."""
    console = Console()
    graph = None
    with open(input_path) as input_file:
        graph = parse_and_transform(input_file.read())
        if graph is None:
            console.print("\nFailed to parse the graph.", style="red bold")
            raise typer.Exit(1)
    import matplotlib.pyplot as plt  # type: ignore
    import networkx as nx  # type: ignore

    nx_graph = graph.to_networkx()

    pos = nx.nx_agraph.graphviz_layout(nx_graph, prog="dot")

    plt.figure(figsize=(10, 10))
    plt.suptitle("Graph preview\nby @hadronomy")
    plt.title(f"{input_path.name}")
    plt.axis("off")
    plt.tight_layout()

    nx.draw_networkx_nodes(
        nx_graph, pos, node_color="white", edgecolors="black", node_size=700
    )
    nx.draw_networkx_edges(nx_graph, pos, edge_color="black", width=5)
    nx.draw_networkx_labels(nx_graph, pos, font_size=15, font_family="sans-serif")
    edge_labels = nx.get_edge_attributes(nx_graph, "weight")
    nx.draw_networkx_edge_labels(nx_graph, pos, edge_labels)

    plt.show()

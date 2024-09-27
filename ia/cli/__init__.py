import typer

from ia.graph import UndirectedGraph, TraversalAlgorithm


def run():
    """
    Configure and execute the CLI.
    """
    app = typer.Typer()
    app.command()(rootCmd)
    app(prog_name="ia")


def rootCmd(algorithm: TraversalAlgorithm = TraversalAlgorithm.dfs):
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

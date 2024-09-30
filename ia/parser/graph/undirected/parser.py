"""Contains the definition of the parser for the graph language."""

from typing import Callable, Optional

from rich import inspect
from rich.console import Console, ConsoleOptions, RenderResult

from ia.graph import UndirectedGraph

from .generated_parser import (
    Discard,
    Lark_StandAlone,
    LarkError,
    Transformer,
    UnexpectedInput,
    VisitError,
    merge_transformers,
)


class UndirectedGraphTransformer(Transformer):
    """Transforms a parse tree into an undirected graph."""

    def NODE_AMOUNT(self, children):
        """
        Convert the first child node to an integer representing the node amount.

        Args
        ----
          children : list
            A list of child nodes, where the first element is
            expected to be convertible to an integer.

        Returns
        -------
          int: The integer value of the first child node.
        """
        return int(children[0])

    def WS(self, children):
        """
        Discard the whitespace token.

        Parameters
        ----------
        children : list
          The list of child nodes associated with the WS token.

        Returns
        -------
        Discard
          Indicates that the WS token should be discarded.
        """
        return Discard

    def NEWLINE(self, children):
        """
        Discard the NEWLINE token.

        Parameters
        ----------
        children : list
          The list of child nodes associated with the NEWLINE token.

        Returns
        -------
        Discard
          Indicates that the NEWLINE token should be discarded.
        """
        return Discard

    def weight(self, children):
        """
        Calculate the weight of an edge based on the given children.

        Args
        ----
          children : list
            A list containing a single element representing the weight of the edge.

        Returns
        -------
          float: The weight of the edge as a float if the value is not "-1".
          int: The weight of the edge as an integer if the value is "-1".
        """
        return float(children[0]) if children[0] != "-1" else int(children[0])

    def edge_weights(self, children):
        """
        Return the edge weights for the given children nodes.

        Parameters
        ----------
        children : list
          A list of child nodes.

        Returns
        -------
        list: The same list of child nodes, representing the edge weights.
        """
        return children

    def graph(self, children) -> UndirectedGraph:
        """Create an undirected graph from the given children nodes."""
        graph = UndirectedGraph()
        node_amount = children[0]
        weights = children[1]
        if node_amount * 2 != len(weights):
            raise UnexpectedInput(
                f"""the number of weights({len(weights)}) \
must be twice the number of nodes({node_amount})."""
            )
        weight_index = 0
        for i in range(1, node_amount):
            for j in range(i + 1, node_amount + 1):
                if weights[weight_index] != -1:
                    graph.add_edge(i, j, weight=weights[weight_index])
                weight_index += 1
        return graph


transformer = merge_transformers(UndirectedGraphTransformer())
undirected_graph_parser = Lark_StandAlone()


def parse_and_transform(
    input: str,
    start: str | None = None,
    on_error: "Optional[Callable[[UnexpectedInput], bool]]" = None,
) -> UndirectedGraph:
    """Parse and transform the given text."""
    on_error = on_error or on_parse_error
    try:
        tree = undirected_graph_parser.parse(input, start=start)
        return transformer.transform(tree)
    except LarkError as error:
        on_error(input, error)


def on_parse_error(text: str, error: UnexpectedInput) -> bool:
    """Handle parse errors."""
    console = Console()
    if error.__class__ == VisitError:
        console.print(f"[red]error[/red]: {error.orig_exc}\n")
        return True
    console.print("[red]error[/red]: invalid syntax\n")
    console.print(get_context(text, error), end="")
    console.print(f"{'=':>6} accepted tokens: {error.accepts}", style="blue")
    console.print(f"{'=':>6} expected tokens: {error.expected}", style="blue")
    console.print(f"{'=':>6} previous tokens: {error.token_history}", style="blue")
    return True


def get_context(text: str, error: UnexpectedInput, span: int = 40) -> str:
    """
    Get the context around the error position in the input text.

    Args
    ----
    text : str
        The input text where the error occurred.
    error : UnexpectedInput
        The error object containing details about the parse error.
    span : int, optional
        The number of characters to include before and after
        the error position (default is 40).

    Returns
    -------
    str
        A formatted string showing the context around the error position.
    """
    assert error.pos_in_stream is not None, error
    pos = error.pos_in_stream
    start = max(pos - span, 0)
    end = pos + span
    hint = ""
    if error.expected == {"NEWLINE"}:
        hint = "Did you forget to add a newline?"
    if not isinstance(text, bytes):
        before = text[start:pos].rsplit("\n", 1)[-1]
        after = text[pos:end].split("\n", 1)[0]
        line_number = text.count("\n", 0, pos) + 1
        column_number = pos - text.rfind("\n", 0, pos)
        return (
            f"     [blue]|[/blue]\n"
            f"[blue]{line_number:>4} |[/blue] [white]{before}{after}[/white]\n"
            f"     [blue]|[/blue] {' ' * (column_number - 1)}[red]^ {hint}[/red]\n"
            f"     [blue]|[/blue]\n"
        )
    else:
        before = text[start:pos].rsplit(b"\n", 1)[-1]
        after = text[pos:end].split(b"\n", 1)[0]
        line_number = text.count(b"\n", 0, pos) + 1
        column_number = pos - text.rfind(b"\n", 0, pos)
        return (
            f"     [blue]|[/blue]\n"
            f"[blue]{line_number:>4} |[/blue] [white]{before.decode()}{after.decode()}[/white]\n"  # noqa: E501
            f"     [blue]|[/blue] {' ' * (column_number - 1)}[red]^[/red]\n"
            f"     [blue]|[/blue]\n"
        )

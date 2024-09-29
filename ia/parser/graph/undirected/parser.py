"""Contains the definition of the parser for the graph language."""

from typing import Callable, Optional

from ia.graph import UndirectedGraph

from .generated_parser import (
    Discard,
    Lark_StandAlone,
    Transformer,
    UnexpectedInput,
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
            raise ValueError(
                f"""The number of weights({len(weights)}) \
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
    text: str,
    start: str | None = None,
    on_error: "Optional[Callable[[UnexpectedInput], bool]]" = None,
) -> UndirectedGraph:
    """Parse and transform the given text."""
    tree = undirected_graph_parser.parse(text, start=start, on_error=on_error)
    return transformer.transform(tree)

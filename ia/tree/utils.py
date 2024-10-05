"""Utility functions for working with trees."""

from __future__ import annotations

from collections.abc import Iterable
from typing import TypeVar

from .constants import ExportConstants
from .iterators import preorder_iter
from .node import Node

NodeT = TypeVar("NodeT", bound=Node)


def get_subtree(
    tree: NodeT,
) -> NodeT:
    """Get subtree from tree.

    Parameters
    ----------
        tree : (NodeT)
            Tree to get subtree from.
        node_name_or_path : (str)
            Node name or path to get subtree from.
        max_depth : (int)
            Maximum depth to get subtree from.

    Returns
    -------
        (NodeT)
    """
    tree = tree.copy()

    if not tree.is_root:
        tree.parent = None

    return tree


def print_tree(
    tree: NodeT,
    all_attributes: bool = False,
    attribute_list: Iterable[str] = None,
    attribute_bracket: list[str] = None,
    style: str | Iterable[str] = "const",
    **kargs: any,
) -> None:
    """Print tree."""
    if attribute_list is None:
        attribute_list = []
    if attribute_bracket is None:
        attribute_bracket = ["[", "]"]

    for pre_str, fill_str, _node in yield_tree(tree, style):
        attribute_str = ""
        if all_attributes or attribute_list:
            if len(attribute_bracket) != 2:
                raise ValueError("Attribute bracket must be a list of 2 strings.")
        attribute_bracket_open, attribute_bracket_close = attribute_bracket
        if all_attributes:
            attributes = _node.describe(exclude_attributes=["name"], exclude_prefix="_")
            attribute_str_list = [f"{key}={value}" for key, value in attributes.items()]
        else:
            attribute_str_list = [
                f"{attribute_name}={_node.get_attribute(attribute_name)}"
                for attribute_name in attribute_list
                if hasattr(_node, attribute_name)
            ]
        attribute_str = ", ".join(attribute_str_list)
        if attribute_str:
            attribute_str = (
                f" {attribute_bracket_open}{attribute_str}{attribute_bracket_close}"
            )
        node_str = f"{_node.name}{attribute_str}"
        print(f"{pre_str}{node_str}{fill_str}", **kargs)


def yield_tree(
    tree: NodeT,
    style: str | Iterable[str] = "const",
) -> Iterable[tuple[str, str, NodeT]]:
    """Generator method for customizing printing of tree, starting from `tree`."""  # noqa: D401
    from .utils import get_subtree

    tree = get_subtree(tree)

    if isinstance(style, str):
        avaidable_styles = ExportConstants.HPRINT_STYLES
        style_stem, style_branch, style_strem_final = avaidable_styles[style]
    elif isinstance(style, list) and len(list(style)) != 3:
        raise ValueError("Style must be a string or list of 3 strings.")
    else:
        style_stem, style_branch, style_strem_final = style

    if not len(style_stem) == len(style_branch) == len(style_strem_final):
        raise ValueError("All attributes must be of same length.")

    gap_str = " " * len(style_stem)
    unclosed_depth = set()
    initial_depth = tree.depth
    for _node in preorder_iter(tree):
        pre_str = ""
        fill_str = ""
        if not _node.is_root:
            node_depth = _node.depth - initial_depth

            if _node.right_sibling:
                unclosed_depth.discard(node_depth)
                fill_str = style_branch
            else:
                if node_depth in unclosed_depth:
                    unclosed_depth.remove(node_depth)
                fill_str = style_strem_final

            pre_str = ""
            for _depth in range(node_depth):
                if _depth in unclosed_depth:
                    pre_str += gap_str
                else:
                    pre_str += style_strem_final

        yield pre_str, fill_str, _node

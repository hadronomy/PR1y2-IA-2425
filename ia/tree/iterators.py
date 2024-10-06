"""Tree iterators."""

from collections.abc import Iterable
from typing import TypeVar

from .node import Node

T = TypeVar("T", bound=Node)


def preorder_iter(
    tree: T,
    max_depth: int = 0,
) -> Iterable[T]:
    """Inorder iterator for tree.

    Parameters
    ----------
        tree : (NodeT)
            Tree to iterate.

    Returns
    -------
        (Iterable[NodeT])
    """
    if tree and (not max_depth or not tree.get_attribute("depth") > max_depth):
        yield tree
        for child in tree.children:
            yield from preorder_iter(child, max_depth)


def postorder_iter(
    tree: T,
    max_depth: int = 0,
) -> Iterable[T]:
    """Inorder iterator for tree.

    Parameters
    ----------
        tree : (NodeT)
            Tree to iterate.

    Returns
    -------
        (Iterable[NodeT])
    """
    if tree and (not max_depth or not tree.get_attribute("depth") > max_depth):
        for child in tree.children:
            yield from postorder_iter(child, max_depth)
        yield tree

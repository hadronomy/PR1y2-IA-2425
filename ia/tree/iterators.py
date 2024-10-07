"""Tree iterators."""

from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import TypeVar

T = TypeVar("T")


def preorder_iter(
    tree: T,
    filter_contidition: Callable[[T], bool] | None = None,
    max_depth: int = 0,
) -> Iterable[T]:
    """Inorder iterator for tree.

    Parameters
    ----------
        tree : (NodeT)
            Tree to iterate.
        filter_contidition : (Callable[[NodeT], bool])
            Filter condition for nodes

    Returns
    -------
        (Iterable[NodeT])
    """
    if tree and (not max_depth or not tree.get_attribute("depth") > max_depth):
        if not filter_contidition or filter_contidition(tree):
            yield tree
        for child in tree.children:
            yield from preorder_iter(child, filter_contidition, max_depth)


def postorder_iter(
    tree: T,
    filter_contidition: Callable[[T], bool] | None = None,
    max_depth: int = 0,
) -> Iterable[T]:
    """Inorder iterator for tree.

    Parameters
    ----------
        tree : (NodeT)
            Tree to iterate.
        filter_contidition : (Callable[[NodeT], bool])
            Filter condition for nodes.

    Returns
    -------
        (Iterable[NodeT])
    """
    if tree and (not max_depth or not tree.get_attribute("depth") > max_depth):
        for child in tree.children:
            yield from postorder_iter(child, filter_contidition, max_depth)
        if not filter_contidition or filter_contidition(tree):
            yield tree

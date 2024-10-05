"""BaseNode module.

Based of `bigtree` python package.
"""

from __future__ import annotations

import copy
import heapq
from typing import TypeVar


class BaseNode:
    """BaseNode extends any Python class to a graph node."""

    def __init__(
        self, parent: T | None = None, children: list[T] | None = None, **kwargs
    ):
        """Initialize the node."""
        self.__parent: T | None = None
        self.__children: list[T] = []
        if children is None:
            children = []
        self.parent = parent
        self.children = children
        if "parents" in kwargs:
            raise AttributeError(
                "Attempting to set 'parents' attribute did you meen 'parent'?"
            )
        self.__dict__.update(kwargs)

    @property
    def parent(self) -> T | None:
        """Get the parent node.

        Returns
        -------
            T | None: The parent node.
        """
        return self.__parent

    @parent.setter
    def parent(self, new_parent: T) -> None:
        """Set the parent node.

        Parameters
        ----------
            new_parent (Self): parent node.
        """
        # Asserts
        self.__check_parent_type(new_parent)
        self.__check_parent_loop(new_parent)

        current_parent = self.parent
        current_child_idx = None

        self.__pre_assign_parent(new_parent)
        try:
            if current_parent is not None:
                if not any(child is self for child in current_parent.children):
                    raise ValueError("Node does not exists as children of it's parent")
                current_child_idx = current_parent.__children.index(self)
                current_parent.__children.remove(self)

            self.__parent = new_parent
            if new_parent is not None:
                new_parent.__children.append(self)
            self.__post_assign_parent(new_parent)
        except Exception as error_info:
            if new_parent is not None:
                new_parent.__children.remove(self)

            self.__parent = current_parent
            if current_child_idx is not None:
                current_parent.__children.insert(current_child_idx, self)

            # TODO: Custom errors
            raise error_info

    @staticmethod
    def __check_parent_type(new_parent: T) -> None:
        if not isinstance(new_parent, BaseNode) or new_parent is None:
            raise TypeError(
                f"""\
                Parent must be of type BaseNode or NoneType, got {type(new_parent)}\
                instead.\
                """
            )

    def __check_parent_loop(self, new_parent: T) -> None:
        """Check parent type.

        Parameters
        ----------
            new_parent (T): The parent node.
        """
        if new_parent is not None:
            if self in new_parent.parents:
                if new_parent is self:
                    raise ValueError("Cannot set parent to self.")
                if any(
                    ancestor is self
                    for ancestor in new_parent.ancestors
                    if new_parent.ancestors
                ):
                    raise ValueError("Node cannot be ancestor of itself.")

    def __pre_assign_parent(self, new_parent: T) -> None:
        """Custom method to check before assigning the parent.

        Can be overriden with `_BaseNode__pre_assign_parent`.

        Parameters
        ----------
            new_parent (T): The parent node.
        """  # noqa: D401
        pass

    def __post_assign_parent(self, new_parent: T) -> None:
        """Custom method to check after assigning the parent.

        Can be overriden with `_BaseNode__post_assign_parent`.

        Parameters
        ----------
            new_parent (T): The parent node.
        """  # noqa: D401
        pass


T = TypeVar("T", bound=BaseNode)

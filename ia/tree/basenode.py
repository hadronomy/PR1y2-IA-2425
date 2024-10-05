"""BaseNode module.

Based of `bigtree` python package.
"""

import copy
import heapq
from typing import List, Optional, TypeVar

T = TypeVar("T", bound="BaseNode")


class BaseNode:
    """BaseNode extends any Python class to a graph node."""

    def __init__(
        self, parent: Optional[T] = None, children: Optional[List[T]] = None, **kwargs
    ):
        """Initialize the node."""
        self.__parent: Optional[T] = None
        self.__children: List[T] = []
        if children is None:
            children = []
        self.parent = parent
        self.children = children
        if "parents" in kwargs:
            raise AttributeError(
                "Attempting to set 'parents' attribute did you meen 'parent'?"
            )
        self.__dict__.update(kwargs)

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

    @property
    def parent(self) -> Optional[T]:
        """Get the parent node.

        Returns
        -------
            Optional[T]: The parent node.
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

        # TODO: Assign parent

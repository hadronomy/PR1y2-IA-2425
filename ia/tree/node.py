"""Node module.

Contains the Node class.
"""

from __future__ import annotations

from collections import Counter
from typing import TypeVar

from .basenode import BaseNode


class Node(BaseNode):
    """Node is an extension of BaseNode, and is able to extend any Python class.

    Nodes can have attributes if they are initialized `Node`, *dictionary*.
    Nodes can be linked to each other with `parent` and `children` setter methods.
    """

    def __init__(self, name: str = "", separator: str = "/", **kargs: any):
        self.name = name
        self._separator = separator
        super().__init__(**kargs)
        if not self.node_name:
            raise ValueError("Node name is required.")

    @property
    def separator(self) -> str:
        """Get separator, gets from root node.

        Returns
        -------
            (str)
        """
        if self.parent is None:
            return self._separator
        return self.parent.separator

    @separator.setter
    def separator(self, value: str) -> None:
        """Set separator, sets to root node.

        Parameters
        ----------
            value : (str)
        """
        self.root._separator = value

    @property
    def node_name(self) -> str:
        """Get node name.

        Returns
        -------
            (str)
        """
        return self.name

    @property
    def path_name(self) -> str:
        """Get path name.

        Returns
        -------
            (str)
        """
        ancestors = [self] + list(self.ancestors)
        separator = ancestors[-1].separator
        return separator + separator.join(
            [str(node.name) for node in reversed(ancestors)]
        )

    def __pre_assign_parent(self, new_parent: T) -> None:
        """Custom method to check before attaching a parent."""
        pass

    def __pre_assign_children(self, new_children: list[T]) -> None:
        """Custom method to check before attaching children."""
        pass

    def _BaseNode__pre_assign_parent(self: T, new_parent: T) -> None:
        """Do not allow duplicate nodes of the same path.

        Parameters
        ----------
            new_parent : (Node)
        """
        self.__pre_assign_parent(new_parent)
        if new_parent is not None:
            if any(
                child.node_name == self.node_name and child is not self
                for child in new_parent.children
            ):
                raise ValueError(
                    f"Duplicate node with the same path\n.",
                    f"There exist a node with the same path: {self.path_name}{new_parent.separator}{self.node_name}",
                )

    def _BaseNode__pre_assign_children(self: T, new_children: list[T]) -> None:
        """Do not allow duplicate nodes of the same path.

        Parameters
        ----------
            new_children : (list[Node])
        """
        self.__pre_assign_children(new_children)
        children_names = [node.node_name for node in new_children]
        duplicate_names = [
            item[0] for item in Counter(children_names).items() if item[1] > 1
        ]
        if len(duplicate_names):
            duplicate_names_str = " and ".join(
                [f"{self.path_name}{self.separator}{name}" for name in duplicate_names]
            )
            raise ValueError(
                f"Duplicate nodes with the same path\n.",
                f"There exist nodes with the same path: {duplicate_names_str}",
            )

    def __getitem__(self, child_name: str) -> Node:
        """Get child node by name.

        Parameters
        ----------
            child_name : (str)

        Returns
        -------
            (Node)
        """
        return self.children[child_name]

    def __repr__(self) -> str:
        """Print format of Node.

        Returns
        -------
            (str)
        """
        class_name = self.__class__.__name__
        node_dict = self.describe(exclude_prefix="_", exclude_attributes=["name"])
        node_description = ", ".join([f"{key}={value}" for key, value in node_dict])
        return f"{class_name}({self.path_name}, {node_description})"


T = TypeVar("T", bound=Node)

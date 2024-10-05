"""Node module.

Contains the Node class.
"""

from __future__ import annotations

from typing import TypeVar

from .basenode import BaseNode


class Node(BaseNode):
    """Node is an extension of BaseNode, and is able to extend any Python class.

    Nodes can have attributes if they are initialized `Node`, *dictionary*.
    Nodes can be linked to each other with `parent` and `children` setter methods.
    """

    def __init__(self, name: str = "", separator: str = "/", **kargs: any):
        self.name = name
        self._sep = separator
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
            return self._sep
        return self.parent.sep

    @separator.setter
    def separator(self, value: str) -> None:
        """Set separator, sets to root node.

        Parameters
        ----------
            value : (str)
        """
        self.root._sep = value

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
        return separator + separator.join([str(node.name) for node in ancestors])

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
        node_description = ", ".join(
            [f"{key}={value}" for key, value in node_dict.items()]
        )
        return f"{class_name}({self.path_name}, {node_description})"


T = TypeVar("T", bound=Node)

"""BaseNode module.

Based of `bigtree` python package.
"""

from __future__ import annotations

import copy
import heapq
from collections.abc import Iterable
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

    @property
    def children(self) -> tuple[T, ...]:
        """Get the children nodes.

        Returns
        -------
            list[T]: The children nodes.
        """
        return tuple(self.__children)

    @children.setter
    def children(self, new_children: list[T] | tuple[T] | set[T]) -> None:
        """Set the children nodes.

        Args:
            new_children (list[T] | tuple[T] | set[T]): child node
        """
        self.__check_children_type(new_children)
        self.__check_children_loop(new_children)

        new_children = list(new_children)

        current_new_children = {
            new_child: (new_child.parent.__children.index(new_child), new_child.parent)
            for new_child in new_children
            if new_child.parent is not None
        }
        current_new_orphan = [
            new_child for new_child in new_children if new_child.parent is None
        ]
        current_children = list(self.children)

        self.__pre_assign_children(new_children)
        try:
            del self.children

            self.__children = new_children
            for new_child in new_children:
                if new_child.parent:
                    new_child.parent.__children.remove(new_child)
                new_child.__parent = self
            self.__post_assign_children(new_children)
        except Exception as error_info:
            for child, idx_parent in current_new_children.items():
                child_idx, parent = idx_parent
                child.__parent = parent
                parent.__children.insert(child_idx, child)
            for child in current_new_orphan:
                child.__parent = None

            self.__children = current_children
            for child in current_children:
                child.__parent = self
            raise error_info

    @children.deleter
    def children(self) -> None:
        """Delete child nodes."""
        for child in self.__children:
            child.__parent.__children.remove(child)
            child.__parent = None

    @staticmethod
    def __check_children_type(new_children: list[T] | tuple[T] | set[T]) -> None:
        if (
            not isinstance(new_children, list)
            and not isinstance(new_children, tuple)
            and not isinstance(new_children, set)
        ):
            raise TypeError(
                f"""Expect children to be List or Tuple or Set type,\
                received input type {type(new_children)}"""
            )

    def __check_children_loop(self, new_children: list[T] | tuple[T] | set[T]) -> None:
        """Check child loop.

        Args
        ----
            new_children (list[T] | tuple[T] | set[T]): _description_
        """
        seen_children = []
        for new_child in new_children:
            if not isinstance(new_child, BaseNode):
                raise TypeError(
                    f"""\
                    Children must be of type BaseNode, got {type(new_child)}\
                    instead.\
                    """
                )
            if new_child is self:
                raise ValueError("Node cannot be child of itself.")
            if any(child is new_child for child in self.ancestors):
                raise ValueError("Node cannot be ancestor of itself.")
            if id(new_child) in seen_children:
                raise ValueError("Cannot have duplicate children.")
            else:
                seen_children.append(id(new_child))

    def __pre_assign_children(self, new_children: list[T] | tuple[T] | set[T]) -> None:
        """Custom method to check before assigning the children.

        Can be overriden with `_BaseNode__pre_assign_children`.

        Parameters
        ----------
            new_children (list[T] | tuple[T] | set[T]): The children nodes.
        """  # noqa: D401
        pass

    def __post_assign_children(self, new_children: list[T] | tuple[T] | set[T]) -> None:
        """Custom method to check after assigning the children.

        Can be overriden with `_BaseNode__post_assign_children`.

        Parameters
        ----------
            new_children (list[T] | tuple[T] | set[T]): The children nodes.
        """  # noqa: D401
        pass

    @property
    def ancestors(self: T) -> Iterable[T]:
        """Get the ancestors nodes.

        Returns
        -------
            list[T]: The ancestors nodes.
        """
        node = self.parent
        while node is not None:
            yield node
            node = node.parent

    @property
    def descendants(self: T) -> Iterable[T]:
        """Get the descendants nodes.

        Returns
        -------
            list[T]: The descendants nodes.
        """
        # TODO: Implement custom iterators
        pass

    @property
    def leaves(self: T) -> Iterable[T]:
        """Get the leaves nodes.

        Returns
        -------
            list[T]: The leaves nodes.
        """
        # TODO: Implement custom iterators
        pass

    @property
    def siblings(self: T) -> Iterable[T]:
        """Get the siblings nodes.

        Returns
        -------
            list[T]: The siblings nodes.
        """
        if self.parent is None:
            return ()
        return tuple(child for child in self.parent.children if child is not self)

    @property
    def left_sibling(self: T) -> T | None:
        """Get the left sibling node.

        Returns
        -------
            T: The left sibling node.
        """
        if self.parent is None:
            return None
        siblings = self.parent.children
        idx = siblings.index(self)
        if idx:
            return self.parent.children[idx - 1]

    @property
    def right_sibling(self: T) -> T | None:
        """Get the right sibling node.

        Returns
        -------
            T: The right sibling node.
        """
        if self.parent is None:
            return None
        siblings = self.parent.children
        idx = siblings.index(self)
        if idx + 1 < len(siblings):
            return self.parent.children[idx + 1]

    @property
    def node_path(self: T) -> Iterable[T]:
        """Get the node path.

        Returns
        -------
            list[T]: The node path.
        """
        # TODO: Check if this works properly
        if self.parent is None:
            return [self]
        return tuple(self.ancestors) + (self,)

    @property
    def is_root(self) -> bool:
        """Check if the node is root.

        Returns
        -------
            bool: True if the node is root, False otherwise.
        """
        return self.parent is None

    @property
    def is_leaf(self) -> bool:
        """Check if the node is leaf.

        Returns
        -------
            bool: True if the node is leaf, False otherwise.
        """
        return not len(list(self.children))

    @property
    def root(self: T) -> T:
        """Get the root node.

        Returns
        -------
            T: The root node.
        """
        return next(iter(self.ancestors), self)

    @property
    def diameter(self) -> int:
        """Get the diameter of the tree.

        Returns
        -------
            int: The diameter of the tree.
        """
        diameter = 0

        if self.is_leaf:
            return diameter

        def _recursive_diameter(node: T) -> int:
            """Get diameter of tree or subtree.

            The length of the longest path between any two nodes

            Args
            ----
                node (T): _description_

            Returns
            -------
                int: _description_
            """
            nonlocal diameter
            if node.is_leaf:
                return 1
            child_length = [_recursive_diameter(child) for child in node.children]
            diameter = max(diameter, sum(heapq.nlargest(2, child_length)))
            return max(child_length) + 1

        _recursive_diameter(self)
        return diameter

    @property
    def depth(self: T) -> int:
        """Get the depth of the node.

        Returns
        -------
            int: The depth of the node.
        """
        return len(list(self.ancestors))

    @classmethod
    def from_dict(cls, input_dict: dict[str, any]) -> BaseNode:
        """Create a tree from a dictionary.

        Args
        ----
            input_dict (dict[str, any]): dictionary with node information,
            key: attribute name, value: attribute value

        Returns
        -------
            (BaseNode)
        """
        return cls(**input_dict)

    def describe(
        self, exclude_attributes: list[str] = None, exclude_prefix: str = ""
    ) -> list[tuple[str, any]]:
        """Describe the node.

        Args
        ----
            exclude_attributes (list[str]): list of attributes to exclude
            exclude_prefix (str): prefix to exclude

        Returns
        -------
            list[tuple[str, any]]: list of attributes and their values
        """
        if exclude_attributes is None:
            exclude_attributes = []
        return [
            (key, value)
            for key, value in sorted(self.__dict__.items())
            if key not in exclude_attributes and not key.startswith(exclude_prefix)
        ]

    def get_attribute(self, attribute_name: str, default_value: any = None) -> any:
        """Get the attribute value.

        Args
        ----
            attribute_name (str): attribute name
            default_value (any): default value if attribute is not found

        Returns
        -------
            any: attribute value
        """
        try:
            return getattr(self, attribute_name)
        except AttributeError:
            return default_value

    def set_attribute(self: T, attributes: dict[str, any]) -> Iterable[T]:
        """Set the attribute value.

        Args
        ----
            node (T): node to travel to from current node,
            inclusive of start and end node

        Returns
        -------
            (Iterable[T])
        """
        self.__dict__.update(attributes)

    def append(self: T, other: T) -> None:
        """Append other as child of self.

        Args
        ----
            other (Self): child to be added
        """
        other.parent = self

    def extend(self: T, other: list[T]) -> None:
        """Extend children of self with other.

        Args
        ----
            other (list[T]): children to be added
        """
        for child in other:
            child.parent = self

    def copy(self: T) -> T:
        """Copy the node.

        Returns
        -------
            (T)
        """
        return copy.deepcopy(self)

    def sort(self: T, **kwargs) -> None:
        """Sort the children nodes.

        Args
        ----
            kwargs: sort arguments
        """
        children = list(self.__children)
        children.sort(**kwargs)
        self.__children = children

    def __copy__(self: T) -> T:
        """Copy the node.

        Returns
        -------
            (T)
        """
        obj: T = type(self).__new__(self.__class__)
        obj.__dict__.update(self.__dict__)
        return obj

    def __repr__(self) -> str:
        """Representation of the node.

        Returns
        -------
            str: string representation of the node
        """
        class_name = self.__class__.__name__
        node_dict = self.describe(exclude_prefix="_")
        node_description = ", ".join(f"{key}={value!r}" for key, value in node_dict)
        return f"{class_name}({node_description})"

    def __rshift__(self, other: T) -> None:
        """Append other as child of self.

        Args
        ----
            other (Self): child to be added
        """
        other.parent = self

    def __lshift__(self, other: T) -> None:
        """Append self as child of other.

        Args
        ----
            other (Self): parent to be added
        """
        self.parent = other

    def __iter__(self: T) -> Iterable[T]:
        """Iterate over the children nodes.

        Returns
        -------
            (Iterable[T])
        """
        yield from self.__children

    def __contains__(self: T, other: T) -> bool:
        """Check if other is in children nodes.

        Args
        ----
            other (Self): node to check

        Returns
        -------
            (bool)
        """
        return other in self.__children


T = TypeVar("T", bound=BaseNode)

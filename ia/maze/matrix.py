"""Module with matrix data structure."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import TypeVar

from ia.maze.utils import number_to_representation


@dataclass(frozen=True, repr=True, eq=True, unsafe_hash=True)
class MatrixPosition:
    """Matrix position data structure."""

    row: int
    col: int

    def representation(
        self, translation_dict: dict[str, list[str]] = None
    ) -> tuple[str, str]:
        """Get the representation of the position.

        Returns
        -------
            (tuple[str, str])
                The representation of the position.
        """
        if translation_dict is None:
            translation_dict = {
                "row": [str(number) for number in range(0, 10)],
                "col": [chr(letter) for letter in range(65, 91)],
            }

        row_representation = number_to_representation(self.row, translation_dict["row"])
        col_representation = number_to_representation(self.col, translation_dict["col"])
        return row_representation, col_representation

    @classmethod
    def from_representation(
        cls,
        representation: tuple[str, str],
    ):
        """Create a position from its representation.

        Parameters
        ----------
            representation : (tuple[str, str])
                The representation of the position.

        Returns
        -------
            (MatrixPosition)
                The position.
        """
        row, col = representation
        translation_dict = {
            "row": [str(number) for number in range(0, 10)],
            "col": [chr(letter) for letter in range(65, 91)],
        }

        def calculate_index(value, translation_dict):
            index = 0
            for char in value:
                index = index * len(translation_dict) + translation_dict.index(char)
            return index

        row_index = calculate_index(row, translation_dict["row"])
        col_index = calculate_index(col, translation_dict["col"])
        return cls(row=row_index, col=col_index)

    def __add__(self, other: MatrixPosition | tuple[int, int]) -> MatrixPosition:
        """Add two positions."""
        if isinstance(other, tuple):
            return MatrixPosition(self.row + other[0], self.col + other[1])
        return MatrixPosition(self.row + other.row, self.col + other.col)

    def __radd__(self, other: MatrixPosition | tuple[int, int]) -> MatrixPosition:
        """Add two positions."""
        return self.__add__(other)

    def __sub__(self, other: MatrixPosition | tuple[int, int]) -> MatrixPosition:
        """Subtract two positions."""
        if isinstance(other, tuple):
            return MatrixPosition(self.row - other[0], self.col - other[1])
        return MatrixPosition(self.row - other.row, self.col - other.col)

    def __rsub__(self, other: MatrixPosition | tuple[int, int]) -> MatrixPosition:
        """Subtract two positions."""
        return self.__sub__(other)

    def __mul__(self, other: int) -> MatrixPosition:
        """Multiply a position by a scalar."""
        return MatrixPosition(self.row * other, self.col * other)

    def __rmul__(self, other: int) -> MatrixPosition:
        """Multiply a position by a scalar."""
        return self.__mul__(other)

    def __str__(self) -> str:
        """Return the position as a string."""
        return f"({self.row}, {self.col})"


class Matrix:
    """Matrix data structure."""

    def __init__(self, *, rows: int, cols: int, default: TContent) -> None:
        self.__rows = rows
        self.__cols = cols
        self.__default = default
        self.__data = [[default for _ in range(cols)] for _ in range(rows)]

    @property
    def rows(self) -> int:
        """Get the number of rows."""
        return self.__rows

    @property
    def cols(self) -> int:
        """Get the number of columns."""
        return self.__cols

    @property
    def default(self) -> TContent:
        """Get the default value."""
        return self.__default

    def neighbors(
        self, row: int, col: int, offsets: list[MatrixPosition] = None
    ) -> dict[MatrixPosition, MatrixPosition]:
        """Get the adjacent cells.

        Parameters
        ----------
            row : (int)
                The row of the cell.
            col : (int)
                The column of the cell.
            offsets : (list[MatrixPosition])
                The offsets to check.
                By default, it checks the 4 cardinal directions and the 4 diagonals.

        Returns
        -------
            (dict[MatrixPosition, MatrixPosition])
                Dictionary with the adjacent cells, where the key is the offset
                and the value is the position.
        """
        if offsets is None:
            offsets = [
                (0, 1),
                (1, 0),
                (0, -1),
                (-1, 0),
                (1, 1),
                (1, -1),
                (-1, 1),
                (-1, -1),
            ]
        adjacent: dict[MatrixPosition, MatrixPosition] = {}
        for row_offset, col_offset in offsets:
            new_row, new_col = row + row_offset, col + col_offset
            if 0 <= new_row < self.__rows and 0 <= new_col < self.__cols:
                adjacent.update(
                    {
                        MatrixPosition(row_offset, col_offset): MatrixPosition(
                            new_row, new_col
                        )
                    }
                )
        return adjacent

    def is_valid(self, row: int, col: int) -> bool:
        """Check if the position is valid.

        Parameters
        ----------
            row : (int)
                The row of the cell.
            col : (int)
                The column of the cell.

        Returns
        -------
            (bool)
                True if the position is valid, False otherwise.
        """
        return 0 <= row < self.__rows and 0 <= col < self.__cols

    def is_valid_position(self, position: MatrixPosition) -> bool:
        """Check if the position is valid.

        Parameters
        ----------
            position : (MatrixPosition)
                The position to check.

        Returns
        -------
            (bool)
                True if the position is valid, False otherwise.
        """
        return self.is_valid(position.row, position.col)

    def __len__(self) -> int:
        """Return the number of elements in the matrix."""
        return self.__rows * self.__cols

    def __getitem__(self, key: MatrixPosition) -> TContent:
        """Get the value of the matrix."""
        if isinstance(key, tuple):
            key = MatrixPosition(*key)
        return self.__data[key.row][key.col]

    def __setitem__(self, key: MatrixPosition, value: TContent) -> None:
        """Set the value of the matrix."""
        if isinstance(key, tuple):
            key = MatrixPosition(*key)
        self.__data[key.row][key.col] = value

    def __contains__(self, item: TContent) -> bool:
        """Check if the matrix contains the item."""
        return item in self.__data

    def __iter__(self) -> Iterable[TContent]:
        """Iterate over the matrix.

        Yields
        ------
            (tuple[MatrixPosition, TContent])
                The position and the value of the matrix tile.
        """
        yield from self.__data

    def __str__(self) -> str:
        """Return the matrix as a string."""
        horizontal_border = "+" + "-" * (self.__cols * 3 + (self.__cols - 1)) + "+"
        rows_str = "\n".join(
            "| " + " ".join(f"{item:2}" for item in row) + " |" for row in self.__data
        )
        return f"{horizontal_border}\n{rows_str}\n{horizontal_border}"

    def __repr__(self) -> str:
        """Return the matrix as a string."""
        return str(self)


TContent = TypeVar("TContent", bound=any)


class enumerate_matrix(Iterable[tuple[MatrixPosition, TContent]]):
    """Enumerate the matrix.

    Parameters
    ----------
        matrix : (Matrix)
            The matrix to enumerate.

    Yields
    ------
        (tuple[MatrixPosition, TContent])
            The position and the value of the matrix tile.
    """

    def __init__(self, matrix: Matrix):
        self.__matrix = matrix

    def __iter__(self) -> Iterable[tuple[MatrixPosition, TContent]]:
        """Iterate over the matrix."""
        for row in range(self.__matrix.rows):
            for col in range(self.__matrix.cols):
                yield MatrixPosition(row, col), self.__matrix[row, col]

    def __str__(self) -> str:
        """Return the matrix as a string."""
        return str(self.__matrix)

    def __repr__(self) -> str:
        """Return the matrix as a string."""
        return str(self.__matrix)

"""Utility functions for the maze module."""


def number_to_representation(number: int, translation_list: list[str]) -> str:
    """Convert a number to a representation.

    Parameters
    ----------
        number : (int)
            The number to convert.
        translation_dict : (list[str])
            The translation dictionary.

    Returns
    -------
        (str)
            The representation of the number.
    """
    representation = translation_list[number % len(translation_list)]
    while number >= len(translation_list):
        number //= len(translation_list)
        representation = (
            translation_list[number % len(translation_list)] + representation
        )
    return representation

"""Utility helpers for displaying the game board.

This module contains small printing functions that were previously scattered
throughout the project.  Grouping them here provides a clear and reusable API
for any scripts that need to display a board or add formatted spacing.
"""

from typing import Sequence


Array2D = Sequence[Sequence[int]]


def print_2d_array(array: Array2D) -> None:
    """Print ``array`` row by row.

    Each element is converted to ``str`` and separated by a single space.
    """

    for row in array:
        print(" ".join(str(element) for element in row))


def print_space() -> None:
    """Print a divider line of ``=`` characters."""

    print("=" * 20)


def extra_space() -> None:
    """Print three divider lines for extra spacing."""

    for _ in range(3):
        print_space()


def print_board(game_board: Array2D) -> None:
    """Display ``game_board`` with surrounding spacing."""

    extra_space()
    print_2d_array(game_board)


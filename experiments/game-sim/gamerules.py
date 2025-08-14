"""Core game rules for the BlockGameAI project.

This module provides small utility functions that operate purely on the
in‑memory representation of the board.  The original repository contained a
number of experimental scripts and GUI prototypes but lacked the basic logic
required to reason about moves programmatically.  The functions implemented
here allow the tests to interact with the game without relying on any GUI
framework.

The board is represented as a two dimensional list (or any sequence of
sequences) containing ``0`` for empty cells and non‑zero values for occupied
cells.  A ``piece`` is represented in the same way.  ``position`` is a tuple of
``(row, column)`` describing the top‑left corner where the piece should be
placed.

The three public helpers are:

``is_valid_placement`` – Checks whether a piece can be placed on the board.
``apply_move`` – Applies a valid move, clears completed lines and returns a
                  reward score.
``line_clear_reward`` – Calculates bonus points for clearing lines.

These functions are intentionally framework agnostic so they can be reused by
AI agents or simple command line programs.
"""

from typing import List, Sequence, Tuple


Board = Sequence[Sequence[int]]
Piece = Sequence[Sequence[int]]
Position = Tuple[int, int]


def is_valid_placement(board: Board, piece: Piece, position: Position) -> bool:
    """Return ``True`` if ``piece`` can be placed on ``board`` at ``position``.

    The function checks that the piece fits entirely inside the board's bounds
    and that it does not overlap with any already occupied cell.
    """

    rows = len(board)
    cols = len(board[0]) if rows else 0
    start_r, start_c = position

    for r in range(len(piece)):
        for c in range(len(piece[0])):
            if piece[r][c]:
                br, bc = start_r + r, start_c + c
                if br < 0 or br >= rows or bc < 0 or bc >= cols:
                    return False
                if board[br][bc]:
                    return False
    return True


def line_clear_reward(lines: int) -> int:
    """Return the bonus score for clearing ``lines`` lines.

    The scoring follows the table used in the early prototypes of the project:

    * 1 line  ->  10 points
    * 2 lines ->  30 points
    * 3 lines ->  60 points
    * 4 lines -> 100 points
    * 5 lines -> 150 points

    For more than five lines a simple linear scaling is used.
    """

    score_table = {1: 10, 2: 30, 3: 60, 4: 100, 5: 150}
    if lines <= 0:
        return 0
    return score_table.get(lines, lines * 30)


def _clear_completed_lines(board: List[List[int]]) -> int:
    """Remove filled rows and columns from ``board`` and return how many.

    The board is modified in place.  The return value is the total number of
    rows and columns cleared.
    """

    rows = len(board)
    cols = len(board[0]) if rows else 0

    rows_to_clear = [r for r in range(rows) if all(board[r][c] for c in range(cols))]
    cols_to_clear = [c for c in range(cols) if all(board[r][c] for r in range(rows))]

    for r in rows_to_clear:
        for c in range(cols):
            board[r][c] = 0

    for c in cols_to_clear:
        for r in range(rows):
            board[r][c] = 0

    return len(rows_to_clear) + len(cols_to_clear)


def apply_move(board: List[List[int]], piece: Piece, position: Position) -> int:
    """Place ``piece`` on ``board`` and return the reward for the move.

    The board is updated in place.  The reward consists of the number of tiles
    placed plus any bonus from clearing lines.  A ``ValueError`` is raised if the
    move is not valid.
    """

    if not is_valid_placement(board, piece, position):
        raise ValueError("Invalid move")

    start_r, start_c = position
    tiles_placed = 0
    for r in range(len(piece)):
        for c in range(len(piece[0])):
            if piece[r][c]:
                board[start_r + r][start_c + c] = 1
                tiles_placed += 1

    lines_cleared = _clear_completed_lines(board)
    reward = tiles_placed + line_clear_reward(lines_cleared)
    return reward


# if the square is clicked, then it stays clicked
# game rule will check if a vertical or a horizontal line has been made that connects end to end
# if true the game will award the points
# if multiples lines are destroyed at once those extra points are awarded
# if the whole board is cleared then the 300 extra points are awarded
# game will check points to see when to upgrade blocks selection

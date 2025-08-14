import random
from typing import Any, Dict, List, Tuple

import numpy as np


def generate_orientations(mask: np.ndarray) -> List[np.ndarray]:
    """Return all unique rotations and reflections of ``mask``.

    Each mask is treated as a boolean array where ``True`` indicates a filled
    cell. The returned list contains unique orientations accounting for the four
    rotations and horizontal reflections.
    """
    if mask.dtype != np.bool_:
        mask = mask.astype(bool)

    variants: List[np.ndarray] = []
    for k in range(4):
        rotated = np.rot90(mask, k)
        for variant in (rotated, np.fliplr(rotated)):
            if not any(np.array_equal(variant, v) for v in variants):
                variants.append(variant)
    return variants


# Example base pieces defined as boolean masks
BASE_PIECES: Dict[str, np.ndarray] = {
    "L": np.array(
        [
            [1, 0],
            [1, 0],
            [1, 1],
        ],
        dtype=bool,
    ),
    "I": np.array(
        [
            [1],
            [1],
            [1],
            [1],
        ],
        dtype=bool,
    ),
}

PIECE_MASKS: Dict[str, List[np.ndarray]] = {
    name: generate_orientations(mask) for name, mask in BASE_PIECES.items()
}


class BlockPuzzleEnv:
    """Block puzzle environment consolidating features from various versions.

    The board is a square grid represented by plain Python lists to keep the
    environment lightweight and easily hashable for tabular methods.
    """

    def __init__(self, size: int = 8):
        self.size = size
        self.action_space = size * size
        self.board: List[List[int]] = []
        self.reset()

    # ------------------------------------------------------------------
    def reset(self) -> Tuple[int, ...]:
        """Reset the board to an empty state and return the initial state."""
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        return self._get_state()

    # ------------------------------------------------------------------
    def _get_state(self) -> Tuple[int, ...]:
        """Return a hashable representation of the current board."""
        return tuple(cell for row in self.board for cell in row)

    # ------------------------------------------------------------------
    def available_actions(self) -> List[int]:
        """Return a list of indices for empty cells."""
        actions = []
        for idx in range(self.action_space):
            row, col = divmod(idx, self.size)
            if self.board[row][col] == 0:
                actions.append(idx)
        return actions

    # Alias used by some older agents
    valid_actions = available_actions

    # ------------------------------------------------------------------
    def _clear_lines(self, board: List[List[int]]) -> Tuple[List[List[int]], int]:
        """Clear any completely filled rows or columns.

        Returns a tuple of the new board and the number of cells cleared.
        """
        cleared = 0
        # Clear full rows
        for r in range(self.size):
            if all(board[r][c] == 1 for c in range(self.size)):
                for c in range(self.size):
                    board[r][c] = 0
                cleared += self.size
        # Clear full columns
        for c in range(self.size):
            if all(board[r][c] == 1 for r in range(self.size)):
                for r in range(self.size):
                    board[r][c] = 0
                cleared += self.size
        return board, cleared

    # ------------------------------------------------------------------
    def _count_gaps(self, board: List[List[int]]) -> int:
        """Count the number of gaps beneath filled cells in each column."""
        gaps = 0
        for c in range(self.size):
            filled_seen = False
            for r in range(self.size):
                if board[r][c] == 1:
                    filled_seen = True
                elif filled_seen:
                    gaps += 1
        return gaps

    # ------------------------------------------------------------------
    def step(self, action: int) -> Tuple[Tuple[int, ...], int, bool, Dict[str, Any]]:
        """Apply the chosen action (placing a single cell)."""
        row, col = divmod(action, self.size)
        reward = 0
        done = False

        if self.board[row][col] == 1:
            reward = -1
            done = True
            return self._get_state(), reward, done, {}

        self.board[row][col] = 1
        reward = 1

        self.board, cleared = self._clear_lines(self.board)
        reward += cleared

        if not self.available_actions():
            done = True

        return self._get_state(), reward, done, {}

    # ------------------------------------------------------------------
    def can_place(self, mask: np.ndarray, top_left: Tuple[int, int]) -> bool:
        """Check if ``mask`` can be placed at ``top_left`` without overlap."""
        r, c = top_left
        h, w = mask.shape
        if r < 0 or c < 0 or r + h > self.size or c + w > self.size:
            return False
        board_arr = np.array(self.board)
        mask_bool = mask.astype(bool)
        board_slice = board_arr[r : r + h, c : c + w]
        return np.all(board_slice[mask_bool] == 0)

    # ------------------------------------------------------------------
    def place_mask(self, mask: np.ndarray, top_left: Tuple[int, int]) -> bool:
        """Place ``mask`` on the board at ``top_left`` if space is available."""
        if not self.can_place(mask, top_left):
            return False
        r, c = top_left
        h, w = mask.shape
        mask_bool = mask.astype(bool)
        for i in range(h):
            for j in range(w):
                if mask_bool[i][j]:
                    self.board[r + i][c + j] = 1
        return True

    # ------------------------------------------------------------------
    def remove_mask(self, mask: np.ndarray, top_left: Tuple[int, int]) -> None:
        """Remove ``mask`` from the board at ``top_left``."""
        r, c = top_left
        h, w = mask.shape
        mask_bool = mask.astype(bool)
        for i in range(h):
            for j in range(w):
                if mask_bool[i][j]:
                    self.board[r + i][c + j] = 0

    # ------------------------------------------------------------------
    def render(self) -> None:
        """Print the current board."""
        for row in self.board:
            print(" ".join(str(cell) for cell in row))

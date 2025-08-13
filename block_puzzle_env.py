import numpy as np
from typing import Dict, List, Tuple


def generate_orientations(mask: np.ndarray) -> List[np.ndarray]:
    """Return all unique rotations and reflections of ``mask``.

    Each mask is treated as a boolean array where ``True`` indicates a filled
    cell. The returned list contains unique orientations accounting for the four
    rotations and horizontal reflections.
    """
    if mask.dtype != np.bool_:  # ensure boolean mask
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
    """Simple board representation for a block puzzle game."""

    def __init__(self, size: int = 8) -> None:
        self.size = size
        # Board represented as integers where ``1`` denotes an occupied cell.
        self.board: np.ndarray = np.zeros((size, size), dtype=int)

    def can_place(self, mask: np.ndarray, top_left: Tuple[int, int]) -> bool:
        """Check if ``mask`` can be placed at ``top_left`` without overlap."""
        r, c = top_left
        h, w = mask.shape
        if r < 0 or c < 0 or r + h > self.size or c + w > self.size:
            return False
        mask_bool = mask.astype(bool)
        board_slice = self.board[r : r + h, c : c + w]
        return np.all(board_slice[mask_bool] == 0)

    def place_mask(self, mask: np.ndarray, top_left: Tuple[int, int]) -> bool:
        """Place ``mask`` on the board at ``top_left`` if space is available."""
        if not self.can_place(mask, top_left):
            return False
        r, c = top_left
        h, w = mask.shape
        mask_bool = mask.astype(bool)
        self.board[r : r + h, c : c + w][mask_bool] = 1
        return True

    def remove_mask(self, mask: np.ndarray, top_left: Tuple[int, int]) -> None:
        """Remove ``mask`` from the board at ``top_left``."""
        r, c = top_left
        h, w = mask.shape
        mask_bool = mask.astype(bool)
        self.board[r : r + h, c : c + w][mask_bool] = 0

    def reset(self) -> None:
        """Reset the board to all zeros."""
        self.board.fill(0)

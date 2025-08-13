import numpy as np
import random
from typing import List, Tuple, Dict, Any


class BlockPuzzleEnv:
    """Simple 8x8 block puzzle environment without any GUI.

    The environment keeps an 8x8 board and a set of block shapes.  Three
    random shapes are sampled at a time.  An action is a tuple of
    ``(shape_index, row, col)`` describing which of the current shapes to
    place and the top-left position where it should be placed.

    The :meth:`step` method returns ``(next_state, reward, done, info)`` so
    the environment can easily be used by learning agents.
    """

    def __init__(self, board_size: int = 8):
        self.board_size = board_size
        self.shapes: List[np.ndarray] = [
            np.array([[1]]),
            np.array([[1, 1], [1, 1]]),
            np.array([[1, 1, 1]]),
            np.array([[1], [1], [1]]),
            np.array([[1, 1, 1, 1]]),
            np.array([[1], [1], [1], [1]]),
        ]
        self.current_shapes: List[np.ndarray] = []
        self.board: np.ndarray = np.zeros((self.board_size, self.board_size), dtype=int)
        self.reset()

    # ------------------------------------------------------------------
    def reset(self) -> np.ndarray:
        """Reset the game board and sample a new set of shapes."""
        self.board = np.zeros((self.board_size, self.board_size), dtype=int)
        self.current_shapes = self._sample_shapes()
        return self.board.copy()

    # ------------------------------------------------------------------
    def _sample_shapes(self) -> List[np.ndarray]:
        return random.sample(self.shapes, 3)

    # ------------------------------------------------------------------
    def valid_actions(self) -> List[Tuple[int, int, int]]:
        """Return all valid actions for the current board and shapes."""
        actions: List[Tuple[int, int, int]] = []
        for idx, shape in enumerate(self.current_shapes):
            h, w = shape.shape
            for r in range(self.board_size - h + 1):
                for c in range(self.board_size - w + 1):
                    region = self.board[r : r + h, c : c + w]
                    if np.all(region == 0):
                        actions.append((idx, r, c))
        return actions

    # ------------------------------------------------------------------
    def _can_place(self, shape: np.ndarray, r: int, c: int) -> bool:
        h, w = shape.shape
        if r < 0 or c < 0 or r + h > self.board_size or c + w > self.board_size:
            return False
        region = self.board[r : r + h, c : c + w]
        return np.all(region == 0)

    # ------------------------------------------------------------------
    def step(self, action: Tuple[int, int, int]) -> Tuple[np.ndarray, int, bool, Dict[str, Any]]:
        """Place a shape on the board.

        Parameters
        ----------
        action : tuple
            ``(shape_index, row, col)`` identifying which shape to place and
            where to place it.
        """
        shape_idx, r, c = action
        shape = self.current_shapes[shape_idx]
        if not self._can_place(shape, r, c):
            raise ValueError("Invalid action")

        h, w = shape.shape
        self.board[r : r + h, c : c + w] += shape

        full_rows = [i for i in range(self.board_size) if np.all(self.board[i] == 1)]
        full_cols = [j for j in range(self.board_size) if np.all(self.board[:, j] == 1)]
        cleared = 0
        for row in full_rows:
            self.board[row, :] = 0
            cleared += self.board_size
        for col in full_cols:
            self.board[:, col] = 0
            cleared += self.board_size
        reward = cleared

        # Remove the used shape and resample if necessary
        del self.current_shapes[shape_idx]
        if not self.current_shapes:
            self.current_shapes = self._sample_shapes()

        done = len(self.valid_actions()) == 0
        info = {"rows_cleared": len(full_rows), "cols_cleared": len(full_cols)}
        return self.board.copy(), reward, done, info

    # ------------------------------------------------------------------
    def render(self) -> None:
        """Print the current board to the console."""
        chars = {0: ".", 1: "#"}
        for row in self.board:
            print("".join(chars[val] for val in row))
        print()

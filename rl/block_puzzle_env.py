from typing import Tuple, List


class BlockPuzzleEnv:
    """Simple block puzzle environment for reinforcement learning.

    The board is a square grid. Each action selects a cell to place a block.
    Completing a full row or column clears it and yields bonus reward.
    """

    def __init__(self, size: int = 4):
        self.size = size
        self.action_space = size * size
        self.board: List[List[int]] = []
        self.reset()

    def reset(self) -> Tuple[int, ...]:
        """Reset the board to an empty state and return the initial state."""
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        return self._get_state()

    def _get_state(self) -> Tuple[int, ...]:
        """Return a hashable representation of the current board."""
        return tuple(cell for row in self.board for cell in row)

    def available_actions(self) -> List[int]:
        """Return a list of indices for empty cells."""
        actions = []
        for idx in range(self.action_space):
            row, col = divmod(idx, self.size)
            if self.board[row][col] == 0:
                actions.append(idx)
        return actions

    def step(self, action: int) -> Tuple[Tuple[int, ...], int, bool, dict]:
        """Apply the chosen action.

        Args:
            action: index of the cell to fill (0 .. size*size-1).

        Returns:
            state, reward, done, info
        """
        row, col = divmod(action, self.size)
        reward = 0
        done = False

        # Invalid move ends the episode with a penalty
        if self.board[row][col] == 1:
            reward = -1
            done = True
            return self._get_state(), reward, done, {}

        # Place block
        self.board[row][col] = 1
        reward = 1

        # Check for completed rows/columns
        lines_cleared = 0
        full_rows = [r for r in range(self.size) if all(self.board[r][c] == 1 for c in range(self.size))]
        full_cols = [c for c in range(self.size) if all(self.board[r][c] == 1 for r in range(self.size))]

        for r in full_rows:
            for c in range(self.size):
                self.board[r][c] = 0
            lines_cleared += 1
        for c in full_cols:
            for r in range(self.size):
                self.board[r][c] = 0
            lines_cleared += 1

        reward += 10 * lines_cleared

        # Episode ends when no empty cells remain
        if not self.available_actions():
            done = True

        return self._get_state(), reward, done, {}

    def render(self) -> None:
        """Print the current board."""
        for row in self.board:
            print(" ".join(str(cell) for cell in row))

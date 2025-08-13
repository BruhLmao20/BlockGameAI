from typing import List, Tuple


class BlockGame:
    """Simple clearing puzzle environment using plain Python lists."""

    def __init__(self, size: int = 8):
        self.size = size
        self.board = [[0 for _ in range(size)] for _ in range(size)]

    def reset(self) -> List[List[int]]:
        for r in range(self.size):
            for c in range(self.size):
                self.board[r][c] = 0
        return [row[:] for row in self.board]

    # --- Helpers -----------------------------------------------------
    def _clear_lines(self, board: List[List[int]]) -> Tuple[List[List[int]], int]:
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

    def _count_gaps(self, board: List[List[int]]) -> int:
        gaps = 0
        for c in range(self.size):
            filled_seen = False
            for r in range(self.size):
                if board[r][c] == 1:
                    filled_seen = True
                elif filled_seen:
                    gaps += 1
        return gaps

    # --- API ---------------------------------------------------------
    def valid_actions(self) -> List[Tuple[int, int]]:
        actions = []
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == 0:
                    actions.append((r, c))
        return actions

    def step(self, action: Tuple[int, int]) -> Tuple[List[List[int]], int, bool]:
        r, c = action
        if self.board[r][c] != 0:
            raise ValueError("Invalid action: cell is already filled")
        self.board[r][c] = 1
        self.board, cleared = self._clear_lines(self.board)
        done = len(self.valid_actions()) == 0
        return [row[:] for row in self.board], int(cleared), done

    def render(self) -> None:
        for row in self.board:
            print(" ".join(str(cell) for cell in row))

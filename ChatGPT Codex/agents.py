import random
from typing import Tuple
from block_env import BlockGame


class RandomAgent:
    """Agent that selects actions uniformly at random."""

    def select_action(self, env: BlockGame) -> Tuple[int, int]:
        actions = env.valid_actions()
        return random.choice(actions)


class GreedyAgent:
    """Agent that evaluates actions with simple heuristics."""

    def select_action(self, env: BlockGame) -> Tuple[int, int]:
        best_score = None
        best_action = None
        for action in env.valid_actions():
            score = self._evaluate(env, action)
            if best_score is None or score > best_score:
                best_score = score
                best_action = action
        # Fallback in case no action evaluated (e.g., board full)
        return best_action if best_action is not None else random.choice(env.valid_actions())

    def _evaluate(self, env: BlockGame, action: Tuple[int, int]) -> float:
        # Simulate placing the block
        board_copy = [row[:] for row in env.board]
        r, c = action
        board_copy[r][c] = 1
        board_copy, cleared = env._clear_lines(board_copy)
        gaps = env._count_gaps(board_copy)
        # Higher score for more cleared cells, lower for gaps
        return cleared * 10 - gaps

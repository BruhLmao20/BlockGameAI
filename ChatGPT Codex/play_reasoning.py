from typing import List, Tuple

from env.block_puzzle import BlockPuzzleEnv


class ReasoningGreedyAgent:
    """Heuristic agent that also reports its reasoning."""

    def select_action_with_reason(
        self, env: BlockPuzzleEnv
    ) -> Tuple[Tuple[int, int], str]:
        best_action, best_score, best_reason = None, None, ""
        for action in env.valid_actions():
            # Simulate the action
            board_copy = [row[:] for row in env.board]
            r, c = action
            board_copy[r][c] = 1
            board_copy, cleared = env._clear_lines(board_copy)
            gaps = env._count_gaps(board_copy)

            score = cleared * 10 - gaps
            reason = (
                f"clears {cleared} cells, leaves {gaps} gaps ⇒ heuristic score {score}"
            )

            if best_score is None or score > best_score:
                best_action, best_score, best_reason = action, score, reason

        return best_action, best_reason


def print_board(board: List[List[int]]) -> None:
    for row in board:
        print(" ".join(str(cell) for cell in row))
    print()


def run_episode(size: int = 8, max_steps: int = 1000):  # int = 100
    """Play one episode using the reasoning agent.

    The original implementation would continue forever because clearing a
    complete row or column makes new actions available again. To keep example
    runs short and avoid the need to interrupt manually, we cap the number of
    steps with ``max_steps``.
    """

    env = BlockPuzzleEnv(size=size)
    agent = ReasoningGreedyAgent()

    board = env.reset()
    print("Initial board:")
    print_board(board)

    done, step = False, 0
    while not done and step < max_steps:
        action, reason = agent.select_action_with_reason(env)
        print(f"Step {step}: placing at {action} because {reason}")
        board, reward, done = env.step(action)
        print_board(board)
        step += 1

    if done:
        print("Game over – no legal moves remain.")
    else:
        print(f"Reached step limit of {max_steps}; stopping.")


if __name__ == "__main__":
    run_episode()

"""Run baseline or reasoning agents against the block puzzle environment."""
import argparse
import time
from typing import Tuple, List, Optional

from agents import RandomAgent, GreedyAgent
from block_env import BlockGame


class ReasoningGreedyAgent:
    """Greedy agent that explains its heuristic decisions."""

    def select_action_with_reason(
        self, env: BlockGame
    ) -> Tuple[Tuple[int, int], str]:
        best_action, best_score, best_reason = None, None, ""
        for action in env.valid_actions():
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


def print_board(board: List[List[int]], highlight: Optional[Tuple[int, int]] = None) -> None:
    """Print the board, highlighting the last move in yellow."""
    for r, row in enumerate(board):
        rendered = []
        for c, cell in enumerate(row):
            if highlight == (r, c):
                rendered.append(f"\033[93m{cell}\033[0m")
            else:
                rendered.append(str(cell))
        print(" ".join(rendered))
    print()


def run_game(
    agent_name: str, size: int, max_steps: int = 1000, delay: float = 0.3
) -> None:
    env = BlockGame(size=size)
    board = env.reset()

    if agent_name == "greedy":
        agent = GreedyAgent()
        reasoning = False
    elif agent_name == "reasoning":
        agent = ReasoningGreedyAgent()
        reasoning = True
        print("Initial board:")
        print_board(board)
    else:
        agent = RandomAgent()
        reasoning = False

    total_reward = 0
    done = False
    steps = 0
    while not done and steps < max_steps:
        if reasoning:
            action, reason = agent.select_action_with_reason(env)
            print(f"Step {steps}: placing at {action} because {reason}")
        else:
            action = agent.select_action(env)
        board, reward, done = env.step(action)
        total_reward += reward
        steps += 1
        if reasoning:
            print_board(board, highlight=action)
            time.sleep(delay)
    if not done:
        print("Reached step limit; terminating game early.")

    print(f"Agent: {agent_name}, board size: {size}")
    env.render()
    print(f"Final score: {total_reward}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--agent", choices=["random", "greedy", "reasoning"], default="random"
    )
    parser.add_argument("--size", type=int, default=8, help="board size")
    parser.add_argument(
        "--delay",
        type=float,
        default=0.3,
        help="seconds to pause between moves for reasoning agent",
    )
    args = parser.parse_args()
    run_game(args.agent, args.size, delay=args.delay)


if __name__ == "__main__":
    main()

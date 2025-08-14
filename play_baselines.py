#<<<<<<< codex/add-q-learning-to-agent-l15ip9
"""Run baseline or reasoning agents against the block puzzle environment."""
#=======
from pygame.time import delay

from play_reasoning import ReasoningGreedyAgent, print_board

"""Run baseline agents against the block puzzle environment.

Example:
    python play_baselines.py --agent greedy --size 8 --max-steps 5000
"""
#>>>>>>> main
import argparse
import time
from typing import Tuple, List, Optional

from agents import RandomAgent, GreedyAgent
from block_env import BlockGame


def run_game(agent_name: str, size: int, max_steps: int) -> None:
#>>>>>>> main
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
#<<<<<<< HEAD
    parser.add_argument("--max-steps", type=int, default=8500, help="maximum steps per game") #default=10000
#=======
#<<<<<<< codex/add-q-learning-to-agent-l15ip9
    parser.add_argument(
        "--delay",
        type=float,
        default=0.3,
        help="seconds to pause between moves for reasoning agent",
    )
    args = parser.parse_args()
    run_game(args.agent, args.size, delay=args.delay)
#=======
    parser.add_argument("--max-steps", type=int, default=1000, help="maximum steps per game")
#>>>>>>> 3a05d83fa40c1771fb62453ee1cf911c3b205437
    args = parser.parse_args()
    run_game(args.agent, args.size, args.max_steps)
#>>>>>>> main


if __name__ == "__main__":
    main()

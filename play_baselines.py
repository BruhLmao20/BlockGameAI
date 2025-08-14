"""Run baseline agents against the block puzzle environment.

Example:
    python play_baselines.py --agent greedy --size 8 --max-steps 5000
"""
import argparse
from agents import RandomAgent, GreedyAgent
from block_env import BlockGame


def run_game(agent_name: str, size: int, max_steps: int) -> None:
    env = BlockGame(size=size)
    env.reset()
    if agent_name == "greedy":
        agent = GreedyAgent()
    else:
        agent = RandomAgent()

    total_reward = 0
    done = False
    steps = 0
    while not done and steps < max_steps:
        action = agent.select_action(env)
        _, reward, done = env.step(action)
        total_reward += reward
        steps += 1
    if not done:
        print("Reached step limit; terminating game early.")

    print(f"Agent: {agent_name}, board size: {size}")
    env.render()
    print(f"Final score: {total_reward}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent", choices=["random", "greedy"], default="random")
    parser.add_argument("--size", type=int, default=8, help="board size")
    parser.add_argument("--max-steps", type=int, default=8500, help="maximum steps per game") #default=10000
    args = parser.parse_args()
    run_game(args.agent, args.size, args.max_steps)


if __name__ == "__main__":
    main()

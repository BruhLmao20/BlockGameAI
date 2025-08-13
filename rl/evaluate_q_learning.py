import os
import pickle

from block_puzzle_env import BlockPuzzleEnv

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "q_table.pkl")


def load_model(path=MODEL_PATH):
    with open(path, "rb") as f:
        return pickle.load(f)


def choose_action(q_table, state, env):
    if state not in q_table:
        return env.available_actions()[0]
    return max(q_table[state], key=q_table[state].get)


def evaluate(episodes: int = 10):
    env = BlockPuzzleEnv()
    q_table = load_model()
    total_reward = 0

    for _ in range(episodes):
        state = env.reset()
        done = False
        steps = 0
        while not done and steps < 100:
            action = choose_action(q_table, state, env)
            state, reward, done, _ = env.step(action)
            total_reward += reward
            steps += 1

    avg_reward = total_reward / episodes
    print(f"Average reward over {episodes} episodes: {avg_reward}")


if __name__ == "__main__":
    evaluate()

import argparse
import os
import pickle
import random

from env.block_puzzle import BlockPuzzleEnv

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "q_table.pkl")


def choose_action(q_table, state, env, epsilon):
    if state not in q_table or not q_table[state] or random.random() < epsilon:
        return random.choice(env.available_actions())
    return max(q_table[state], key=q_table[state].get)


def train(episodes: int = 500, alpha: float = 0.1, gamma: float = 0.95, epsilon: float = 0.1):
    env = BlockPuzzleEnv()
    q_table = {}

    for _ in range(episodes):
        state = env.reset()
        done = False
        steps = 0

        while not done and steps < 100:
            action = choose_action(q_table, state, env, epsilon)
            next_state, reward, done, _ = env.step(action)

            q_table.setdefault(state, {})
            q_table.setdefault(next_state, {})
            best_next = max(q_table[next_state].values()) if q_table[next_state] else 0.0
            old_value = q_table[state].get(action, 0.0)
            q_table[state][action] = old_value + alpha * (reward + gamma * best_next - old_value)
            state = next_state
            steps += 1

    os.makedirs(os.path.join(os.path.dirname(__file__), "..", "models"), exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(dict(q_table), f)
    print(f"Saved model to {MODEL_PATH}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--episodes", type=int, default=100, help="Number of training episodes")
    args = parser.parse_args()
    train(episodes=args.episodes)

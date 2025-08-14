import importlib.util
import sys
from pathlib import Path


def load_module(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(
        name, Path(__file__).resolve().parents[1] / relative
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module

block_env = load_module("block_env", "ChatGPT Codex/block_env.py")
sys.modules["block_env"] = block_env
agents = load_module("agents", "ChatGPT Codex/agents.py")

BlockGame = block_env.BlockGame
RandomAgent = agents.RandomAgent
GreedyAgent = agents.GreedyAgent


def test_random_agent_selects_valid_action():
    env = BlockGame(size=4)
    agent = RandomAgent()
    valid = env.valid_actions()
    for _ in range(5):
        action = agent.select_action(env)
        assert action in valid


def test_greedy_agent_prefers_clearing_move():
    env = BlockGame(size=4)
    env.board[0] = [1, 1, 1, 0]
    agent = GreedyAgent()
    action = agent.select_action(env)
    assert action == (0, 3)

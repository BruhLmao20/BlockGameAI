import importlib.util
from pathlib import Path


def load_module(name: str, relative: str):
    """Utility to load a module from a file path."""
    spec = importlib.util.spec_from_file_location(
        name, Path(__file__).resolve().parents[1] / relative
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module

block_env = load_module("block_env", "ChatGPT Codex/block_env.py")
BlockGame = block_env.BlockGame


def test_clear_lines():
    env = BlockGame(size=4)
    # Fill first two rows completely
    env.board[0] = [1, 1, 1, 1]
    env.board[1] = [1, 1, 1, 1]
    board_after, cleared = env._clear_lines([row[:] for row in env.board])
    assert cleared == 8
    assert all(all(cell == 0 for cell in row) for row in board_after)


def test_count_gaps():
    env = BlockGame(size=4)
    # Create gaps below filled cells in first column
    env.board[0][0] = 1
    env.board[2][0] = 1
    gaps = env._count_gaps(env.board)
    assert gaps == 2

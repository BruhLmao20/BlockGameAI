from __future__ import annotations

import random
import statistics
from typing import Dict, List, Optional


class Agent:
    """Simple agent interface used for evaluation.

    Each agent must implement :meth:`play_episode` returning a dictionary of
    metrics for a single episode. At minimum ``score`` and ``lines_cleared``
    keys are expected. This light‑weight interface keeps the evaluation script
    independent from the specific agent implementations used by the project.
    """

    def play_episode(self) -> Dict[str, float]:
        raise NotImplementedError


def evaluate_agents(agents: List[Agent], episodes: int = 10, *, plot: bool = True) -> Dict[str, Dict[str, List[float]]]:
    """Run multiple episodes for each agent and collect metrics.

    Parameters
    ----------
    agents:
        Sequence of agents to evaluate.
    episodes:
        Number of episodes each agent will play.
    plot:
        When ``True`` an attempt will be made to plot episode scores using
        :mod:`matplotlib`. If the library is unavailable the evaluation
        continues without plotting.
    """

    results: Dict[str, Dict[str, List[float]]] = {}

    for agent in agents:
        name = agent.__class__.__name__
        scores: List[float] = []
        lines: List[float] = []
        for _ in range(episodes):
            metrics = agent.play_episode()
            scores.append(metrics.get("score", 0.0))
            lines.append(metrics.get("lines_cleared", 0.0))
        avg_score = statistics.mean(scores) if scores else 0.0
        avg_lines = statistics.mean(lines) if lines else 0.0
        results[name] = {
            "scores": scores,
            "lines_cleared": lines,
            "avg_score": [avg_score],
            "avg_lines_cleared": [avg_lines],
        }
        print(f"Agent {name}: Avg Score {avg_score:.2f}, Avg Lines {avg_lines:.2f}")

    if plot:
        try:
            import matplotlib.pyplot as plt  # type: ignore
        except Exception as exc:  # pragma: no cover - optional dependency
            print("Matplotlib not available, skipping plots:", exc)
        else:  # pragma: no branch - plotting is optional
            for name, data in results.items():
                plt.plot(data["scores"], label=name)
            plt.xlabel("Episode")
            plt.ylabel("Score")
            plt.title("Scores per Episode")
            plt.legend()
            plt.show()

    return results


class RandomAgent(Agent):
    """Very small demonstration agent returning random metrics."""

    def __init__(self, score_range: Optional[tuple[int, int]] = None,
                 line_range: Optional[tuple[int, int]] = None) -> None:
        self.score_range = score_range or (0, 100)
        self.line_range = line_range or (0, 10)

    def play_episode(self) -> Dict[str, float]:
        score = float(random.randint(*self.score_range))
        lines = float(random.randint(*self.line_range))
        return {"score": score, "lines_cleared": lines}


if __name__ == "__main__":
    # Run a small demonstration when executed directly.
    demo_agents = [RandomAgent(), RandomAgent()]
    evaluate_agents(demo_agents, episodes=5, plot=False)

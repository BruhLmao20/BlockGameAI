# BlockGameAI

#BlockGameAI is a collection of tools for experimenting with a grid-based block puzzle game. It bundles a basic simulator, GUI demos, and reinforcement learning experiments.

## Project overview
- `game-sim/` – early simulation utilities for board mechanics.
- `testing/` – Tkinter demo for manually interacting with the board.
- `rl/` – Q-learning environment, training, and evaluation scripts.
- `ChatGPT Codex/` – experimental agents and evaluation helpers.

## Dependencies
The project targets **Python 3.9+** and relies on a few external libraries:

| Purpose | Packages |
|---------|----------|
| Core mechanics | `numpy` |
| GUI and demos | `tkinter` (bundled with Python), `pyautogui`, `opencv-python`, `keyboard` |
| Optional plotting | `matplotlib` |

## Setup
```bash
git clone <repo-url>
cd BlockGameAI
python -m venv .venv
source .venv/bin/activate
pip install numpy pyautogui opencv-python keyboard matplotlib
```

## Running demos and training
- **Tkinter demo:** `python testing/run.py`
- **Basic simulator:** `python game-sim/sim.py`
- **Train Q-learning agent:** `python rl/train_q_learning.py --episodes 500`
- **Evaluate trained agent:** `python rl/evaluate_q_learning.py`

Trained models are saved to `models/q_table.pkl`.

## Experiments and research notes
Further exploration scripts live in [`ChatGPT Codex/`](ChatGPT%20Codex/) and text notes in [`text_files/`](text_files/). These directories can be used as starting points for custom experiments or research notebooks.
=======
This project provides AI agents and tools for playing and analyzing block-based puzzles.

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Refer to the source code and scripts within the repository for examples on running simulations and experiments.
# main

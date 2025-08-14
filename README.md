# BlockGameAI

This repository contains experimentation for a block puzzle game. The main playable example lives in `game-sim/xonclick.py` and shows a grid where cells can be toggled.

## Running the Demo

The easiest way to start the demo is:

```bash
python3 game-sim/xonclick.py
```

When the script launches it shows a brief popup via `show_instructions()` explaining the basic controls. After closing the popup, an 8×8 board appears where you can click to place or remove blocks.

### Requirements

- Python 3
- `tkinter` (usually included with Python)
- `numpy`

Install missing packages with `pip install numpy`.

## Repository Layout

- **game-sim** – runnable scripts and experiments such as `xonclick.py`.
- **helpers** – small utility modules used by the game code.
- **res**, **pics**, **text_files** – assorted resources and notes.
- **test-field** and **testing** – scripts used for development and testing.



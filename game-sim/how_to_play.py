import tkinter as tk
from tkinter import messagebox


def show_instructions():
    """Display basic instructions for the puzzle game."""
    instructions = (
        "Block Puzzle Game Rules:\n"
        "- The board is an 8x8 grid.\n"
        "- Click any cell to toggle a block on or off.\n"
        "- Completing a full row or column clears it and grants points.\n"
        "- Clearing multiple lines at once grants bonus points.\n"
        "- Clearing the entire board awards a big bonus."
    )
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showinfo("How to Play", instructions)
    root.destroy()


if __name__ == "__main__":
    show_instructions()

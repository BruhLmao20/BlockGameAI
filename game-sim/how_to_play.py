import tkinter as tk
from tkinter import messagebox


def show_instructions():
    """Display a simple message box explaining how to play the puzzle."""
    instructions = (
        "Block Puzzle Game Rules:\n"
        "- The board is an 8x8 grid.\n"
        "- Select or click cells to place blocks.\n"
        "- Filling an entire row or column clears it and grants points.\n"
        "- Clearing multiple lines at once gives bonus points.\n"
        "- Clearing the whole board awards a large bonus.\n"
        "Use the provided buttons in the prototype to toggle tiles."
    )
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showinfo("How to Play", instructions)
    root.destroy()


if __name__ == "__main__":
    show_instructions()


# make the game physics only with creating a 2d array and filling it with shapes with every turn
# then check that if the array vertical or horizontal checks

from tkinter import messagebox
import numpy as np
import tkinter as tk
import random

# Step 1: Define the game board
game_board = np.zeros((8, 8), dtype=int)
print(game_board)

# def button_pressed(row, column):
#     game_board[row][column] = 1

def on_button_click(row, col):
    # Update the game board and button text when a button is clicked
    if game_board[row][col] == 0:
        game_board[row][col] = 1
        board_buttons[row][col].config(text="X")

def main():
    global game_board, board_buttons
    # global board_size, game_board, board_buttons, random_shapes, shape_buttons

    board_size = 8

    # Create a list to store the buttons representing the game board
    board_buttons = []

    # Create a 2D list to represent the game board
    game_board = [[0] * board_size for _ in range(board_size)]

    # Create a Tkinter window
    window = tk.Tk()
    window.title("Block Puzzle Game")

    # Create the game board GUI
    for row in range(board_size):
        button_row = []
        for col in range(board_size):
            # Create a button for each cell in the game board
            button = tk.Button(window, text="", width=2, height=1, command=lambda r=row, c=col: on_button_click(r, c))
            button.grid(row=row, column=col, padx=2, pady=2)
            button_row.append(button)
        board_buttons.append(button_row)

    # Create a frame to hold the shape buttons
    shape_frame = tk.Frame(window)
    shape_frame.grid(row=board_size, column=0, columnspan=board_size)

    # Create the shape buttons and add drag-and-drop functionality
    shape_buttons = []
    for i, shape in enumerate(random_shapes):
        shape_button = tk.Button(shape_frame, text=f"Shape {i + 1}")
        shape_button.grid(row=0, column=i, padx=2, pady=2)
        shape_buttons.append(shape_button)

    print(board_buttons)

    # Start the Tkinter event loop
    window.mainloop()

    if __name__ == "__main__":
        main()

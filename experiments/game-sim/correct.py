# the correct functioning program to be transferred here
# TRANSFER CODE FROM test1
# CODE FUNCTIONALITY SO FAR
#   - code can create the board
#   - code can insert whether the button was pressed and sends it to the game_board array
import numpy as np
import tkinter as tk
import os
import time

# Step 1: Define the game board
game_board = np.zeros((8, 8), dtype=int)


# Text and Help Function ====================
def print_2d_array(array):
    for row in array:
        for element in row:
            print(element, end=' ')
        print()


def print_space():
    print("=" * 20)  # Repeat "=" 20 times


def extra_space():
    print_space()
    print_space()
    print_space()


# Game Physics Functions ====================
def on_button_click_true(row, col):
    # Update the game board and button text when a button is clicked
    if game_board[row][col] == 0:
        game_board[row][col] = 1
        board_buttons[row][col].config(text="X")
        extra_space()
        print_2d_array(game_board)


def on_button_click_false(row, col):
    # Update the game board and button text when a button is clicked
    if game_board[row][col] == 1:
        game_board[row][col] = 0
        board_buttons[row][col].config(text="")
        extra_space()
        print_2d_array(game_board)

# Next Functions
#   - Once 8 line is created, clear line, and award points
#   -


def main():
    global game_board, board_buttons

    # Define the dimensions of the game board
    board_size = 8

    # print(game_board)

    # Create a 2D list to represent the game board
    game_board = [[0] * board_size for _ in range(board_size)]

    # Create a Tkinter window
    window = tk.Tk()
    window.title("Block Puzzle Game")

    # Create a list to store the buttons representing the game board
    board_buttons = []

    # Create the game board GUI
    for row in range(board_size):
        button_row = []
        for col in range(board_size):
            # Create a button for each cell in the game board
            button = tk.Button(window, text="", width=2, height=1,
                               command=lambda r=row, c=col: on_button_click_true(r, c))
            # button = tk.Button(window, text="", width=2, height=1,
            #                    command=lambda r=row, c=col: on_button_click_false(r, c))
            button.grid(row=row, column=col, padx=2, pady=2)
            button_row.append(button)
        board_buttons.append(button_row)

    # Create a frame to hold the shape buttons
    shape_frame = tk.Frame(window)
    shape_frame.grid(row=board_size, column=0, columnspan=board_size)

    window.mainloop()


if __name__ == "__main__":
    # print(game_board)
    main()

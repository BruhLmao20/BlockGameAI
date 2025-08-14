# the correct functioning program to be transferred here
# TRANSFER CODE FROM test1
# CODE FUNCTIONALITY SO FAR
#   - code can create the board
#   - code can insert whether the button was pressed and sends it to the game_board array
import numpy as np
import tkinter as tk
import testing_functions
from helpers import extra_space, print_2d_array, print_board
import os
import time

# Step 1: Define the game board
game_board = np.zeros((8, 8), dtype=int)

total_points = 0


# XONCLICK: MAIN CLICKING FUNCTION
def toggle_button_state(row, col):
    global total_points  # Declare 'points' as a global variable to modify it within the function
    button = board_buttons[row][col]
    current_state = button.cget("text")
    if current_state == "":
        button.config(text="X")
        game_board[row][col] = 1
        # total_points += 1  # add this points system to the testing_functions system
        # total_points += 1 + testing_functions.total_points_system(game_board)
        testing_functions.total_logic(game_board)
        testing_functions.print_points(game_board)
        print_board(game_board)
        # CLEAR COMMENTS IN NEXT COMMIT 5-26-23
        # extra_space()
        # print_2d_array(game_board)
    else:
        button.config(text="")  # use this on a function to clear the board
        game_board[row][col] = 0
        testing_functions.print_points(game_board)
        print_board(game_board)
        # CLEAR COMMENTS IN NEXT COMMIT 5-26-23
        # print_board(game_board) combines the functions below into 1
        # - extra_space()
        # - print_2d_array(game_board)



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


# WHAT VARIABLES DO WHAT?
# - game_board:

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
                               command=lambda r=row, c=col: toggle_button_state(r, c))
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

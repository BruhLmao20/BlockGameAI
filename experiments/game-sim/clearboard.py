# the correct functioning program to be transferred here
# TRANSFER CODE FROM test1
# CODE FUNCTIONALITY SO FAR
#   - code can create the board
#   - code can insert whether the button was pressed and sends it to the game_board array
import numpy as np
import tkinter as tk
import testing_functions
from helpers import *
import os
import time

# Step 1: Define the game board
game_board = np.zeros((8, 8), dtype=int)

total_points = 0
is_running = True


# CLEARBOARD: MAIN CLICKING FUNCTION

# runs the gui so that once an update is needed to change, it can be running and updated through here
def run_GUI(array):
    while is_running:
        # make the GUI a function
        # then can add update functions to that function that will allow for x's to change



def check_clear_rows(board_buttons):
    global game_board

    rows_to_clear = []
    for row in range(len(game_board)):
        if all(cell == 1 for cell in game_board[row]):
            rows_to_clear.append(row)

    for row in rows_to_clear:
        for col in range(len(game_board[row])):
            button = board_buttons[row][col]
            button.config(text="")
            game_board[row][col] = 0


def check_clear_columns(board_buttons):
    global game_board

    cols_to_clear = []
    for col in range(len(game_board[0])):
        if all(game_board[row][col] == 1 for row in range(len(game_board))):
            cols_to_clear.append(col)

    for col in cols_to_clear:
        for row in range(len(game_board)):
            button = board_buttons[row][col]
            button.config(text="")
            game_board[row][col] = 0


def button_click(row, col, board_buttons):
    toggle_button_state(row, col)
    check_clear_rows(board_buttons)
    check_clear_columns(board_buttons)


def toggle_button_state(row, col):
    global total_points, game_board, board_buttons

    button = board_buttons[row][col]
    current_state = button.cget("text")

    # MAYBE RUN A WHILE LOOP AND IF THE BUTTON IS FULLL THEN IT CAN JUMP TO FULL THEN CAN CLEAR AFTER THAT
    if current_state == "":
        button.config(text="X")
        game_board[row][col] = 1
        testing_functions.total_logic(game_board)
        print_board(game_board)
    else:
        button.config(text="")
        game_board[row][col] = 0
        print_board(game_board)

    check_clear_rows(board_buttons)
    check_clear_columns(board_buttons)


# def check_clear_rows():
#     global game_board, board_buttons
#
#     rows_to_clear = []
#     for row in range(len(game_board)):
#         if all(cell == 1 for cell in game_board[row]):
#             rows_to_clear.append(row)
#
#     for row in rows_to_clear:
#         for col in range(len(game_board[row])):
#             button = board_buttons[row][col]
#             button.config(text="")
#             game_board[row][col] = 0
#
#
# def check_clear_columns():
#     global game_board, board_buttons
#
#     cols_to_clear = []
#     for col in range(len(game_board[0])):
#         if all(game_board[row][col] == 1 for row in range(len(game_board))):
#             cols_to_clear.append(col)
#
#     for col in cols_to_clear:
#         for row in range(len(game_board)):
#             button = board_buttons[row][col]
#             button.config(text="")
#             game_board[row][col] = 0
#
#
# def button_click(row, col):
#     toggle_button_state(row, col)
#     check_clear_rows()
#     check_clear_columns()


# clear x's on buttons
# def reset_button(button):


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


def print_board(game_board):
    extra_space()
    testing_functions.print_points(game_board)
    print_2d_array(game_board)


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
    # NEED TO CREATE AN UPDATE FUNCTION THAT UPDATES THIS
    for row in range(board_size):
        button_row = []
        for col in range(board_size):
            # Create a button for each cell in the game board
            button = tk.Button(window, text="", width=2, height=1,
                               command=lambda r=row, c=col: button_click(r, c, board_buttons))
            button.grid(row=row, column=col, padx=2, pady=2)
            button_row.append(button)
        board_buttons.append(button_row)

    # Create a frame to hold the shape buttons
    shape_frame = tk.Frame(window)
    shape_frame.grid(row=board_size, column=0, columnspan=board_size)

    # print(board_buttons)
    # print(button_row)
    print_2d_array(board_buttons)
    # print_2d_array(button_row)

    window.mainloop()


if __name__ == "__main__":
    # print(game_board)
    main()

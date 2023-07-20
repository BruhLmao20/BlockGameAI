import numpy as np
import tkinter as tk
import os
import time

# Step 1: Define the game board
game_board = np.zeros((8, 8), dtype=int)

global total_points
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
        total_logic(button, game_board)
        points_awarded(game_board, total_points)
        print_board(game_board)
        # CLEAR COMMENTS IN NEXT COMMIT 5-26-23
        # extra_space()
        # print_2d_array(game_board)
    else:
        button.config(text="")  # use this on a function to clear the board
        game_board[row][col] = 0
        print_board(game_board)
        # CLEAR COMMENTS IN NEXT COMMIT 5-26-23
        # print_board(game_board) combines the functions below into 1
        # - extra_space()
        # - print_2d_array(game_board)


# ========== testing_functions ==========
def total_logic(button, array):
    any_line_checker(array)  # boolean, if true, then
    # total_points_system(array)
    clear_lines(array)
    reset_button(button, game_board)

def clear_lines(array):
    clear_row(array)
    clear_columns(array)
    # total_points_system(array)


def total_points_system(array):  # ran in the clear function
    if row_full_boolean(array) or columns_full_boolean(array):
        all_points = points_awarded(array, total_points)
        print_points(array)
        return all_points
    else:
        total_points += 1
        return total_points


def points_awarded(array, total_points):
    total_points += points_multiplier(any_line_checker(array))
    return total_points


def print_points(array):
    current_points = 1
    current_points += points_multiplier(any_line_checker(array))

    print('Points: ' + str(current_points))


def any_line_checker(array):
    number_of_lines = 0
    if row_full_boolean(array) or columns_full_boolean(array):
        number_of_lines += len(is_row_full(array)) + len(is_columns_full(array))
        return number_of_lines  # returns into so that points may be awarded


# then award points and clear lines


# check if line is true
def row_full_boolean(array):
    for row in array:  # row is == to i
        if all(element == 1 for element in row):
            return True
    return False


def columns_full_boolean(array):
    for columns in array:
        if all(element == 1 for element in columns):
            return True
    return False


# ACTUAL NUMBER OF ROWS AND COLUMNS THAT ARE FULL
def is_row_full(array):
    row_location = []
    for row in array:  # row is == to i
        if all(element == 1 for element in row):
            row_location.append(row)
    return row_location


# return how many rows are full and where they are positions in the 2d array


def is_columns_full(array):
    col_location = []
    for col in array:  # row is == to i
        if all(element == 1 for element in col):
            col_location.append(col)
    return col_location


# return how many columns are full and where they are positions in the 2d array


# FIX BUG
# def clear_row(array):
#     for columns in array:
#         if all(element == 1 for element in columns):


def clear_row(array):
    rows = len(array)
    columns = len(array[0])

    for row in range(rows):
        if all(element == 1 for element in array[row]):
            array[row] = [0] * columns


def clear_columns(array):
    rows = len(array)
    columns = len(array[0])

    for col in range(columns):
        if all(array[row][col] == 1 for row in range(rows)):
            for row in range(rows):
                array[row][col] = 0


def lines_completed(array):
    is_row_full(array)  # returns all the rows that are full
    # use the count of rows to then award to points based on amount of rows completed
    points_awarded = 0
    rows_completed = len(is_row_full(array))
    return rows_completed  # , points_awarded

    # is_columns_full(array)


def points_multiplier(lines):  # number of lines INT, take in anylinechecker
    points_multiplied = 0
    if lines == 1:
        points_multiplied += lines * 10
    elif lines == 2:
        points_multiplied += lines * 15
    elif lines == 3:
        points_multiplied += lines * 20
    elif lines == 4:
        points_multiplied += lines * 25
    elif lines == 5:
        points_multiplied += lines * 30
    return points_multiplied


# ========== testing_functions ==========


# clear x's on buttons
def reset_button(button, array):
    clear_lines(array)
    for row in array:  # row is == to i
        if all(element == 1 for element in row):
            button.config(text="")
    for columns in array:
        if all(element == 1 for element in columns):
            button.config(text="")


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
    print_points(game_board)
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

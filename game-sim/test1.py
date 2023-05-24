from tkinter import messagebox
import numpy as np
import tkinter as tk
import random

# Step 1: Define the game board
game_board = np.zeros((8, 8), dtype=int)

# Step 2: Define the block shapes
# POINTS:
block_shapes1 = [
    np.array([[1]]),  # 1x1 square block
    np.array([[1, 1], [1, 1]]),  # 2x2 square block

    np.array([[1, 1, 1]]),  # Horizontal block of length 3
    np.array([[1], [1], [1]]),  # Vertical block of length 3

    np.array([[1, 1, 1, 1]]),  # Horizontal block of length 4
    np.array([[1], [1], [1], [1]]),  # Vertical block of length 4
    # Add more block shapes as needed

]
# POINTS:
block_shapes2 = [
    np.array([[1, 1, 1, 1]]),           # Horizontal block of length 4
    np.array([[1], [1], [1], [1]]),     # Vertical block of length 4
    np.array([[1, 1], [1, 1]]),         # 2x2 square block
    np.array([[1, 1], [1, 0]]),         # 2x1 (right (r)) square block
    np.array([[1, 1], [0, 1]]),         # 2x1 (left) square block

# POINTS:

    # 2 level size
    np.array([[0, 1, 0], [1, 1, 1]]),   # triangle up

 # POINTS:

    # 3x3 size
    np.array([[1, 1, 1], [0, 0, 1], [0, 0, 1]]),  # BIG r Left
    np.array([[1, 1, 1], [1, 0, 0], [1, 0, 0]]),  # BIG r Right
    np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]),  # BIG 3x3

    # Add more block shapes as needed

]

# Testing: Print the initial game board
# print(game_board)

def on_button_click_true(row, col):
    # Update the game board and button text when a button is clicked
    if game_board[row][col] == 0:
        game_board[row][col] = 1
        board_buttons[row][col].config(text="X")
        print(game_board)

def on_button_click_false(row, col):
    # Update the game board and button text when a button is clicked
    if game_board[row][col] == 1:
        game_board[row][col] = 0
        board_buttons[row][col].config(text="")
        print(game_board)

# def on_shape_press(event, shape_index):
#     # Start dragging the shape when a shape button is pressed
#     shape_button = shape_buttons[shape_index]
#     shape_button.start_dragging()

# def on_shape_release(event, shape_index):
#     # Check if the shape is dropped inside the game board
#     shape_button = shape_buttons[shape_index]
#     x, y, _, _ = shape_button.get_position()
#     if x < board_size and y < board_size:
#         row = int(y)
#         col = int(x)
#         if can_place_shape(row, col, random_shapes[shape_index]):
#             place_shape(row, col, random_shapes[shape_index])
#         else:
#             messagebox.showinfo("Invalid Placement", "Cannot place the shape there!")

# def can_place_shape(row, col, shape):
#     # Check if the shape can be placed at the given position
#     shape_height = len(shape)
#     shape_width = len(shape[0])
#
#     if row + shape_height > board_size or col + shape_width > board_size:
#         return False
#
#     for i in range(shape_height):
#         for j in range(shape_width):
#             if shape[i][j] == 1 and game_board[row + i][col + j] == 1:
#                 return False
#
#     return True

# def place_shape(row, col, shape):
#     # Place the shape on the game board
#     shape_height = len(shape)
#     shape_width = len(shape[0])
#
#     for i in range(shape_height):
#         for j in range(shape_width):
#             if shape[i][j] == 1:
#                 game_board[row + i][col + j] = 1
#                 board_buttons[row + i][col + j].config(text="X")

# def on_shape_drag(event, shape_index):
#     # Update the position of the shape button during dragging
#     shape_button = shape_buttons[shape_index]
#     x, y, _, _ = shape_button.get_position()
#     shape_button.move(event.x_root - x, event.y_root - y)


def main():
    global board_size, game_board, board_buttons, random_shapes, shape_buttons

    # Define the dimensions of the game board
    board_size = 8

    print(game_board)
    # # # Define the block shapes
    # block_shapes = [
    #     [[1, 1, 1, 1]],  # Horizontal block of length 4
    #     [[1], [1], [1], [1]],  # Vertical block of length 4
    #     [[1, 1], [1, 1]],  # 2x2 square block
    #     # Add more block shapes as needed
    # ]

    # # Select three random block shapes
    # random_shapes = random.sample(block_shapes, 3)

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
            button = tk.Button(window, text="", width=2, height=1,
                               command=lambda r=row, c=col: on_button_click_false(r, c))
            button.grid(row=row, column=col, padx=2, pady=2)
            button_row.append(button)
        board_buttons.append(button_row)

    # Create a frame to hold the shape buttons
    shape_frame = tk.Frame(window)
    shape_frame.grid(row=board_size, column=0, columnspan=board_size)

    # CORRECT CODE
    # if
    # on_button_click_true(row, col)
    # on_button_click_false(row, col)

    # Create the shape buttons and add drag-and-drop functionality
    # shape_buttons = []
    # for i, shape in enumerate(random_shapes):
    #     shape_button = tk.Button(shape_frame, text=f"Shape {i+1}")
    #     shape_button.grid(row=0, column=i, padx=2, pady=2)
    #     shape_button.bind("<ButtonPress-1>", lambda event, index=i: on_shape_press(event, index))
    #     shape_button.bind("<ButtonRelease-1>", lambda event, index=i: on_shape_release(event, index))
    #     shape_button.bind("<B1-Motion>", lambda event, index=i: on_shape_drag(event, index))
    #     shape_buttons.append(shape_button)

    # Start the Tkinter event loop
    window.mainloop()


if __name__ == "__main__":

    main()


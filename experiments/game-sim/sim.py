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
print(game_board)

def on_button_click(row, col):
    # Update the game board and button text when a button is clicked
    if game_board[row][col] == 0:
        game_board[row][col] = 1
        board_buttons[row][col].config(text="X")

def main():
    # Define the dimensions of the game board
    board_size = 8

    # Define the block shapes
    block_shapes = [
        [[1, 1, 1, 1]],  # Horizontal block of length 4
        [[1], [1], [1], [1]],  # Vertical block of length 4
        [[1, 1], [1, 1]],  # 2x2 square block
        # Add more block shapes as needed
    ]

    # Select three random block shapes
    random_shapes = random.sample(block_shapes, 3)

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
                               command=lambda r=row, c=col: on_button_click(r, c))
            button.grid(row=row, column=col, padx=2, pady=2)
            button_row.append(button)
        board_buttons.append(button_row)

    # Start the Tkinter event loop
    window.mainloop()

    def on_button_click(row, col):
        # Update the game board and button text when a button is clicked
        if game_board[row][col] == 0:
            game_board[row][col] = 1
            board_buttons[row][col].config(text="X")

if __name__ == "__main__":
    main()


# # Define the dimensions of the game board
# board_size = 8
#
# # Create a 2D list to represent the game board
# game_board = [[0] * board_size for _ in range(board_size)]
#
# # Create a Tkinter window
# window = tk.Tk()
# window.title("Block Puzzle Game")
#
# # Create a list to store the buttons representing the game board
# board_buttons = []
#
# # Function to handle button clicks
# def on_button_click(row, col):
#     # Update the game board and button text when a button is clicked
#     if game_board[row][col] == 0:
#         game_board[row][col] = 1
#         board_buttons[row][col].config(text="X")
#
# # Create the game board GUI
# for row in range(board_size):
#     button_row = []
#     for col in range(board_size):
#         # Create a button for each cell in the game board
#         button = tk.Button(window, text="", width=2, height=1,
#                            command=lambda r=row, c=col: on_button_click(r, c))
#         button.grid(row=row, column=col, padx=2, pady=2)
#         button_row.append(button)
#     board_buttons.append(button_row)
#
# # Start the Tkinter event loop
# window.mainloop()

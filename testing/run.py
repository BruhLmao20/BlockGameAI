import pyautogui
import cv2
import os
import sys
import time
import keyboard
import tkinter as tk



def main():
    # Define the dimensions of the game board
    board_size = 8

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

    # is_running = True
    # while is_running:
    #     print("Enter Input")
    #     update()
    #     if not is_running:
    #         break


# def update():
#     is_running = True
#     while is_running:
#         user_input = input("Press 'w' or 'q': ")
#         print("(Hit ENTER after to execute the action)")
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             is_running = False
#
#         while is_running:
#             if user_input in ['w']:
#                 if user_input == 'w':
#                     for i in range(10):
#                         sys.stdout.write(print(pyautogui.position()))
#                         sys.stdout.flush()
                        # time.sleep(1)
                    # print(pyautogui.position())

def update():
    is_running = True
    points = [10]
    while is_running:
        user_input = input("Press 'w': ")
        print("(Hit ENTER after to execute the action)")
        # if user_input == 'q':
        #     is_running = False

        while is_running and user_input == 'w':
            for i in range(10):
                sys.stdout.write('\rMouse position: ' + str(pyautogui.position()))
                sys.stdout.flush()
                # Wait for a short amount of time to prevent screen flickering
                time.sleep(0.01)
                if keyboard.is_pressed('f'):
                    for j in range(10):
                        points[i] = pyautogui.position()
                if keyboard.is_pressed('j'):
                    for l in range(10):
                        print('\n'+points[l])
                if keyboard.is_pressed('q'):
                    is_running = False
                    print('')
                    break


if __name__ == "__main__":
    main()

# V.1
# def update():
#     is_running = True
#     while is_running:
#         user_input = input("Press 'w' or 'q': ")
#         print("(Hit ENTER after to execute the action)")
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             is_running = False
#
#         while is_running:
#             if user_input in ['w']:
#                 if user_input == 'w':
#                     print(pyautogui.position())


# import pyautogui
#
# is_running = True
#
#
# def run():
#     while is_running:
#         print("Enter Input")
#         update()
#
#
# def update():
#     user_input = input("Press:  'w' or 'q': ")
#     print("(Hit ENTER after to execute the action)")
#     while True:
#         # user_input = input("Press 'w', 's', 't', 'b' or 'q' to continue: ")
#         if user_input in ['w', 'q']:
#             if user_input == 'w':
#                 print(pyautogui.position())

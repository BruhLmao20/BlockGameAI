import pyautogui
import cv2
import os
import sys
import time
import keyboard


def main():
    is_running = True
    while is_running:
        print("Enter Input")
        update()
        if not is_running:
            break


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

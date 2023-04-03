import pyautogui
# import cv2
# import time
# import numpy as np
# https://stackoverflow.com/questions/35340043/python-pyautogui-attributeerror-module-object-has-no-attribute-size
# https://stackoverflow.com/questions/47500832/algorithm-to-find-best-strategy-for-placing-blocks

# borders = cv2.imread('fullborders.png', cv2.IMREAD_UNCHANGED)
# print(borders)


# get the position and size of the Bluestacks window
bluestacks_window = pyautogui.getWindowsWithTitle("BlueStacks App Player")[0]
bluestacks_window_left, bluestacks_window_top, bluestacks_window_width, bluestacks_window_height = \
    bluestacks_window.left, bluestacks_window.top, bluestacks_window.width, bluestacks_window.height

# get the position and size of the Bluestacks phone screen within the Bluestacks window
left = bluestacks_window_left + 8  # bluestacks_phone_screen_left
top = bluestacks_window_top + 29  # bluestacks_phone_screen_top
width = bluestacks_window_width - 16  # bluestacks_phone_screen_width
height = bluestacks_window_height - 36  # bluestacks_phone_screen_height

print("Bluestacks phone screen width: ", width)
print("Bluestacks phone screen height: ", height)

# Get the coordinates of the selection box
# left, top, width, height = pyautogui.locateOnScreen('selection_box.png')

# Take a screenshot of the selected area
screenshot = pyautogui.screenshot(region=(left, top, width, height))

# Display the screenshot for confirmation
screenshot.show()


# play_area_img = cv2.imread('PlayArea.png', cv2.IMREAD_UNCHANGED)
# # p_a_img =

# fullapp = cv2.imread('fullapp.png', cv2.IMREAD_UNCHANGED)
# block = cv2.imread('block.png', cv2.IMREAD_UNCHANGED)
#
# # cv2.imshow('fullapp', fullapp)
# # cv2.waitKey()
# # cv2.destroyAllWindows()
# #
# # cv2.imshow('PlayArea', play_area_img)
# # cv2.waitKey()
# # cv2.destroyAllWindows()
# # res = pyautogui.locateOnScreen('PlayArea.png')
# # print(res)
#
# # pyautogui.hotkey("alt", "tab")
# # time.sleep(2)
# # # res = pyautogui.locateOnScreen("PlayArea.PNG")
# # print(play_area_img)
# result = cv2.matchTemplate(block, fullapp, cv2.TM_CCOEFF_NORMED)
# cv2.imshow('Result', result)
# cv2.waitKey()
# cv2.destroyAllWindows()

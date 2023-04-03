import pyautogui
import win32gui
import numpy as np
import cv2
import time

pyautogui.hotkey("alt", "tab")
time.sleep(2)
# Get the active window object
active_window = pyautogui.getActiveWindow()

# Get the window position
window_rect = win32gui.GetWindowRect(active_window._hWnd)

# Get the position and size of the active window
win_pos = pyautogui.getWindowPosition()
win_size = pyautogui.getWindowSize()

# Take a screenshot of the active window
screenshot = pyautogui.screenshot(region=(win_pos[0], win_pos[1], win_size[0], win_size[1]))

# Convert the screenshot to a numpy array for OpenCV processing
screenshot_array = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

# Show the screenshot
cv2.imshow('Screenshot', screenshot_array)
cv2.waitKey(0)


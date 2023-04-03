import pyautogui
import cv2
import time

# Load the PlayArea image
play_area_img = cv2.imread('PlayArea.png', cv2.IMREAD_UNCHANGED)

# Hotkey to switch to the target application
pyautogui.hotkey("alt", "tab")
time.sleep(1)

# Find the location of the PlayArea on the screen
play_area_location = pyautogui.locateOnScreen('PlayArea.png')

# Take a screenshot of the region specified by the coordinates of the PlayArea
screenshot = pyautogui.screenshot(region=play_area_location)

# Save the screenshot as an image file
screenshot.save('screenshot.png')

cv2.imshow('screenshot.png')

import numpy as np
import pyautogui
import cv2
import time

# Load the reference image
ref_img = cv2.imread('PlayArea.png', cv2.IMREAD_UNCHANGED)

pyautogui.hotkey("alt", "tab")
time.sleep(1)

try:
    # Search for the reference image on the screen
    location = pyautogui.locateOnScreen('PlayArea.png')

    if location is not None:
        # Extract the bounding box coordinates
        left, top, width, height = location

        # Take a screenshot of the screen
        screenshot = pyautogui.screenshot()

        # Crop the screenshot to the bounding box
        cropped_img = screenshot.crop((left, top, left + width, top + height))

        # Convert the cropped image to a numpy array for OpenCV processing
        cropped_array = cv2.cvtColor(np.array(cropped_img), cv2.COLOR_RGB2BGR)

        # Show the reference image and the cropped image side by side
        cv2.imshow('Reference Image', ref_img)
        cv2.imshow('Cropped Image', cropped_array)
        cv2.waitKey(0)
    else:
        print('Reference image not found on the screen.')
except Exception as e:
    print('Error:', e)

cv2.destroyAllWindows()

#
# # Search for the reference image on the screen
# location = pyautogui.locateOnScreen('PlayArea.png')
# screenshot = pyautogui.screenshot(region=location)
# if location is not None:
#     # Extract the bounding box coordinates
#     left, top, width, height = location
#
#     # Take a screenshot of the screen
#     screenshot = pyautogui.screenshot()
#
#     # Crop the screenshot to the bounding box
#     cropped_img = screenshot.crop((left, top, left + width, top + height))
#
#     # Convert the cropped image to a numpy array for OpenCV processing
#     cropped_array = cv2.cvtColor(np.array(cropped_img), cv2.COLOR_RGB2BGR)
#
#     # Show the cropped image
#     cv2.imshow('Cropped Image', cropped_array)
#     cv2.waitKey(0)
# else:
#     print('Reference image not found on the screen.')


    # import numpy as np
    # import pyautogui
    # import cv2
    #
    # # Load the reference image
    # ref_img = cv2.imread('PlayArea.png', cv2.IMREAD_UNCHANGED)
    #
    # # Search for the reference image on the screen
    # location = pyautogui.locateOnScreen('PlayArea.png')
    # if location is not None:
    #     # Extract the bounding box coordinates
    #     left, top, width, height = location
    #
    #     # Take a screenshot of the screen
    #     screenshot = pyautogui.screenshot()
    #
    #     # Crop the screenshot to the bounding box
    #     cropped_img = screenshot.crop((left, top, left + width, top + height))
    #
    #     # Convert the cropped image to a numpy array for OpenCV processing
    #     cropped_array = cv2.cvtColor(np.array(cropped_img), cv2.COLOR_RGB2BGR)
    #
    #     # Show the cropped image
    #     cv2.imshow('Cropped Image', cropped_array)
    #     cv2.waitKey(0)
    # else:
    #     print('Reference image not found on the screen.')
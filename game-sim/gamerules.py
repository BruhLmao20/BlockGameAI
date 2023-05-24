from tkinter import messagebox
import numpy as np
import tkinter as tk
import random


# if the square is clicked, then it stays clicked
# game rule will check if a vertical or a horizontal line has been made that connects end to end
# if true the game will award the points
# if multiples lines are destroyed at once those extra points are awarded
# if the whole board is cleared then the 300 extra points are awarded
# game will check points to see when to upgrade blocks selection

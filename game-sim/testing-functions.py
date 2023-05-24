# if all numbers in a whole row or a whole colum all contain 1, then said line would
# disappear and award points

points = 0

def is_row_full(array):
    for row in array:
        if all(element == 1 for element in row):
            return True
    return False


def is_columns_full(array):
    for columns in array:
        if all(element == 1 for element in columns):
            return True
    return False


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

# def points_awarded(array, points):
#

# POINTS
# placing down a shape; according to shapes size,
# points are awarded to corresponding 1x1 cube shape places per shape

# 1 line:   10 points
# 2 lines:  30 points
# 3 lines:  60 points
# 4 lines:  100 points
# 5 lines:  150 points

# clear the board: 300 points

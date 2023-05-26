# if all numbers in a whole row or a whole colum all contain 1, then said line would
# disappear and award points

points = 0


def is_row_full(array):
    row_location = []
    for row in array:  # row is == to i
        if all(element == 1 for element in row):
            row_location.append(row)
    return row_location


# return how many rows are full and where they are positions in the 2d array


def is_columns_full(array):
    for columns in array:
        if all(element == 1 for element in columns):
            return True
    return False


# return how many columns are full and where they are positions in the 2d array


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


def lines_completed(array):
    is_row_full(array)  # returns all the rows that are full
    # use the count of rows to then award to points based on amount of rows completed
    points_awarded = 0
    rows_completed = len(is_row_full(array))
    return

    # is_columns_full(array)


def points_multiplier(lines):
    points_multiplied = 0
    if lines == 1:
        points_multiplied = lines * 10
    elif lines == 2:
        points_multiplied = lines * 15
    elif lines == 3:
        points_multiplied = lines * 20
    elif lines == 4:
        points_multiplied = lines * 25
    elif lines == 5:
        points_multiplied = lines * 30
    return points_multiplied

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

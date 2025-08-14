# if all numbers in a whole row or a whole colum all contain 1, then said line would
# disappear and award points
import xonclick


# CHECK LINE CHECKER.txt file
# first check if there even is any line that is complete
# using boolean to just check if its even true
# once found true, seach for how many lines are completed
# once lines found out, then return their locaiton on the array
# award points, then clear the lines


def total_logic(array):
    """Run the line clearing logic and return points awarded."""
    points = total_points_system(array)
    clear_lines(array)
    return points



def clear_lines(array):
    clear_row(array)
    clear_columns(array)
    # total_points_system(array)


def total_points_system(array):  # ran in the clear function
    if row_full_boolean(array) or columns_full_boolean(array):
        all_points = points_awarded(array)
        print_points(array)
        return all_points
    else:
        all_points = 0
        return all_points


def points_awarded(array):
    points = 0
    points = points + points_multiplier(any_line_checker(array))
    return points


def print_points(array):
    current_points = points_multiplier(any_line_checker(array))
    print('Points: ' + str(current_points))


def any_line_checker(array):
    number_of_lines = 0
    if row_full_boolean(array) or columns_full_boolean(array):
        number_of_lines = len(is_row_full(array)) + len(is_columns_full(array))
        return number_of_lines  # returns int so that points may be awarded
    return number_of_lines


# then award points and clear lines


# check if line is true
def row_full_boolean(array):
    for row in array:  # row is == to i
        if all(element == 1 for element in row):
            return True
    return False


def columns_full_boolean(array):
    for columns in array:
        if all(element == 1 for element in columns):
            return True
    return False


# ACTUAL NUMBER OF ROWS AND COLUMNS THAT ARE FULL
def is_row_full(array):
    row_location = []
    for row in array:  # row is == to i
        if all(element == 1 for element in row):
            row_location.append(row)
    return row_location


# return how many rows are full and where they are positions in the 2d array


def is_columns_full(array):
    """Return column indexes that are completely filled."""
    col_locations = []
    for col_index in range(len(array[0])):
        if all(row[col_index] == 1 for row in array):
            col_locations.append(col_index)
    return col_locations


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
    return rows_completed  # , points_awarded

    # is_columns_full(array)


def points_multiplier(lines):  # number of lines INT, take in anylinechecker
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


# PRINT STATEMENT FUNCTIONS
# def print_board(game_board):
#     xonclick.extra_space()
#     xonclick.print_2d_array(game_board)

from helpers import print_2d_array


def points_multiplier(lines):  # number of lines INT, take in anylinechecker
    points_multiplied = 0
    if lines == 1:
        points_multiplied += lines * 10
    elif lines == 2:
        points_multiplied = lines * 15
    elif lines == 3:
        points_multiplied += lines * 20
    elif lines == 4:
        points_multiplied += lines * 25
    elif lines == 5:
        points_multiplied += lines * 30
    return points_multiplied


# lines = 2
#
# # points_multiplier(lines)
# print(str(points_multiplier(lines)))


# TEXT FILE SOLO_TEST_POINTS


# TEST 2 ==============================================================================

def any_line_checker(array):
    number_of_lines = 0
    if row_full_boolean(array) or columns_full_boolean(array):
        number_of_lines += len(is_row_full(array)) + len(is_columns_full(array))
        return number_of_lines  # returns into so that points may be awarded


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


# def is_columns_full(array):
#     col_location = []
#     for col in array:  # row is == to i
#         if all(element == 1 for element in col):
#             col_location.append(col)
#     return col_location

# new col function
def is_columns_full(array):
    col_locations = []
    for col_index in range(len(array[0])):
        if all(row[col_index] == 1 for row in array):
            col_locations.append(col_index)
    return col_locations


first = [[0] * 8 for _ in range(7)]
first.append([1] * 8)
# second = first.append([1] * 8)
# second = first

print(first)  # row print array
print_2d_array(first)  # from helpers.S import *
print(str(any_line_checker(first)))  # print number of lines complete


print(str(is_columns_full(first)))  # prints whole columns that are fully complete

rowt = True
rowf = False
colt = True
colf = False

# array1 = []

rows = 8
cols = 8

# Create a 2D array with all elements initialized to 0  ## WHAT DOES THIS MEAN? AND WHY COL FIRST?
array1 = [[0] * cols for _ in range(rows)]

# Fill the bottom row with 1
array1[rows - 1] = [1] * cols

# Fill the right column with 1
for i in range(rows):
    array1[i][cols - 1] = 1

total_points = 0  # Initialize the total points variable


# Function to update total points
def update_points(points):
    global total_points  # Use the global total_points variable
    total_points += points


def print_points(array):
    current_points = 0
    current_points += points_multiplier(array)  # any_line_checker(array) went inside as parameter as number of lines

    print('Points: ' + str(current_points))


# ===== 2 =====
def points_awarded(array):
    global total_points
    total_points += points_multiplier(
        lines(array))  # any_line_checker(array) went inside as parameter as number of lines
    return total_points


# row_num = 2
# col_num = 3


# ===== 1 =====
def total_points_system(array):
    global total_points

    if is_row_full(array) or is_columns_full(array):
        # lines(array)
        # PM(lines(array)

        # = = = = = = = = = = =
        # total_points += points_awarded(array)
        points_awarded(array)
        # = = = = = = = = = = =

        # print_points(array)
        # return total_points
    # else:
    # # print_points(array)
    # return total_points


# ===== 4 =====
def lines(array):
    all_lines = len(is_row_full(array)) + len(is_columns_full(array))
    return all_lines


def is_row_full(array):
    full_row_indices = []
    for row_index, row in enumerate(array):
        if all(element == 1 for element in row) and len(row) == row.count(1):
            full_row_indices.append(row_index + 1)  # Add the row index (+1 to make it 1-based)

    return full_row_indices


# def is_columns_full(array):
#     col_location = []
#     num_cols = len(array[0])  # Number of columns in the array
#     for col_index in range(num_cols):
#         col = [row[col_index] for row in array]  # Get the column elements
#         if all(element == 1 for element in col):
#             col_location.append(col)
#     return col_location


def format_output(columns):
    if not columns:
        return "No columns are full."
    else:
        column_indices = ', '.join(str(col) for col in columns)
        return f"Column(s): {column_indices} are full."


def is_columns_full(array):
    full_col_indices = []
    num_cols = len(array[0])  # Number of columns in the array
    for col_index in range(num_cols):
        col = [row[col_index] for row in array]  # Get the column elements
        if all(element == 1 for element in col) and len(col) == col.count(1):
            full_col_indices.append(col_index + 1)  # Add the column index (+1 to make it 1-based)

    return full_col_indices


# get lines from IS FULL COL AND ROW PUT INTO ONE
# ===== 3 =====
def points_multiplier(lines):  # number of lines INT, take in anylinechecker
    points_multiplied = 0
    if lines == 1:
        points_multiplied += lines * 10
    elif lines == 2:
        points_multiplied += lines * 15
    elif lines == 3:
        points_multiplied += lines * 20
    elif lines == 4:
        points_multiplied += lines * 25
    elif lines == 5:
        points_multiplied += lines * 30
    return points_multiplied


# Implement into the CODE
def fill_array_with_ones(current_array):
    # Get the number of rows and columns to fill from the user
    rows = int(input("Enter the number of rows to fill with 1's: "))
    cols = int(input("Enter the number of columns to fill with 1's: "))

    # Fill the specified rows with 1's
    for row in range(rows):
        for col in range(len(current_array[0])):
            current_array[row][col] = 1

    # Fill the specified columns with 1's
    for row in range(len(current_array)):
        for col in range(cols):
            current_array[row][col] = 1

    return current_array


def print_2d_array(array):
    for row in array:
        for element in row:
            print(element, end=' ')
        print()


def initial_fill(array):
    print_2d_array(array1)
    # create array [8x8]
    print(is_row_full(array1))
    print(is_columns_full(array1))


# def initialize():
#     # maybe create_array()


def create_array():
    ca_rows = 8
    ca_cols = 8
    array_ca = [[0] * ca_cols for _ in range(ca_rows)]
    array1[ca_rows - 1] = [1] * ca_cols
    for i in range(ca_rows):
        array_ca[i][cols - 1] = 1
    return array_ca


# Call the function and assign the returned array to a variable
# my_array = create_array()

def create_array_custom(row, col):
    rows = row
    cols = col

    # Create a 2D array with all elements initialized to 0  ## WHAT DOES THIS MEAN? AND WHY COL FIRST?
    array_c = [[0] * cols for _ in range(rows)]

    # Fill the bottom row with 1
    array_c[rows - 1] = [1] * cols

    # Fill the right column with 1
    for i in range(rows):
        array1[i][cols - 1] = 1

    return array_c


# ===== ===== POINTS ===== =====
def points(array):  # CONFLICT: 30pt turned to 120 here
    # update_points(points_awarded(array))
    print(total_points)


# ===== ===== LOGIC ===== =====


# ===== ===== INITIALIZE ===== =====

# def all_points(array, total_points):


def main():
    initial_fill(array1)
    total_points_system(array1)
    points(array1)

    # initialize
    # points system
    # - or if lines full
    # - if true, points awarded go to totalpoints (points awarded path)
    #   - PA -
    # -


# TPS
# OR FULL
# TP += PA
# TP += PM [goes into
# PM(LINES) [goes into PA]
# LINES(ARRAY) [goes into PM]

if __name__ == "__main__":
    # print(game_board)
    main()

# in the def main funciton

# # Example usage
# update_points(10)  # Add 10 points
# print("Total points:", total_points)  # Output: Total points: 10
#
# update_points(5)  # Add 5 points
# print("Total points:", total_points)  # Output: Total points: 15

# print_2d_array(array1)
# print(is_row_full(array1))
# print(is_columns_full(array1))
# fill_array_with_ones(array1)
# print(is_row_full(array1))
# print(is_columns_full(array1))


# print_2d_array(array1)
# total_points_system(array1)
# fill_array_with_ones(array1)
# total_points_system(array1)


# print_points(array1)
# fill_array_with_ones(array1)
# print_points(array1)
# fill_array_with_ones(array1)
# print_points(array1)
# def points_awarded(array, total_points):
#     total_points += points_multiplier(3)  # any_line_checker(array) went inside as parameter as number of lines
#     return total_points
# gets how many lines are there
#

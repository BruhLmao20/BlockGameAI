# PRE COMMENT ERASED FILE IS ON FILE "OLD CODE\POINTS\ppi.fixed.py
import keyboard

total_points = 0  # Initialize the total points variable


# ===== ===== POINTS ===== =====
# ===== 1 =====
def total_points_system(array):
    global total_points

    if is_row_full(array) or is_columns_full(array):
        points_awarded(array)
        # empty_array(array) # ADD AFTER TPS


# ===== 2 =====
def points_awarded(array):
    global total_points
    total_points += points_multiplier(
        lines(array))  # any_line_checker(array) went inside as parameter as number of lines
    clear_row_or_col(array)
    return total_points


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
    elif lines == 6:
        points_multiplied += lines * 35
    return points_multiplied


# max amount of lines that can be destroyed is 6 lines destroyed at once


# ===== 4 =====
def lines(array):
    all_lines = len(is_row_full(array)) + len(is_columns_full(array))
    return all_lines


# Function to update total points
def update_points(points):
    global total_points  # Use the global total_points variable
    total_points += points


def print_points(array):
    current_points = 0
    current_points += points_multiplier(array)  # any_line_checker(array) went inside as parameter as number of lines

    print('Points: ' + str(current_points))


def points(array):  # CONFLICT: 30pt turned to 120 here
    # global total_points

    # update_points(points_awarded(array))
    print(total_points)


# ===== ===== LOGIC ===== =====
def is_row_full(array):
    full_row_indices = []
    for row_index, row in enumerate(array):
        if all(element == 1 for element in row) and len(row) == row.count(1):
            full_row_indices.append(row_index + 1)  # Add the row index (+1 to make it 1-based)

    return full_row_indices


def is_columns_full(array):
    full_col_indices = []
    num_cols = len(array[0])  # Number of columns in the array
    for col_index in range(num_cols):
        col = [row[col_index] for row in array]  # Get the column elements
        if all(element == 1 for element in col) and len(col) == col.count(1):
            full_col_indices.append(col_index + 1)  # Add the column index (+1 to make it 1-based)

    return full_col_indices


def clear_rows(array):
    full_row_indices = []
    num_rows = len(array)  # Number of rows in the array
    # vvv checks if the rows are full
    for row_index in range(num_rows):
        row = array[row_index]  # Get the row elements
        if all(element == 1 for element in row) and len(row) == row.count(1):
            full_row_indices.append(row_index)
    # vvv clears the rows
    for row_index in full_row_indices:
        array[row_index] = [0] * len(array[row_index])  # Replace the full row with zeros

    return array


def clear_columns(array):
    full_col_indices = is_columns_full(array)  # Get the indices of full columns
    num_rows = len(array)  # Number of rows in the array
    for row_index in range(num_rows):
        for col_index in full_col_indices:
            array[row_index][col_index] = 0  # Replace the element in the full column with zero

    return array


def clear_row_or_col(array):
    array = clear_rows(array)
    array = clear_columns(array)
    return array


# https://chat.openai.com/share/1ff9549a-e83c-430a-979b-9f311e2e0742


# ===== ===== INITIALIZE ===== =====
# RENAME: P2A
def print_2d_array(array):
    for row in array:
        for element in row:
            print(element, end=' ')
        print()


def format_r_output(lines):
    if not lines:
        return "No rows are full."
    else:
        line_indices = ', '.join(str(line) for line in lines)
        return f"Row(s): {line_indices} are full."


def format_c_output(lines):
    if not lines:
        return "No columns are full."
    else:
        line_indices = ', '.join(str(line) for line in lines)
        return f"Column(s): {line_indices} are full."
    # NEED TO MAKE COL AND ROW SPECIFIC OUTPUT
    # IF rows or cols are connected make out put (row or col's: 1-5 or #-# are full)


def initial_fill(array):
    print_2d_array(array)
    # create array [8x8]
    print(is_row_full(array))
    print(is_columns_full(array))


def test_start(array):  # Important Code
    # UNCOMMENT THESE LINES
    # print_2d_array(array)
    # print(is_row_full(array))
    # print(is_columns_full(array))
    print(format_r_output(is_row_full(array)))
    print(format_c_output(is_columns_full(array)))


def empty_array():
    em_rows = 8
    em_cols = 8
    em_array = [[0] * em_cols for _ in range(em_rows)]
    # em_array[em_rows - 1] = [1] * em_cols
    # for i in range(em_rows):
    #     em_array[i][em_cols - 1] = 0
    return em_array


def create_array(array):
    ca_rows = 8
    ca_cols = 8
    array_ca = [[0] * ca_cols for _ in range(ca_rows)]
    array[ca_rows - 1] = [1] * ca_cols
    for i in range(ca_rows):
        array_ca[i][ca_cols - 1] = 0
    return array_ca


def create_array_custom(row, col, array):
    c_rows = row
    c_cols = col

    # Create a 2D array with all elements initialized to 0  ## WHAT DOES THIS MEAN? AND WHY COL FIRST?
    array_c = [[0] * c_cols for _ in range(c_rows)]

    # Fill the bottom row with 1
    array_c[c_rows - 1] = [1] * c_cols

    # Fill the right column with 1
    for i in range(c_rows):
        array_c[i][c_cols - 1] = 1  # array not _c

    return array_c


def fill_array_with_ones(current_array):
    # Get the number of rows and columns to fill from the user
    rows = int(input("Enter the number [1-6] of rows to fill with 1's: "))
    cols = int(input("Enter the number [1-6] of columns to fill with 1's: "))

    # Fill the specified rows with 1's
    for row in range(rows):
        for col in range(len(current_array[0])):
            current_array[row][col] = 1

    # Fill the specified columns with 1's
    for row in range(len(current_array)):
        for col in range(cols):
            current_array[row][col] = 1

    return current_array


def quick_points(array):
    total_points_system(array)
    # empty_array(array)  # NEW ADDED
    points(array)


def practice(test_array):
    print_2d_array(test_array)  # print array
    fill_array_with_ones(test_array)  # 1, 1 get 30 points
    print_2d_array(test_array)  # print array
    test_start(test_array)  # formatted response
    # quick_points(test_array)
    total_points_system(test_array)
    # ^^^ Points: 1 -> 2 -> 4 ->  total_points += 3
    points(test_array)


# def practice2(test_array):


def main():
    test_array = empty_array()
    # practice(test_array)
    # # need to clear the 1's that were used in previous line
    # practice(test_array)

    while True:
        practice(test_array)

        if keyboard.is_pressed(" "):
            break


if __name__ == "__main__":
    main()

# def build():
#     # array1 = []
#
#     rows = 8
#     cols = 8
#
#     # Create a 2D array with all elements initialized to 0  ## WHAT DOES THIS MEAN? AND WHY COL FIRST?
#     array1 = [[0] * cols for _ in range(rows)]
#
#     # Fill the bottom row with 1
#     array1[rows - 1] = [1] * cols
#
#     # Fill the right column with 1
#     for i in range(rows):
#         array1[i][cols - 1] = 1
#
#     return array1

#
# def infinite_game(test_array):
#     while True:
#         practice(test_array)
#
#     key = cv2.waitKey(1)
#     if key == 27:
#         break

# TOP OF CODE 
# rowt = True
# rowf = False
# colt = True
# colf = False
#
# # array1 = []
#
# rows = 8
# cols = 8
#
# # Create a 2D array with all elements initialized to 0  ## WHAT DOES THIS MEAN? AND WHY COL FIRST?
# array1 = [[0] * cols for _ in range(rows)]
#
# # Fill the bottom row with 1
# array1[rows - 1] = [1] * cols
#
# # Fill the right column with 1
# for i in range(rows):
#     array1[i][cols - 1] = 1

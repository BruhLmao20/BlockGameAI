global total_points
total_points = 0
rowt = True
rowf = False
colt = True
colf = False

# array1 = []

rows = 8  # Number of rows in the array
cols = 8  # Number of columns in the array

# Create a 2D array with all elements initialized to 0
array1 = [[0] * cols for _ in range(rows)]

# Fill the bottom row with 1
array1[rows - 1] = [1] * cols

# Fill the right column with 1
for i in range(rows):
    array1[i][cols - 1] = 1


def print_points(array):
    current_points = 1
    current_points += points_multiplier(2)  # any_line_checker(array) went inside as parameter as number of lines

    print('Points: ' + str(current_points))


def points_awarded(array, total_points):
    total_points += points_multiplier(3)  # any_line_checker(array) went inside as parameter as number of lines
    return total_points


# row_num = 2
# col_num = 3


#
def total_points_system(array):  # ran in the clear function
    if rowt or colt:  # is true? row_full_boolean(array) columns_full_boolean(array)
        all_points = points_awarded(array, total_points)
        print_points(array)
        return all_points
    else:
        total_points += 1
        return total_points


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


def print_2d_array(array):
    for row in array:
        for element in row:
            print(element, end=' ')
        print()


def main():
    print_2d_array(array1)
    print_points(array1)
    # def points_awarded(array, total_points):
    #     total_points += points_multiplier(3)  # any_line_checker(array) went inside as parameter as number of lines
    #     return total_points
    # gets how many lines are there
    #


if __name__ == "__main__":
    # print(game_board)
    main()

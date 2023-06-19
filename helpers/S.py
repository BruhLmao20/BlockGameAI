# import testing_functions
# from helpers import S
# S.my_function()
# S.print_2d_array(array)

# ALL FUNCTIONS
# print_2d_array(array)
# print_space()
# extra_space()
# print_board(game_board)


# Text and Help Function ====================
def print_2d_array(array):
    for row in array:
        for element in row:
            print(element, end=' ')
        print()


def print_space():
    print("=" * 20)  # Repeat "=" 20 times


def extra_space():
    print_space()
    print_space()
    print_space()


def print_board(game_board):
    extra_space()
    # print_points(game_board)
    print_2d_array(game_board)


# import testing_functions.py
# def print_points(array):
#     current_points = points_multiplier(any_line_checker(array))
#     print('Points: ' + str(current_points))

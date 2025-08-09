# have a high score txt
# current score txt
#


def load_points():
    try:
        with open("points.txt", "r") as file:
            points = int(file.read())
    except FileNotFoundError:
        # If the file is not found (first time running the game), initialize points to 0
        points = 0
    return points


# def write_points():
#     try:
#         with open("points.txt", "w") as file:
#             points = int(file.read())
#     except FileNotFoundError:
#         # If the file is not found (first time running the game), initialize points to 0
#         points = 0
#     return points

def save_points(points):
    with open("points.txt", "w") as file:
        file.write(str(points))

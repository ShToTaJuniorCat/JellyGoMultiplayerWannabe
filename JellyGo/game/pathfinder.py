import math
import heapq
import pygame
import random
import numpy as np
import time


class Cell:
    def __init__(self, parent_i=0, parent_j=0, f=0, g=0, h=0):
        self.parent_i = parent_i
        self.parent_j = parent_j
        self.f = f
        self.g = g
        self.h = h


def is_valid(row, col, max_row, max_col):
    return 0 <= row < max_row and 0 <= col < max_col


def is_unblocked(grid, row, col):
    return grid[row][col] == 1


def is_destination(row, col, destination):
    return row == destination[0] and col == destination[1]


def calculate_h_value(row, col, destination):
    return math.sqrt((row - destination[0]) ** 2 + (col - destination[1]) ** 2)


def trace_path(cell_details, destination):
    row, col = destination
    path = []

    while not (cell_details[row][col].parent_i == row and cell_details[row][col].parent_j == col):
        path.append((row, col))
        row, col = cell_details[row][col].parent_i, cell_details[row][col].parent_j

    path.append((row, col))
    returned_path = [(p[0], p[1] - 1) if p[0] == 2 or p[0] == 1 else (p[0], p[1]) for p in path[::-1]]

    return returned_path


def a_star_search(grid, src, destination):
    print(f"Until search called: {time.time() - start_time}")

    max_row, max_col = len(grid), len(grid[0])
    #src = [src[1], src[0]]
    #destination = [destination[1], destination[0]]

    if not (is_valid(src[0], src[1], max_row, max_col) and is_valid(destination[0], destination[1], max_row, max_col)):
        print("Source or destination is invalid")
        return

    if not (is_unblocked(grid, src[0], src[1]) and is_unblocked(grid, destination[0], destination[1])):
        print("Source or destination is blocked")
        return

    if is_destination(src[0], src[1], destination):
        print("Already at the destination")
        return []

    print(f"Until after bound checks: {time.time() - start_time}")

    closed_list = [[False for _ in range(max_col)] for _ in range(max_row)]
    cell_details = [[Cell() for _ in range(max_col)] for _ in range(max_row)]

    print(f"Until before for loop: {time.time() - start_time}")

    for i in range(max_row):
        for j in range(max_col):
            cell_details[i][j].f = math.inf
            cell_details[i][j].g = math.inf
            cell_details[i][j].h = math.inf
            cell_details[i][j].parent_i = -1
            cell_details[i][j].parent_j = -1

    i, j = src[0], src[1]
    cell_details[i][j].f = 0
    cell_details[i][j].g = 0
    cell_details[i][j].h = 0
    cell_details[i][j].parent_i = i
    cell_details[i][j].parent_j = j

    open_list = [(0, i, j)]

    print(f"Until search started: {time.time() - start_time}")

    while open_list:
        _, i, j = heapq.heappop(open_list)
        closed_list[i][j] = True

        successors = [
            (i - 1, j), (i + 1, j), (i, j + 1), (i, j - 1),
            (i - 1, j + 1), (i - 1, j - 1), (i + 1, j + 1), (i + 1, j - 1)
        ]

        # screen.set_at((j, i), (0, 0, 255))
        # pygame.draw.circle(screen, (255, 255, 0), (src[1], src[0]), 3)
        # pygame.draw.circle(screen, (255, 255, 0), (destination[1], destination[0]), 3)
        # pygame.display.update()

        for successor in successors:
            row, col = successor

            if is_valid(row, col, max_row, max_col) and is_unblocked(grid, row, col):
                if is_destination(row, col, destination):
                    cell_details[row][col].parent_i = i
                    cell_details[row][col].parent_j = j
                    return trace_path(cell_details, destination)

                if not closed_list[row][col]:
                    g_new = cell_details[i][j].g + 1 if i == row or j == col else cell_details[i][j].g + 1.414
                    h_new = calculate_h_value(row, col, destination)
                    f_new = g_new + h_new

                    if cell_details[row][col].f == math.inf or cell_details[row][col].f > f_new:
                        heapq.heappush(open_list, (f_new, row, col))
                        cell_details[row][col].f = f_new
                        cell_details[row][col].g = g_new
                        cell_details[row][col].h = h_new
                        cell_details[row][col].parent_i = i
                        cell_details[row][col].parent_j = j

    print("Failed to find the Destination Cell")

def choose_random_index_optimized(matrix):
        # Convert the matrix to a NumPy array
        np_matrix = np.array(matrix)

        # Find indices with value 1 using NumPy's argwhere
        indices_with_ones = np.argwhere(np_matrix == 1)

        # Choose a random index with value 1
        if indices_with_ones.size > 0:
            return tuple(indices_with_ones[random.randint(0, indices_with_ones.shape[0] - 1)])
        else:
            return None  # No index with value 1 found


def example(print_maze=False):
    # maze = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
    #         [0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, ],
    #         [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, ],
    #         [0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, ],
    #         [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, ],
    #         [0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, ],
    #         [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, ],
    #         [0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, ],
    #         [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, ],
    #         [0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, ],
    #         [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, ],
    #         [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, ],
    #         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, ]]

    if display_progress:
        # Draw the maze
        for row_index, row in enumerate(maze):
            for col_index, col in enumerate(row):
                pygame.draw.rect(screen, (255 * maze[row_index][col_index],) * 3,
                                 pygame.Rect(col_index, row_index, 1, 1))

    points = [(253, 367), (334, 1150), (253, 1612),
              (522, 367), (541, 628), (522, 908), (541, 1365), (523, 1612),
              (788, 367), (714, 1148), (779, 1612)]
    start = random.choice(points)
    end = random.choice(points)

    print(start, end)

    if display_progress:
        pygame.draw.circle(screen, (255, 255, 0), (start[1], start[0]), 3)
        pygame.draw.circle(screen, (255, 255, 0), (end[1], end[0]), 3)
        pygame.display.update()

    print("Start")

    path = a_star_search(maze, start, end)
    print(f"Total time: {time.time() - start_time}")

    if print_maze:
        for step in path:
            maze[step[0]][step[1]] = 2

        for row in maze:
            line = []
            for col in row:
                if col == 1:
                    line.append("\u2588")
                elif col == 0:
                    line.append(" ")
                elif col == 2:
                    line.append(".")
            print("".join(line))


# Problems: (212, 492) (507, 124)
if __name__ == "__main__":
    # Initialize an empty maze list
    maze = []
    display_progress = False
    start_time = time.time()

    # Open the file for reading
    with open(r'pixels.txt', 'r') as file:
        # Iterate over each line in the file
        for line in file:
            # Create a list for the current row and append each digit as an integer
            maze_row = [int(digit) for digit in line.strip()]

            # Append the row to the maze
            maze.append(maze_row)

    # Initialize pygame screen
    if display_progress:
        pygame.init()
        screen = pygame.display.set_mode((1920, 1080))

    example()

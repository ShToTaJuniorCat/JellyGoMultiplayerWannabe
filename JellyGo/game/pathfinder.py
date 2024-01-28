import math
import heapq
import pygame
import random
import numpy as np
import time


class Cell:
    def __init__(self, parent_i=-1, parent_j=-1, f=math.inf, g=math.inf, h=math.inf):
        self.parent_i = parent_i
        self.parent_j = parent_j
        self.f = f
        self.g = g
        self.h = h


class Pathfinder:
    def __init__(self, grid, is_unblocked):
        self.grid = grid
        self.is_unblocked_function = is_unblocked
        self.max_row = len(grid)
        self.max_col = len(grid[0])
        self.closed_list = []
        self.cell_details = None

    def initialize_values(self):
        # self.closed_list = np.full((self.max_row, self.max_col), False, dtype=bool)
        print(f"Until cell details: {time.time() - start_time}")
        self.cell_details = [[Cell() for _ in range(self.max_col)] for _ in range(self.max_row)]

    def is_valid(self, row, col):
        return 0 <= row < self.max_row and 0 <= col < self.max_col

    def is_unblocked(self, row, col):
        return self.grid[row][col] == 1

    @staticmethod
    def is_destination(row, col, destination):
        return row == destination[0] and col == destination[1]

    @staticmethod
    def calculate_h_value(row, col, destination):
        return math.sqrt((row - destination[0]) ** 2 + (col - destination[1]) ** 2)

    @staticmethod
    def trace_path(cell_details, destination):
        row, col = destination
        path = []

        while not (cell_details[row][col].parent_i == row and cell_details[row][col].parent_j == col):
            path.append((row, col))
            row, col = cell_details[row][col].parent_i, cell_details[row][col].parent_j

        path.append((row, col))
        returned_path = [(p[0], p[1] - 1) if p[0] == 2 or p[0] == 1 else (p[0], p[1]) for p in path[::-1]]

        return returned_path

    def a_star_search(self, src, destination):
        # src = [src[1], src[0]]
        # destination = [destination[1], destination[0]]

        if not (self.is_valid(src[0], src[1]) and self.is_valid(destination[0], destination[1])):
            print("Source or destination is invalid")
            return

        if not (self.is_unblocked_function(src[0], src[1]) and self.is_unblocked_function(destination[0], destination[1])):
            print("Source or destination is blocked")
            return

        if self.is_destination(src[0], src[1], destination):
            print("Already at the destination")
            return []

        i, j = src[0], src[1]
        self.cell_details[i][j].f = 0
        self.cell_details[i][j].g = 0
        self.cell_details[i][j].h = 0
        self.cell_details[i][j].parent_i = i
        self.cell_details[i][j].parent_j = j

        open_list = [(0, i, j)]
        heapq.heapify(open_list)

        print(f"Until search started: {time.time() - start_time}")

        while open_list:
            _, i, j = heapq.heappop(open_list)
            self.closed_list.append((i, j))

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

                if self.is_valid(row, col) and self.is_unblocked_function(row, col):
                    if self.is_destination(row, col, destination):
                        self.cell_details[row][col].parent_i = i
                        self.cell_details[row][col].parent_j = j
                        print("V Pathfinding finished correctly.")
                        return self.trace_path(self.cell_details, destination)

                    if (i, j) in self.closed_list:
                        g_new = self.cell_details[i][j].g + 1 if i == row or j == col else self.cell_details[i][j].g + 1.414
                        h_new = self.calculate_h_value(row, col, destination)
                        f_new = g_new + h_new

                        if self.cell_details[row][col].f == math.inf or self.cell_details[row][col].f > f_new:
                            heapq.heappush(open_list, (f_new, row, col))
                            self.cell_details[row][col].f = f_new
                            self.cell_details[row][col].g = g_new
                            self.cell_details[row][col].h = h_new
                            self.cell_details[row][col].parent_i = i
                            self.cell_details[row][col].parent_j = j

        print("X Failed to find the Destination Cell")


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
    points.remove(start)
    end = random.choice(points)

    if display_progress:
        pygame.draw.circle(screen, (255, 255, 0), (start[1], start[0]), 3)
        pygame.draw.circle(screen, (255, 255, 0), (end[1], end[0]), 3)
        pygame.display.update()

    pathfinder = Pathfinder(maze, is_unblocked)
    print(f"Start initialization: {time.time() - start_time}")
    pathfinder.initialize_values()
    print(f"Call a*: {time.time() - start_time}")
    path = pathfinder.a_star_search(start, end)
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


def is_unblocked(row, col):
    return maze[row][col] == 1


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

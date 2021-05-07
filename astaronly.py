import pygame
import random
import time
import math
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("MazeFinding")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        # self.barrier_cells = []
        # self.visited = []
        # self.cell_stack = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == BLUE

    def is_end(self):
        return self.color == YELLOW

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = BLUE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = YELLOW

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # Down
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # Up
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # Right
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # Left
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


def heuristic(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf")for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf")for row in grid for spot in row}
    f_score[start] = heuristic(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Node(i, j, gap, rows)
            grid[i].append(spot)
    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col


# def knock_up(win, x, y, width):
#     pygame.draw.rect(win, YELLOW, (x, y, width, width))
#     pygame.display.update()
#
#
# def knock_down(win, x, y, width):
#     pygame.draw.rect(win, YELLOW, (x, y, width, width))
#     pygame.display.update()
#
#
# def knock_left(win, x, y, width):
#     pygame.draw.rect(win, YELLOW, (x, y, width, width))
#     pygame.display.update()
#
#
# def knock_right(win, x, y, width):
#     pygame.draw.rect(win, YELLOW, (x, y, width, width))
#     pygame.display.update()
#
#
# def single_cell(win, x, y, width):
#     pygame.draw.rect(win, BLUE, (x, y, width, width))
#
#
# def recursive_cell(win, x, y, width):
#     pygame.draw.rect(win, RED, (x, y, width, width))
#     pygame.display.update()


# def create_maze(win, grid):
#     rows = len(grid)
#     width = rows * grid[0][0].width
#     row, col = 0,0
#     gap = width // rows
#
#     print(gap)
#
#     visited = []
#     cell_stack = []
#
#     single_cell(win, row * gap, col * gap, gap)
#     visited.append((row, col))
#     cell_stack.append((row, col))
#
#     row_col_list = []
#     for l in grid:
#         for n in l:
#             row_col_list.append(n.get_pos())
#
#     #print(row_col_list)
#
#     while len(cell_stack) > 0:
#         time.sleep(0.07)
#         cell = []
#
#         # if (row + gap, col) not in visited and ((row + gap, col) in row_col_list):
#         #     cell.append("Right")
#         #     print(1)
#         # if (row - gap, col) not in visited and ((row - gap, col) in row_col_list):
#         #     cell.append("Left")
#         #     print(2)
#         # if (row, col + gap) not in visited and ((row, col + gap) in row_col_list):
#         #     cell.append("Down")
#         #     print(3)
#         # if (row, col - gap) not in visited and ((row, col - gap) in row_col_list):
#         #     cell.append("Up")
#         #     print(4)
#
#         if (row + 1, col) not in visited and ((row + 1, col) in row_col_list):
#             cell.append("Right")
#             print(1)
#         if (row - 1, col) not in visited and ((row - 1, col) in row_col_list):
#             cell.append("Left")
#             print(2)
#         if (row, col + 1) not in visited and ((row, col + 1) in row_col_list):
#             cell.append("Down")
#             print(3)
#         if (row, col - 1) not in visited and ((row, col - 1) in row_col_list):
#             cell.append("Up")
#             print(4)
#         if len(cell) > 0:
#             current_cell = (random.choice(cell))
#
#             if current_cell == "Right":
#                 knock_right(win, row * gap, col * gap, gap)
#                 # path[(x + gap, y)] = x, y
#                 row += 1
#                 cell_stack.append((row, col))
#                 visited.append((row, col))
#
#
#             elif current_cell == "Left":
#                 knock_left(win, row * gap, col * gap, gap)
#                 # path[(x - c_width, y)] = x, y
#                 row -= 1
#                 cell_stack.append((row, col))
#                 visited.append((row, col))
#
#
#             elif current_cell == "Up":
#                 knock_up(win, row * gap, col * gap, gap)  # lol
#                 # path[(x, y - c_width)] = x, y
#                 col -= 1
#                 cell_stack.append((row, col))
#                 visited.append((row, col))
#
#
#             elif current_cell == "Down":
#                 knock_down(win, row * gap, col * gap, gap)
#                 # path[(x, y + c_width)] = x, y
#                 col += 1
#                 cell_stack.append((row, col))
#                 visited.append((row, col))
#
#
#         else:
#             row, col = cell_stack.pop()
#             single_cell(win, row * gap, col * gap, gap)
#             visited.append((row, col))
#
#             time.sleep(0.05)
#             recursive_cell(win, row * gap, col * gap, gap)

def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    started = False
    while run:
        draw(win, grid, ROWS, width)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()

                elif not end and spot != start:
                    end = spot
                    end.make_end()

                elif spot != end and spot != start:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()


main(WIN, WIDTH)

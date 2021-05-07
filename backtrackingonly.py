import time
import random
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

Width, Height = 1000, 1000
FPS = 30

# set up pygame
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("MazeFinder")
window = pygame.display.set_mode((Width, Height))
window.fill(WHITE)
pygame.display.update()
clock = pygame.time.Clock()

x = 0  # x cord
y = 0  # y cord
c_width = 40  # cell width
grid = []
visited = []
cell_stack = []
path = {}
time.sleep(2)


def build_grid(x, y, c_width=c_width):
    for i in range(20):
        x = 40
        y = y + 40
        for j in range(20):
            pygame.draw.line(window, BLACK, [x, y], [x + c_width, y], 2)                         # Top Wall
            pygame.draw.line(window, BLACK, [x + c_width, y], [x + c_width, y + c_width], 2)     # Right Wall
            pygame.draw.line(window, BLACK, [x, y], [x, y + c_width], 2)                         # Left Wall
            pygame.draw.line(window, BLACK, [x, y + c_width], [x + c_width, y + c_width], 2)     # Bottom Wall

            grid.append((x, y))
            x = x + 40
            pygame.display.update()


def knock_up(x, y):
    pygame.draw.rect(window, YELLOW, (x + 1, y - c_width + 1, 39, 79), 0)
    pygame.display.update()


def knock_down(x, y):
    pygame.draw.rect(window, YELLOW, (x + 1, y + 1, 39, 79), 0)
    pygame.display.update()


def knock_left(x, y):
    pygame.draw.rect(window, YELLOW, (x - c_width + 1, y + 1, 79, 39), 0)
    pygame.display.update()


def knock_right(x, y):
    pygame.draw.rect(window, YELLOW, (x + 1, y + 1, 79, 39), 0)
    pygame.display.update()


def single_cell(x, y):
    pygame.draw.rect(window, BLUE, (x + 1, y + 1, 38, 38), 0)
    pygame.display.update()


def recursive_cell(x, y):
    pygame.draw.rect(window, YELLOW, (x + 1, y + 1, 38, 38), 0)
    pygame.display.update()


def path_tracker(x, y):
    pygame.draw.rect(window, GREEN, (x + 8, y + 8, 10, 10), 0)
    pygame.display.update()


def maze(x, y):
    single_cell(x, y)
    cell_stack.append((x, y))
    visited.append((x, y))

    while len(cell_stack) > 0:
        time.sleep(0.07)
        cell = []

        if (x + c_width, y) not in visited and (x + c_width, y) in grid:
            cell.append("Right")
        if (x - c_width, y) not in visited and (x - c_width, y) in grid:
            cell.append("Left")
        if (x, y + c_width) not in visited and (x, y + c_width) in grid:
            cell.append("Down")
        if (x, y - c_width) not in visited and (x, y - c_width) in grid:
            cell.append("Up")


        if len(cell) > 0:
            current_cell = (random.choice(cell))

            if current_cell == "Right":
                knock_right(x, y)
                path[(x + c_width, y)] = x, y
                x = x + c_width
                cell_stack.append((x, y))
                visited.append((x, y))

            elif current_cell == "Left":
                knock_left(x, y)
                path[(x - c_width, y)] = x, y
                x = x - c_width
                cell_stack.append((x, y))
                visited.append((x, y))

            elif current_cell == "Up":
                knock_up(x, y)  # lol
                path[(x, y - c_width)] = x, y
                y = y - c_width
                cell_stack.append((x, y))
                visited.append((x, y))

            elif current_cell == "Down":
                knock_down(x, y)
                path[(x, y + c_width)] = x, y
                y = y + c_width
                cell_stack.append((x, y))
                visited.append((x, y))

        else:
            x, y = cell_stack.pop()
            single_cell(x, y)
            time.sleep(0.05)
            recursive_cell(x, y)


def path_tracer(x, y):
    path_tracker(x, y)
    while (x, y) != (40, 40):
        x, y = path[x, y]
        path_tracker(x, y)
        time.sleep(0.1)


x, y = 40, 40

build_grid(40, 0, 40)
maze(x, y)
path_tracer(400, 400)

RUNNING = True
while RUNNING:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
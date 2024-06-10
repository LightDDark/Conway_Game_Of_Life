import numpy as np
import pygame
import time


COLOR_BG = (0, 0, 0)
COLOR_GRID = (40, 40, 40)
COLOR_ALIVE = (255, 255, 255)
SIZE_MULT = 10

ACTIVATED_CELLS = set()


def add_to_set(row, col, set_to_update):
    set_to_update.add((row - 1, col - 1))
    set_to_update.add((row - 1, col))
    set_to_update.add((row - 1, col + 1))
    set_to_update.add((row, col - 1))
    set_to_update.add((row, col))
    set_to_update.add((row, col + 1))
    set_to_update.add((row + 1, col - 1))
    set_to_update.add((row + 1, col))
    set_to_update.add((row + 1, col + 1))


def update(screen, cells, size):
    global ACTIVATED_CELLS
    updated_cells = np.zeros_like(cells, dtype=bool)
    updated_set = set()
    for (row, col) in ACTIVATED_CELLS:
        alive_neighbours = np.sum(cells[row - 1:row + 2, col - 1:col + 2]) - cells[row, col]
        color = COLOR_BG
        if cells[row, col]:
            if 2 <= alive_neighbours <= 3:
                color = COLOR_ALIVE
                add_to_set(row, col, updated_set)
            else:
                updated_cells[row, col] = False
        else:
            if alive_neighbours == 3:
                color = COLOR_ALIVE
                add_to_set(row, col, updated_set)
                updated_cells[row, col] = True

        pygame.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))

    ACTIVATED_CELLS = updated_set
    return updated_cells


def game_loop():
    pygame.init()
    screen = pygame.display.set_mode((80 * SIZE_MULT, 60 * SIZE_MULT))
    cells = np.zeros((60, 80), dtype=bool)
    screen.fill(COLOR_GRID)
    update(screen, cells, SIZE_MULT)
    pygame.display.flip()
    pygame.display.update()
    running = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = not running
                update(screen, cells, SIZE_MULT)
                pygame.display.update()
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                cells[pos[1] // SIZE_MULT, pos[0] // SIZE_MULT] = True
                update(screen, cells, SIZE_MULT)
                pygame.display.update()
            screen.fill(COLOR_GRID)
            if running:
                cells = update(screen, cells, SIZE_MULT)
                pygame.display.update()
            time.sleep(0.1)


if __name__ == '__main__':
    # get command-line args
    game_loop()

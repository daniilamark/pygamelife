import pygame
from random import randint
from copy import deepcopy
import numpy as np
from numba import njit

RES = WIDTH, HEIGHT = 1200, 700
TILE = 5
W, H = WIDTH // TILE, HEIGHT // TILE

FPS = 10

pygame.init()
surface = pygame.display.set_mode(RES)
clock = pygame.time.Clock()

next_field = np.array([[0 for i in range(W)] for j in range(H)])

#current_field = np.array([[randint(0, 1) for i in range(W)] for j in range(H)])

current_field = np.array([[1 if not i % 33 else 0 for i in range(W)] for j in range(H)])

@njit(fastmath=True)
def check_cells(current_field, next_field):
    res = []
    for x in range(1, W - 1):
        for y in range(1, H - 1):
            count = 0
            for j in range(y - 1, y + 2):
                for i in range(x - 1, x + 2):
                    if current_field[j][i] == 1:
                        count += 1
            if current_field[y][x] == 1:
                count -= 1
                if count == 2 or count == 3:
                    next_field[y][x] = 1
                    res.append((x, y))
                else:
                    next_field[y][x] = 0

            else:
                if count == 3:
                    next_field[y][x] = 1
                    res.append((x, y))
                else:
                    next_field[y][x] = 0
    return next_field, res







while True:
    surface.fill(pygame.Color('black'))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    # draw grid
    next_field, res = check_cells(current_field, next_field)
    [pygame.draw.rect(surface, pygame.Color('darkorange'),
                      (x * TILE + 1, y * TILE, TILE - 1, TILE - 1)) for x, y in res]

    current_field = deepcopy(next_field)
    pygame.display.flip()
    clock.tick(FPS)

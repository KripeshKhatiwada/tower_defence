import pygame
import random
from constants import CELL_SIZE, UI_HEIGHT, ROWS, COLS

_grass1 = pygame.image.load("assets/tiles/grass.png")
_grass1 = pygame.transform.scale(_grass1, (CELL_SIZE, CELL_SIZE))
_grass2 = pygame.image.load("assets/tiles/grass_2.png")
_grass2 = pygame.transform.scale(_grass2, (CELL_SIZE, CELL_SIZE))
_road = pygame.image.load("assets/tiles/road.png")
_road = pygame.transform.scale(_road, (CELL_SIZE, CELL_SIZE))
_tree = pygame.image.load("assets/tiles/tree_2.png")
_tree = pygame.transform.scale(_tree, (CELL_SIZE, CELL_SIZE))
_mushroom = pygame.image.load("assets/tiles/mushroom.png")
_mushroom = pygame.transform.scale(_mushroom, (CELL_SIZE, CELL_SIZE))


def draw_background(screen, path):
    random.seed(42)
    placed = set(path)
    for r in range(ROWS):
        for c in range(COLS):
            x = c * CELL_SIZE
            y = r * CELL_SIZE + UI_HEIGHT
    
            if (r, c) in path:
              screen.blit(_road, (x, y))
            else:
                if (r + c) % 2 == 0:
                    screen.blit(_grass1, (x, y))
                else:
                    screen.blit(_grass2, (x, y))
    
    num_decor = (ROWS * COLS) // 20
    for _ in range(num_decor):
        r = random.randrange(ROWS)
        c = random.randrange(COLS)
        if (r, c) in placed:
            continue
        placed.add((r, c))
        img = _tree if random.random() < 0.6 else _mushroom
        screen.blit(img, (c * CELL_SIZE, r * CELL_SIZE + UI_HEIGHT))






    


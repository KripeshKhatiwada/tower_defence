# background.py

import os
import pygame
from constants import CELL_SIZE, ROWS, COLS, UI_HEIGHT

def load_landscape_tiles(folder, count):
    tiles = []
    for i in range(count):
        if i < 10:
            filename = f"landscape_0{i}.png"
        else:
            filename = f"landscape_{i}.png"
        fullpath = os.path.join(folder, filename)
        img = pygame.image.load(fullpath).convert_alpha()
        tiles.append(img)
    return tiles


def draw_background(screen: pygame.Surface, tiles: list[pygame.Surface], tile_map: list[list[int]]) -> None:
    for row in range(ROWS):
        for col in range(COLS):
            idx = tile_map[row][col]
            x = col * CELL_SIZE
            y = row * CELL_SIZE + UI_HEIGHT
            screen.blit(tiles[idx], (x, y))

# background.py

import pygame
import random
from constants import CELL_SIZE, UI_HEIGHT, ROWS, COLS

def scale_sprite(img):
    """Scale sprite so its width matches CELL_SIZE, height proportionally."""
    w, h = img.get_size()
    new_h = int(h * (CELL_SIZE / w))
    return pygame.transform.scale(img, (CELL_SIZE, new_h))

# load & scale ground tiles
_grass         = scale_sprite(pygame.image.load("assets/tiles/grass.png"))
_place_grass   = scale_sprite(pygame.image.load("assets/tiles/place_grass.png"))
_sand          = scale_sprite(pygame.image.load("assets/tiles/sand.png"))
_place_sand    = scale_sprite(pygame.image.load("assets/tiles/place_sand.png"))
_road          = scale_sprite(pygame.image.load("assets/tiles/road.png"))

# load & scale all decorations
_crystal1      = scale_sprite(pygame.image.load("assets/tiles/crystal_1.png"))
_crystal2      = scale_sprite(pygame.image.load("assets/tiles/crystal_2.png"))
_tree1         = scale_sprite(pygame.image.load("assets/tiles/tree_1.png"))
_tree2         = scale_sprite(pygame.image.load("assets/tiles/tree_2.png"))
_stone         = scale_sprite(pygame.image.load("assets/tiles/stone.png"))
_stone_ground  = scale_sprite(pygame.image.load("assets/tiles/stone_ground.png"))
_decoration1   = scale_sprite(pygame.image.load("assets/tiles/decoration_1.png"))

ALL_DECOR      = [
    _crystal1, _crystal2,
    _tree1,    _tree2,
    _stone,    _stone_ground,
    _decoration1
]

def draw_background(screen, path):
    """
    Draws:
     • road along `path`
     • alternating grass/sand tiles elsewhere
     • scattered decorations from ALL_DECOR, bottom-aligned
    """
    random.seed(99)
    occupied = set(path)

    # 1) tile ground
    for r in range(ROWS):
        for c in range(COLS):
            x = c * CELL_SIZE
            y = r * CELL_SIZE + UI_HEIGHT

            if (r, c) in path:
                screen.blit(_road, (x, y))
            else:
                # alternate between grass and sand fills
                if (r + c) % 4 < 2:
                    # alternating grass patterns
                    img = _grass if (r + c) % 2 == 0 else _place_grass
                else:
                    # alternating sand patterns
                    img = _sand if (r + c) % 2 == 0 else _place_sand
                screen.blit(img, (x, y))

    # 2) scatter decorations off-path
    decor_count = (ROWS * COLS) // 12  # adjust density here
    for _ in range(decor_count):
        r = random.randrange(ROWS)
        c = random.randrange(COLS)
        if (r, c) in occupied:
            continue
        occupied.add((r, c))

        img = random.choice(ALL_DECOR)
        w, h = img.get_size()

        # bottom-align the sprite to the tile at (r,c)
        draw_x = c * CELL_SIZE
        draw_y = r * CELL_SIZE + UI_HEIGHT + (CELL_SIZE - h)
        screen.blit(img, (draw_x, draw_y))

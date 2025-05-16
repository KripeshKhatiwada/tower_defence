import pygame
import sys

# Grid and window setup
ROWS, COLS = 16, 16               # Grid size
CELL_SIZE = 40                   # Each cell's pixel size
SIDES = COLS * CELL_SIZE         # Window size (square)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ENEMY_COLOR = (222, 10, 10)
TOWER_COLOR = (0, 200, 255)

# Game state
tower_positions = []
TOWER_RANGE = 2  # Manhattan distance
ENEMY_PATH = [(5, i) for i in range(COLS)]  # Enemy path: row 5 left to right


def draw_grid(screen):
    """Draws the grid lines."""
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(screen, WHITE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SIDES, SIDES))
    pygame.display.set_caption("Tower Defense - v1")

    enemy_pos_index = 0
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(BLACK)
        draw_grid(screen)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                col = mouse_x // CELL_SIZE
                row = mouse_y // CELL_SIZE
                if (row, col) not in tower_positions and (row, col) not in ENEMY_PATH:
                    tower_positions.append((row, col))
                    print(f"Tower placed at ({row}, {col})")

        # Draw towers
        for t_row, t_col in tower_positions:
            pygame.draw.rect(screen, TOWER_COLOR, (t_col * CELL_SIZE, t_row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Move and draw enemy
        if enemy_pos_index < len(ENEMY_PATH):
            enemy_row, enemy_col = ENEMY_PATH[enemy_pos_index]
            pygame.draw.rect(screen, ENEMY_COLOR, (enemy_col * CELL_SIZE, enemy_row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            enemy_pos_index += 1

            # Check for tower detection
            for t_row, t_col in tower_positions:
                dist = abs(t_row - enemy_row) + abs(t_col - enemy_col)
                if dist <= TOWER_RANGE:
                    print(f"Tower at ({t_row},{t_col}) sees enemy at ({enemy_row},{enemy_col})!")

        else:
            enemy_pos_index = 0

        pygame.display.flip()
        clock.tick(4)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

import pygame
import sys

# Grid and window setup
ROWS, COLS = 16, 16               # Number of rows and columns in the grid
CELL_SIZE = 40                   # Size of each cell in pixels
SIDES = COLS * CELL_SIZE         # Window width and height (square)
WHITE = (255, 255, 255)          # Color for grid lines (white)
BLACK = (0, 0, 0)                # Background color (black)
ENEMY_COLOR = (222, 10, 10)      # Color of the enemy (red)

# Enemy path: moves along row 5, from column 0 to 9
ENEMY_PATH = [(5, i) for i in range(COLS)]  

def draw_grid(screen):
    """
    Draws the grid lines on the screen.
    Loops over all rows and columns, drawing a square outline at each cell.
    """
    for row in range(ROWS):
        for col in range(COLS):
            # Draw rectangle border with thickness 1 (just the outline)
            pygame.draw.rect(screen, WHITE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SIDES, SIDES))  # Create window
    pygame.display.set_caption("Tower Defense - vr1")
    
    enemy_pos_index = 0      # Tracks enemy's current position along the path
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(BLACK)    # Clear screen each frame with black background
        draw_grid(screen)     # Draw the grid lines

        # Handle events (like window close)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw the enemy square at its current position on the path
        if enemy_pos_index < len(ENEMY_PATH):
            row, col = ENEMY_PATH[enemy_pos_index]
            pygame.draw.rect(screen, ENEMY_COLOR, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            enemy_pos_index += 1  # Move enemy to next position on next frame
        else:
            enemy_pos_index = 0   # Reset to start of path when done

        pygame.display.flip()   # Update the display
        clock.tick(2)           # Limit frame rate to 2 FPS (enemy moves every 0.5 seconds)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

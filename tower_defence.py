import pygame
import sys
from Enemy_path import generate_enemy_path
from Enemy_Bullets_Class import Enemy, Bullet
from constants import *

ENEMY_PATH = generate_enemy_path(ROWS, COLS)

# Draw grid lines
def draw_grid(screen):
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(
                screen,
                WHITE,
                (col * CELL_SIZE, row * CELL_SIZE + UI_HEIGHT, CELL_SIZE, CELL_SIZE),
                1
            )

def draw_text(screen, text,x,y,font,color=WHITE):
    text_surface= font.render(text,True,color)
    screen.blit(text_surface, (x, y))
# Main game loop
def main():
    pygame.init()
    screen = pygame.display.set_mode((SIDES, SIDES + UI_HEIGHT))
    pygame.display.set_caption("Tower Defense - v3")
    score=0
    lives=5
    font = pygame.font.SysFont("Impact", 36)
    clock = pygame.time.Clock()
    running = True

    tower_positions = []
    TOWER_RANGE = 2

    enemies = []
    bullets = []

    spawn_timer = 0
    spawn_interval = 60  # frames (~1 second)

    enemy_move_timer = 0
    enemy_move_interval = 20  # move every 20 frames

    tower_cooldowns = {}  # (row, col): cooldown value
    tower_fire_interval = 30  # frames between shots

    while running:
        screen.fill(BLACK)
        pygame.draw.rect(screen, LIGHT_BLACK, (0, 0, SIDES, UI_HEIGHT))
        for row, col in ENEMY_PATH:
                pygame.draw.rect(
                screen,
                PATH_COLOR,
                (col * CELL_SIZE, row * CELL_SIZE + UI_HEIGHT, CELL_SIZE, CELL_SIZE)
            )
        draw_grid(screen)

        # Handle events like closing window or clicking
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouse_y -= UI_HEIGHT 
                
                if mouse_y < 0:
                     continue  # Click was on the UI, ignore
                col = mouse_x // CELL_SIZE
                row = mouse_y // CELL_SIZE

                if (row, col) not in tower_positions and (row, col) not in ENEMY_PATH:
                    tower_positions.append((row, col))
                    print(f"Placed tower at ({row}, {col})")

        # Draw towers
        for t_row, t_col in tower_positions:
            pygame.draw.rect(
                screen,
                TOWER_COLOR,
                (t_col * CELL_SIZE, t_row * CELL_SIZE+ UI_HEIGHT, CELL_SIZE, CELL_SIZE)
            )

        # Spawn new enemy every few seconds
        spawn_timer += 1
        if spawn_timer >= spawn_interval:
            enemies.append(Enemy(ENEMY_PATH))
            spawn_timer = 0

        # Move enemies slowly (not every frame)
        enemy_move_timer += 1
        if enemy_move_timer >= enemy_move_interval:
            for enemy in enemies:
                if enemy.is_alive():
                    enemy.move()
            enemy_move_timer = 0

        # Draw enemies
        for enemy in enemies[:]:
            if enemy.is_alive():
                if enemy.row is not None:
                    pygame.draw.rect(
                        screen,
                        ENEMY_COLOR,
                        (enemy.col * CELL_SIZE, enemy.row * CELL_SIZE+ UI_HEIGHT, CELL_SIZE, CELL_SIZE)
                    )
                else:
                    if enemy.row is None:
                        lives -= 1
                        print("Enemy reached the end! Lives left:", lives)
                        enemies.remove(enemy)
  # Reached end
            else:
                score += 1
                print("Enemy destroyed! Score:", score)
                enemies.remove(enemy) # Killed

        # Towers shoot bullets at enemies in range
        for tower in tower_positions:
            # Increase cooldown
            tower_cooldowns[tower] = tower_cooldowns.get(tower, 0) + 1

            # If tower is ready to fire
            if tower_cooldowns[tower] >= tower_fire_interval:
                t_row, t_col = tower

                for enemy in enemies:
                    if enemy.is_alive():
                        dist = abs(enemy.row - t_row) + abs(enemy.col - t_col)
                        if dist <= TOWER_RANGE:
                            bullets.append(Bullet((t_row, t_col), enemy))
                            tower_cooldowns[tower] = 0
                            break

        # Move and draw bullets
        for bullet in bullets[:]:
            hit = bullet.move()
            if hit:
                bullets.remove(bullet)
            else:
                pygame.draw.circle(
                    screen,
                    BULLET_COLOR,
                    (int(bullet.x), int(bullet.y)),
                    5
                )
        draw_text(screen, f"Score: {score}", 10, 10,font)
        draw_text(screen, f"Lives: {lives}", 450, 10, font)
        pygame.display.flip()
        clock.tick(60)  # 60 FPS
        if lives <= 0:
            print("Game Over!")
            running = False


    pygame.quit()
    sys.exit()


# Start the game
if __name__ == "__main__":
    main()

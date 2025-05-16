import pygame
import sys

# Grid and window setup
ROWS = 16
COLS = 16
CELL_SIZE = 40
SIDES = COLS * CELL_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ENEMY_COLOR = (222, 10, 10)
TOWER_COLOR = (0, 200, 255)
BULLET_COLOR = (255, 255, 0)

# Path the enemy follows (row 5, all columns left to right)
ENEMY_PATH = [(5, i) for i in range(COLS)]

# Class for enemies
class Enemy:
    def __init__(self, path):
        self.path = path
        self.pos_index = 0
        self.row, self.col = path[0]
        self.hp = 3  # Hit points

    def move(self):
        if self.pos_index < len(self.path) - 1:
            self.pos_index += 1
            self.row, self.col = self.path[self.pos_index]
        else:
            # Reached the end of the path
            self.row = None
            self.col = None

    def is_alive(self):
        return self.hp > 0


# Class for bullets
class Bullet:
    def __init__(self, tower_pos, target_enemy):
        self.x = tower_pos[1] * CELL_SIZE + CELL_SIZE // 2
        self.y = tower_pos[0] * CELL_SIZE + CELL_SIZE // 2
        self.target = target_enemy
        self.speed = 8

    def move(self):
        if not self.target.is_alive():
            return True  # Bullet disappears if target is dead

        target_x = self.target.col * CELL_SIZE + CELL_SIZE // 2
        target_y = self.target.row * CELL_SIZE + CELL_SIZE // 2

        dx = target_x - self.x
        dy = target_y - self.y

        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance < self.speed or distance == 0:
            # Hit the target
            self.target.hp -= 1
            return True  # Bullet is removed
        else:
            # Move the bullet closer to the target
            self.x += self.speed * dx / distance
            self.y += self.speed * dy / distance
            return False


# Draw grid lines
def draw_grid(screen):
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(
                screen,
                WHITE,
                (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                1
            )


# Main game loop
def main():
    pygame.init()
    screen = pygame.display.set_mode((SIDES, SIDES))
    pygame.display.set_caption("Tower Defense - v3")

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
        draw_grid(screen)

        # Handle events like closing window or clicking
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
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
                (t_col * CELL_SIZE, t_row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
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
                        (enemy.col * CELL_SIZE, enemy.row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    )
                else:
                    enemies.remove(enemy)  # Reached end
            else:
                enemies.remove(enemy)  # Killed

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

        pygame.display.flip()
        clock.tick(60)  # 60 FPS

    pygame.quit()
    sys.exit()


# Start the game
if __name__ == "__main__":
    main()

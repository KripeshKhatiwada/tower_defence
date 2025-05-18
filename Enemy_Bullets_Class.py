from constants import CELL_SIZE, UI_HEIGHT

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
        self.y = tower_pos[0] * CELL_SIZE + CELL_SIZE // 2 + UI_HEIGHT
        self.target = target_enemy
        self.speed = 8

    def move(self):
        if not self.target.is_alive():
            return True  # Bullet disappears if target is dead

        target_x = self.target.col * CELL_SIZE + CELL_SIZE // 2
        target_y = self.target.row * CELL_SIZE + CELL_SIZE // 2 + UI_HEIGHT

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


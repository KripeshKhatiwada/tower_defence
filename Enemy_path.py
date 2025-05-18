import random
from constants import *
def generate_enemy_path(ROWS, COLS):
    sides = ['top', 'bottom', 'left', 'right']
    start_side = random.choice(sides)
    end_side = random.choice([s for s in sides if s != start_side])

    def random_point_on(side):
        if side == 'top':
            return (0, random.randint(0, COLS - 1))
        elif side == 'bottom':
            return (ROWS - 1, random.randint(0, COLS - 1))
        elif side == 'left':
            return (random.randint(0, ROWS - 1), 0)
        elif side == 'right':
            return (random.randint(0, ROWS - 1), COLS - 1)

    start = random_point_on(start_side)
    end = random_point_on(end_side)

    bend_count = random.choice([1, 2])
    bends = []
    for _ in range(bend_count):
        bend = (random.randint(1, ROWS - 2), random.randint(1, COLS - 2))
        bends.append(bend)

    points = [start] + bends + [end]

    path = []
    for i in range(len(points) - 1):
        curr = points[i]
        next_p = points[i + 1]
        temp_path = []

        row1, col1 = curr
        row2, col2 = next_p

        if col1 != col2:
            step = 1 if col2 > col1 else -1
            for c in range(col1, col2 + step, step):
                temp_path.append((row1, c))
        if row1 != row2:
            step = 1 if row2 > row1 else -1
            for r in range(row1 + step, row2 + step, step):
                temp_path.append((r, col2))

        path += temp_path

    return path



from random import randint

import pygame as pg

import sys

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()

# Центр экрана:
CENTER = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))


# Тут опишите все классы игры.
class GameObject:
    """Класс описывает игровые объекты на поле."""

    def __init__(self, body_color=None):
        self.position = CENTER
        self.body_color = body_color

    def draw(self):
        """Рисует игровой объект на поле."""
        raise NotImplementedError('Дочерний класс не реализовал метод draw()')

    def get_rect(self, position):
        """Возвращает объект pygame.Rect с заданной позицией и размером."""
        return pg.Rect(position, (GRID_SIZE, GRID_SIZE))


class Apple(GameObject):
    """Класс описывает Яблоко. Родительский класс — GameObject."""

    def __init__(self, body_color=None):
        super().__init__(body_color)

    def draw(self):
        """Рисует яблоко на игровом поле."""
        rect = self.get_rect(self.position)
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    @staticmethod
    def randomize_position(snake):
        """
        Устанавливает случайное положение яблока на игровом поле,
        а также проверяет, чтобы яблоко не генерировалось внутри тела змеи.
        """
        while True:
            position = (
                randint(0, GRID_WIDTH - GRID_SIZE) * GRID_SIZE,
                randint(0, GRID_HEIGHT - GRID_SIZE) * GRID_SIZE
            )
            if position not in snake.positions:
                return position


class Snake(GameObject):
    """Класс описывает Змею. Родительский класс — GameObject."""

    def __init__(self, body_color=None):
        super().__init__(body_color)
        self.reset()
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self):
        """Отрисовывает змейку на экране, затирая след"""
        # Отрисовка всех сегментов змейки, кроме головы и хвоста
        for position in self.positions[1:-1]:
            rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание хвоста змейки
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def move(self):
        """Обновляет позиции змейки."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head_x = (head_x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_head_y = (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_head_x, new_head_y)
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length + 1:
            self.positions.pop()

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.length = 1
        self.positions = [CENTER]
        self.direction = RIGHT
        self.next_direction = None


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш, чтобы изменить направление."""
    direction_map = {
        pg.K_UP: UP,
        pg.K_DOWN: DOWN,
        pg.K_LEFT: LEFT,
        pg.K_RIGHT: RIGHT
    }
    opposite_direction_map = {
        UP: DOWN,
        DOWN: UP,
        LEFT: RIGHT,
        RIGHT: LEFT
    }
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key in direction_map and direction_map[event.key] \
                    != opposite_direction_map[game_object.direction]:
                game_object.next_direction = direction_map[event.key]


def main():
    """Основная логика программы."""
    # Инициализация pg:
    pg.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake(SNAKE_COLOR)
    apple = Apple(APPLE_COLOR)
    apple.position = apple.randomize_position(snake)

    while True:
        screen.fill(BOARD_BACKGROUND_COLOR)
        clock.tick(SPEED)
        snake.draw()
        apple.draw()
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        snake.update_direction()
        if check_apple_eaten(snake, apple):
            apple.position = apple.randomize_position(snake)
        if check_self_collision(snake):
            snake.reset()
        pg.display.update()


def check_apple_eaten(snake, apple):
    """Проверка, кушает ли голова змейки яблоко."""
    head_position = snake.get_head_position()
    if head_position == apple.position:
        snake.length += 1
        return True
    return False


def check_self_collision(snake):
    """Проверка столкновения змейки с собой."""
    head_position = snake.get_head_position()
    if head_position in snake.positions[4:]:
        snake.reset()
        return True
    return False


if __name__ == '__main__':
    main()

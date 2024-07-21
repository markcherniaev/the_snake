from random import choice, randint

import pygame

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
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()

# Центр экрана:
CENTER = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))


# Тут опишите все классы игры.
class GameObject:
    """Класс описывает игровые объекты на поле"""

    def __init__(self):
        self.position = CENTER
        self.body_color = None

    def draw(self):
        """Рисует игровой объект на поле"""
        pass


class Apple(GameObject):
    """Класс описывает Яблоко. Родительский класс — GameObject"""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position()

    def draw(self):
        """Рисует яблоко на игровом поле"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле"""
        random_x = randint(0, SCREEN_WIDTH - 20)
        random_y = randint(0, SCREEN_HEIGHT - 20)
        return ((random_x), (random_y))


class Snake(GameObject):
    """Класс описывает Змею. Родительский класс — GameObject"""

    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.positions = [CENTER]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self):
        """Отрисовывает змейку на экране, затирая след"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def move(self):
        """Обновляет позиции змейки"""
        self.update_direction()
        head_x, head_y = self.get_head_position()
        new_head_x = (head_x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH
        new_head_y = (head_y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_head_x, new_head_y)
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length + 1:
            self.last = self.positions.pop()
        else:
            self.last = None

    def get_head_position(self):
        """Возвращает позицию головы змейки"""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние"""
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.length = 1
        self.positions = [CENTER]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None

    def check_apple_eaten(self, apple):
        """Проверка, кушает ли голова змейки яблоко"""
        head_x, head_y = self.get_head_position()
        head_right, head_bottom = head_x + GRID_SIZE, head_y + GRID_SIZE
        apple_x, apple_y = apple.position
        apple_right, apple_bottom = apple_x + GRID_SIZE, apple_y + GRID_SIZE
        if not (head_right < apple_x or head_x > apple_right
                or head_bottom < apple_y or head_y > apple_bottom):
            self.length += 1
            apple.position = apple.randomize_position()
            return True
        return False

    def check_self_collision(self):
        """Проверка столкновения змейки с собой"""
        head_position = self.get_head_position()
        if head_position in self.positions[1:]:
            self.reset()


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш, чтобы изменить направление"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная логика программы"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        screen.fill(BOARD_BACKGROUND_COLOR)
        clock.tick(SPEED)
        snake.draw()
        apple.draw()
        handle_keys(snake)
        snake.update_direction()
        snake.check_self_collision()
        pygame.display.update()
        snake.move()
        snake.check_apple_eaten(apple)


if __name__ == '__main__':
    main()

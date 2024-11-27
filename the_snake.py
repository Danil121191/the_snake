from random import choice

import pygame

import sys

# Константы для определения размера игравого поля, а так же размер сетки
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Константы для определения направления движения змейки
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIRECT = [UP, DOWN, LEFT, RIGHT]

# Константы определяющие цвета объектов
BOARD_BACKGROUND_COLOR = (0, 0, 0)

BORDER_COLOR = (93, 216, 228)

APPLE_COLOR = (255, 0, 0)

SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки
SPEED = 20

START_SNAKE_POSITION = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]

ALL_CELLS = []
for i in range(0, SCREEN_WIDTH, GRID_SIZE):
    for j in range(0, SCREEN_HEIGHT, GRID_SIZE):
        ALL_CELLS.append((i, j))


# Настройки игравого окна: задание размера, цвета и названия
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Родительский класс."""

    def __init__(self, position=None, body_color=None):
        """Конструктор класса."""
        self.position = position or START_SNAKE_POSITION
        self.body_color = body_color or APPLE_COLOR

    def draw(self):
        """Медод отрисовки элемента."""

    def draw_object(self, position, body_color):
        """Отрисовка объекта"""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Дочерний класс GameObject, описывающий объект яблоко."""

    def __init__(self, body_color=None):
        if body_color is not None:
            self.body_color = body_color
        else:
            """Переопределение атрибутов родительского класса GameObject."""
            super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Случайное определение позиции яблоко на игровом поле."""
        self.position = choice([x for x in ALL_CELLS
                                if x not in START_SNAKE_POSITION])

    def draw(self):
        """Отрисовка яблока"""
        self.draw_object(self.position, self.body_color)


class Snake(GameObject):
    """Дочерний класс GameObject, описывающий змейку."""

    def __init__(self, body_color=None):
        if body_color is not None:
            self.body_color = body_color
        else:
            super().__init__(body_color=SNAKE_COLOR)
        self.length = 1
        START_SNAKE_POSITION = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.positions = START_SNAKE_POSITION
        self.direction = choice(DIRECT)
        self.next_direction = None
        self.last = None

    def move(self):
        """Метод, отвечающий за движение змейки."""
        head = self.get_head_position()
        x_head = head[0]
        y_head = head[1]

        next_head = ((x_head + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
                     (y_head + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT)
        if len(self.positions) < self.length:
            self.positions.insert(0, next_head)
        elif len(self.positions) == self.length:
            self.positions.insert(0, next_head)
            START_SNAKE_POSITION.insert(0, next_head)
            self.last = self.positions.pop()
            START_SNAKE_POSITION.pop()
        else:
            self.reset()

    def draw(self):
        """Отрисовка змейки."""
        self.draw_object(self.positions[0], self.body_color)

        if self.last:
            """Затирание последенего элемента хвоста змеи."""
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self, next_direction):
        """Метод отвечающий за смену напрвления движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Возвращает начальное состояние, если змейка укусит тело."""
        self.length = 1
        self.positions = START_SNAKE_POSITION
        self.direction = choice(DIRECT)
        self.next_direction = None
        self.last = None
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object):
    """Функция обрабатывающая все события в игре."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            elif event.key == pygame.K_ESCAPE:
                sys.exit()
            game_object.update_direction(game_object.next_direction)


def main():
    """Функция логики игры."""
    pygame.init()
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        pygame.display.update()
        apple.draw()
        snake.draw()
        snake.move()
        if snake.positions[0] == apple.position:
            snake.length += 1
            apple.randomize_position()
        elif snake.positions[0] in snake.positions[1:]:
            snake.reset()


if __name__ == '__main__':
    main()

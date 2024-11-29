import sys
from random import choice, randint

import pygame


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

START_SNAKE_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Настройки игравого окна: задание размера, цвета и названия
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Родительский класс."""

    def __init__(self, position=START_SNAKE_POSITION,
                 body_color=BOARD_BACKGROUND_COLOR):
        """Конструктор класса."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Метод отрисовки элемента."""

    def draw_object(self, position, body_color):
        """Отрисовка объекта"""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Дочерний класс яблоко."""

    def __init__(self, occupided_cells=None, body_color=APPLE_COLOR):
        if occupided_cells is None:
            occupided_cells = []
        super().__init__(body_color=body_color)
        self.randomize_position(occupided_cells)

    def randomize_position(self, occupided_cells):
        """Метод для определения позиции яблока"""
        while True:
            self.position = (
                ((randint(0, SCREEN_WIDTH // GRID_SIZE - 1)) * GRID_SIZE),
                ((randint(0, SCREEN_HEIGHT // GRID_SIZE - 1)) * GRID_SIZE))
            if (self.position not in occupided_cells):
                break

    def draw(self):
        """Метод отрисовки яблока"""
        self.draw_object(self.position, self.body_color)


class Snake(GameObject):
    """Класс описывающий змейку"""

    def __init__(self, position=START_SNAKE_POSITION, body_color=SNAKE_COLOR):
        super().__init__(position, body_color)
        self.length = 1
        self.positions = [self.position]
        self.direction = choice(DIRECT)
        self.next_direction = None
        self.last = None

    def update_direction(self, next_direction):
        """Метод отвечающий за смену напрвления движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод, отвечающий за движение змейки."""
        head = self.get_head_position()
        x_head = head[0]
        y_head = head[1]

        next_head = ((x_head + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
                     (y_head + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT)

        self.positions.insert(0, next_head)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = self.last

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def draw(self):
        """Отрисовка змейки."""
        self.draw_object(self.get_head_position(), self.body_color)

        if self.last:
            """Затирание последенего элемента хвоста змеи."""
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Возвращает начальное состояние, если змейка укусит тело."""
        self.length = 1
        self.positions = [self.position]
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
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        pygame.display.update()
        apple.draw()
        snake.draw()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        elif snake.get_head_position() in snake.positions[4:]:
            snake.reset()


if __name__ == '__main__':
    main()

from random import randint

import pygame

"""Константы для определения размера игравого поля, а так же размер сетки"""
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

"""Константы для определения направления движения змейки"""
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

"""Константы определяющие цвет заднего фона, окантовки,
а так же, цвета объектов"""
BOARD_BACKGROUND_COLOR = (0, 0, 0)

BORDER_COLOR = (93, 216, 228)

APPLE_COLOR = (255, 0, 0)

SNAKE_COLOR = (0, 255, 0)

"""Скорость движения змейки"""
SPEED = 20

"""Настройки игравого окна: задание размера, цвета и названия"""
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """
    Родительский класс от которого наследуются атрибуты:
    позиция на игровом поле и цвет объекта, а так же метод отрисовки объектов
    """

    def __init__(self):
        """Конструктор класса"""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw(self):
        """Медод отрисовки предназначенный для наследования"""
        pass


class Apple(GameObject):
    """Дочерний класс, описывающий объект яблоко"""

    def __init__(self):
        """Переопределение атрибутов родительского класса GameObject"""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position()

    def randomize_position(self):
        """Случайное определение позиции яблоко на игровом поле"""
        return (
            ((randint(0, SCREEN_WIDTH // GRID_SIZE - 1)) * GRID_SIZE),
            ((randint(0, SCREEN_HEIGHT // GRID_SIZE - 1)) * GRID_SIZE)
        )

    def draw(self):
        """Отрисовка яблока"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """
    Дочерний класс Snake, унаследовавший атрибуты и метод
    от родительского класса GameObject
    """

    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self):
        """
        Метод возвращает первоначальные параметры объекта
        Snake при укусе змейки самой себя
        """
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def move(self):
        """
        Метод отвечает за определение положения головы змейки при выходе за
        границы игрового поля, а так же  за определение координаты головы змеи
        и добавление в список positions кортежа из координат х и y
        """
        head = self.get_head_position()
        x_head = head[0]
        y_head = head[1]

        if x_head >= SCREEN_WIDTH:
            x_head = -GRID_SIZE
        elif x_head < 0:
            x_head = SCREEN_WIDTH

        if y_head >= SCREEN_HEIGHT:
            y_head = -GRID_SIZE
        elif y_head < 0:
            y_head = SCREEN_HEIGHT

        if self.direction == RIGHT:
            self.positions.insert(0, (x_head + GRID_SIZE, y_head))
        elif self.direction == LEFT:
            self.positions.insert(0, (x_head - GRID_SIZE, y_head))
        elif self.direction == UP:
            self.positions.insert(0, (x_head, y_head - GRID_SIZE))
        elif self.direction == DOWN:
            self.positions.insert(0, (x_head, y_head + GRID_SIZE))
        self.last = self.positions[-1]

    def draw(self):
        """
        Отрисовка каждого элемента змейки от начала до конца
        не включая последний элемент
        """
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect, 0, 5)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        """Отрисовка головы змеи"""
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            """Затирание последенего элемента хвоста змеи"""
            self.positions = self.positions[:-1]
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self, next_direction):
        """Метод отвечающий за смену напрвления движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]


def handle_keys(game_object):
    """Функция обрабатывающая все события в игре"""
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
    """
    Основная функция где созданы экземпляры классов,
    а так же прописана логика игры
    """
    pygame.init()
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction(snake.next_direction)
        pygame.display.update()
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        snake.move()
        if snake.positions[0] == apple.position:
            snake.positions.append(snake.last)
            apple = Apple()
        elif snake.positions[0] in snake.positions[1:]:
            snake.reset()


if __name__ == '__main__':
    main()

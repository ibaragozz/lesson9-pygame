import pygame
import sys
import math

# Инициализация Pygame
pygame.init()

# Настройка параметров игры
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Basketball Game")

# Цвет фона
BACKGROUND_COLOR = (225, 191, 55)

# Загрузка изображений
ball_img = pygame.image.load("ball.png")
basket_img = pygame.image.load("basket.png")

ball_rect = ball_img.get_rect()
basket_rect = basket_img.get_rect()

# Параметры мяча и корзины
BALL_SPEED_CONSTANT = 15  # Константа силы броска
ball_speed = [0, 0]
ball_pos = [WIDTH // 2, HEIGHT - ball_rect.height // 2]
is_ball_thrown = False
basket_pos = [WIDTH // 2 - basket_rect.width // 2, HEIGHT // 4 + 10]  # Центрирование корзины и смещение вниз на 10 пикселей
basket_speed = 5
score = 0
misses = 0
basket_moving_right = True
max_misses = 10

# Определение границ кольца
ring_top = basket_pos[1] + 100  # Верх кольца (80 пикселей от нижнего края)
ring_bottom = ring_top + 20    # Нижняя граница кольца (примерное значение для высоты кольца)

# Функция для отображения текста на экране
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

# Основной игровой цикл
running = True
while running:
    screen.fill(BACKGROUND_COLOR)  # Фон указанного цвета

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and not is_ball_thrown:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dx = mouse_x - ball_pos[0]
            dy = mouse_y - ball_pos[1]
            distance = math.hypot(dx, dy)
            ball_speed[0] = (dx / distance) * BALL_SPEED_CONSTANT
            ball_speed[1] = (dy / distance) * BALL_SPEED_CONSTANT
            is_ball_thrown = True

    # Обновление позиции мяча
    if is_ball_thrown:
        ball_pos[0] += ball_speed[0]
        ball_pos[1] += ball_speed[1]

        # Проверка на столкновение с вертикальными границами экрана
        if ball_pos[0] <= 0 or ball_pos[0] >= WIDTH:
            ball_speed[0] = -ball_speed[0]

        # Проверка на столкновение с потолком
        if ball_pos[1] <= 0:
            ball_speed[1] = -ball_speed[1]  # Отскок от потолка

        # Проверка на попадание в нижнюю часть корзины (отскок)
        if (basket_pos[0] < ball_pos[0] < basket_pos[0] + basket_rect.width and
            ring_top < ball_pos[1] < ring_bottom):
            ball_speed[1] = -ball_speed[1]  # Отскок от нижней части кольца

        # Проверка на попадание в корзину сверху (засчитывание очка)
        if (basket_pos[0] < ball_pos[0] < basket_pos[0] + basket_rect.width and
            ball_pos[1] < ring_top and
            ball_speed[1] < 0):  # Мяч должен двигаться вверх
            score += 1
            is_ball_thrown = False
            ball_pos = [WIDTH // 2, HEIGHT - ball_rect.height // 2]
            ball_speed = [0, 0]
            basket_speed *= 1.05  # Увеличение скорости на 5%

        # Проверка на промах
        elif ball_pos[1] > HEIGHT:
            is_ball_thrown = False
            ball_pos = [WIDTH // 2, HEIGHT - ball_rect.height // 2]
            ball_speed = [0, 0]
            misses += 1

    # Обновление позиции корзины
    if basket_moving_right:
        basket_pos[0] += basket_speed
        if basket_pos[0] > WIDTH - basket_rect.width:
            basket_moving_right = False
    else:
        basket_pos[0] -= basket_speed
        if basket_pos[0] < 0:
            basket_moving_right = True

    # Отрисовка объектов
    basket_rect.topleft = basket_pos
    screen.blit(basket_img, basket_rect)
    screen.blit(ball_img, (ball_pos[0] - ball_rect.width // 2, ball_pos[1] - ball_rect.height // 2))

    # Отображение счета и промахов
    font = pygame.font.Font(None, 36)
    draw_text(f"Score: {score}", font, (0, 0, 0), screen, WIDTH // 2 - 100, 50)
    draw_text(f"Misses: {misses}", font, (0, 0, 0), screen, WIDTH // 2 + 100, 50)

    # Проверка на окончание игры
    if misses >= max_misses:
        draw_text(f"Game Over. Final Score: {score}", font, (255, 0, 0), screen, WIDTH // 2, HEIGHT // 2)
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    pygame.display.flip()
    pygame.time.Clock().tick(60)

# Завершение игры
pygame.quit()
sys.exit()

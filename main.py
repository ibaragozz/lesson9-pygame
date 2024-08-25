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
ball_speed = [0, 0]
ball_pos = [WIDTH // 2, HEIGHT - ball_rect.height // 2]
is_ball_thrown = False
basket_pos = [WIDTH // 2, HEIGHT // 4]
basket_speed = 5
score = 0
misses = 0
basket_moving_right = True
max_misses = 10

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
            ball_speed[0] = (mouse_x - ball_pos[0]) / 10
            ball_speed[1] = (mouse_y - ball_pos[1]) / 10
            is_ball_thrown = True

    # Обновление позиции мяча
    if is_ball_thrown:
        ball_pos[0] += ball_speed[0]
        ball_pos[1] += ball_speed[1]

        # Проверка на столкновение с потолком
        if ball_pos[1] <= 0:
            ball_speed[1] = -ball_speed[1]  # Отскок от потолка

        # Проверка на попадание в корзину
        if basket_rect.collidepoint(ball_pos[0], ball_pos[1]):
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

    # Отображение счета
    font = pygame.font.Font(None, 36)
    draw_text(f"Score: {score}", font, (0, 0, 0), screen, WIDTH // 2, 50)

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

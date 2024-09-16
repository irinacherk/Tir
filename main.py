import pygame
import random

# Инициализация Pygame
pygame.init()

# Задаем размеры экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Задаем название окна
pygame.display.set_caption("Игра Тир")

# Задаем параметры мяча
ball_radius = 40  # Радиус мяча
ball_x = random.randint(ball_radius, SCREEN_WIDTH - ball_radius)
ball_y = random.randint(ball_radius, SCREEN_HEIGHT - ball_radius)

# Начальная скорость движения мяча
speed_x = 5
speed_y = 5

# Задаем начальный счет
score = 0

# Задаем шрифт для отображения текста
font = pygame.font.Font(None, 36)

# Устанавливаем темно-синий цвет фона
background_color = (0, 0, 128)
hit_background_color = (255, 255, 0)  # Желтый фон при попадании

# Ограничение FPS
clock = pygame.time.Clock()
FPS = 60  # Количество кадров в секунду

# Таймер на 30 секунд
start_time = pygame.time.get_ticks()  # Запоминаем стартовое время
game_duration = 30000  # Длительность игры в миллисекундах (30 секунд)

# Флаг для изменения цвета фона
flash_timer = 0
flash_duration = 200  # Длительность вспышки в миллисекундах

# Функция для отрисовки мяча
def draw_ball(x, y, radius):
    pygame.draw.circle(screen, (255, 255, 255), (x, y), radius)  # Белый круг как основа мяча
    pygame.draw.circle(screen, (0, 0, 0), (x, y), radius, 5)  # Черная окантовка
    pygame.draw.line(screen, (0, 0, 0), (x - radius, y), (x + radius, y), 5)  # Горизонтальная полоса
    pygame.draw.line(screen, (0, 0, 0), (x, y - radius), (x, y + radius), 5)  # Вертикальная полоса

# Основной цикл игры
running = True
game_over = False
while running:
    # Заполняем экран темно-синим фоном, если нет вспышки
    if pygame.time.get_ticks() - flash_timer < flash_duration:
        screen.fill(hit_background_color)
    else:
        screen.fill(background_color)

    # Проверяем, не истекло ли время
    elapsed_time = pygame.time.get_ticks() - start_time
    if elapsed_time >= game_duration:
        game_over = True  # Время вышло
        running = False

    # Обрабатываем события
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Проверяем, попала ли мышь в мяч
            distance = ((ball_x - mouse_x) ** 2 + (ball_y - mouse_y) ** 2) ** 0.5
            if distance <= ball_radius:
                score += 1  # Увеличиваем счет при попадании
                flash_timer = pygame.time.get_ticks()  # Начинаем вспышку
                ball_x = random.randint(ball_radius, SCREEN_WIDTH - ball_radius)
                ball_y = random.randint(ball_radius, SCREEN_HEIGHT - ball_radius)
                speed_x += 0.5  # Увеличиваем скорость при попадании
                speed_y += 0.5

    # Двигаем мяч
    ball_x += speed_x
    ball_y += speed_y

    # Проверяем, не выходит ли мяч за границы экрана
    if ball_x - ball_radius <= 0 or ball_x + ball_radius >= SCREEN_WIDTH:
        speed_x = -speed_x
    if ball_y - ball_radius <= 0 or ball_y + ball_radius >= SCREEN_HEIGHT:
        speed_y = -speed_y

    # Рисуем мяч
    draw_ball(ball_x, ball_y, ball_radius)

    # Отображаем счет
    text = font.render(f'Score: {score}', True, (255, 255, 255))  # Белый текст для лучшей видимости
    screen.blit(text, (10, 10))

    # Отображаем оставшееся время
    time_left = (game_duration - elapsed_time) // 1000
    time_text = font.render(f'Time Left: {time_left}', True, (255, 255, 255))
    screen.blit(time_text, (SCREEN_WIDTH - 200, 10))

    # Обновляем экран
    pygame.display.update()

    # Ограничиваем количество кадров в секунду
    clock.tick(FPS)

# Показываем финальный экран с результатом
screen.fill(background_color)
final_text = font.render(f'Game Over! Your score: {score}', True, (255, 255, 255))
screen.blit(final_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
pygame.display.update()
pygame.time.wait(3000)  # Показываем экран с результатом в течение 3 секунд

# Завершаем Pygame
pygame.quit()

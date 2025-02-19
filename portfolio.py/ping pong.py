import pygame
import random

# Inicializace Pygame
pygame.init()

# Velikost okna
width, height = 800, 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong")

# Barvy
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Nastavení pálky a míčku
paddle_width, paddle_height = 15, 100
ball_radius = 10

# Rychlost pálky a míčku
paddle_speed = 15
ball_speed_x = 7
ball_speed_y = 7

# Pozice pálky a míčku
left_paddle = pygame.Rect(50, height//2 - paddle_height//2, paddle_width, paddle_height)
right_paddle = pygame.Rect(width - 50 - paddle_width, height//2 - paddle_height//2, paddle_width, paddle_height)
ball = pygame.Rect(width//2 - ball_radius//2, height//2 - ball_radius//2, ball_radius*2, ball_radius*2)

# Rychlost pohybu pálky
left_paddle_speed = 0
right_paddle_speed = 0

# Skóre
left_score = 0
right_score = 0
font = pygame.font.SysFont('Arial', 30)

# Hlavní herní smyčka
run = True
while run:
    pygame.time.delay(30)  # Ovlivní rychlost hry

    # Zpracování událostí
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Ovládání pálky
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle_speed = -paddle_speed
    elif keys[pygame.K_s] and left_paddle.bottom < height:
        left_paddle_speed = paddle_speed
    else:
        left_paddle_speed = 0

    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle_speed = -paddle_speed
    elif keys[pygame.K_DOWN] and right_paddle.bottom < height:
        right_paddle_speed = paddle_speed
    else:
        right_paddle_speed = 0

    left_paddle.y += left_paddle_speed
    right_paddle.y += right_paddle_speed

    # Pohyb míčku
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Kolize s horní a dolní hranicí
    if ball.top <= 0 or ball.bottom >= height:
        ball_speed_y = -ball_speed_y

    # Kolize s pálkami
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_speed_x = -ball_speed_x

    # Gól
    if ball.left <= 0:
        right_score += 1
        ball.x = width//2 - ball_radius//2
        ball_speed_x = -ball_speed_x
    elif ball.right >= width:
        left_score += 1
        ball.x = width//2 - ball_radius//2
        ball_speed_x = -ball_speed_x

    # Vykreslení
    win.fill(BLACK)
    pygame.draw.rect(win, WHITE, left_paddle)
    pygame.draw.rect(win, WHITE, right_paddle)
    pygame.draw.ellipse(win, WHITE, ball)

    # Zobrazení skóre
    score_text = font.render(f"{left_score} - {right_score}", True, WHITE)
    win.blit(score_text, (width//2 - score_text.get_width()//2, 20))

    pygame.display.update()

# Ukončení hry
pygame.quit()
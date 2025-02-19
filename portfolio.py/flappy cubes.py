import pygame
import random

# Inicializace Pygame
pygame.init()

# Nastavení obrazovky
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

# Barvy
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)  # Světle modrá
DARK_BLUE = (0, 0, 139)  # Tmavě modrá
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Nastavení hodin
clock = pygame.time.Clock()

# Počáteční pozice a nastavení pro ptáka
bird_width = 40
bird_height = 40
bird_x = screen_width // 4
bird_y = screen_height // 2
bird_velocity = 0
gravity = 1
jump_strength = -15

# Počáteční pozice pro potrubí
pipe_width = 70
pipe_gap = 150
pipe_velocity = 4
pipes = []

# Nastavení fontu pro text
font = pygame.font.SysFont("Arial", 36)

# Funkce pro vykreslení ptáka
def draw_bird(x, y):
    pygame.draw.rect(screen, BLUE, (x, y, bird_width, bird_height))

# Funkce pro vykreslení potrubí
def draw_pipes(pipes):
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, pipe['top'])
        pygame.draw.rect(screen, GREEN, pipe['bottom'])

# Funkce pro zobrazení "Game Over" textu
def display_game_over():
    game_over_text = font.render("Game Over", True, BLACK)
    screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 3))

# Funkce pro zobrazení skóre
def draw_score(score):
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

# Funkce pro přidání nového potrubí
def add_pipe():
    height = random.randint(100, screen_height - pipe_gap - 100)
    top = pygame.Rect(screen_width, 0, pipe_width, height)
    bottom = pygame.Rect(screen_width, height + pipe_gap, pipe_width, screen_height - height - pipe_gap)
    return {'top': top, 'bottom': bottom}

# Funkce pro vykreslení pozadí s obláčky
def draw_background(offset):
    # Vykreslení tmavě modrého pozadí
    screen.fill(DARK_BLUE)

    # Vykreslení světle modrých "kostek"
    for i in range(0, screen_width, 100):
        pygame.draw.rect(screen, LIGHT_BLUE, (i + offset, 50, 100, 100))  # Kostky v pozadí

    # Vykreslení obláčků
    for i in range(0, screen_width, 300):
        pygame.draw.ellipse(screen, WHITE, (i + offset, 100, 120, 60))  # Obláčky na různých pozicích

# Hlavní herní smyčka
def game_loop():
    global bird_y, bird_velocity, pipes
    bird_y = screen_height // 2  # Reset pozice ptáka na začátku
    bird_velocity = 0  # Reset rychlosti ptáka
    pipes = []  # Prázdný seznam pro potrubí
    score = 0  # Počáteční skóre
    game_over = False
    background_offset = 0  # Počáteční posun pro pozadí

    while True:
        screen.fill(WHITE)  # Barva pozadí

        # Zpracování událostí
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    # Pokud není hra ukončena, pták vyskočí
                    bird_velocity = jump_strength

        # Pohyb ptáka
        bird_velocity += gravity
        bird_y += bird_velocity

        # Přidání potrubí
        if not game_over:
            if len(pipes) == 0 or pipes[-1]['top'].right < screen_width - 200:
                pipes.append(add_pipe())

        # Pohyb potrubí
        for pipe in pipes:
            pipe['top'].x -= pipe_velocity
            pipe['bottom'].x -= pipe_velocity

        # Odstranění potrubí, která jsou mimo obrazovku
        pipes = [pipe for pipe in pipes if pipe['top'].right > 0]

        # Kontrola kolize s potrubím
        bird_rect = pygame.Rect(bird_x, bird_y, bird_width, bird_height)
        for pipe in pipes:
            if bird_rect.colliderect(pipe['top']) or bird_rect.colliderect(pipe['bottom']):
                game_over = True

        # Kontrola, jestli pták nevyletěl mimo obrazovku
        if bird_y < 0 or bird_y > screen_height - bird_height:
            game_over = True

        # Vykreslení pozadí
        draw_background(background_offset)
        background_offset -= 2  # Pozadí se pohybuje

        if background_offset <= -screen_width:
            background_offset = 0  # Resetovat pozadí, když dosáhne konce

        # Vykreslení ptáka
        draw_bird(bird_x, bird_y)

        # Vykreslení potrubí
        draw_pipes(pipes)

        # Vykreslení skóre
        draw_score(score)

        # Pokud hra skončila, zobrazí se text o "Game Over"
        if game_over:
            display_game_over()

        # Pokud hra skončila, začni znovu hned po malé pauze
        if game_over:
            pygame.display.update()
            pygame.time.wait(1000)  # Pauza 1 sekundu pro "Game Over"
            return game_loop()  # Restartování hry

        # Aktualizace obrazovky
        pygame.display.update()

        # FPS nastavení
        clock.tick(60)

# Spuštění hry
game_loop()

# Ukončení Pygame
pygame.quit()
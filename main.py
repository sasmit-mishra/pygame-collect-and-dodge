import pygame
import random
import sys
import os

# Initialize pygame
pygame.init()

infoObject = pygame.display.Info()
WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (100, 100, 100)
BLUE = (0, 120, 255)
ORANGE = (255, 165, 0)
DARK_GRAY = (40, 40, 40)
LIGHT_RED = (255, 100, 100)
LIGHT_GREEN = (100, 255, 100)

# Screen and fonts
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Collect and Dodge")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 36)

# Base directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, "assets", "images")
SND_DIR = os.path.join(BASE_DIR, "assets", "sounds")

# Load and scale images
def add_padding(image, padding=5):
    w, h = image.get_size()
    new_img = pygame.Surface((w + 2 * padding, h + 2 * padding), pygame.SRCALPHA)
    new_img.blit(image, (padding, padding))
    return new_img

player_img = pygame.image.load(os.path.join(IMG_DIR, "player.png")).convert_alpha()
player_img = add_padding(player_img)
player_img = pygame.transform.scale(player_img, (80, 80))

enemy_img = pygame.image.load(os.path.join(IMG_DIR, "enemy.png")).convert_alpha()
enemy_img = add_padding(enemy_img)
enemy_img = pygame.transform.scale(enemy_img, (80, 80))

item_img = pygame.image.load(os.path.join(IMG_DIR, "item.png")).convert_alpha()
item_img = pygame.transform.scale(item_img, (160, 160))

skull_img = pygame.image.load(os.path.join(IMG_DIR, "skull.png")).convert_alpha()
skull_img = pygame.transform.scale(skull_img, (100, 85))

# Sounds
collect_sound = pygame.mixer.Sound(os.path.join(SND_DIR, "collect.wav"))
gameover_sound = pygame.mixer.Sound(os.path.join(SND_DIR, "gameover.wav"))
pygame.mixer.music.load(os.path.join(SND_DIR, "background_music.mp3"))
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)

# Game state
player = pygame.Rect(WIDTH // 2, HEIGHT - 120, 80, 80)
player_speed = 4
player_speed_limit = 7

item = pygame.Rect(random.randint(50, WIDTH - 100), random.randint(100, HEIGHT - 100), 60, 60)

level = 1
score = 0

highscore_file = os.path.join(BASE_DIR, "highscore.txt")
if os.path.exists(highscore_file):
    with open(highscore_file, 'r') as f:
        highscore = int(f.read())
else:
    highscore = 0

enemy_size = 80
scoreboard_height = 100
enemy_start_y = scoreboard_height + 10
enemy_speed = 3

def generate_enemy():
    return pygame.Rect(random.randint(50, WIDTH - 100), enemy_start_y, enemy_size, enemy_size)

enemies = [generate_enemy() for _ in range(5)]

# Buttons
btn_width = 200
btn_height = 60
btn_margin = 20
top_y = (scoreboard_height - btn_height) // 2

howtoplay_button = pygame.Rect(btn_margin, top_y, btn_width, btn_height)
pause_button = pygame.Rect(WIDTH - btn_width * 2 - btn_margin * 2, top_y, btn_width, btn_height)
exit_button = pygame.Rect(WIDTH - btn_width - btn_margin, top_y, btn_width, btn_height)

# Flags
game_over = False
fullscreen = False
paused = False
show_howtoplay = False

# Helpers
def reset_item():
    return pygame.Rect(random.randint(50, WIDTH - 100), random.randint(enemy_start_y + 10, HEIGHT - 100), 60, 60)

def draw_text(text, color, x, y, size=48):
    temp_font = pygame.font.SysFont(None, size)
    img = temp_font.render(text, True, color)
    screen.blit(img, (x, y))

def restart_game():
    global level, score, enemy_speed, player_speed, enemies, player, game_over
    level = 1
    score = 0
    enemy_speed = 3
    player_speed = 4
    enemies = [generate_enemy() for _ in range(3)]
    player.midbottom = (WIDTH // 2, HEIGHT - 30)
    pygame.mixer.music.play(-1)
    game_over = False

# Main loop
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_p:
                paused = not paused
                if paused:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
            if event.key == pygame.K_RETURN and game_over:
                restart_game()
            if event.key == pygame.K_F11:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_over:
                restart_btn = pygame.Rect(WIDTH // 2 - 220, HEIGHT // 2 + 60, 170, 50)
                exit_btn = pygame.Rect(WIDTH // 2 + 40, HEIGHT // 2 + 60, 170, 50)
                if restart_btn.collidepoint(event.pos):
                    restart_game()
                elif exit_btn.collidepoint(event.pos):
                    running = False
            else:
                if howtoplay_button.collidepoint(event.pos):
                    show_howtoplay = not show_howtoplay
                elif exit_button.collidepoint(event.pos):
                    running = False
                elif pause_button.collidepoint(event.pos):
                    paused = not paused
                    if paused:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()

    if not paused and not game_over and not show_howtoplay:
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player.left > 0:
            player.x -= min(player_speed, player_speed_limit)
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player.right < WIDTH:
            player.x += min(player_speed, player_speed_limit)
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and player.top > enemy_start_y:
            player.y -= min(player_speed, player_speed_limit)
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player.bottom < HEIGHT:
            player.y += min(player_speed, player_speed_limit)

        for enemy in enemies:
            enemy.y += enemy_speed
            if enemy.top > HEIGHT:
                enemy.x = random.randint(50, WIDTH - 100)
                enemy.y = enemy_start_y

        if player.colliderect(item):
            score += 10
            collect_sound.play()
            item = reset_item()

        for enemy in enemies:
            if player.colliderect(enemy):
                gameover_sound.play()
                pygame.mixer.music.pause()
                game_over = True
                if score > highscore:
                    highscore = score
                    with open(highscore_file, 'w') as f:
                        f.write(str(highscore))
                break

        if score // 50 > level - 1:
            level += 1
            enemy_speed += 1
            player_speed += 1
            enemies = [generate_enemy() for _ in range(level + 2)]

    pygame.draw.line(screen, WHITE, (0, scoreboard_height), (WIDTH, scoreboard_height), 2)
    pygame.draw.rect(screen, GRAY, howtoplay_button, border_radius=8)
    draw_text("How to Play", BLACK, howtoplay_button.x + 10, howtoplay_button.y + 10, 30)
    pygame.draw.rect(screen, GRAY, pause_button, border_radius=8)
    draw_text("Pause", BLACK, pause_button.x + 30, pause_button.y + 10, 30)
    pygame.draw.rect(screen, GRAY, exit_button, border_radius=8)
    draw_text("Exit", BLACK, exit_button.x + 45, exit_button.y + 10, 30)
    draw_text(f"Highscore: {highscore}   Score: {score}   Level: {level}", WHITE, WIDTH // 2 - 220, top_y + 10, 30)

    if show_howtoplay:
        pygame.draw.rect(screen, (0, 0, 0), (0, scoreboard_height, 400, HEIGHT))
        draw_text("How to Play:", GREEN, 20, scoreboard_height + 20, 40)
        rules = [
            "1. Use WASD or Arrow keys to move",
            "2. Avoid enemies",
            "3. Collect green items",
            "4. Score increases by 10 per item",
            "5. Level increases every 50 points"
        ]
        for i, rule in enumerate(rules):
            draw_text(rule, WHITE, 20, scoreboard_height + 80 + i * 40, 28)
    elif not game_over:
        screen.blit(player_img, (player.x, player.y))
        for enemy in enemies:
            screen.blit(enemy_img, (enemy.x, enemy.y))
        screen.blit(item_img, (item.x, item.y))

    if paused:
        draw_text("PAUSED", RED, WIDTH // 2 - 100, HEIGHT // 2)

    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        screen.blit(skull_img, (WIDTH // 2 - 62, HEIGHT // 2 - 200))
        draw_text("GAME OVER", ORANGE, WIDTH // 2 - 150, HEIGHT // 2 - 100, 64)
        score_line = f"Your Score: {score}    |    High Score: {highscore}"
        draw_text(score_line, WHITE, WIDTH // 2 - 200, HEIGHT // 2 - 20, 30)
        restart_btn = pygame.Rect(WIDTH // 2 - 220, HEIGHT // 2 + 60, 170, 50)
        exit_btn = pygame.Rect(WIDTH // 2 + 40, HEIGHT // 2 + 60, 170, 50)
        pygame.draw.rect(screen, LIGHT_GREEN, restart_btn)
        pygame.draw.rect(screen, LIGHT_RED, exit_btn)
        draw_text("Restart", BLACK, restart_btn.x + 30, restart_btn.y + 10, 36)
        draw_text("Exit", BLACK, exit_btn.x + 55, exit_btn.y + 10, 36)
        draw_text("Press Enter", WHITE, restart_btn.centerx - 60, restart_btn.bottom + 10, 24)
        draw_text("Press Esc", WHITE, exit_btn.centerx - 50, exit_btn.bottom + 10, 24)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

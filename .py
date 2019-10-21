"""Block Dodge, coded by Archie Piket"""

# Importing modules
import pygame
import random
import sys
import time

# Initialize the game
pygame.init()

WIDTH = 800
HEIGHT = 600

RED = (255, 0, 0)
BLUE = (0, 100, 0)
YELLOW = (255, 255, 0)
BACKGROUND_COLOUR = (0, 0, 40)

player_size = 40
player_pos = [380, HEIGHT-2*player_size]

enemy_size = 50
enemy_pos = [random.randint(0, WIDTH-enemy_size), 0]
enemy_list = [enemy_pos]

SPEED = 10

score = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT))

game_over = False

clock = pygame.time.Clock()

myFont = pygame.font.SysFont("monospace", 35)


def set_level(score, SPEED):
    if score < 10:
        SPEED = 2
    elif score < 20:
        SPEED = 3
    elif score < 30:
        SPEED = 4
    elif score < 40:
        SPEED = 5
    elif score < 50:
        SPEED = 6
    elif score < 80:
        SPEED = 7
    elif score < 100:
        SPEED = 9
    elif score < 150:
        SPEED = 11
    elif score < 200:
        SPEED = 15
    else:
        SPEED = 30
    return SPEED


def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < 8 and delay < 0.1:
        x_pos = random.randint(0, WIDTH-enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])


def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        pygame.draw.rect(screen, BLUE, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))


def update_enemy_positions(enemy_list, score):
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT:
            enemy_pos[1] += SPEED
        else:
            enemy_list.pop(idx)
            score += 1
    return score


def collision_check(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if detect_collision(enemy_pos, player_pos):
            time.sleep(4)
            return True
    return False


def detect_collision(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]
    if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x + enemy_size)):
        if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y + enemy_size)):
            return True
    return False


while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            x = player_pos[0]
            y = player_pos[1]
            if event.key == pygame.K_LEFT and player_pos[0] > 25:
                x -= player_size
            elif event.key == pygame.K_RIGHT and player_pos[0] < 725:
                x += player_size
            elif event.key == pygame.K_UP:
                y -= player_size
            elif event.key == pygame.K_DOWN:
                y += player_size

            player_pos = [x, y]

    screen.fill(BACKGROUND_COLOUR)

    if detect_collision(player_pos, enemy_pos):
        game_over = True

    drop_enemies(enemy_list)
    score = update_enemy_positions(enemy_list, score)
    SPEED = set_level(score, SPEED)

    text = "Score:" + str(score)
    label = myFont.render(text, 1, YELLOW)

    screen.blit(label, (WIDTH-200, HEIGHT-40))

    if collision_check(enemy_list, player_pos):
        game_over = True
        break
    draw_enemies(enemy_list)

    player = pygame.draw.rect(screen, RED, (player_pos[0], player_pos[1], player_size, player_size))

    clock.tick(30)

    pygame.display.update()

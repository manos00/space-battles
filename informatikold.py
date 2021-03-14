import pygame
import random
import math
import time

from pygame import display

# INITIALIZE

pygame.init()

# CREATE WINDOW

window = pygame.display.set_mode((800, 600))

running = True
alive = True  # false

pygame.display.set_caption('iNfOrMaTiK pRoJeKt')
icon = pygame.image.load('img/icon.png')
pygame.display.set_icon(icon)

background = pygame.image.load('img/background.png')

# ENTITIES

playerIMG = pygame.image.load('img/spaceship.png')
# Icon made by dDara from www.flaticon.com
playerX = 400 - 64/2
playerY = 480
playerXchange = 0
playerYchange = 0

enemyIMG = []
enemyX = []
enemyY = []
enemyXchange = []
enemyYchange = []
enemy_count = 10

for i in range(enemy_count):
    enemyIMG.append(pygame.image.load('img/enemy.png'))
    # Icon made by dDara from www.flaticon.com
    enemyX.append(random.randint(0, 800-64))
    enemyY.append(random.randint(50, 150))
    enemyXchange.append(0.15)
    enemyYchange.append(0.04)

bulletIMG = pygame.image.load('img/bullet.png')
bulletX = 0
bulletY = 480
bulletXchange = 0
bulletYchange = -1
bullet_state = 'ready'

score = 0

font = pygame.font.Font('arial.ttf', 25)
font2 = pygame.font.Font('arial.ttf', 45)
textX = 10
textY = 10

click = False

# METHODS


def player(x, y):
    window.blit(playerIMG, (x, y))


def enemy(x, y):
    window.blit(enemyIMG[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    window.blit(bulletIMG, (x + 32, y + 10))


def collision_detection_bullet(enemyX, enemyY, bulletX, bulletY):
    coll_bullet = math.sqrt((math.pow(enemyX - bulletX, 2)) +
                            math.pow(enemyY - bulletY, 2))
    if coll_bullet < 27:
        return True
    else:
        return False


def collision_detection_player(playerX, playerY, enemyX, enemyY):
    coll_enemy = math.sqrt((math.pow(playerX - enemyX, 2)) +
                           math.pow(playerY - enemyY, 2))
    if coll_enemy < 32:
        return True
    else:
        return False


def score_text(x, y):
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    window.blit(score_text, (x, y))


def final_score():
    score_text = font2.render(
        f'You scored {score} points this round!', True, (255, 255, 255))
    window.blit(score_text, (200, 250))


def menu():
    global running
    running = True
    global alive
    alive = False
    while running and not alive:

        window.fill((0, 0, 0))
        window.blit(background, (0, 0))

        window.blit(
            (font2.render('Start Game', True, (255, 255, 255))), (50, 50))

        mx, my = pygame.mouse.get_pos()

        button1 = pygame.Rect(30, 45, 280, 60)
        pygame.draw.rect(background, (255, 0, 0), button1)

        if button1.collidepoint((mx, my)):
            if click:
                alive = True
                pass

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()


def game_over():
    window.fill((0, 0, 0))
    window.blit(background, (0, 0))
    final_score()
    pygame.display.update()
    global alive
    alive = False
    time.sleep(3)


# (400-(14*0.75)*(12.5+len(strscore)/2), 300)
# WHILE LOOP TO KEEP WINDOW OPEN / KEEP PROGRAM RUNNING

while running and alive:
    # window.fill((52, 235, 177))
    window.fill((0, 0, 0))
    window.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerXchange = -0.5
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerXchange = 0.5
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bulletX = playerX - 16
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerXchange = 0

    playerX += playerXchange
    if playerX <= 0:
        playerX = 0
    if playerX >= 800 - 64:
        playerX = 800 - 64

    for i in range(enemy_count):
        enemyX[i] += enemyXchange[i]
        if enemyX[i] <= 0:
            enemyXchange[i] = 0.1
        if enemyX[i] >= 800 - 64:
            enemyXchange[i] = -0.1
        enemyY[i] += enemyYchange[i]

        collision_bullet = collision_detection_bullet(
            enemyX[i], enemyY[i], bulletX, bulletY)
        if collision_bullet:
            bulletY = 480
            bullet_state = 'ready'
            score += 1
            # print(score)
            enemyX[i] = random.randint(0, 800-64)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i])

        collision_player = collision_detection_player(
            playerX, playerY, enemyX[i], enemyY[i])

        if enemyY[i] >= 600 + 16 or collision_player:
            # print(f'Your final score is {score}!')
            for j in range(enemy_count):
                enemyXchange[j] = 0
                enemyYchange[j] = 0
                enemyX[j] = 1000
                enemyY[j] = -1000
            game_over()

    # if enemyY <= 50:
    #     enemyYchange = 0.01
    # if enemyY >= 150:
    #     enemyYchange = -0.01

    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY += bulletYchange

    if bulletY <= -32:
        bulletY = 480
        bullet_state = 'ready'

    player(playerX, playerY)
    score_text(textX, textY)
    pygame.display.update()


# menu()

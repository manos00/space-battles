import pygame
import random
import math
import time
import sqlite3

from pygame import display

pygame.init()

window = pygame.display.set_mode((800, 600))

running = True
alive = False

pygame.display.set_caption('iNfOrMaTiK pRoJeKt')
icon = pygame.image.load('img/icon.png')
pygame.display.set_icon(icon)

background = pygame.image.load('img/background.png')

playerIMG = pygame.image.load('img/spaceship.png')

score = 0

alien1img = pygame.image.load('img/alien1.png')
alien2img = pygame.image.load('img/alien2.png')
alien3img = pygame.image.load('img/alien3.png')
enemyIMGS = [alien1img, alien2img, alien3img]
enemyIMG = []
enemyX = []
enemyY = []
enemyXchange = []
enemyYchange = []
enemy_count = 15
enemyIMG = random.choices(enemyIMGS, weights=[1, 1, 1], k=enemy_count)

for i in range(enemy_count):
    enemyX.append(random.randint(0, 800-64))
    enemyY.append(random.randint(50, 150))
    enemyXchange.append(0.15)
    enemyYchange.append(0.02)
    # print(enemyIMG[i])


bulletIMG = pygame.image.load('img/bullet.png')

font = pygame.font.Font('arial.ttf', 25)
font2 = pygame.font.Font('arial.ttf', 45)
textX = 10
textY = 10

bullet_state = 'ready'

conn = sqlite3.connect('highscores/highscores.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS highscores(Score INTEGER)')


def player(x, y):
    window.blit(playerIMG, (x, y))


def aliens(x, y, img):
    window.blit(img, (x, y))


# def alien2(x, y):
#     window.blit(alien2img, (x, y))


# def alien3(x, y):
#     window.blit(alien3img, (x, y))


# def alienchoice():
#     counter = 10
#     alien1 = random.randint(0, counter)
#     counter -= alien1
#     alien2 = random.randint(0, counter)
#     counter -= alien2
#     alien3 = counter
#     for i in range(alien1):
#         alien1()
#     for i in range(alien2):
#         alien2()
#     for i in range(alien3):
#         alien3()


# do one enemy function randomly chooses variable value depending on that blits different alien


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    window.blit(bulletIMG, (x + 32, y + 10))


def collision_detection_bullet(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(bulletX+16 - enemyX+16, 2) +
                         math.pow(bulletY+16 - enemyY+16, 2))
    if distance < 20:
        return True


def collision_detection_player(plrX, plrY, eneX, eneY):
    distance = math.sqrt(math.pow(plrX - eneX+16, 2) +
                         math.pow(plrY - eneY+16, 2))
    if distance < 32:
        return True


def score_text(x, y):
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    window.blit(score_text, (x, y))


def final_score():
    global score
    score_text = font2.render(
        f'You scored {score} points this round!', True, (255, 255, 255))
    window.blit(score_text, (75, 250))


def menu():
    global running
    running = True
    click = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        window.fill((0, 0, 0))
        window.blit(background, (0, 0))

        button1 = pygame.Rect(30, 45, 280, 60)
        pygame.draw.rect(window, (52, 235, 177), button1, border_radius=20)
        window.blit(
            (font2.render('Start Game', True, (255, 255, 255))), (50, 50))

        if click:
            mx, my = pygame.mouse.get_pos()
            if button1.collidepoint(mx, my):
                global alive
                alive = True
                game()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()


def game_over():
    window.fill((0, 0, 0))
    window.blit(background, (0, 0))
    final_score()
    pygame.display.update()
    time.sleep(3)
    menu()


# (400-(14*0.75)*(12.5+len(strscore)/2), 300)
# WHILE LOOP TO KEEP WINDOW OPEN / KEEP PROGRAM RUNNING

def game():
    global score
    global bullet_state
    playerX = 400 - 32
    playerY = 480
    playerXchange = 0
    bulletX = 0
    bulletY = 480
    bulletYchange = -1
    bullet_state = 'ready'
    score = 0

    for i in range(enemy_count):
        enemyX[i] = (random.randint(0, 800-64))
        enemyY[i] = (random.randint(50, 150))
        enemyXchange[i] = 0.15
        enemyYchange[i] = 0.02
        # enemy(enemyX[i], enemyY[i])

    global running
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
            if enemyX[i] <= 0:
                enemyXchange[i] = 0.1
            elif enemyX[i] >= 800 - 32:
                enemyXchange[i] = -0.1
            enemyX[i] += enemyXchange[i]
            enemyY[i] += enemyYchange[i]

            collision_bullet = collision_detection_bullet(
                enemyX[i], enemyY[i], bulletX, bulletY)
            if collision_bullet and bullet_state == 'fire':
                bulletY = 480
                bullet_state = 'ready'
                score += 1
                # print(score)
                enemyX[i] = random.randint(0, 800-64)
                enemyY[i] = random.randint(50, 150)
                enemyIMG[i] = random.choice(enemyIMGS)

            aliens(enemyX[i], enemyY[i], enemyIMG[i])

            collision_player = collision_detection_player(
                playerX, playerY, enemyX[i], enemyY[i])

            if enemyY[i] >= 616 or collision_player:
                # print(f'Your final score is {score}!')
                for j in range(enemy_count):
                    enemyXchange[j] = 0
                    enemyYchange[j] = 0
                    enemyX[j] = 1000
                c.execute("INSERT INTO highscores(Score) VALUES(?)",
                          (score,))
                conn.commit()
                game_over()
                # running = False

        if bullet_state == 'fire':
            fire_bullet(bulletX, bulletY)
            bulletY += bulletYchange

        if bulletY <= -32:
            bulletY = 480
            bullet_state = 'ready'

        player(playerX, playerY)
        score_text(textX, textY)
        pygame.display.update()


menu()

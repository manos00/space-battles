import pygame
import random
import math
import time
import sqlite3
import threading

pygame.init()

window = pygame.display.set_mode((800, 600))

# clock = pygame.time.Clock()
# clock.tick(60)

running = True

pygame.display.set_caption('iNfOrMaTiK pRoJeKt')
icon = pygame.image.load('img/icon.png')
pygame.display.set_icon(icon)

background = pygame.image.load('img/background.png')

playerIMG = pygame.image.load('img/spaceship.png')

powerup_state = 'away'

timevarpowerup = 15

score = 0

alien1img = pygame.image.load('img/alien1.png')
alien2img = pygame.image.load('img/alien2.png')
alien3img = pygame.image.load('img/alien3.png')
ufoimg = pygame.image.load('img/ufo.png')
enemyIMGS = [alien1img, alien2img, alien3img, ufoimg]
enemyIMG = []
enemy_count = 15
enemyIMG = random.choices(enemyIMGS, weights=[33, 33, 33, 1], k=enemy_count)

bulletIMG = pygame.image.load('img/bullet.png')

powerupimg = pygame.image.load('img/powerup.png')

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


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    window.blit(bulletIMG, (x + 32, y + 10))


def drop_powerup(x, y):
    window.blit(powerupimg, (x + 16, y + 16))


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


def collision_detection_powerup(plrX, plrY, powrupX, powrupY):
    distance = math.sqrt(math.pow(plrX - powrupX+16, 2) +
                         math.pow(plrY - powrupY+16, 2))
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
    while running:
        click = False
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

        button2 = pygame.Rect(30, 115, 280, 60)
        pygame.draw.rect(window, (52, 235, 177), button2, border_radius=20)
        window.blit(
            (font2.render('Start Game', True, (255, 255, 255))), (50, 50))

        button3 = pygame.Rect(30, 185, 280, 60)
        pygame.draw.rect(window, (52, 235, 177), button2, border_radius=20)
        window.blit(
            (font2.render('Start Game', True, (255, 255, 255))), (50, 50))

        if click:
            if button1.collidepoint(pygame.mouse.get_pos()):
                game()
            elif button2.collidepoint(pygame.mouse.get_pos()):
                print('button 2')
            elif button3.collidepoint(pygame.mouse.get_pos()):
                print('button3')
            else:
                print('empty')

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


def game():
    global score
    global bullet_state
    global powerup_state
    global running
    playerX = 368
    playerY = 480
    playerXchange = 0
    bulletX = 0
    bulletY = 480
    bullet_state = 'ready'
    score = 0
    enemyX = []
    enemyY = []
    enemyXchange = []
    enemyYchange = []
    powerupX = 1000
    powerupY = 0
    powerupYchange = 0.2
    pwrup1 = 0
    pwrup2 = 0

    for i in range(enemy_count):
        enemyX.append(random.randint(0, 800-64))
        enemyY.append(random.randint(50, 150))
        enemyXchange.append(random.choice([0.15, -0.15]))
        enemyYchange.append(0.02)

    while running:
        window.fill((0, 0, 0))
        window.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerXchange = -0.5 - pwrup1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    playerXchange = 0.5 + pwrup1
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
        if playerX >= 736:
            playerX = 736

        for i in range(enemy_count):
            if enemyX[i] < 0:
                enemyXchange[i] = 0.1
            elif enemyX[i] > 768:
                enemyXchange[i] = -0.1
            enemyX[i] += enemyXchange[i]
            enemyY[i] += enemyYchange[i]

            collision_bullet = collision_detection_bullet(
                enemyX[i], enemyY[i], bulletX, bulletY)
            if collision_bullet and bullet_state == 'fire':
                bulletY = 480
                bullet_state = 'ready'
                score += 1
                if enemyIMG[i] == ufoimg:
                    powerup_state = 'drop'
                    powerupX = enemyX[i]
                    powerupY = enemyY[i]
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(50, 150)
                enemyIMG[i] = random.choices(
                    enemyIMGS, weights=[33, 33, 33, 1], k=1)[0]

            aliens(enemyX[i], enemyY[i], enemyIMG[i])

            collision_powerup = collision_detection_powerup(
                playerX, playerY, powerupX, powerupY)

            def counterpowerup():
                global timevarpowerup
                for i in range(timevarpowerup):
                    timevarpowerup -= 1
                    time.sleep(1)

            timerpowerup = threading.Thread(target=counterpowerup)

            if collision_powerup:
                if timevarpowerup == 15:
                    timerpowerup.start()
                powerup_state = 'away'
                powerupX = 1000
                ability = random.choice(['playerspeed', 'bulletspeed'])
                if ability == 'playerspeed':
                    pwrup1 = 0.5
                elif ability == 'bulletspeed':
                    pwrup2 = 1.5

            if timevarpowerup == 0:
                pwrup1 = 0
                pwrup2 = 0

            collision_player = collision_detection_player(
                playerX, playerY, enemyX[i], enemyY[i])

            if enemyY[i] >= 616 or collision_player:
                for j in range(enemy_count):
                    enemyXchange[j] = 0
                    enemyYchange[j] = 0
                    enemyX[j] = 1000
                c.execute("INSERT INTO highscores(Score) VALUES(?)",
                          (score,))
                conn.commit()
                game_over()

        if powerup_state == 'drop':
            drop_powerup(powerupX, powerupY)
            powerupY += powerupYchange

        if bullet_state == 'fire':
            fire_bullet(bulletX, bulletY)
            bulletYchange = -1 - pwrup2
            bulletY += bulletYchange

        if bulletY <= -32:
            bulletY = 480
            bullet_state = 'ready'

        player(playerX, playerY)
        score_text(textX, textY)
        if timevarpowerup < 15 and timevarpowerup > 0:
            window.blit(font.render(
                f'Powerup time: {timevarpowerup}', True, (255, 255, 255)), (textX, textY+30))
        pygame.display.update()


menu()

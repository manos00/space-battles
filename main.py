#!/bin/env python3

from platform import system
import random
from math import sqrt, pow
from time import sleep
from sqlite3 import connect
from threading import Thread
from pandas import read_sql_query
from os import mkdir, environ, path
from pygame.draw import line

pygame.init()

img='./img'
db='./highscores'
alien1path=img+'/alien1.png'
alien2path=img+'/alien2.png'
alien3path=img+'/alien3.png'
ufopath=img+'/ufo.png'
iconpath=img+'/icon.png'
bulletpath=img+'/bullet.png'
backgroundpath=img+'/background.png'
spaceshippath=img+'/spaceship.png'
poweruppath=img+'/powerup.png'
fontpath='./arial.ttf'
databasepath=db+'/highscores.db'
if not path.exists(db):
    mkdir(db)

window=pygame.display.set_mode((800, 600))

running=True

pygame.display.set_caption('SPACE BATTLES')
icon=pygame.image.load(iconpath)
pygame.display.set_icon(icon)

background=pygame.image.load(backgroundpath)

playerIMG=pygame.image.load(spaceshippath)

powerup_state='away'

timevarpowerup=0

score=0

alien1img=pygame.image.load(alien1path)
alien2img=pygame.image.load(alien2path)
alien3img=pygame.image.load(alien3path)
ufoimg=pygame.image.load(ufopath)
enemyIMGS=[alien1img, alien2img, alien3img, ufoimg]
enemyIMG=[]
enemy_count=15
enemyIMG=random.choices(enemyIMGS, weights=[33, 33, 33, 1], k=enemy_count)

bulletIMG=pygame.image.load(bulletpath)

powerupimg=pygame.image.load(poweruppath)

font=pygame.font.Font(fontpath, 25)
font2=pygame.font.Font(fontpath, 45)
textX=10
textY=10

bullet_state='ready'

conn=connect(databasepath)
c=conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS highscores(Score INTEGER, Names TEXT)')


def player(x, y):
    window.blit(playerIMG, (x, y))


def aliens(x, y, img):
    window.blit(img, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state='fire'
    window.blit(bulletIMG, (x + 32, y + 10))


def drop_powerup(x, y):
    window.blit(powerupimg, (x + 16, y + 16))


def collision_detection_bullet(enemyX, enemyY, bulletX, bulletY):
    distance=sqrt(pow(bulletX+16 - enemyX+16, 2) +
                         pow(bulletY+16 - enemyY+16, 2))
    if distance < 20:
        return True


def collision_detection_player(plrX, plrY, eneX, eneY):
    distance=sqrt(pow(plrX - eneX+16, 2) +
                         pow(plrY - eneY+16, 2))
    if distance < 32:
        return True


def collision_detection_powerup(plrX, plrY, powrupX, powrupY):
    distance=sqrt(pow(plrX - powrupX+16, 2) +
                         pow(plrY - powrupY+16, 2))
    if distance < 40:
        return True


def score_text(x, y):
    score_text=font.render(f'Score: {score}', True, (255, 255, 255))
    window.blit(score_text, (x, y))


def final_score():
    score_text=font2.render(
        f'You scored {score} points this round!', True, (255, 255, 255))
    window.blit(score_text, (75, 250))


def menu():
    highscorestr=(read_sql_query(
        "SELECT * FROM highscores ORDER BY score DESC LIMIT 5", conn).to_string(index=False).replace('Score', '')).replace('Names', '').replace('Empty DataFrame', '').replace('Columns: [, ]', '').replace('Index: []', '').splitlines()
    global running
    while running:
        click=False
        event_list=pygame.event.get()
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click=True
            if event.type == pygame.QUIT:
                running=False

        window.fill((0, 0, 0))
        window.blit(background, (0, 0))

        counter=-1

        window.blit(
            (font2.render('Highscores:', True, (255, 255, 255))), (400, 110))

        for line in highscorestr:
            counter += 1
            window.blit(
                (font2.render(line[3:], True, (255, 255, 255))), (400, 110+counter*55))
        counter=0
        window.blit(
            (font2.render('Space Battles', True, (255, 255, 255))), (400, 50))

        button1=pygame.Rect(30, 45, 280, 60)
        pygame.draw.rect(window, (52, 235, 177), button1, border_radius=20)
        window.blit(
            (font2.render('Start Game', True, (255, 255, 255))), (50, 50))

        button2=pygame.Rect(30, 115, 280, 60)
        pygame.draw.rect(window, (52, 235, 177), button2, border_radius=20)
        window.blit(
            (font2.render('Guide', True, (255, 255, 255))), (50, 120))

        button3=pygame.Rect(30, 185, 280, 60)
        pygame.draw.rect(window, (52, 235, 177), button3, border_radius=20)
        window.blit(
            (font2.render('Quit Game', True, (255, 255, 255))), (50, 190))

        if click:
            if button1.collidepoint(pygame.mouse.get_pos()):
                game()
            elif button2.collidepoint(pygame.mouse.get_pos()):
                guide()
            elif button3.collidepoint(pygame.mouse.get_pos()):
                running=False

        pygame.display.update()


def guide():
    global running
    while running:
        click=False
        event_list=pygame.event.get()
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click=True
            if event.type == pygame.QUIT:
                running=False
        window.fill((0, 0, 0))
        window.blit(background, (0, 0))
        button=pygame.Rect(30, 515, 280, 60)
        pygame.draw.rect(window, (52, 235, 177), button, border_radius=20)
        window.blit(
            (font2.render('Back', True, (255, 255, 255))), (50, 520))
        if click:
            if button.collidepoint(pygame.mouse.get_pos()):
                menu()
        window.blit(
            (font.render('Kill the Aliens by moving around with the arrow keys and', True, (255, 255, 255))), (50, 50))
        window.blit(
            (font.render('shooting by pressing the spacebar.', True, (255, 255, 255))), (50, 75))
        window.blit(
            (font.render('There’s a 1% chance of an UFO spawning', True, (255, 255, 255))), (50, 125))
        window.blit(
            (font.render('When killed it drops a powerup which either makes you move', True, (255, 255, 255))), (50, 175))
        window.blit(
            (font.render('faster or lets you shoot faster for 15 seconds.', True, (255, 255, 255))), (50, 200))
        window.blit(
            (font.render('At the end of a round, your final score will be', True, (255, 255, 255))), (50, 250))
        window.blit(
            (font.render('displayed, and you can either press ‘ESC’ to', True, (255, 255, 255))), (50, 275))
        window.blit(
            (font.render('instantly return to the main menu or enter your name.', True, (255, 255, 255))), (50, 300))
        window.blit(
            (font.render('If you choose to enter your name, by hitting ‘Return’,', True, (255, 255, 255))), (50, 325))
        window.blit(
            (font.render('you can save your Score under your name.', True, (255, 255, 255))), (50, 350))
        window.blit(
            (font.render('The top 5 highest scores will be displayed', True, (255, 255, 255))), (50, 375))
        window.blit(
            (font.render('on the right side of the main menu.', True, (255, 255, 255))), (50, 400))
        pygame.display.update()


def game_over():
    global running
    done=False
    text=''
    while not done:
        window.fill((0, 0, 0))
        window.blit(background, (0, 0))
        final_score()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done=True
                running=False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    done=True
                    c.execute(
                        "INSERT INTO highscores(Score, Names) VALUES(?, ?)", (score, text))
                    conn.commit()
                elif event.key == pygame.K_BACKSPACE:
                    text=text[:-1]
                elif event.key == pygame.K_ESCAPE:
                    menu()
                    done=True
                    break
                else:
                    text += event.unicode
        window.blit(
            (font2.render('Enter your name here:', True, (255, 255, 255))), (160, 300))
        window.blit(
            (font2.render(text, True, (255, 255, 255))), (330, 350))
        pygame.display.update()
    menu()


def game():
    global score
    global bullet_state
    global powerup_state
    global running
    playerX=368
    playerY=480
    playerXchange=0
    bulletX=0
    bulletY=480
    bullet_state='ready'
    score=0
    enemyX=[]
    enemyY=[]
    enemyXchange=[]
    enemyYchange=[]
    powerupX=1000
    powerupY=0
    powerupYchange=0.2
    pwrup1=0
    pwrup2=0

    for i in range(enemy_count):
        enemyX.append(random.randint(0, 800-32))
        enemyY.append(random.randint(50, 150))
        enemyXchange.append(random.choice([0.15, -0.15]))
        enemyYchange.append(0.02)

    while running:
        window.fill((0, 0, 0))
        window.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerXchange=-0.5 - pwrup1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    playerXchange=0.5 + pwrup1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if bullet_state == 'ready':
                        bulletX=playerX - 16
                        fire_bullet(bulletX, bulletY)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    playerXchange=0

        playerX += playerXchange
        if playerX <= 0:
            playerX=0
        if playerX >= 736:
            playerX=736

        for i in range(enemy_count):
            if enemyX[i] < 0:
                enemyXchange[i]=0.1
            elif enemyX[i] > 768:
                enemyXchange[i]=-0.1
            enemyX[i] += enemyXchange[i]
            enemyY[i] += enemyYchange[i]

            collision_bullet=collision_detection_bullet(
                enemyX[i], enemyY[i], bulletX, bulletY)
            if collision_bullet and bullet_state == 'fire':
                bulletY=480
                bullet_state='ready'
                score += 1
                if enemyIMG[i] == ufoimg:
                    powerup_state='drop'
                    powerupX=enemyX[i]
                    powerupY=enemyY[i]
                enemyX[i]=random.randint(0, 736)
                enemyY[i]=random.randint(50, 150)
                enemyIMG[i]=random.choices(
                    enemyIMGS, weights=[33, 33, 33, 1], k=1)[0]

            aliens(enemyX[i], enemyY[i], enemyIMG[i])

            collision_powerup=collision_detection_powerup(
                playerX, playerY, powerupX, powerupY)

            def counterpowerup():
                global timevarpowerup
                while timevarpowerup != 0:
                    timevarpowerup -= 1
                    sleep(1)

            timerpowerup=Thread(target=counterpowerup)

            global timevarpowerup

            if collision_powerup:
                if timevarpowerup == 0:
                    timevarpowerup += 15
                    timerpowerup.start()
                elif timevarpowerup > 0:
                    timevarpowerup += 15
                powerup_state='away'
                powerupX=1000
                ability=random.choice(['playerspeed', 'bulletspeed'])
                if ability == 'playerspeed':
                    pwrup1=0.5
                elif ability == 'bulletspeed':
                    pwrup2=1.5

            if timevarpowerup == 0:
                pwrup1=0
                pwrup2=0

            collision_player=collision_detection_player(
                playerX, playerY, enemyX[i], enemyY[i])

            if enemyY[i] >= 616 or collision_player:
                for j in range(enemy_count):
                    enemyXchange[j]=0
                    enemyYchange[j]=0
                    enemyX[j]=1000
                game_over()

        if powerup_state == 'drop':
            drop_powerup(powerupX, powerupY)
            powerupY += powerupYchange

        if bullet_state == 'fire':
            fire_bullet(bulletX, bulletY)
            bulletYchange=-1 - pwrup2
            bulletY += bulletYchange

        if bulletY <= -32:
            bulletY=480
            bullet_state='ready'

        player(playerX, playerY)
        score_text(textX, textY)
        if timevarpowerup > 0:
            window.blit(font.render(
                f'Powerup time: {timevarpowerup}', True, (255, 255, 255)), (textX, textY+30))
        pygame.display.update()

menu()

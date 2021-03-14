import random
import pygame

window = pygame.display.set_mode((800, 600))
running = True


enemyIMGS = [pygame.image.load('img/alien1.png'), pygame.image.load(
    'img/alien2.png'), pygame.image.load('img/alien3.png')]
# enemyIMGS = ['img/alien1.png', 'img/alien2.png', 'img/alien3.png']
enemyX = []
enemyY = []
enemyXchange = []
enemyYchange = []
enemy_count = 10
enemyIMG = random.choices(enemyIMGS, weights=[1, 1, 1], k=10)

for i in range(enemy_count):
    enemyX.append(random.randint(0, 800-64))
    enemyY.append(random.randint(50, 150))


def enemy(x, y):
    window.blit(enemyIMG[i], (x, y))


while running:
    window.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runnning = False

    for i in range(enemy_count):
        enemy(enemyX[i], enemyY[i])

    pygame.display.update()

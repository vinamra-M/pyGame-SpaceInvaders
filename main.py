import pygame
import random
import math
from pygame import mixer

# initialize the pygame
pygame.init()
clock = pygame.time.Clock()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')
# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Background Music
mixer.music.load('background.wav')
mixer.music.play(-1)
# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = playerX
bulletY = 480
bulletX_change = 0
bulletY_change = -10

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game Over Text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def bullet(x, y):
    screen.blit(bulletImg, (x, y))


def isCollision(enemyX, enemyY, bulletX, bulletY, i):
    a = enemyX[i] - bulletX
    b = enemyY[i] - bulletY
    a = a * a
    b = b * b
    distance = math.sqrt(a + b)
    if distance < 27:
        return True
    else:
        return False


bulletPress = False
running = True

while running:

    # RGB
    screen.blit(background, (0, 0))
    player(playerX, playerY)
    # enemy(enemyX, enemyY)
    # playerX += 0.1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_SPACE and bulletY == 480:
                bullet_Sound = mixer.Sound('laser.wav')
                bullet_Sound.play()
                bulletPress = True
                bulletX = playerX
                # bullet(bulletX, bulletY)

    playerX += playerX_change
    enemyX += enemyX_change
    # bulletY += bulletY_change
    # bulletX = playerX
    if bulletPress:
        bullet(bulletX, bulletY)
        bulletY += bulletY_change
        # bullet_Sound = mixer.Sound('laser.wav')
        # bullet_Sound.play()
        if bulletY < 0:
            bulletPress = False
            bulletY = 480

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(num_of_enemies):

        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

            # Collision
        collision = isCollision(enemyX, enemyY, bulletX, bulletY, i)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bulletPress = False
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # calling player def
    show_score(textX, textY)
    pygame.display.update()
# print(score)

# import python packages
import math
import pygame
import random
from pygame import mixer

# initiate pygame
pygame.init()
clock = pygame.time.Clock()

# set the pygame screen
screen = pygame.display.set_mode((800, 600))

# set the caption and the icon for pygame window
pygame.display.set_caption("Space invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# set the background for pygame window
background = pygame.image.load("background.png")

# set the background's music
mixer.music.load("background.wav")
mixer.music.play(-1)

# set the player's image:
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# set the enemies image:
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.7)
    enemyY_change.append(10)

# Bullet:
# Ready: You can't see the bullet on the screen
# Fire: The bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 2
bullet_state = "ready"

# font
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

# define show score function
def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (0, 255, 0))
    screen.blit(score, (x, y))

# define the game over text
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

# define the player's image on the pygame window
def player(x, y):
    screen.blit(playerImg, (x, y))

# define the enemy's image on the pygame window
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

# define the bullet's image on the pygame window
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

# define the collision
def is_Collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletY, 2)) + (math.pow(enemyY-bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

# keep opening the window until closing it
running = True
while running:

    # RGB = Red Green Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether it's right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_Sound = mixer.Sound("laser.wav")
                    bullet_Sound.play()
                    # Get the current coordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1
    # Player's movement
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 735:
        playerX = 735

    # Enemies' movement
    for i in range(num_of_enemies):

        # Game over
        if enemyY[i] > 200:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.7
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.7
            enemyY[i] += enemyY_change[i]

        # Collision:
        collision = is_Collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound("explosion.wav")
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)
    # Bullet's movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # draw the player image on the screen
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()










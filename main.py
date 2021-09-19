# Icon made by surang from www.flaticon.com
# Icon made by Freepik from www.flaticon.com

import pygame
import random
import math
from pygame import mixer

pygame.init()
clock = pygame.time.Clock()

# Game variables
SCREENWIDTH = 800
SCREENHEIGHT = 600
black = (0, 0, 0)
player_vel = 5
target_vel = 2
enemy_vel = 2
fps = 60

# Preparing the screen and the background
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
background = pygame.image.load("Images/background.png")
try:
	mixer.music.load('Sounds/bgmusic.mp3')
except pygame.error:
	mixer.music.load('Sounds/bgmusic.wav')
mixer.music.play(-1)

pygame.display.set_caption("Catch the Starfish")
icon = pygame.image.load('Images/starfish.png')
pygame.display.set_icon(icon)

# Player (Octopus)
playerImg = pygame.image.load("Images/octopus.png")
playerX = SCREENWIDTH//2 - 32
playerY = SCREENHEIGHT - 74
playerX_change = 0
playerY_change = 0

# Target (Starfish)
targetImgs = []
targetX = []
targetY = []
targetY_change = []

for _ in range(4):
    targetImgs.append(pygame.image.load("Images/starfish.png"))
    targetX.append(random.randint(0, SCREENWIDTH - 32))
    targetY.append(random.randint(0, 20))
    targetY_change.append(target_vel)

# Enemy (Bomb)
enemyImgs = []
enemyX = []
enemyY = []
enemyY_change = []

for _ in range(4):
    enemyImgs.append(pygame.image.load("Images/bomb.png"))
    enemyX.append(random.randint(0, SCREENWIDTH - 32))
    enemyY.append(random.randint(0, 40))
    enemyY_change.append(enemy_vel)

# Variables to display score and game over text
score_value = 0
font = pygame.font.Font('ARIAL.TTF', 32)
over_font = pygame.font.Font('ARIAL.TTF', 70)

# Functions
def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, black)
    screen.blit(score, (x, y))

def player(x, y):
    screen.blit(playerImg, (x, y))

def target(x, y, k):
    screen.blit(targetImgs[k], (x, y))

def enemy(x, y, k):
    screen.blit(enemyImgs[k], (x, y))

def is_collision(x1, y1, x2, y2):
    d = math.sqrt(math.pow((x1 - x2), 2) + math.pow((y1 - y2), 2))
    if d < 40:
        return True
    else:
        return False

def game_over_text():
    over_text = over_font.render("GAME OVER", True, black)
    screen.blit(over_text, (200, 250))

running = True
game_over = False

# Game Loop
while running:
    screen.fill(black)
    screen.blit(background, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -player_vel

            if event.key == pygame.K_RIGHT:
                playerX_change = player_vel
            
            if event.key == pygame.K_UP:
                playerY_change = -player_vel
            
            if event.key == pygame.K_DOWN:
                playerY_change = player_vel
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerX_change = 0
                playerY_change = 0
                
        if event.type == pygame.QUIT:
            running = False
    
    # Player movement
    playerX += playerX_change
    playerY += playerY_change
    
    if playerX <= 0:
        playerX = 0
    elif playerX >= SCREENWIDTH - 64:
        playerX = SCREENWIDTH - 64
    elif playerY <= 400:
        playerY = 400
    elif playerY >= SCREENHEIGHT - 64:
        playerY = SCREENHEIGHT - 64

    if game_over:
        game_over_text()

    else:
    	# Target movement
        for i in range(4):
            targetY[i] += targetY_change[i]
        
            if targetY[i] >= SCREENHEIGHT - 32:
                targetX[i] = random.randint(0, SCREENWIDTH - 32)
                targetY[i] = random.randint(0, 20)
        
            if is_collision(targetX[i], targetY[i], playerX, playerY):
                hit = mixer.Sound('Sounds/bubble.wav')
                hit.play()
                
                score_value += 1
                targetX[i] = random.randint(0, SCREENWIDTH - 32)
                targetY[i] = random.randint(0, 20)
            
            target(targetX[i], targetY[i], i)

    	# Enemy movement
        for i in range(4):
            enemyY[i] += enemyY_change[i]
        
            if enemyY[i] >= SCREENHEIGHT - 32:
                enemyX[i] = random.randint(0, SCREENWIDTH - 32)
                enemyY[i] = random.randint(0, 40)
        
            if is_collision(enemyX[i], enemyY[i], playerX, playerY):
                bomb_hit = mixer.Sound('Sounds/explosion.wav')
                bomb_hit.play()

                game_over = True
            
            enemy(enemyX[i], enemyY[i], i)

    player(playerX, playerY)
    show_score(10, 10)
    clock.tick(fps)
    pygame.display.update()
